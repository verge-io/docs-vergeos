---

# Local Node Tier 0 Metadata Redundancy

## Overview

{% hint style="info" %}
**Key Points**

- **Automatic** — Tier 0 local mirroring is automatically applied whenever a node contains more than one Tier 0 drive.
- **Additive** — Local disk redundancy (D+x) operates *in addition to* node‑to‑node redundancy (N+x).
- **Drive‑limited** — Local redundancy is capped by the number of Tier 0 drives physically present in the node.
- **Highest priority** — Tier 0 stores metadata, making its protection the most critical part of the storage stack.
{% endhint %}

Tier 0 is the most critical storage tier in a VergeOS cluster — it holds metadata, and **without metadata, data on all tiers becomes inaccessible**. To protect this metadata, VergeOS applies an additional layer of *local* redundancy whenever a node has multiple Tier 0 drives: a disk‑level mirror (D+1 or D+2) inside the node.

This local protection is **independent of and additive to** the cluster’s node‑to‑node redundancy (N+1 or N+2).  
However, **local redundancy cannot exceed the number of Tier 0 drives available**.  
For example, an N+2 system requires three local copies (D+2), but a node with only two Tier 0 drives can only provide two local copies.

---

## How It Works

### Node‑to‑node redundancy (N+1 / N+2)

All storage tiers, including Tier 0, benefit from VergeOS’s node‑to‑node redundancy:

- **N+1** — two cross‑node copies  
- **N+2** — three cross‑node copies  

If a node fails, metadata and data remain available from surviving nodes.

---

### Local Tier 0 redundancy (D+1 / D+2), capped by drive count

When a node contains more than one Tier 0 drive, VergeOS automatically applies local redundancy:

- **D+1** — two local copies  
- **D+2** — three local copies  

But **local redundancy is limited by the number of drives**:

| System Redundancy | Desired Local Copies | Required Drives | Actual Local Copies (if drives < required) |
|-------------------|----------------------|-----------------|--------------------------------------------|
| N+1               | 2 (D+1)              | ≥2              | min(drives, 2)                             |
| N+2               | 3 (D+2)              | ≥3              | min(drives, 3)                             |

Examples:

- N+2 system with **2 Tier 0 drives** → only **2 local copies** (D+1 behavior)  
- N+2 system with **3+ Tier 0 drives** → full **3 local copies** (D+2)  
- N+1 system with **2+ drives** → full **2 local copies** (D+1)

If a Tier 0 drive fails, the remaining drive(s) continue serving metadata without interruption.

> **Why only Tier 0?**  
> Tier 0 stores metadata — the index that maps every block of every volume to its physical location. Losing metadata means losing access to all data, even if the underlying blocks are intact.

---

## Drive Count, Usable Capacity, and Redundancy

Local redundancy depends on both **drive count** and **system redundancy level**, but is **capped by available drives**.

### N+1 System (D+1 Target)

| Tier 0 Drives | Raw Capacity | Local Copies | Usable Capacity | Local Redundancy |
|:-------------:|-------------:|-------------:|----------------:|:----------------:|
| 1             | 1 TB         | 1            | 1 TB (100%)     | None             |
| 2             | 2 TB         | 2            | 1 TB (50%)      | ✓ D+1            |
| 3             | 3 TB         | 2            | 1.5 TB (50%)    | ✓ D+1            |
| 4             | 4 TB         | 2            | 2 TB (50%)      | ✓ D+1            |

### N+2 System (D+2 Target)

| Tier 0 Drives | Raw Capacity | Local Copies | Usable Capacity | Local Redundancy |
|:-------------:|-------------:|-------------:|----------------:|:----------------:|
| 1             | 1 TB         | 1            | 1 TB (100%)     | None             |
| 2             | 2 TB         | 2            | 1 TB (50%)      | ✓ Partial (D+1) |
| 3             | 3 TB         | 3            | 1 TB (33%)      | ✓ Full (D+2)    |
| 4             | 4 TB         | 3            | 1.33 TB (33%)   | ✓ Full (D+2)    |

**Key behavior:**

- N+2 requires **three drives** for full local redundancy.  
- With fewer than three drives, the node provides **the maximum possible local copies**, even if that is fewer than the system redundancy level.  
- Usable capacity = raw ÷ local copies.

> **Single‑drive nodes:**  
> A node with only one Tier 0 drive still benefits from N+1 or N+2 redundancy across nodes, but has **no local protection**.

---
