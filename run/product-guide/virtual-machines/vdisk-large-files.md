---
title: "Optimize a vDisk with the Large Files Setting"
description: "Use the Optimize For setting on a vDisk to increase throughput for a dedicated, high-throughput workload, and measure the change with fio."
semantic_keywords:
  - "vDisk Optimize For Large Files General Usage"
  - "VM disk throughput tuning VergeOS"
  - "fio benchmark virtual disk block size iodepth"
  - "per-vDisk queue depth outstanding I/O"
  - "SQL database VM disk performance"
use_cases:
  - tune_vdisk_throughput
  - configure_large_files_setting
  - benchmark_vm_disk_with_fio
  - plan_parallel_vdisk_io
tags:
  - virtual-machines
  - drives
  - vdisk
  - performance
  - storage
  - fio
  - queue-depth
  - benchmarking
categories:
  - Virtual Machines
---

# Optimize a vDisk with the Large Files Setting

This guide tells how to use the **Optimize For** setting on a vDisk to increase throughput for a dedicated workload. It also tells how to measure the change with `fio`.

## Overview

Each VM drive of media type **Disk** has an **Optimize For** setting with two options:

- **General Usage** (default) – the vDisk accepts I/O requests of up to 64 KB from the guest.
- **Large Files** – the vDisk accepts I/O requests of up to 1 MB from the guest.

Each I/O request crosses from the guest to the host. This transition is the expensive part of a VM disk operation. With **Large Files**, the guest sends fewer, larger requests for the same data. Fewer transitions give more throughput, mainly for sequential I/O and for large block sizes.

### Why General Usage is the default

Many VergeOS systems run a large number of workloads on one cluster, for example in a multi-tenant or MSP environment. The 64 KB cap keeps one VM from using a large share of the vSAN at the cost of the other workloads. **General Usage** is the correct choice when many workloads share a cluster and no single workload must have maximum throughput.

### When to use Large Files

Use **Large Files** for a vDisk that gives high-throughput I/O on a cluster where that workload has priority. Examples:

- A dedicated database VM, for example SQL Server data and log volumes.
- An analytics or reporting VM that reads large files sequentially.
- A VM that is the only important workload on its cluster or node.

In internal tests on a dedicated VM, **Large Files** increased throughput for most block sizes, from 4 KB to 2 MB, for read and for write. The one regression in those tests was 64 KB direct writes at an I/O depth of 32. That result was approximately 30-40% slower. Test your own workload before you change production vDisks.

### What does not change

The setting changes only the size of the requests between the guest and the host. The vSAN does not change:

- The vSAN keeps its native 64 KB block size. It divides each request of up to 1 MB into 64 KB blocks.
- Hashes, deduplication, and redundancy use the same 64 KB blocks as before.
- Storage capacity use does not change.

### Small synchronous writes

Some workloads, for example a database, send small synchronous writes such as 8 KB. **Large Files** does not hold these writes back to fill a larger block. Each write goes through the vSAN transaction system when the guest sends it, so the setting does not add a risk of data loss.

A write smaller than 64 KB is not in the native vSAN format. The vSAN reads the 64 KB block, merges the change, and writes the block. To make this faster, the vSAN caches the block on the local node after the first small write. Later small writes to the same block do not have to cross the network each time.

### What you'll learn

- How to change the **Optimize For** setting on a vDisk.
- How the per-vDisk queue depth limit affects throughput.
- When to use more than one vDisk, or more than one virtual controller, for parallel I/O.
- How to measure the change with `fio`.

### What you'll need

- A user with permission to edit the VM.
- Knowledge of [VM drives](vm-drives.md) and [storage tiers](../storage/storage-tiers.md).
- A benchmark tool in the guest, such as `fio`.
- A maintenance window, because the VM must restart to apply the change.

## Measure the baseline

Measure the vDisk with **General Usage** first. A baseline lets you compare the results after the change.

1. Install `fio` in the guest OS.
2. Make a test file on the vDisk that you will tune. Use a file larger than the guest RAM, so the guest cache does not change the results.
3. Run the tests in [Benchmark tests with fio](#benchmark-tests-with-fio).
4. Record the throughput (MB/s), IOPS, and latency for each test.

{% hint style="warning" %}
Do not run write tests on a vDisk that holds production data. Use a test file, a test vDisk, or a clone of the VM.
{% endhint %}

## Change the Optimize For setting

1. From the VM dashboard, click **Drives**.
2. Select the vDisk.
3. Click **Edit**.
4. Expand the **Advanced** section.
5. In **Optimize For**, select **Large Files**.
6. Click **Submit**.
7. Restart the VM to apply the setting.

The vDisk shows **Large Files** in the **Optimize For** field.

Run the same `fio` tests again and compare the results with the baseline. If the workload is slower, set **Optimize For** back to **General Usage** and restart the VM.

## Queue depth for each vDisk

The vSAN limits the number of outstanding I/O requests for each vDisk. This limit is the per-vDisk queue depth. It keeps one vDisk from using all the storage bandwidth of the system. The default limit is 8 outstanding requests.

When the guest sends more requests than the limit, the extra requests wait in a queue. Guest monitoring tools then show a high disk queue length. This result is expected when a workload uses an I/O depth higher than 8.

Increase the limit only when all of these conditions are true:

- The workload is dedicated and uses a high I/O depth, for example 32 or more.
- Benchmark results or guest monitoring show that the vDisk queue is the bottleneck.
- Other workloads on the cluster can accept less share of the storage.

The queue depth limit is a vSAN tuning setting. To change it, contact [VergeOS Support](https://app.gitbook.com/s/uJc5d3O7cwI7qD8muSyG/support-and-services).

## Use more vDisks for parallel I/O

One vDisk gives one stream of I/O, with its own queue depth limit. More vDisks give more streams that operate in parallel. Use these methods to increase parallel I/O:

- **More vDisks with a volume manager.** Add two or more vDisks and join them in the guest, for example with an LVM volume group or Windows Storage Spaces. The guest spreads I/O across all the vDisks.
- **A separate virtual controller for each vDisk.** Set the **Interface** of each high-I/O vDisk to **Virtio-SCSI (Dedicated Controller)**. The guest sees each vDisk on its own controller. This method helped SQL Server data volumes in production deployments.
- **Separate vDisks for each data type.** For a database, put the data files, the log files, and the temp files on separate vDisks.

These methods add complexity. Each vDisk adds a device to monitor, expand, and back up in the guest. A volume that spans many vDisks is harder to resize and to recover. Use the minimum number of vDisks that gives the necessary throughput. A few large vDisks are better than many small ones.

## Benchmark tests with fio

Use the same tests before and after each change. Run each test with direct I/O, so the guest page cache does not change the results.

Use these values:

| Parameter | Values | Why |
|-----------|--------|-----|
| Block size (`--bs`) | `4k`, `64k`, `128k`, `256k`, `512k`, `1m`, `2m` | Shows the effect of the 64 KB and 1 MB request sizes. |
| I/O depth (`--iodepth`) | `1`, `32` | `1` shows latency. `32` shows throughput under load. |
| Jobs (`--numjobs`) | `1`, then the number of guest vCPUs | Shows the effect of parallel streams. |
| Direct I/O (`--direct`) | `1` | Bypasses the guest page cache. |
| Mode (`--rw`) | `read`, `write`, `randread`, `randwrite` | Sequential and random patterns. |

An I/O depth of 256 is not realistic for most workloads. Use it only to find the maximum of the hardware.

On a Linux guest, this command runs one sequential read test:

```bash
fio --name=seqread --filename=/data/fio-test --size=20G \
    --rw=read --bs=1m --iodepth=32 --numjobs=1 \
    --direct=1 --ioengine=libaio --time_based --runtime=60 \
    --group_reporting
```

On a Windows guest, use `--ioengine=windowsaio` and a Windows path, for example `--filename=D\:\fio-test`.

Change `--rw`, `--bs`, `--iodepth`, and `--numjobs` for each test in the table. Compare the `bw` (throughput) and `lat` (latency) values in the output between the two settings.

## Summary

You set **Optimize For** to **Large Files** on a vDisk and measured the change with `fio`. The vDisk now accepts I/O requests of up to 1 MB from the guest. The vSAN still stores, hashes, and deduplicates the data in 64 KB blocks.

### Next steps

- [Virtual Machine Drives](vm-drives.md)
- [Virtual Machine Best Practices](vm-best-practices.md)
- [Storage Tiers](../storage/storage-tiers.md)
