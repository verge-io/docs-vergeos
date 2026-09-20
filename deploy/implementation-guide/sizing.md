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
  - "maximum supported hardware specifications VergeOS"
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
3. Size Tier 0 from usable Tier 1–5 capacity and from your snapshot schedule and retention.
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

VergeOS Sales, Support, and authorized resellers can help with workload review and hardware selection. See [Support and services](https://app.gitbook.com/s/uJc5d3O7cwI7qD8muSyG/support-and-services).

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

- Use enterprise media with a **minimum of 1 DWPD** (or an equivalent endurance profile). Do not use read-intensive or consumer NVMe for production Tier 0 or production workload tiers.
- Prefer enough capacity at 1 DWPD over a chase for 3 DWPD when 1 DWPD enterprise media meets the need.
- Do not use HDDs larger than **8 TB** outside archive-specific environments. Large HDDs extend rebuild time and can affect performance and availability.

### Tier 0 capacity and snapshots

Tier 0 holds vSAN metadata. See [Storage Tiers in VergeOS vSAN](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/storage-tiers).

Snapshot schedule and retention are the main drivers of Tier 0 capacity growth. Size Tier 0 for your snapshot policy, not only for raw capacity. For schedule and retention settings, see [Snapshot Profiles](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/snapshot-profiles).

**Standard baseline:** plan about **5 GB of Tier 0 usable capacity per 1 TB of usable Tier 1–5 capacity**, on high-endurance enterprise media (for example 5 GB/TB at 3 DWPD, or an equivalent profile such as 15 GB/TB at 1 DWPD). Minimum acceptable endurance: **1 DWPD**.

{% hint style="info" %}
**Field validation in progress**

VergeOS continues to validate Tier 0 capacity ratios with field data after the v26 metadata spillover fix. Until that review finishes, use the 5 GB per 1 TB usable baseline for Standard Production. For Performance and large-scale systems, contact a VergeOS partner or the VergeOS sales team.
{% endhint %}

To add Tier 0 after installation, see [Adding Tier 0 to an Existing System](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/storage-vsan/adding-tier-zero).

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

#### Controller role (nodes 1 and 2; plus node 3 in an N+2 design)

On HCI systems, these nodes also run storage and compute. Dedicated controllers are optional. For N+1 and N+2 requirements, see [Understanding vSAN Redundancy Levels](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-redundancy-levels).

- **Processor:** 2.7 GHz+ CPU (base clock)
- **RAM:** 1 GB RAM per 1 TB raw storage per node (plus guest workload RAM)
- **Tier 0:**
  - 1 or 2 enterprise-grade NVMe (or equivalent high-endurance) SSDs at 3 DWPD or equivalent
  - Multiple Tier 0 devices provide local mirror redundancy
  - Capacity: about 5 GB usable Tier 0 per 1 TB usable Tier 1–5 storage (see [Tier 0 capacity and snapshots](#tier-0-capacity-and-snapshots))

#### Storage participants (vSAN)

At least two nodes with matching disk layouts (except [single-node systems](#single-node-systems)).

- **Processor:** 2.7 GHz+ CPU (base clock). Base clock also affects storage performance on nodes that run compute.
- **RAM:** 1 GB RAM per 1 TB raw storage
- **CPU:** about 1 core per storage disk
- **Storage:**
  - At least one enterprise NVMe or SATA/SAS SSD per node (primary tier)
  - Enterprise HDDs are acceptable for low performance, snapshots, archive, or file services
  - HDDs larger than 8 TB are not recommended outside archive-specific environments

#### Compute-only nodes (optional)

Follow the generic requirements. Size CPU and RAM for the workloads that run on these nodes. CPU base clock affects storage performance when the node also participates in storage.

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
- On **1–2 node** systems where the primary tier is already all-NVMe or all-SSD, a **dedicated** Tier 0 device is often unnecessary. Confirm the layout with Sales, Support, or an authorized reseller when unsure.
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
- **Network:** see [generic node requirements](#generic-node-requirements)
- **Storage:**
  - Lower-performance, lower-endurance enterprise devices are acceptable
  - HDDs larger than 8 TB may be used for archive-specific layouts; expect extended rebuild times
- **Note:** Not appropriate for performance-sensitive workloads

---

### Single-node systems

Official support is planned for **October 2026**. VergeOS will publish full requirements with that release.

---

## Scaling considerations

VergeOS clusters scale horizontally. Add nodes to increase storage capacity and compute. See [Core concepts](concepts.md) for node and cluster types.

When you plan controller capacity:

- Size **Tier 0 storage and RAM** for total cluster storage and for snapshot policy.
- As VM density grows, controller and HCI nodes may need more CPU.

As the environment grows, review the hardware profile again. A design that fit the first deployment can be wrong after large capacity or workload increases.

## Maximum supported hardware specifications

The following table outlines the maximum supported hardware specifications for various resources in the VergeOS system as of version 4.12:

| Resource                        | Maximum | Resource Type |
|---------------------------------|---------|---------------|
| Nodes per system                | 200     | node          |
| Individual physical disk size   | 64      | terabyte      |
| RAM per node [^2]               | 5       | terabyte      |
| vDisk size                      | 256     | terabyte      |
| Disks per VM [^3]               | 2000    | vdisk         |
| Clusters per system             | 100     | cluster       |
| Tiers of storage per system     | 5       | tiers         |
| vSAN Fault domains per system   | 2       | vSAN          |

[^1]: Graphics cards are supported for VM usage and may not function for console access.
[^2]: vSAN nodes require a minimum 1GB of RAM per 1TB of Storage
[^3]: Virtio-SCSI Interface required
