---
title: Using Shared Disks for Windows Clustering
slug: using-shared-disks-windows-clustering
description: Step-by-step setup of shared disk for use by clustering applications
author: VergeOS Documentation Team
date: 2026-09-28T14:15:07.757Z
semantic_keywords:
  - "configure windows cluster drives"
  - "shared cluster disk"
  - "shared drive
use_cases:
  - windows clustering on VergeOS
  - multiple vms with shared disk access
tags:
  - drive
  - disk
  - cluster
  - persistent reservations
categories:
  - VM
  - vSAN
editor: markdown
dateCreated: 2026-09-24T17:26:07.927Z
---

## Overview

{% hint style="info" %}
**Key Points**

- VergeOS supports shared disks using **SCSI‑3 Persistent Reservations**, enabling multiple VMs to attach the same virtual disk safely.  
- This guide walks through creating shared disks, attaching them to multiple VMs, verifying configuration, and preparing VMs for WSFC installation.  
- Windows‑side configuration (cluster creation, quorum setup, CSV enablement, etc.) must be performed using Microsoft documentation.

{% endhint %}


# Using Shared Disks for Windows Clustering  
  
Windows Server Failover Clustering (WSFC) requires shared storage that supports **SCSI‑3 Persistent Reservations** so cluster nodes can safely coordinate access to quorum, data, and Cluster Shared Volumes (CSV). VergeOS supports shared disks that meet these requirements, enabling multiple VMs to access the same virtual drive concurrently.

This guide explains **how to configure shared disks in VergeOS** for use by Windows clustering. It focuses on the VergeOS configuration steps only. For cluster creation, quorum configuration, CSV setup, and node‑level requirements, consult Microsoft’s official WSFC documentation.


{% hint style="warning" %}

**Important:**  Consult official WSFC documentation for guidance on cluster node configuration, disk sizing, quorum models, CSV requirements, and validation steps.

{% endhint %}

---


## 1. Prepare Active Directory and DNS

Before configuring shared disks, build the foundational services required for WSFC:

- Deploy and configure **Active Directory Domain Services**.  
- Ensure **DNS** is functioning and resolvable by all future cluster nodes.  
- Verify the domain controller is powered on and reachable.

{% hint style="success" %}
**Hint:** Always confirm your domain controller is online before powering on cluster node VMs.

{% endhint %}

---

## 2. Create Cluster Node Virtual Machines

Create the VMs that will serve as WSFC cluster nodes:

- Deploy each VM with its own **OS disk**.  
- Install Windows Server and join each VM to the domain.
- Power off the VMs. 

---

## 3. Add Shared Disks to the First Cluster Node

On the first cluster node VM, add the disks that will be shared across the cluster (e.g., **quorum**, **application/data**, **CSV** disks).

For each disk:

- **Name:** Use a clear, descriptive name (e.g., `Cluster-Quorum`, `Cluster-Data01`, `Cluster-CSV01`).  
  This name will appear when attaching the disk to other nodes.
- **Media:** `Disk`  
- **Interface:** `virtio SCSI` or `virtio SCSI (Dedicated Controller)`  
  These interfaces support SCSI‑3 PR behavior required by WSFC.


---

## 4. Attach Shared Disks to Additional Cluster Nodes

Create the second (and any additional) cluster node VM. For each shared disk:

- **Name:** Use a descriptive name for administrative clarity.  
- **Shared Disk:** Enable this option (found under **Advanced**).  
- **Media File:** Select the disk created on the first cluster node.  
  The dropdown will list all drives belonging to that VM.

Repeat for each shared disk required by the cluster.

---

## 5. Verify Shared Disk Configuration in VergeOS

To confirm shared disks are properly configured:

1. Navigate to **Virtual Machines → VM Drives**.  
2. Under the **Shared** column, select **Yes** to filter the list.  
3. Verify that each shared disk appears once for **each cluster node VM**.  
4. The **Media File** column displays the same underlying filename (e.g., disk_28_16.raw) across all nodes for a shared disk.  This identical filename indicates that all cluster nodes are attached to the same virtual disk object, which is required for WSFC.


This ensures all nodes have access to the same virtual disk objects.

---

## 6. Configure Anti‑Affinity for Cluster Nodes

Cluster nodes should run on **different VergeOS host nodes** to ensure high availability. Anti‑affinity prevents both VMs from running on the same physical host.

- Set the **HA Group** to the same value on all cluster node VMs.  
- Submit changes.  
- This ensures VergeOS places the VMs on separate nodes whenever possible.

For more details, see the KB article on [Settings that Influence VM Placement](automation-api/determine-node-where-vm-runs.md)

---

## 7. Power On Cluster Nodes

Power on the cluster node VMs and verify:

- Each VM starts on a **different VergeOS host node**.  
- All shared disks are visible inside Windows Disk Management.  
- The domain controller is online and reachable.

---

## 8. Proceed with WSFC Installation

Your VMs are now ready for Windows Server Failover Clustering installation and configuration. Follow Microsoft’s documentation to:

- Validate the cluster  
- Configure quorum  
- Enable CSV (if applicable)  
- Install clustered roles or applications

Tools such as **Failover Cluster Manager** and **Cluster Validation Wizard** can confirm shared disk behavior before finalizing cluster setup.

---
