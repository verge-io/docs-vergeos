---
title: "Sharing Data Between Virtual Machines"
description: "Compare the methods to share disks and data between VMs in VergeOS: Clone Disk, Non-Persistent drives, NAS shares, and Shared Disk (26.2 or later), with guidance on when to use each."
semantic_keywords:
  - "share data between VMs VergeOS"
  - "share disk between VMs VergeOS"
  - "shared storage virtual machines"
  - "clone disk vs NAS share vs shared disk"
  - "non-persistent drive golden image multiple VMs"
  - "multi-attach disk VergeOS"
  - "shared file system VMs SMB NFS"
use_cases:
  - share_data_between_vms
  - seed_vm_from_existing_disk
  - share_golden_image_non_persistent
  - provide_shared_file_storage
  - attach_disk_to_multiple_vms
  - choose_disk_sharing_method
tags:
  - virtual-machines
  - drives
  - storage
  - sharing
  - clone-disk
  - non-persistent
  - golden-image
  - shared-disk
  - nas
  - shares
categories:
  - Virtual Machines
---

# Sharing Data Between Virtual Machines

## Overview

VergeOS gives four methods to share a disk or its data between virtual machines. **Clone Disk** gives each VM its own independent copy of a disk. A **Non-Persistent** drive gives a VM its own copy of a disk that goes back to its original state each time the VM restarts. A **NAS share** gives multiple VMs file-level access to the same data over the network. **Shared Disk** (VergeOS 26.2 or later) attaches one block device to multiple running VMs at the same time, for guest clusters. This page explains what each method does, when to choose it, and where to find the procedure.

### What You'll Learn

- The difference between Clone Disk, Non-Persistent drives, NAS shares, and Shared Disk
- When to use each method based on your use case

### What You'll Need

- A running VergeOS environment with at least two virtual machines
- Administrative access to the VergeOS UI
- For NAS shares: a configured [NAS service](../nas/overview.md)
- For Shared Disk: VergeOS 26.2 or later, and a cluster-aware guest OS or application

## Comparison

| Method | What it shares | Read/Write semantics | Best for | Limitations |
|---|---|---|---|---|
| **Clone Disk** | An independent copy of an existing `.raw` disk, made at drive-creation time | Each VM owns a private read/write copy. Changes are **not** synchronized back to the source or to other clones. | Seeding new VMs from a known-good disk image, handing off a point-in-time dataset to another VM | One-time copy only — not a live sharing mechanism. Clones diverge from the source the moment they are created. Permissions are inherited from the source disk. |
| **Non-Persistent** | A copy of an existing `.raw` disk, made at drive-creation time, that reverts on every restart | Each VM can read and write during its session. Its changes are private to that VM and are **discarded** when the VM restarts. The source disk is not changed. | Golden image and VDI deployments, kiosks, labs, and training VMs that must return to a known state on every restart | Changes do not survive a restart; store user data on a separate persistent drive or a NAS share. Later changes to the source disk do not reach existing Non-Persistent drives. To roll out an updated image, create the drives again from the updated source. |
| **NAS share (SMB/NFS)** | A NAS volume exposed as a network share and mounted by multiple guests | Concurrent read/write at the **file** level, mediated by the NAS service and the share protocol | Shared application data, file repositories, content libraries, and any workflow where multiple VMs need to read or write the same files | File-level only, not block-level. Network overhead compared to local disk I/O. Concurrency, locking, and performance depend on the protocol and the guest OS. Granular share-level and filesystem-level permissions are available. |
| **Shared Disk** *(26.2 or later)* | One `.raw` disk attached as a block device to multiple running VMs | Concurrent read/write at the **block** level. The guest cluster coordinates access with SCSI-3 Persistent Reservations. | Guest clusters that need shared block storage, such as Windows Server Failover Clustering and Cluster Shared Volumes (CSV) | The guest must coordinate writes. Set **Shared Disk** when you create the drive; you cannot turn it on later. Interface must be **Virtio-SCSI** or **Virtio-SCSI (Dedicated Controller)**. |

## Method 1 — Clone Disk

A **Clone Disk** is a point-in-time copy of an existing `.raw` drive (the default format for VergeOS VM disks) on the same VergeOS system. To create one, add a drive to a VM and select **Clone Disk** as the media type. The clone is fully independent of the source: writes to the clone stay in the clone, and writes to the source do not show in the clone. Because the clone is a full copy, later changes to the source drive, or its removal, do not affect it. Use Clone Disk to *initialize* a VM from an existing disk, not to keep data in sync between VMs.

For the step-by-step procedure, see [**Virtual Machine Drives**](vm-drives.md#adding-a-drive) and select **Clone Disk** in the **Media** field.

## Method 2 — Non-Persistent Drive

A **Non-Persistent** drive starts as a copy of an existing `.raw` disk (the golden image). The VM can write to the drive as normal during its session, but those writes are discarded when the VM restarts, and the drive goes back to the state it had when you created it. A guest reboot and a power cycle both discard the changes.

You can create Non-Persistent drives on multiple VMs from the same source disk. Each drive is independent: VMs do not see each other's changes, and no VM changes the source disk. With deduplication, the copies do not use additional space for the data they have in common with the source disk.

The copy is made when you create the drive. Later changes to the source disk do not reach Non-Persistent drives that already exist. To move VMs to an updated image, update the source disk, then create the Non-Persistent drives again from it.

To create one, add a drive to a VM, set **Media** to **Non-Persistent**, and select the source disk in **Media File**.

{% hint style="info" %}
Any data a user saves to a Non-Persistent drive is lost at restart. Keep data that must persist on a separate standard **Disk** drive or on a NAS share.
{% endhint %}

For the field details, see [**Virtual Machine Drives**](vm-drives.md#adding-a-drive) and select **Non-Persistent** in the **Media** field. For a step-by-step procedure, see the KB article [Making a Non-Persistent VM](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/making-a-nonpersistent-vm).

## Method 3 — NAS Share

A **NAS share** is a volume on the VergeOS NAS service, exposed over SMB or NFS. Each VM mounts the share like any other network file system, and the NAS coordinates concurrent access from all connected guests. Use a NAS share when multiple VMs need simultaneous read/write access to the same files.

For setup, see the [**NAS Overview**](../nas/overview.md) and [**NAS Shares**](../nas/nas-shares.md).

## Method 4 — Shared Disk

A **Shared Disk** attaches one existing disk to multiple VMs at the same time. The disk exists once. You create it as a normal **Disk** on the first VM. On each other VM, you add a drive with **Shared Disk** enabled and select that disk in **Media File**. This attaches the same disk; it does not create new storage.

Shared disks present NAA/WWN identity and support SCSI-3 Persistent Reservations, which guest clusters use to coordinate access. If an I/O error occurs, VergeOS passes it through to the guest and does not stop the VM. The clustered guest can then make its own failover decision.

Requirements:

- Enable **Shared Disk** when you create the drive. You cannot turn it on later by editing the drive.
- Set the **Interface** to **Virtio-SCSI** or **Virtio-SCSI (Dedicated Controller)**.
- You cannot attach the same disk to the same VM twice.

{% hint style="danger" %}
Do not use Shared Disk with a file system that is not cluster-aware, such as a standard NTFS, ext4, or XFS volume. VergeOS does not coordinate writes between the VMs. Uncoordinated writes from multiple VMs corrupt the file system.
{% endhint %}

For the field details, see [**Virtual Machine Drives**](vm-drives.md#advanced-fields). For a full procedure, see the KB article [Using Shared Disks for Windows Clustering](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/using-shared-disks-windows-clustering).

## Choosing Between Them

- **Use Clone Disk** when a new VM must *start* with a copy of an existing disk and then change independently — for example, to deploy several VMs from the same prepared OS or data disk.
- **Use Clone Disk** for a one-time data hand-off where the receiving VM must own its copy.
- **Use Non-Persistent drives** when many VMs must start from the same image and return to that state on every restart — for example, VDI desktops, kiosks, classroom or lab VMs, and test VMs.
- **Use Non-Persistent drives** when each VM must discard its session changes — for example, to remove user changes or malware at every restart.
- **Use a NAS share** when two or more VMs need to read or write the *same* files concurrently.
- **Use a NAS share** for shared application content, team file storage, build artifacts, media libraries, or any workflow where consistency across VMs matters.
- **Use Shared Disk** when a guest cluster needs the same block device on every node — for example, a Windows Server Failover Clustering quorum disk or CSV volume.
- **Do not** use Clone Disk to keep data in sync between VMs — clones diverge immediately and there is no merge-back.
- **Do not** use Non-Persistent drives for data that must be kept — changes are discarded at every restart.
- **Do not** use Non-Persistent drives to keep VMs in sync with a source disk — existing drives do not pick up changes to the source.
- **Do not** use Shared Disk as a general file-sharing method between VMs that are not clustered. Use a NAS share instead.

## Summary

In short: **Clone Disk for seeding, Non-Persistent for golden images, NAS for file sharing, Shared Disk for guest clusters.** This page covered the four methods to share data between virtual machines in VergeOS:

- **Clone Disk** for independent, point-in-time copies of an existing drive — local block-level I/O, no network overhead, but no synchronization
- **Non-Persistent drives** for VMs that start from a copy of one golden image — each VM's changes are private and discarded at restart
- **NAS shares** for concurrent, file-level access from multiple VMs over SMB or NFS — with granular access control, at the cost of network overhead
- **Shared Disk** for concurrent, block-level access from the nodes of a guest cluster — with SCSI-3 Persistent Reservations, where the guest cluster coordinates writes

### Next Steps

- [Virtual Machine Drives](vm-drives.md#adding-a-drive) — Create a Clone Disk, Non-Persistent drive, or Shared Disk
- [Making a Non-Persistent VM](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/making-a-nonpersistent-vm) — Convert a VM to boot from a Non-Persistent drive
- [NAS Overview](../nas/overview.md) — Set up the NAS service
- [NAS Shares](../nas/nas-shares.md) — Create and manage file shares
- [Using Shared Disks for Windows Clustering](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/using-shared-disks-windows-clustering) — Configure shared disks for a Windows failover cluster
