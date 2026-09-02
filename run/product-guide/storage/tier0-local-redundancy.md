# Local Node Tier 0 Redundancy


## Overview

{% hint style="info" %}
**Key Points**

- **Automatic** — local tier 0 mirroring is automatically applied whenever more than one tier 0 drive is present in a node - it requires no configuration.
- **Additive** — D+1 does not replace N+1; both operate simultaneously.
- **Capacity cost is fixed** — regardless of how many tier 0 drives are in the node, usable capacity is always 50% of raw once D+1 is active (i.e. more than one local tier 0 drive).
- **Designed for the most critical data** — tier 0 holds metadata, making its protection the highest priority in the storage stack.
{% endhint %}

Tier 0 is the most critical storage tier in a VergeOS cluster — it holds metadata, and **without metadata, your data is inaccessible**. For this reason, VergeOS applies an additional layer of local redundancy to tier 0 whenever a node has more than one tier 0 drive: a disk-level mirror (D+1) within the node itself.

This local mirroring works *on top of* the node-to-node redundancy (N+1) that already protects data across the cluster, giving tier 0 a double layer of protection that no other tier receives by default.

## How It Works

### Node-to-node redundancy (N+1)

All storage tiers benefit from VergeOS's built-in node-to-node redundancy. Each piece of data is written to at least two nodes in the cluster, so the failure of any single node does not result in data loss or downtime.

### Local disk mirroring (D+1)

When a node contains more than one tier 0 drive, VergeOS automatically mirrors those drives within the node. This is a 1:1 mirror — every write to one drive is simultaneously written to the other. If a drive fails, the surviving drive continues serving reads and writes without interruption, and the node remains fully operational.

The result is **two independent failure domains for tier 0**: a drive can fail *and* a node can fail simultaneously, and the cluster continues without data loss.

> **Why only tier 0?**  
> Tier 0 stores metadata — the index that maps every block of every volume to its physical location on disk. Losing metadata means losing access to all data those volumes contain, even if the data blocks themselves are intact. Local mirroring of tier 0 reflects how critical that metadata is, and is applied automatically by design whenever the hardware allows it.

## Drive Count, Usable Capacity, and Redundancy

The table below shows how local redundancy scales with the number of tier 0 drives in a single node. Usable capacity figures assume 1 TB raw drives.

| Tier 0 Drives | Raw Capacity | Usable Capacity | Local Redundancy |
|:---:|---:|---:|:---:|
| 1 | 1 TB | 1 TB (100%) | None |
| 2 | 2 TB | 1 TB (50%) | ✓ Redundant (D+1) |
| 3 | 3 TB | 1.5 TB (50%) | ✓ Redundant (D+1) |
| 4 | 4 TB | 2 TB (50%) | ✓ Redundant (D+1) |

With two or more tier 0 drives, usable capacity is always 50% of raw — the cost of the mirror — but the tradeoff is a drive failure that would otherwise take the node offline becomes a non-event.

> **Single-drive nodes:** A node with only one tier 0 drive still benefits from N+1 redundancy across nodes, but there is no local disk mirror. This is an acceptable configuration, though adding a second tier 0 drive is recommended wherever the hardware supports it.

## Double Redundancy: N+1 and D+1 Together

The diagram below illustrates how the two redundancy layers work together across a typical three-node cluster. Each node has two tier 0 drives (mirrored locally), and each write is replicated to at least one other node.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        VergeOS Cluster                              │
│                                                                     │
│  ┌──────────────────┐   ┌──────────────────┐   ┌────────────────┐  │
│  │      Node A      │   │      Node B      │   │     Node C     │  │
│  │                  │   │                  │   │                │  │
│  │  Tier 0 (D+1)   │   │  Tier 0 (D+1)   │   │  Tier 0 (D+1) │  │
│  │  ┌────┐ ┌────┐  │   │  ┌────┐ ┌────┐  │   │  ┌────┐┌────┐ │  │
│  │  │Drv1│↔│Drv2│  │   │  │Drv1│↔│Drv2│  │   │  │Drv1││Drv2│ │  │
│  │  └────┘ └────┘  │   │  └────┘ └────┘  │   │  └────┘└────┘ │  │
│  │   Local mirror  │   │   Local mirror  │   │  Local mirror  │  │
│  │   (D+1)         │   │   (D+1)         │   │  (D+1)         │  │
│  └────────┬─────────┘   └────────┬────────┘   └───────┬────────┘  │
│           │                      │                     │           │
│           └──────────────────────┴─────────────────────┘           │
│                     Node-to-node replication (N+1)                 │
└─────────────────────────────────────────────────────────────────────┘

Failure scenario examples:

  Drive fails on Node A  →  Node A's mirror absorbs it.  No impact.
  Node A fails entirely  →  N+1 replication covers it.   No impact.
  Drive fails on Node A
    + Node B fails        →  Both layers absorb each.    No impact.
```

