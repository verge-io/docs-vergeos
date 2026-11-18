---
title: "Optimize a vDisk with the Large Files Setting"
description: "Use the Optimize For setting on a vDisk to increase throughput for a dedicated, high-throughput workload."
semantic_keywords:
  - "vDisk Optimize For Large Files General Usage"
  - "VM disk throughput tuning VergeOS"
  - "per-vDisk queue depth outstanding I/O"
  - "parallel vDisk I/O dedicated controller"
use_cases:
  - tune_vdisk_throughput
  - configure_large_files_setting
  - plan_parallel_vdisk_io
tags:
  - virtual-machines
  - drives
  - vdisk
  - performance
  - storage
  - queue-depth
categories:
  - Virtual Machines
---

# Optimize a vDisk with the Large Files Setting

This guide tells how to use the **Optimize For** setting on a vDisk to increase throughput for a dedicated workload.

## Overview

Each VM drive of media type **Disk** has an **Optimize For** setting with two options:

- **General Usage** (default) – the vDisk advertises an optimal I/O size of 64 KB to the guest. This value is the native vSAN block size.
- **Large Files** – the vDisk advertises an optimal I/O size of 1 MB to the guest.

The setting is a hint to the guest. It is not a limit that the host enforces. The host accepts requests larger than the advertised size with either setting.

Each I/O request crosses from the guest to the host. This transition is the expensive part of a VM disk operation. When the guest uses the hint, **Large Files** makes the guest send fewer, larger requests for the same data. Fewer transitions give more throughput, mainly for sequential I/O and for large block sizes.

{% hint style="warning" %}
The effect of the setting depends on the vDisk interface and the guest OS. Some interfaces do not send the hint, and some guests ignore it. Before you change a vDisk, see [Guest and Interface Support for the Large Files Setting](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/optimize-for-large-files-guest-support).
{% endhint %}

### When to use Large Files

Use **Large Files** for a vDisk that gives high-throughput I/O on a cluster where that workload has priority. Examples:

- A dedicated database VM.
- An analytics or reporting VM that reads large files sequentially.
- A VM that is the only important workload on its cluster or node.

Test your own workload before you change production vDisks.

### What does not change

The setting changes only the optimal I/O size that the vDisk advertises to the guest. The vSAN does not change:

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

### What you'll need

- A user with permission to edit the VM.
- A vDisk interface and guest OS that use the setting. See [Guest and Interface Support for the Large Files Setting](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/optimize-for-large-files-guest-support).
- Knowledge of [VM drives](vm-drives.md) and [storage tiers](../storage/storage-tiers.md).
- A maintenance window, because the VM must restart to apply the change.

## Change the Optimize For setting

Measure the vDisk with **General Usage** before you change it, so that you can compare the results. For a benchmark method, see [Guest and Interface Support for the Large Files Setting](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/optimize-for-large-files-guest-support).

1. From the VM dashboard, click **Drives**.
2. Select the vDisk.
3. Click **Edit**.
4. Expand the **Advanced** section.
5. In **Optimize For**, select **Large Files**.
6. Click **Submit**.
7. Restart the VM to apply the setting.

The vDisk shows **Large Files** in the **Optimize For** field.

Measure the vDisk again and compare the results with the baseline. If the workload is slower, set **Optimize For** back to **General Usage** and restart the VM.

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

## Summary

You set **Optimize For** to **Large Files** on a vDisk. The vDisk now advertises an optimal I/O size of 1 MB to the guest, and a guest that uses the hint sends requests of up to 1 MB. The vSAN still stores, hashes, and deduplicates the data in 64 KB blocks.

### Next steps

- [Guest and Interface Support for the Large Files Setting](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/optimize-for-large-files-guest-support)
- [Virtual Machine Drives](vm-drives.md)
- [Virtual Machine Best Practices](vm-best-practices.md)
- [Storage Tiers](../storage/storage-tiers.md)
