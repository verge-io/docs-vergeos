---
title: "Node sizing"
description: >-
  Baseline hardware profiles for VergeOS nodes. Use these recommendations to
  plan Standard Production, Small/Edge, Backup deployments. Contact Sales or a partner for Performance or large-scale designs.
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

# Node sizing

Use this guide to plan hardware for a VergeOS deployment.

The profiles below are **baseline recommendations**, not hard minimums. Start with the profile that matches your deployment. Then adjust for workload density, snapshot schedule and retention, maintenance windows, and growth.

{% hint style="info" %}
**Workload resources**

Values in this guide cover VergeOS system operation. Allocate extra CPU, RAM, and storage for virtual machines, applications, peak load, and growth.
{% endhint %}

## Deployment model selection

Use this table to select the correct profile to size nodes. These models are intended as directional guidance rather than rigid prescriptions. Choose the model that fits your environment, then adapt to your specific requirements.

| Deployment Model | Typical Use Cases | Key Characteristics | When to Choose |
|------------------|------------------|---------------------|----------------|
| [**Standard Production**](#standard-production) | Mixed workloads, moderate databases, general business apps | Balanced CPU/RAM, predictable performance, full redundancy | General-purpose deployments that need straightforward scaling and predictable performance for line-of-business applications |
| [**Backup**](#backup-nodes) | Archive retention, synchronized backups | Lower endurance media acceptable, Tier 0 only on controller nodes | When nodes store backup data, not production workloads |
| [**Small / Edge**](#small--edge) | Retail, remote sites, sensors, light analytics | 1–2 nodes, simple, low density, often no dedicated Tier 0 | When simplicity and footprint matter more than performance |
| [**Single-node**](#single-node-systems) | Small sites, labs, test environments | No Core Fabric, metadata on primary tier | When redundancy is not required |
| [**Performance / High Capacity / Scale**](#performance--high-capacity--scale) | High-IOPS databases, GPU analytics, large VDI, multi-tenant hosting | High base clock CPUs, large RAM buffers, high-endurance Tier 0, NVMe-heavy | When performance or scale is the primary requirement |

## How to use this guide

1. [Apply generic node requirements](#generic-node-requirements) — CPU, RAM, NICs, disk type, endurance
2. [Identify your deployment model](#deployment-model-selection) — use the table above to select your profile
3. [Size Tier 0 (metadata)](#tier-0-metadata-sizing) — based on usable Tier 1–5 capacity and snapshot retention
4. [Add CPU and RAM for workloads](#ram-for-storage) — VergeOS system requirements plus guest workload resources

Most Standard Production systems run as one HCI cluster. Cluster count is a short proxy for the deployment model:

- **1 cluster:** HCI. Controller, storage, and compute roles can share the same nodes.
- **2 clusters:** hybrid UCI/HCI.
- **3 or more clusters:** full UCI.

For HCI and UCI models, node types, and when to separate roles, see [HCI vs UCI: Deployment Models](https://app.gitbook.com/s/qLUTTK5fxfW4S9FoS9GE/module-1-architecture-fundamentals/02-hci-vs-uci) and [Clusters & Node Types](https://app.gitbook.com/s/qLUTTK5fxfW4S9FoS9GE/module-1-architecture-fundamentals/05-clusters-nodes) in Learn the Platform.

{% hint style="info" %}
**HCI is the default**

Most Standard Production systems run as one HCI cluster. Controller, storage, and compute roles can share the same nodes. Dedicated controller, storage-only, or compute-only nodes are optional design choices, not a requirement for every deployment.
{% endhint %}

VergeOS Sales, Support, and authorized resellers can help with workload review and hardware selection. See [Contact Verge.io](https://www.verge.io/contact/).

## Generic node requirements

These minimums apply to all node types and profiles:

- AMD or Intel x86_64 processor with hardware virtualization
- Minimum **16 GB RAM** dedicated to VergeOS
- IPMI, iDRAC, iLO, or equivalent out-of-band management
- HBA or RAID controller in **JBOD or IT mode** (no RAID); NVMe direct-attach preferred
- **1 × 1 GbE** NIC for the External Network (Intel, NVIDIA Mellanox, or Broadcom)
- **1 × 10 GbE** NIC for the Core Fabric Network (Intel, NVIDIA Mellanox, or Broadcom; not required for single-node deployments)

For core fabric and external network design, see [Network design](network-design.md).

### Disk and endurance guidance

Review this guidance before you select disks for a profile.

{% hint style="danger" %}
**Enterprise disks only (production)**

VergeOS does not officially support consumer-grade disks in production or in backup-of-production systems. Use enterprise-grade devices. Consumer-grade disks can be acceptable for test, development, or proof of concept when data loss is acceptable. Some consumer devices fail because of firmware limits or non-standard commands.
{% endhint %}

{% hint style="warning" %}
**Boot-only devices (including Dell BOSS)**

Boot-oriented devices such as Dell BOSS cards are for **boot or OS only**. Do not assign them to storage tiers 0–5. Select them as boot-only devices for VergeOS. These devices lack the write endurance and write buffer that Tier 0 and workload tiers need.
{% endhint %}

- **Tier 0:** Use enterprise media only. Do not use consumer NVMe. For endurance and capacity requirements, see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing).
- **Production workload tiers (Tier 1–5):** Use enterprise media only. Do not use consumer NVMe. For write-oriented or general-purpose media, use a minimum of **1 drive-write per day (DWPD)**. You can use read-intensive enterprise media when that media matches the workload.
- HDDs larger than **8 TB** are not recommended outside archive-specific environments. Large HDDs extend rebuild time and can affect performance and availability.

### Tier 0 (metadata) sizing

Tier 0 holds vSAN metadata: the structural information VergeOS uses to track usable data. Correct Tier 0 sizing is essential for stable vSAN operation in every deployment profile. Metadata needs vary with workload behavior, snapshot strategy, and vSAN scale. See [Storage Tiers in VergeOS vSAN](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/storage-tiers).

**Where metadata is stored:** most deployments store metadata on a dedicated Tier 0. Small/Edge systems [can store metadata on the primary tier instead](#small--edge). The same sizing guidance applies; reserve the required metadata capacity within the primary tier.

#### Baseline Tier 0 requirements

- **Media:** enterprise SSD. Tier 0 does not have to be NVMe — enterprise SAS SSD is acceptable when it meets the endurance and capacity requirements below.
- **Minimum endurance:** 1 DWPD
- **Capacity:** about **5 GB of usable Tier 0 per 1 TB of usable Tier 1–5 capacity** at 3 DWPD, or an equivalent capacity and endurance profile (for example, 15 GB per 1 TB at 1 DWPD)

Both sides of this ratio are **system-wide usable capacity**, measured after redundancy. Copies of metadata — across controller nodes, and across local drives within a node — are redundancy, not added usable capacity: usable Tier 0 is raw Tier 0 divided by the number of local copies. See [Local Node Tier 0 Metadata Redundancy (D+x)](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/tier0-local-redundancy).

The equivalence trades capacity for endurance: metadata occupies about 5 GB per 1 TB either way. On 1 DWPD media, the extra capacity is endurance headroom, not additional metadata space. Prefer enough capacity at 1 DWPD over a chase for 3 DWPD when 1 DWPD enterprise media meets the need.

This baseline assumes the default [*System Snapshots* profile](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/snapshot-profiles) or a similar schedule. That profile retains **7 snapshots** at once: 3 hourly, 3 daily (midnight), and 1 daily (noon). When you count your own retained snapshots, include VM and volume snapshot profiles as well as the system profile.

#### When to increase Tier 0 capacity

**Increased snapshot retention**

Snapshot behavior is a primary driver of metadata growth. Each retained snapshot can add up to about **0.5 GB per 1 TB of usable Tier 1–5 capacity** (an upper bound). Actual use depends on the snapshot delta: write-intensive workloads such as heavy SQL or random-write patterns approach the upper bound, while sequential or low-change workloads use less metadata per snapshot.

The conservative baseline absorbs moderate retention beyond the default profile. For most systems with a **low to moderate change rate**, the baseline (5 GB/TB) can hold about **25–30 snapshots**. Fleet telemetry confirms this: the 75th percentile at 25 snapshots is about 4.7 GB/TB, right at the baseline. Systems with **moderate to high change rate** (for example dense SQL database usage, high-frequency trading systems, PLCs) should increase to about **10 GB usable Tier 0 per 1 TB usable Tier 1–5 capacity** when retaining 25–30 snapshots.

**Tier 0 sizing examples**

| Change Rate | Retained Snapshots | Tier 0 Sizing | Notes |
|-------------|-------------------|---------------|-------|
| Low to Moderate | 7 (default) | 5 GB/TB (baseline) | Baseline safely absorbs the default 7 snapshots |
| Low to Moderate | 25–30 | 5 GB/TB (baseline) | 25–30 snapshots can still be absorbed |
| Moderate to High | 7 (default) | 5 GB/TB (baseline) | Baseline safely absorbs the default 7 snapshots |
| Moderate to High | 25–30 | 10 GB/TB | Higher guideline for increased snapshot retention with moderate to high change rate |

If you plan to retain more than about 25–30 snapshots or face workloads beyond this table, contact VergeOS Sales or an authorized reseller partner for assistance. See [Contact Verge.io](https://www.verge.io/contact/).

**Planned vSAN capacity expansion**

Size Tier 0 for total vSAN usable capacity. If you expect near-term scaling (adding storage nodes or expanding Tiers 1–5), upsize Tier 0 in advance to avoid replacing metadata devices later.

To add Tier 0 after installation, see [Adding Tier 0 to an Existing System](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/storage-vsan/adding-tier-zero).

Metadata sizing involves multiple interdependent factors. VergeOS Sales and authorized reseller partners can assist with workload evaluation and Tier 0 planning for new deployments and expansions. See [Contact Verge.io](https://www.verge.io/contact/).

### RAM for storage

- **Baseline:** on each node, reserve **16 GB for VergeOS plus 1 GB RAM per 1 TB of raw storage** on that node. Guest workload RAM is additional. For example, a node with 8 TB raw reserves 24 GB before guest RAM.
- **Storage buffer (cache) RAM** is a separate, additive need. It matters most in performance environments. Do not treat a single higher GB/TB figure as a substitute for both needs. For sizing [Performance](#performance--high-capacity--scale) deployment model nodes and their storage buffer, contact a VergeOS partner or the VergeOS sales team.

### CPU and storage disks

For Standard Production and Backup profiles, plan **1 physical core per storage disk** on each node that contributes vSAN disks. Count Tier 0 devices as storage disks. Do not count the boot device, and do not count hardware threads as extra cores.

## Deployment profiles

### Standard Production

Balanced, general-purpose deployments for mixed workloads with predictable performance, moderate VM density, full redundancy, and straightforward scaling.

**Typically suitable for:** line-of-business applications, moderate databases, light AI/ML workloads.

**Example use cases:**

- Manufacturing company that runs ERP, SQL, file services, and a small VDI pool
- Consulting firm that runs Windows Server workloads, SQL databases, document management, and seasonal high-load applications

#### Role flexibility

VergeOS supports flexible node role design. The requirements below describe the functional needs of the controller, storage, and compute roles; these roles can be combined on the same physical nodes depending on hardware availability, workload density, and deployment scale. Most Standard Production systems use nodes that serve as both controllers and storage participants, and smaller environments may run controller, storage, and compute workloads on the same nodes. For node role design, see [Clusters & Node Types](https://app.gitbook.com/s/qLUTTK5fxfW4S9FoS9GE/module-1-architecture-fundamentals/05-clusters-nodes).

The generic NIC list is a floor. Production systems use two Core Fabric Networks with redundant connections, typically 4 × 10/25/40/100 GbE ports per node. See [Network design](network-design.md).

#### Controller role (nodes 1 and 2; plus node 3 in an N+2 design)

Nodes that fulfill the controller role can also participate in storage and run workloads, depending on deployment design. For N+1 and N+2 requirements, see [Understanding vSAN Redundancy Levels](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-redundancy-levels).

- **Processor:** 2.7 GHz+ CPU (base clock)
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node, plus guest workload RAM (see [RAM for storage](#ram-for-storage))
- **Tier 0 (metadata storage):**
  - High-endurance enterprise SSD (NVMe or equivalent) that provides 5 GB of usable Tier 0 per 1 TB of usable Tier 1–5 capacity at 3 DWPD, or an equivalent endurance profile (for example, 15 GB per 1 TB at 1 DWPD)
  - Minimum acceptable endurance: 1 DWPD

{% hint style="info" %}
**Capacity considerations**

- When a node has more than one Tier 0 drive, VergeOS automatically mirrors metadata across the local drives to match the system redundancy level (two copies on N+1, three on N+2), up to the drive count. Usable Tier 0 capacity is total raw Tier 0 capacity divided by the number of local copies; drives beyond the required copy count add usable capacity. For details, see [Local Node Tier 0 Metadata Redundancy (D+x)](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/tier0-local-redundancy).
- Install two Tier 0 drives per controller node on an N+1 system, and three on an N+2 system, for full local protection.
- Metadata capacity must be increased for environments with high data change rates and/or expanded snapshot retention; see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing).
{% endhint %}

#### Storage role (vSAN participants)

Nodes that fulfill the storage role can also serve as controllers or run compute workloads. Use at least two nodes with identical disk configurations (except [single-node systems](#single-node-systems)).

- **Processor:** 2.7 GHz+ CPU (base clock). Base clock also affects storage performance on nodes that run compute.
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node (see [RAM for storage](#ram-for-storage))
- **CPU:** 1 physical core per storage disk (see [CPU and storage disks](#cpu-and-storage-disks))
- **Storage:**
  - At least one enterprise NVMe or SATA/SAS SSD per node (primary tier)
  - Enterprise HDDs are acceptable for low performance, snapshots, archive, or file services (see [disk and endurance guidance](#disk-and-endurance-guidance))

#### Compute role

Compute-only nodes are optional; compute workloads can run on controller or storage nodes in smaller or consolidated deployments.

- **Compute-only nodes:** follow the [generic node requirements](#generic-node-requirements) and size CPU and RAM for the workloads hosted on them. Base clock still affects guest disk latency: a compute-only node processes I/O even when the disks are on other nodes.
- **Combined roles:** when compute workloads run on nodes that also serve controller or storage roles, allocate sufficient additional resources. Guest workloads require their own CPU and RAM capacity, separate from what VergeOS needs for controller functions, metadata handling, and vSAN participation. Size combined-role nodes with extra RAM for guest memory and enough CPU headroom to keep performance predictable for both system services and hosted workloads.

---

### Performance / high capacity / scale

Use this profile for high-density, high-IOPS, low-latency environments, large snapshot counts, sustained write patterns, or large east-west traffic.

Flat GB-per-TB ratios that work for Standard Production do not scale in a linear way into large Performance systems. Snapshot schedule and retention drive metadata need. Storage buffer RAM is a separate additive requirement.

{% hint style="warning" %}
**Architect with a partner or Sales**

Contact a VergeOS partner or the VergeOS sales team to architect your performance environment. Use published [reference architectures](../reference-architecture/data-science.md) where they apply. Do not treat Standard Production ratios as linear guidance for very large NVMe systems (for example multi-dozen nodes at petabyte class).
{% endhint %}

**Example use cases:**

- Financial services with high-transaction databases, large VDI, or GPU analytics
- Regional MSPs that deliver multi-tenant hosting and GPU-accelerated workloads

When a partner designs the system, typical building blocks include higher base clock CPUs, more RAM per TB raw storage plus explicit storage buffer RAM, redundant high-endurance Tier 0, multiple enterprise SSDs or NVMe devices per storage node, and 25/40/100 GbE fabrics. Exact values depend on workload and scale.

Related pages:

- [High-performance cluster deployments](../reference-architecture/data-science.md)
- [Multi-tenant deployments](../reference-architecture/csp.md)

---

### Small / Edge

Two nodes or fewer. Compact deployments that prioritize simplicity and low operational overhead. Suitable for small sites, retail, remote facilities, and distributed edge. Workloads are modest and not dense.

**Examples:**

- Remote monitoring stations that ingest sensors and run light analytics
- Retail locations that report to a central or regional site

#### Node requirements

- **Processor:** see [generic node requirements](#generic-node-requirements)
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node (see [RAM for storage](#ram-for-storage))
- **Tier 0:** Still plan for Tier 0 when the design needs dedicated metadata devices. Tier 0 does not have to be NVMe; enterprise SAS or NVMe SSD is acceptable.
- On **1–2 node** systems where the primary tier is already all-NVMe or all-SSD, a **dedicated** Tier 0 device is often unnecessary. Metadata then resides on the primary tier; the same sizing guidance applies, so reserve the required metadata capacity within the primary tier (see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing)). Confirm the layout with Sales, Support, or an authorized reseller when unsure.
- **Network:** see [generic node requirements](#generic-node-requirements)
- **Cluster size:** 2-node minimum unless you deploy a [single-node system](#single-node-systems)
- **Note:** Not appropriate for performance-sensitive workloads

For a topology example, see [Edge cluster deployments](../reference-architecture/edge.md).

---

### Backup nodes

Storage-focused nodes for backup or archive retention.

**Examples:**

- Storage nodes in a production cluster that use lower-DWPD enterprise SSDs for backup data
- Nodes in a separate VergeOS backup cluster that receive synchronized backups

#### Node requirements

- **Processor:** see [generic node requirements](#generic-node-requirements)
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node (see [RAM for storage](#ram-for-storage))
- **CPU:** 1 physical core per storage disk (see [CPU and storage disks](#cpu-and-storage-disks))
- **Tier 0:** Size Tier 0 on the controller nodes of the backup system (nodes 1 and 2). Backup systems in this profile run N+1, so there are two controller nodes. Do not add dedicated Tier 0 devices to every backup storage node. Tier 0 does not have to be NVMe. Use enterprise SAS or NVMe SSD; do not use consumer devices. Minimum acceptable endurance: **1 DWPD**. Retaining more snapshots than the default profile can drive additional metadata consumption and may require increased Tier 0 capacity; see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing).
- **Network:** see [generic node requirements](#generic-node-requirements)
- **Storage:**
  - Lower-performance, lower-endurance enterprise devices are acceptable
  - HDDs larger than 8 TB may be used for archive-specific layouts; expect extended rebuild times
- **Note:** Not appropriate for performance-sensitive workloads

---

### Single-node systems

Single-node systems follow the **Small / Edge** profile above, with one difference: a single-node system has no node-to-node vSAN or fabric traffic, so **no Core Fabric Network is required**.

#### Node requirements

- **Processor:** see [generic node requirements](#generic-node-requirements)
- **RAM:** 16 GB + 1 GB per 1 TB raw storage per node (see [RAM for storage](#ram-for-storage))
- **Tier 0:** same guidance as Small / Edge. Where the primary tier is all-NVMe or all-SSD, a dedicated Tier 0 device is often unnecessary; metadata then resides on the primary tier, so reserve the required metadata capacity there (see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing))
- **Network:** 1 × 1 GbE NIC for the External Network; no Core Fabric NIC required
- **Note:** A single node provides no node-level redundancy. Redundancy comes from copies across the node's local drives — see [Local Node Tier 0 Metadata Redundancy (D+x)](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/tier0-local-redundancy). Protect workloads with snapshots and off-site sync or backup.

---

## Scaling considerations

VergeOS clusters scale horizontally. Add nodes to increase storage capacity and compute. See [Core concepts](concepts.md) for node and cluster types.

When you plan controller capacity:

- Size **Tier 0 storage and RAM** for total cluster storage and for snapshot policy.
- As VM density grows, controller and HCI nodes may need more CPU.

As the environment grows, review the hardware profile again. A design that fit the first deployment can be wrong after large capacity or workload increases.
