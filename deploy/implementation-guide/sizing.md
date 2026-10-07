---
title: "Node sizing"
description: >-
  Baseline hardware profiles for VergeOS nodes. Use these recommendations to
  plan Standard Production, Small/Edge, and Backup deployments. Contact a
  partner or Sales for Performance and large-scale designs.
semantic_keywords:
  - "VergeOS node sizing CPU RAM storage"
  - "VergeOS hardware baseline Standard Production HCI"
  - "Tier 0 metadata capacity snapshot retention"
  - "enterprise disk endurance DWPD boot-only Dell BOSS"
use_cases:
  - hardware_procurement
  - capacity_planning
  - node_sizing
  - storage_tier_design
tags:
  - sizing
  - hardware
  - requirements
  - cpu
  - ram
  - storage
  - nvme
  - vsan
categories:
  - Installation
---

# VergeOS Node Sizing Guide 
 
Overview 

A clear, hierarchical, decision‑driven guide for planning VergeOS hardware.  

---

## Purpose of This Guide**

This guide provides a structured method for sizing VergeOS nodes across all deployment models. VergeOS is hardware‑agnostic and highly flexible, which means sizing depends on workload behavior, snapshot strategy, redundancy level, and growth expectations.  

This document gives you a **repeatable sizing workflow**, **baseline profiles**, and **decision rules** to design predictable, stable VergeOS systems.
---

# How to Use This Guide**

Follow this workflow:

1. [**Apply generic node requirements**](#generic-node-requirements)  
   CPU, RAM, NICs, disk type, endurance

2. [**Identify your deployment model**](#deployment-model-selection)  
Deployment models help orient initial design and hardware decisions     
   (Standard Production, Performance, Small/Edge, Backup, or Single‑Node)

3. [**Size Tier 0 (metadata)**](##tier-0-metadata-sizing)  
   Based on usable Tier 1–5 capacity and snapshot retention

4. [**Size RAM for storage**](#ram-sizing)  
   VergeOS RAM + raw storage RAM + guest RAM.

5. [**Size CPU for storage disks and workloads**](#cpu-sizing)  
   One physical core per storage disk

6. [**Validate storage tier selection**](#storage-tier-1-5-selection)  
   Enterprise media only; endurance rules

7. [**Validate network requirements**](#network-requirements)  
   External + Core Fabric requirements

8. [**Apply scaling considerations**](#scaling-considerations)  
   Growth, snapshot expansion, and future capacity

---

## Generic Node Requirements
## (Apply to All Nodes)

These minimum requirements apply universally, regardless of profile or role.

- AMD or Intel x86_64 CPU with hardware virtualization
- Minimum **16 GB RAM** dedicated to VergeOS
- IPMI/iDRAC/iLO or equivalent
- HBA/RAID controller in **JBOD or IT mode** (no RAID)
- Enterprise‑grade storage media only
- Boot‑only devices (e.g., Dell BOSS) must **not** be used for Tier 0–5
- **1 × 1 GbE** NIC for External Network
- **1 × 10 GbE** NIC (not required for single-node deployments)
For core fabric and external network design, see [Network design](network-design.md).

{% hint style="info" %}
**Hardware Driver Reference**

VergeOS includes a broad set of networking and storage drivers as part of the platform. If you are planning a deployment and want to review the driver inventory, see:

- [Included Ethernet Drivers](nic-driver-list.md)
- [Included Storage Drivers](storage-driver-list.md)

If you do not see hardware you intend to use, contact **VergeOS Sales** for guidance.
{% endhint %}

VergeOS Sales, Support, and authorized resellers can help with workload review and hardware selection. See [Contact Verge.io](https://www.verge.io/contact/).

---

## Deployment Model Selection**

Use this table to select the correct profile to size nodes.  These models are intended as directional guidance rather than rigid prescriptions. Choose the model that fits your environment, then adapt to your specific requirements.

| Deployment Model | Typical Use Cases | Key Characteristics | When to Choose |
|------------------|------------------|---------------------|----------------|
| [**Standard Production**](#standard-production) | Mixed workloads, moderate databases, general business apps | Balanced CPU/RAM, predictable performance, full redundancy | <!-- when to choose standard production model --> |
| [**Backup**](#backup) | Archive retention, synchronized backups | Lower endurance media acceptable, Tier 0 only on controller nodes | When nodes store backup data, not production workloads |
| [**Small / Edge**](#small-edge) | Retail, remote sites, sensors, light analytics | 1–2 nodes, simple, low density, often no dedicated Tier 0 | When simplicity and footprint matter more than performance |
| [**Single‑Node**](#single-node) | Small sites, labs, test environments | No Core Fabric, metadata on primary tier | When redundancy is not required |
| [**Performance / High Capacity / Scale**](#performance-high-capacity-scale) | High‑IOPS databases, GPU analytics, large VDI, multi‑tenant hosting | High base clock CPUs, large RAM buffers, high‑endurance Tier 0, NVMe-heavy | When performance or scale is the primary requirement |
---


---

### Standard Production

Balanced, general-purpose deployments for mixed workloads with predictable performance, moderate VM density, full redundancy, and straightforward scaling.

**Typically suitable for:** line-of-business applications, moderate databases, light AI/ML workloads.

**Example use cases:**

- Manufacturing company that runs ERP, SQL, file services, and a small VDI pool
- Consulting firm that runs Windows Server workloads, SQL databases, document management, and seasonal high-load applications


{% hint style="info" %}
**Node Roles**
- Most standard production deployments run as one HCI cluster where controller, storage, and compute roles share the same nodes.
- Dedicated controller, storage-only, or compute-only nodes are optional design choices 

For HCI and UCI models, node types, and when to separate roles, see [HCI vs UCI: Deployment Models](https://app.gitbook.com/s/qLUTTK5fxfW4S9FoS9GE/module-1-architecture-fundamentals/02-hci-vs-uci) and [Clusters & Node Types](https://app.gitbook.com/s/qLUTTK5fxfW4S9FoS9GE/module-1-architecture-fundamentals/05-clusters-nodes) in Learn the Platform.

{% endhint %}


#### Node requirements

- **Processor:** 2.7 GHz+ CPU (base clock)
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node, plus guest workload RAM (see [RAM for storage](#ram-sizing))
- **Tier 0 (metadata storage):**
  - High-endurance enterprise SSD (NVMe or equivalent) that provides 5 GB of usable Tier 0 per 1 TB of usable Tier 1–5 capacity at 3 DWPD, or an equivalent endurance profile (for example, 15 GB per 1 TB at 1 DWPD). Minimum acceptable endurance: 1 DWPD. (see [Tier 0 (Metadata) Sizing ](#tier-0-metadata-sizing))
- **Storage (Tiers 1-5):**
  - At least one enterprise NVMe or SATA/SAS SSD per node (primary tier)
  - Each storage tier should be run on at least two nodes with identical disk configuration for that tier 
  - Enterprise HDDs are acceptable for low performance, snapshots, archive, or file services (see [**Storage Tier Selection**](#storage-tier-1-5-selection)
- **CPU:** 
  - 1 physical core per storage disk (see [CPU Sizing](#cpu-sizing)
  - **Combined roles:** Compute workloads can run on controller or storage nodes in smaller or consolidated deployments; when compute workloads run on nodes that also serve controller or storage roles, allocate sufficient additional resources. Guest workloads require their own CPU and RAM capacity, separate from what VergeOS needs for controller functions, metadata handling, and vSAN participation. Size combined-role nodes with extra RAM for guest memory and enough CPU headroom to keep performance predictable for both system services and hosted workloads.
  - **Compute-only nodes (optional):**  - Follow the [generic node requirements](#generic-node-requirements) and size CPU and RAM for the workloads hosted on them. Base clock still affects guest disk latency: a compute-only node processes I/O even when the disks are on other nodes.
- **Network:** Production systems use two Core Fabric Networks with redundant connections, typically 4 × 10/25/40/100 GbE ports per node. See [Network design](network-design.md).

---

### Backup nodes

Storage-focused nodes for backup or archive retention.

**Examples:**

- Storage nodes in a production cluster that use lower-DWPD enterprise SSDs for backup data
- Nodes in a separate VergeOS backup cluster that receive synchronized backups

#### Node requirements

- **Processor:** see [generic node requirements](#generic-node-requirements)
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node (see [RAM Sizing](#ram-sizing))
- **CPU:** 
  - 1 physical core per storage disk (see [CPU Sizing](#cpu-sizing))
- **Tier 0/Metadata:** Size Tier 0 on the controller nodes of the backup system (nodes 1 and 2) See [Tier 0 (Metadata) Sizing ](#tier-0-metadata-sizing). 
  - Backup systems in this profile run N+1, so there are two controller nodes. 
  - Metadata can be placed on primary storage tier (must be Enterprise SAS or NVMe SSD. Minimum acceptable endurance: **1 DWPD**.) See [Tier 0 (metadata) sizing](#tier-0-metadata-sizing).
- **Network:** see [generic node requirements](#generic-node-requirements)
- **Storage:**
  - Lower-performance, lower-endurance enterprise devices are acceptable
  - HDDs larger than 8 TB may be used for archive-specific layouts; expect extended rebuild times
- **Note:** Not appropriate for performance-sensitive workloads

---

### Small / Edge

Two nodes or fewer. Compact deployments that prioritize simplicity and low operational overhead. Suitable for small sites, retail, remote facilities, and distributed edge. Workloads are modest and not dense.

**Examples:**

- Remote monitoring stations that ingest sensors and run light analytics
- Retail locations that report to a central or regional site

#### Node requirements

- **Processor:** see [generic node requirements](#generic-node-requirements)
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node (see [RAM Sizing](#ram-sizing))
- **Tier 0/Metadata:** 
  - On **1–2 node** systems where the primary tier is already all-NVMe or all-SSD, a **dedicated** Tier 0 device is often unnecessary. Metadata then resides on the primary tier; the same sizing guidance applies, so reserve the required metadata capacity within the primary tier (see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing)).
  - Use dedicated Tier 0 devices when the design needs dictate (e.g., very write-intensive workloads, high storage capacity)
  - Tier 0 does not have to be NVMe; enterprise SAS or NVMe SSD is acceptable.
- **Network:** see [generic node requirements](#generic-node-requirements)
- **Cluster size:** 2-node minimum unless you deploy a [single-node system](#single-node-systems)
- **Note:** Not appropriate for performance-sensitive workloads

For a topology example, see [Edge cluster deployments](../reference-architecture/edge.md).

---

### Single-node systems

Single-node systems follow the **Small / Edge** profile above, with one difference: a single-node system has no node-to-node vSAN or fabric traffic, so **no Core Fabric Network is required**.

#### Node requirements

- **Processor:** see [generic node requirements](#generic-node-requirements)
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node (see [RAM Sizing](#ram-sizing)
- **Tier 0:** same guidance as Small / Edge. Where the primary tier is all-NVMe or all-SSD, a dedicated Tier 0 device is often unnecessary; metadata then resides on the primary tier, so reserve the required metadata capacity there (see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing))
- **Network:** 1 × 1 GbE NIC for the External Network; no Core Fabric NIC required
- **Note:** A single node provides no node-level redundancy. Redundancy comes from copies across the node's local drives — see [Local Node Tier 0 Metadata Redundancy (D+x)](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/tier0-local-redundancy). Protect workloads with snapshots and off-site sync or backup.

---

### Performance / high capacity / scale

Use this profile for high-density, high-IOPS, low-latency environments, large snapshot counts, sustained write patterns, or large east-west traffic.

Flat GB-per-TB ratios that work for Standard Production do not scale in a linear way into large Performance systems. Snapshot schedule and retention drive metadata need. Storage buffer RAM is a separate additive requirement.

{% hint style="warning" %}
**Architect with a partner or Sales**

[Contact a VergeOS partner or the VergeOS sales team](https://www.verge.io/contact/) to architect your performance environment. Use published [reference architectures](../reference-architecture/data-science.md) where they apply. Do not treat Standard Production ratios as linear guidance for very large NVMe systems (for example multi-dozen nodes at petabyte class).
{% endhint %}

**Example use cases:**

- Financial services with high-transaction databases, large VDI, or GPU analytics
- Regional MSPs that deliver multi-tenant hosting and GPU-accelerated workloads

When a partner designs the system, typical building blocks include higher base clock CPUs, more RAM per TB raw storage plus explicit storage buffer RAM, redundant high-endurance Tier 0, multiple enterprise SSDs or NVMe devices per storage node, and 25/40/100 GbE fabrics. Exact values depend on workload and scale.

Related pages:

- [High-performance cluster deployments](../reference-architecture/data-science.md)
- [Multi-tenant deployments](../reference-architecture/csp.md)

---

## Tier 0 (Metadata) Sizing

Tier 0 holds vSAN metadata: the structural information VergeOS uses to track usable data. Correct Tier 0 sizing is essential for stable vSAN operation in every deployment.   Metadata needs vary with workload behavior, snapshot strategy, and vSAN scale. 

{% hint style="info"}
See [Storage Tiers in VergeOS vSAN](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/storage-tiers) for more information.

{% endhint %}

**Where metadata is stored:** most deployments store metadata on a dedicated Tier 0. Small/Edge and backup/archive systems can store metadata on the primary tier instead. The same sizing guidance applies; reserve the required metadata capacity within the primary tier.  <!-- For simplicity/readability, metadata is typically referred to generically as tier 0. -->


### Baseline Tier 0 requirements

- **Media:** enterprise SSD. Tier 0 - enterprise NVMe or SAS SSD 
- **Minimum endurance:** 1 DWPD
- **Capacity:** about **5 GB of usable Tier 0 per 1 TB of usable Tier 1–5 capacity** at 3 DWPD, or an equivalent capacity and endurance profile (for example, 15 GB per 1 TB at 1 DWPD)  metadata occupies about 5 GB per 1 TB either way. **Note:** On 1 DWPD media, the extra capacity is endurance headroom, not additional metadata space. 
{% hint style="info" %}

**Important:** Metadata capacity guidelines reflect the *usable* storage size. Copies of metadata — across controller nodes, and across local drives within a node — are redundancy, not added usable capacity: usable Tier 0 is raw Tier 0 divided by the number of local copies. See [Local Node Tier 0 Metadata Redundancy (D+x)](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/tier0-local-redundancy).  

This baseline assumes the default [*System Snapshots* profile](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/snapshot-profiles) or a similar schedule. That profile retains **7 snapshots** at once: 3 hourly, 3 daily (midnight), and 1 daily (noon). When you count your own retained snapshots, include VM and volume snapshot profiles as well as the system profile.  


### When to increase Tier 0 capacity

**Increased Snapshot Retention**

Snapshot behavior is a primary driver of metadata growth. Each retained snapshot can add up to about **0.5 GB per 1 TB of usable Tier 1–5 capacity (upper bound)** 
Actual use depends on the snapshot delta: write-intensive systems such as heavy SQL or random-write pattern workloads approach the upper bound, while sequential or low-change workloads will use much less metadata per snapshot.


The conservative baseline absorbs **moderate retention beyond the default profile**.  

Increase Tier 0 capacity if you plan to retain a larger number of snapshots.

As an average, most systems with a moderate change rate can safely absorb about 25–30 snapshots at the baseline tier 0 capacity guideline.


Systems with very high change rate (e.g., dense SQL database usage, HFT systems, PLCs) should increase to ~10Gb/1TB when retaining 25-30 snapshots


Tier 0 Sizing Examples

| Change Rate | Snapshot Retention |  Tier 0 sizing | Notes |
|------------------|----------------|-------------------------|-------|
| Low to Moderate  | 25-30 | 5Gb/1Tb (baseline) | 25-30 snapshots can still be absorbed|
| Moderate to High | default | 5Gb/1Tb (baseline) | baseline safely absorbs the default 7 snapshots | 
| Moderate to High | 25-30 | 10Gb/1Tb | Higher guideline for increased snapshot retention | 


{% hint style="success" %}
**Planning to store large numbers of snapshots?**
If you plan to store more than ~ 25-30 snapshots and need help sizing tier 0 to fit your environment, contact VergeOS or an authorized reseller partner for assistance.
See [Contact Verge.io](https://www.verge.io/contact/).
{% endhint %}  


**Planned vSAN capacity expansion**
Size Tier 0 for total vSAN usable capacity. If you expect near-term scaling (adding storage nodes or expanding Tiers 1–5), upsize Tier 0 in advance to avoid replacing metadata devices later.


Metadata sizing involves multiple interdependent factors. VergeOS Sales and authorized reseller partners can assist with workload evaluation and Tier 0 planning for new deployments and expansions. See [Contact Verge.io](https://www.verge.io/contact/).

---

# RAM Sizing

- **Baseline:** on each node, reserve **16 GB for VergeOS plus 1 GB RAM per 1 TB of raw storage** on that node. Guest workload RAM is additional. For example, a node with 8 TB raw disk reserves 24 GB before guest RAM.
- **Storage buffer (cache) RAM** is a separate, additive need for performance environments.  For Performance sizing, contact a VergeOS partner or the VergeOS sales team.

### Overview

Minimum **16 GB** per node.
Add **1 GB RAM per 1 TB raw storage** on the node.
Example:  
8 TB raw → 16 GB + 8 GB = **24 GB** + Additional RAM needed for guest workloads
Performance environments require additional buffer RAM.  
This is **additive** and not a substitute for baseline RAM.

---

## CPU Sizing

Minimum **1 physical core per storage disk** on each node that contributes vSAN disks. Count Tier 0 devices as storage disks (Boot device should not be counted). Hardware  threads do not count as extra cores.

### Overview

**Storage CPU Rule**: **1 physical core per storage disk** (including Tier 0).  
Do not count hardware threads.

### Base Clock

Minimum **2.7 GHz** base clock for Standard Production systems  
Higher base clock recommended for Performance.
Compute‑only nodes still process I/O and benefit from higher base clock.

---

## Storage Tier (1-5) Selection

Production systems must use enterprise disks
Tier 1–5: minimum **1 DWPD** for write‑oriented workloads  
Read‑intensive enterprise SSD acceptable when workload matches
HDDs > 8 TB are not recommended except for archive‑specific layouts

---

## Network Requirements

### External Network

Minimum **1 × 1 GbE** NIC


### Core Fabric Network


Minimum **1 × 10 GbE** NIC 
2 separate NICs recommended for increased resiliency. 
Production systems typically use **4 × 10/25/40/100 GbE**

{% hint style="info" %}

**Single‑Node Exception:**
Single‑node systems do not require Core Fabric.

{% endhint %}


---

## Scaling Considerations

VergeOS clusters scale horizontally. Add nodes to increase storage capacity and compute. See [Core concepts](concepts.md) for node and cluster types.

When you plan controller capacity:

- Size **Tier 0 storage and RAM** for total cluster storage and for snapshot policy.
- As VM density grows, controller and HCI nodes may need more CPU.

As the environment grows, review the hardware profile again. A design that fit the first deployment may not remain appropriate as substantial additions to node count, workload, or storage capacity are introduced.  



---

