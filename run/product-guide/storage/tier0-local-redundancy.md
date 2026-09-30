---
title: "Local Node Tier 0 Metadata Redundancy (D+x)"
description: "How VergeOS mirrors Tier 0 metadata across a controller node's local drives (D+x) to match the system redundancy level, and how the drive count sets usable metadata capacity."
semantic_keywords:
  - "Metadata local resiliency"
  - "Metadata protection"
  - "Understanding Tier 0 scaling"
  - "Tier 0 usable vs raw"
use_cases:
  - capacity_planning
  - tier_0_scaling_planning
tags:
  - storage
  - capacity-planning
  - metadata
  - tier0
categories:
  - Storage
---

# Local Node Tier 0 Metadata Redundancy (D+x)

## Overview

{% hint style="info" %}
**Key Points**

* **The rule** — Each controller node keeps as many local copies of Tier 0 metadata as the system redundancy level requires (two for N+1, three for N+2), up to the number of Tier 0 drives in that node.
* **Automatic** — VergeOS mirrors metadata locally whenever a controller node has more than one Tier 0 drive. There is nothing to configure.
* **Sizing impact** — Usable Tier 0 capacity is the total raw Tier 0 capacity divided by the number of local copies. Two 1.6 TB drives on an N+1 system yield ~1.6 TB usable.
{% endhint %}

Tier 0 is the most critical storage tier in a VergeOS system. It holds metadata, and **without metadata, data on all tiers becomes inaccessible**. Tier 0 lives only on controller nodes.

[Node-to-node redundancy](vsan-redundancy-levels.md) (N+1 or N+2) keeps metadata copies across controller nodes. Inside each controller node, VergeOS also mirrors metadata across the node's local Tier 0 drives. This local mirroring (D+x) matches the system redundancy level: an N+1 system keeps two local copies (D+1), and an N+2 system keeps three (D+2) — but never more copies than the node has Tier 0 drives.

{% hint style="info" %}
**Why only Tier 0?**

Tier 0 stores metadata — the index that maps every block of every volume to its physical location. Losing metadata means losing access to all data, even if the underlying blocks are intact. For metadata, VergeOS matches the cluster's resilience locally on each controller node.
{% endhint %}

## Local Copies and Usable Capacity by Drive Count

Local copies divide raw capacity:

**Usable Tier 0 capacity ≈ total raw Tier 0 capacity ÷ number of local copies**

The table below uses 1 TB drives for simplicity:

| System redundancy | Tier 0 drives | Raw capacity | Local copies | Usable capacity | Local protection |
| ----------------- | ------------- | ------------ | ------------ | --------------- | ---------------- |
| N+1               | 1             | 1 TB         | 1            | 1 TB            | None             |
| N+1               | 2             | 2 TB         | 2            | 1 TB            | Full (D+1)       |
| N+1               | 3             | 3 TB         | 2            | 1.5 TB          | Full (D+1)       |
| N+1               | 4             | 4 TB         | 2            | 2 TB            | Full (D+1)       |
| N+2               | 1             | 1 TB         | 1            | 1 TB            | None             |
| N+2               | 2             | 2 TB         | 2            | 1 TB            | Partial (D+1)    |
| N+2               | 3             | 3 TB         | 3            | 1 TB            | Full (D+2)       |
| N+2               | 4             | 4 TB         | 3            | 1.33 TB         | Full (D+2)       |

For example, an N+2 system targets three local copies (D+2), but a controller node with only two Tier 0 drives can only provide two. Drives beyond the required copy count add usable capacity, not more copies. As a real-world example, a controller node with two 1.6 TB drives on an N+1 system provides ~1.6 TB of usable metadata capacity.

{% hint style="warning" %}
**Single-drive controller nodes**

A controller node with only one Tier 0 drive has no local metadata protection. N+1 or N+2 redundancy still protects the metadata across nodes, but any Tier 0 drive failure on that node leaves it dependent on the other controller nodes' copies. Install at least two Tier 0 drives per controller node.
{% endhint %}

## Sizing Recommendations

* Install the same number of Tier 0 drives, of the same size, in each controller node.
* For N+1 systems, install two Tier 0 drives per controller node for full local protection (D+1).
* For N+2 systems, install three Tier 0 drives per controller node for full local protection (D+2).
* For per-terabyte metadata sizing guidance, see the [Node Sizing Guide](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/sizing).

## When a Tier 0 Drive Fails

If a Tier 0 drive fails, the remaining drives continue to serve metadata without interruption. The tier then runs with reduced local protection until you replace the drive. While the drive is down, the **Redundant** checkbox on the tier's status card is cleared — see [Viewing Tier Redundancy Status](vsan-redundancy-levels.md#viewing-tier-redundancy-status). Replace the failed drive as soon as possible.

## Next Steps

* [Understanding vSAN Redundancy Levels](vsan-redundancy-levels.md) — N+1 and N+2 node-to-node redundancy.
* [Storage Tiers in VergeOS vSAN](storage-tiers.md) — the full tier model, including Tier 0 hardware guidance.
* [Replacing a Defective or End-of-life Drive](../operations/drive-replacement.md) — the drive replacement procedure.
* [Node Sizing Guide](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/sizing) — Tier 0 capacity and drive recommendations.
