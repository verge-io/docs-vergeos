---
title: Guest and Interface Support for the Large Files Setting
slug: optimize-for-large-files-guest-support
author: VergeOS Documentation Team
date: 2026-11-18T12:00:00.000Z
semantic_keywords:
  - "vDisk Optimize For Large Files no effect"
  - "optimal I/O size hint guest max_sectors_kb"
  - "virtio-scsi vioscsi Linux kernel request size"
  - "fio benchmark virtual disk block size iodepth"
use_cases:
  - check_large_files_guest_support
  - verify_guest_max_request_size
  - benchmark_vm_disk_with_fio
  - troubleshoot_no_throughput_change
categories:
  - VM
editor: markdown
dateCreated: 2026-11-18T12:00:00.000Z
description: >-
  Which vDisk interfaces and guest operating systems use the Optimize For
  setting, how to verify it in a Linux guest, and how to benchmark the change.
tags:
  - virtual-machines
  - vdisk
  - performance
  - fio
  - virtio-scsi
  - linux
  - windows
---

# Guest and Interface Support for the Large Files Setting

## Overview

{% hint style="info" %}
**Key Points**

- **Optimize For** sets the optimal I/O size that a vDisk advertises to the guest: 64 KB for **General Usage**, 1 MB for **Large Files**.
- The value is a hint. The host does not enforce it, and some guests ignore it.
- The setting has an effect only on SCSI-family, AHCI, IDE, and USB interfaces, in a guest that uses the hint.
{% endhint %}

This article tells which configurations use the **Optimize For** setting, how to verify the setting in a Linux guest, and how to benchmark it. For the setting itself and how to change it, see [Optimize a vDisk with the Large Files Setting](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/virtual-machines/vdisk-large-files).

## Interfaces that send the hint

The vDisk sends the optimal I/O size to the guest on these interfaces:

- **Virtio-SCSI** and **Virtio-SCSI (Dedicated Controller)**
- The **LSI** controllers
- **SATA (AHCI)**, **IDE**, and **USB**

The vDisk does not send the hint on **Virtio (Legacy)** or **NVMe**. On these interfaces, the **Optimize For** setting does nothing.

## Guests that use the hint

| Guest | Uses the hint |
|-------|---------------|
| Linux, kernel 6.10 or earlier (for example RHEL 8 and 9, Ubuntu 22.04, Debian 12) | Yes. The SCSI disk driver sets its maximum request size to the advertised value. |
| Linux, kernel 6.11 or later | No. The driver records the value but does not use it as its maximum request size. |
| Windows, with the `vioscsi` driver | No. The driver sets its maximum transfer size from its scatter-gather limits: 2 MB with indirect descriptors, 128 KB without. |

## Verify the setting in a Linux guest

1. Find the device name of the vDisk.

    ```bash
    lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
    ```

2. Read the optimal I/O size that the vDisk advertises. Replace `sdb` with your device name.

    ```bash
    cat /sys/block/sdb/queue/optimal_io_size
    ```

    The value is `65536` with **General Usage** and `1048576` with **Large Files**.

3. Read the maximum request size that the guest uses.

    ```bash
    cat /sys/block/sdb/queue/max_sectors_kb
    ```

    On a guest that uses the hint, the value is `64` with **General Usage** and `1024` with **Large Files**.

If `optimal_io_size` is `0`, the interface does not send the hint. If `optimal_io_size` is correct but `max_sectors_kb` does not match it, the guest does not use the hint.

## Benchmark the change with fio

Run the same tests with **General Usage** and with **Large Files**. Run each test with direct I/O, so the guest page cache does not change the results.

{% hint style="warning" %}
Do not run write tests on a vDisk that holds production data. Use a test file, a test vDisk, or a clone of the VM.
{% endhint %}

1. Install `fio` in the guest.
2. Make a test file on the vDisk. Use a file larger than the guest RAM.
3. Run each test in the table with **General Usage**.
4. Record the throughput (MB/s), IOPS, and latency for each test.
5. Change the vDisk to **Large Files** and restart the VM.
6. Run the same tests again and compare the results.

| Parameter | Values | Why |
|-----------|--------|-----|
| Block size (`--bs`) | `4k`, `64k`, `128k`, `256k`, `512k`, `1m`, `2m` | Shows the effect of the 64 KB and 1 MB request sizes. |
| I/O depth (`--iodepth`) | `1`, `32` | `1` shows latency. `32` shows throughput under load. |
| Jobs (`--numjobs`) | `1`, then the number of guest vCPUs | Shows the effect of parallel streams. |
| Direct I/O (`--direct`) | `1` | Bypasses the guest page cache. |
| Mode (`--rw`) | `read`, `write`, `randread`, `randwrite` | Sequential and random patterns. |

An I/O depth of 256 is not realistic for most workloads. Use it only to find the maximum of the hardware.

## Examples

On a Linux guest, this command runs one sequential read test:

```bash
fio --name=seqread --filename=/data/fio-test --size=20G \
    --rw=read --bs=1m --iodepth=32 --numjobs=1 \
    --direct=1 --ioengine=libaio --time_based --runtime=60 \
    --group_reporting
```

On a Windows guest, use `--ioengine=windowsaio` and a Windows path, for example `--filename=D\:\fio-test`.

Change `--rw`, `--bs`, `--iodepth`, and `--numjobs` for each test in the table. Compare the `bw` (throughput) and `lat` (latency) values in the output.

In tests on a dedicated single-node system, **Large Files** increased throughput for most block sizes, from 4 KB to 2 MB, for read and for write. The one regression was 64 KB direct writes at an I/O depth of 32, which was approximately 30-40% slower. Your results depend on the guest, the interface, and the hardware.

## Troubleshooting

### Throughput does not change after you select Large Files

**Cause**: The vDisk interface does not send the hint, or the guest does not use it. Windows guests and Linux guests with kernel 6.11 or later do not use it.

**Solution**:

1. Make sure that the VM restarted after the change.
2. Make sure that the vDisk interface is in [Interfaces that send the hint](#interfaces-that-send-the-hint).
3. On a Linux guest, do the steps in [Verify the setting in a Linux guest](#verify-the-setting-in-a-linux-guest).
4. If the guest does not use the hint, set **Optimize For** back to **General Usage**.

### Guest monitoring shows a high disk queue length

**Cause**: The vSAN limits the number of outstanding I/O requests for each vDisk. The default limit is 8. A workload with a higher I/O depth waits in the queue.

**Solution**: See [Queue depth for each vDisk](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/virtual-machines/vdisk-large-files#queue-depth-for-each-vdisk).

## Additional Resources

- [Optimize a vDisk with the Large Files Setting](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/virtual-machines/vdisk-large-files)
- [Virtual Machine Drives](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/virtual-machines/vm-drives)

{% hint style="info" %}
**Need Help?**

If you have questions or problems with this procedure, contact the VergeOS support team.
{% endhint %}
