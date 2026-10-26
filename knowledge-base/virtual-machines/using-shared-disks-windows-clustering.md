---
title: Using Shared Disks for Windows Clustering
slug: using-shared-disks-windows-clustering
author: VergeOS Documentation Team
date: 2026-10-08T12:00:00.000Z
semantic_keywords:
  - "configure windows cluster shared drives"
  - "shared cluster disk WSFC failover"
  - "scsi-3 persistent reservations shared drive"
use_cases:
  - windows_failover_clustering_on_vergeos
  - shared_disk_multi_vm_access
  - cluster_shared_volumes_setup
categories:
  - VM
  - vSAN
editor: markdown
dateCreated: 2026-09-24T17:26:07.927Z
description: >-
  Configure VergeOS shared disks for Windows Server Failover Clustering:
  create the disks, attach them to each cluster node VM, verify, and set
  anti-affinity.
tags:
  - drive
  - disk
  - cluster
  - shared-disk
  - persistent-reservations
  - wsfc
---

# Using Shared Disks for Windows Clustering

## Overview

{% hint style="info" %}
**Key Points**

- VergeOS supports shared disks with **SCSI‑3 Persistent Reservations**, so multiple VMs can attach the same virtual disk safely.
- This article covers the VergeOS configuration only: create the shared disks, attach them to each cluster node VM, verify, and set anti-affinity.
- Perform all Windows-side configuration (cluster validation, quorum, CSV) with Microsoft's WSFC documentation.
{% endhint %}

Windows Server Failover Clustering (WSFC) requires shared storage that all cluster nodes can access. VergeOS shared disks meet this requirement: one virtual disk attaches to multiple VMs concurrently, and SCSI-3 Persistent Reservations let the guest cluster coordinate access.

## Prerequisites

- VergeOS 26.2 or later.
- A user with permission to create and modify VMs.
- Networking, Active Directory Domain Services, and DNS reachable by all planned cluster nodes.
- Windows Server installation media and licenses for each cluster node.

## How shared disks work

A shared disk exists once. Create it as a normal **Disk** on the first cluster node. On every other node, add a drive with the **Shared Disk** option enabled and select the existing disk — this attaches the same disk, it does not create new storage.

{% hint style="warning" %}
Enable **Shared Disk** when you create the drive on each additional node. The option cannot be turned on later by editing the drive.
{% endhint %}

## Steps

### 1. Create the cluster node VMs

1. Create each cluster node VM with its own OS disk.
2. Add a NIC for client access and, if your design requires it, a separate NIC for cluster heartbeat.
3. Install Windows Server on each VM.
4. Join each VM to the domain.

Make sure the domain controller is powered on and reachable before you power on the cluster node VMs.

For drive and NIC field details, see [Virtual Machine Drives](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/virtual-machines/vm-drives).

### 2. Add the shared disks to the first cluster node

On the first cluster node VM, create the disks the cluster shares — for example a quorum disk, data disks, and CSV disks.

For each disk:

1. From the VM dashboard, click **New Drive**.
2. Enter a clear **Name**, for example `Cluster-Quorum`, `Cluster-Data01`, or `Cluster-CSV01`. This name identifies the disk when you attach it to the other nodes.
3. Set **Media** to **Disk**.
4. Set **Interface** to **Virtio-SCSI** or **Virtio-SCSI (Dedicated Controller)**. These interfaces support the SCSI-3 Persistent Reservations WSFC requires.
5. Set the **Disk Size**.
6. Click **Submit**.

### 3. Attach the shared disks to each additional cluster node

On each additional cluster node VM, attach every shared disk:

1. From the VM dashboard, click **New Drive**.
2. Enter a descriptive **Name**.
3. Expand the **Advanced** section and enable **Shared Disk**. The **Interface** choices reduce to **Virtio-SCSI** and **Virtio-SCSI (Dedicated Controller)**.
4. In **Media File**, select the disk created on the first node. The list shows existing disks grouped by VM, as drive name and description.
5. Click **Submit**.

Repeat for each shared disk the cluster requires.

### 4. Verify the shared disk configuration

1. Navigate to **Virtual Machines > VM Drives**.
2. In the filter row under the **Shared** column, select **Yes**.
3. Verify each shared disk appears once for each cluster node VM.
4. Verify the **Media File** column shows the same file name (for example `disk_28_16.raw`) on every node's entry for a given disk. The identical file name confirms all nodes attach the same virtual disk.

### 5. Configure anti-affinity for the cluster nodes

Run the cluster node VMs on different VergeOS nodes so one physical failure takes down only one cluster node.

1. On each cluster node VM, click **Edit**.
2. Set **HA Group** to the same value on every cluster node VM, for example `wsfc-nodes`. Do not start the value with `+` — a leading `+` requests same-node affinity, the opposite behavior.
3. Click **Submit**.

VergeOS now places the VMs on separate nodes whenever possible. For details, see [Settings that Influence VM Node Selection](../automation-api/determine-node-where-vm-runs.md).

### 6. Power on the cluster nodes

1. Power on each cluster node VM.
2. Verify each VM starts on a different VergeOS node.
3. In Windows Disk Management on each node, verify all shared disks are visible.

### 7. Continue with WSFC installation

The VergeOS configuration is complete. Follow Microsoft's WSFC documentation to validate the cluster, configure quorum, enable CSV if applicable, and install clustered roles. The **Cluster Validation Wizard** confirms shared disk behavior before you finalize the cluster.

## Additional Resources

- [Virtual Machine Drives](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/virtual-machines/vm-drives) — all drive configuration fields, including Shared Disk.
- [Settings that Influence VM Node Selection](../automation-api/determine-node-where-vm-runs.md) — HA groups, preferred node, and cluster placement.
- [26.2 Release Notes](https://app.gitbook.com/s/33mA7es4mQYkyUa7dMvu/2026/26-2-release-notes) — the release that introduced shared disks.

{% hint style="info" %}
**Need Help?**

If you have questions or problems with this procedure, contact the VergeOS support team.
{% endhint %}
