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

# Node sizing

Use this guide to plan hardware for a VergeOS deployment.

The profiles below are **baseline recommendations**, not hard minimums. Start with the profile that matches your deployment. Then adjust for workload density, snapshot schedule and retention, maintenance windows, and growth.

{% hint style="info" %}
**Workload resources**

Values in this guide cover VergeOS system operation. Allocate extra CPU, RAM, and storage for virtual machines, applications, peak load, and growth.
{% endhint %}

## How to use this guide

1. Select the profile that matches your deployment.
2. Apply the [generic node requirements](#generic-node-requirements) to every node.
3. Size [Tier 0 (metadata)](#tier-0-metadata-sizing) from usable Tier 1–5 capacity and from your snapshot schedule and retention.
4. Add CPU and RAM for guest workloads.

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
- **1 × 10 GbE** NIC for the Core Fabric Network (Intel, NVIDIA Mellanox, or Broadcom)

For core fabric and external network design, see [Network design](network-design.md).

### Disk and endurance guidance

Review this guidance before you select disks for a profile.

{% hint style="warning" %}
**Enterprise disks only (production)**

VergeOS does not officially support consumer-grade disks in production or in backup-of-production systems. Use enterprise-grade devices. Consumer-grade disks can be acceptable for test, development, or proof of concept when data loss is acceptable. Some consumer devices fail because of firmware limits or non-standard commands.
{% endhint %}

{% hint style="warning" %}
**Boot-only devices (including Dell BOSS)**

Boot-oriented devices such as Dell BOSS cards are for **boot or OS only**. Do not assign them to storage tiers 0–5. Select them as boot-only devices for VergeOS. These devices lack the write endurance and write buffer that Tier 0 and workload tiers need.
{% endhint %}

- **Tier 0:** Use enterprise media only. Do not use consumer NVMe. For endurance and capacity requirements, see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing).
- **Production workload tiers (Tier 1–5):** Use enterprise media only. Do not use consumer NVMe. For write-oriented or general-purpose media, use a **minimum of 1 DWPD**. You can use read-intensive enterprise media when that media matches the workload.
- HDDs larger than **8 TB** are not recommended outside archive-specific environments. Large HDDs extend rebuild time and can affect performance and availability.

### Tier 0 (metadata) sizing

Tier 0 holds vSAN metadata: the structural information VergeOS uses to track usable data. Correct Tier 0 sizing is essential for stable vSAN operation in every deployment profile. Metadata needs vary with workload behavior, snapshot strategy, and vSAN scale. See [Storage Tiers in VergeOS vSAN](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/storage-tiers).

**Where metadata is stored:** most deployments store metadata on a dedicated Tier 0. Small/Edge systems can store metadata on the primary tier instead. The same sizing guidance applies; reserve the required metadata capacity within the primary tier.

#### Baseline Tier 0 requirements

- **Minimum endurance:** 1 DWPD
- **Capacity:** about **5 GB of usable Tier 0 per 1 TB of usable Tier 1–5 capacity** at 3 DWPD, or an equivalent capacity and endurance profile (for example, 15 GB per 1 TB at 1 DWPD)

Prefer enough capacity at 1 DWPD over a chase for 3 DWPD when 1 DWPD enterprise media meets the need.

This baseline assumes the default snapshot schedule (the *System Snapshots* [snapshot profile](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/snapshot-profiles)) or similar, with about seven or fewer regularly retained snapshots.

#### When to increase Tier 0 capacity

- **Snapshot retention above about seven snapshots.** Snapshot behavior is a primary driver of metadata growth. Each retained snapshot can add up to about **0.5 GB per 1 TB of usable capacity** (an upper bound). Actual use depends on the snapshot delta: write-intensive workloads such as heavy SQL or random-write patterns approach the upper bound, while sequential or low-change workloads use less metadata per snapshot. Increase Tier 0 capacity above the baseline if you plan to retain more than about seven snapshots.
- **Planned vSAN capacity expansion.** Size Tier 0 for total vSAN usable capacity. If you expect near-term scaling (adding storage nodes or expanding Tiers 1–5), upsize Tier 0 in advance to avoid replacing metadata devices later.

To add Tier 0 after installation, see [Adding Tier 0 to an Existing System](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/storage-vsan/adding-tier-zero).

Metadata sizing involves multiple interdependent factors. VergeOS Sales and authorized reseller partners can assist with workload evaluation and Tier 0 planning for new deployments and expansions. See [Contact Verge.io](https://www.verge.io/contact/).

### RAM for storage

- **Baseline:** about **1 GB RAM per 1 TB raw storage** per node for VergeOS storage operation.
- **Storage buffer (cache) RAM** is a separate, additive need. It matters most in performance environments. Do not treat a single higher GB/TB figure as a substitute for both needs. For Performance sizing, contact a VergeOS partner or the VergeOS sales team.

### CPU and storage disks

For Standard Production and Backup profiles, plan about **1 CPU core per storage disk** on nodes that present storage. This rule does not scale in a linear way for very large Performance systems.

## Deployment profiles

### Standard Production

Balanced, general-purpose deployments for mixed workloads with predictable performance, moderate VM density, full redundancy, and straightforward scaling.

**Typically suitable for:** line-of-business applications, moderate databases, light AI/ML workloads.

**Example use cases:**

- Manufacturing company that runs ERP, SQL, file services, and a small VDI pool
- Consulting firm that runs Windows Server workloads, SQL databases, document management, and seasonal high-load applications

#### Role flexibility

VergeOS supports flexible node role design. The requirements below describe the functional needs of the controller, storage, and compute roles; these roles can be combined on the same physical nodes depending on hardware availability, workload density, and deployment scale. Most Standard Production systems use nodes that serve as both controllers and storage participants, and smaller environments may run controller, storage, and compute workloads on the same nodes. For node role design, see [Clusters & Node Types](https://app.gitbook.com/s/qLUTTK5fxfW4S9FoS9GE/module-1-architecture-fundamentals/05-clusters-nodes).

#### Controller role (nodes 1 and 2; plus node 3 in an N+2 design)

Nodes that fulfill the controller role can also participate in storage and run workloads, depending on deployment design. For N+1 and N+2 requirements, see [Understanding vSAN Redundancy Levels](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-redundancy-levels).

- **Processor:** 2.7 GHz+ CPU (base clock)
- **RAM:** 1 GB RAM per 1 TB raw storage per node (plus guest workload RAM)
- **Tier 0 (metadata storage):**
  - High-endurance enterprise SSD (NVMe or equivalent) that provides 5 GB of storage per 1 TB at 3 DWPD, or an equivalent endurance profile (for example, 15 GB per 1 TB at 1 DWPD)
  - Minimum acceptable endurance: 1 DWPD

{% hint style="info" %}
**Capacity considerations**

- When more than one Tier 0 device is present, VergeOS automatically mirrors metadata locally on the additional drive. This provides extra protection for the metadata tier but does not increase Tier 0 usable capacity — the second device is used exclusively for redundancy. For details, see [Local Node Tier 0 Metadata Redundancy](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/tier0-local-redundancy).
- Metadata capacity must be increased for environments with high data change rates and/or expanded snapshot retention; see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing).
{% endhint %}

#### Storage role (vSAN participants)

Nodes that fulfill the storage role can also serve as controllers or run compute workloads. Use at least two nodes with identical disk configurations (except [single-node systems](#single-node-systems)).

- **Processor:** 2.7 GHz+ CPU (base clock). Base clock also affects storage performance on nodes that run compute.
- **RAM:** 1 GB RAM per 1 TB raw storage
- **CPU:** about 1 core per storage disk
- **Storage:**
  - At least one enterprise NVMe or SATA/SAS SSD per node (primary tier)
  - Enterprise HDDs are acceptable for low performance, snapshots, archive, or file services
  - HDDs larger than 8 TB are not recommended outside archive-specific environments because of extended rebuild times

#### Compute role

Compute-only nodes are optional; compute workloads can run on controller or storage nodes in smaller or consolidated deployments.

- **Compute-only nodes:** follow the [generic node requirements](#generic-node-requirements) and size CPU and RAM for the workloads hosted on them. CPU base clock also affects disk performance on compute nodes.
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
- **RAM:** 1 GB RAM per 1 TB raw storage
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
- **RAM:** 1 GB RAM per 1 TB raw storage
- **CPU:** about 1 core per storage disk
- **Tier 0:** Size Tier 0 on the controller nodes of the backup system (nodes 1 and 2). Do not add dedicated Tier 0 devices to every backup storage node. Tier 0 does not have to be NVMe. Use enterprise SAS or NVMe SSD; do not use consumer devices. Minimum acceptable endurance: **1 DWPD**. Retaining more snapshots than the default profile can drive additional metadata consumption and may require increased Tier 0 capacity; see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing).
- **Network:** see [generic node requirements](#generic-node-requirements)
- **Storage:**
  - Lower-performance, lower-endurance enterprise devices are acceptable
  - HDDs larger than 8 TB may be used for archive-specific layouts; expect extended rebuild times
- **Note:** Not appropriate for performance-sensitive workloads

---

### Single-node systems

Official support begins with the **October 2026** release.

Single-node systems follow the **Small / Edge** profile above, with one difference: a single-node system has no node-to-node vSAN or fabric traffic, so **no Core Fabric Network is required**.

#### Node requirements

- **Processor:** see [generic node requirements](#generic-node-requirements)
- **RAM:** 1 GB RAM per 1 TB raw storage
- **Tier 0:** same guidance as Small / Edge. Where the primary tier is all-NVMe or all-SSD, a dedicated Tier 0 device is often unnecessary; metadata then resides on the primary tier, so reserve the required metadata capacity there (see [Tier 0 (metadata) sizing](#tier-0-metadata-sizing))
- **Network:** 1 × 1 GbE NIC for the External Network; no Core Fabric NIC required
- **Note:** A single node provides no node-level redundancy. Protect workloads with snapshots and off-site sync or backup.

---

## Scaling considerations

VergeOS clusters scale horizontally. Add nodes to increase storage capacity and compute. See [Core concepts](concepts.md) for node and cluster types.

When you plan controller capacity:

- Size **Tier 0 storage and RAM** for total cluster storage and for snapshot policy.
- As VM density grows, controller and HCI nodes may need more CPU.

As the environment grows, review the hardware profile again. A design that fit the first deployment can be wrong after large capacity or workload increases.
