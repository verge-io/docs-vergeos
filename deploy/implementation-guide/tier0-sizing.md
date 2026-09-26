## Tier 0 (Metadata) Sizing Guidance
Metadata stores the structural information VergeOS uses to track usable data. In VergeOS, metadata is stored on Tier 0, and correctly sizing this tier is essential for stable vSAN operation across all deployment profiles.
Metadata capacity needs vary based on workload behavior, snapshot strategy, and vSAN scale. The following guidance provides a clear baseline and identifies the conditions where additional Tier 0 capacity may be required.
### Where Metadata Is Stored
In the majority of VergeOS deployments, metadata is stored on a dedicated Tier 0 device. In Small/Edge systems, metadata may reside on the primary tier; in these cases, the same sizing guidance applies and required metadata capacity must be reserved within the primary tier.
### Baseline Tier 0 Requirements
• Minimum endurance: 1 DWPD
• Baseline capacity: 5 GB tier 0 per 1 TB usable storage (tier 1-5) at 3DWPD or equivalent capacity/endurance profile, e.g. 15GB/1TB at 1DWPD)
This baseline assumes a default snapshot schedule (*System Snapshots* profile) or similiar, with ≅ 7 or fewer regularly retained snapshots.
### When to Increase Tier 0 Capacity
**1. Snapshot Retention Above Approximately Seven Snapshots**
Snapshot behavior is a primary driver of metadata growth.  Each retained snapshot can potentially add up to approximately 0.5 GB per 1 TB usable storage (upper bound), with the actual usage dependent on snapshot delta: write-intensive workloads such as heavy SQL or random-write patterns will tend to approach that upper bound, while sequential or low-change workloads will consume lower amounts of metadata per snapshot. 
Increase Tier 0 capacity above baseline if you plan to retain more than seven snapshots

**2. Planned vSAN Capacity Expansion**
Tier 0 must be sized for total vSAN usable capacity. If you expect near-term scaling (adding storage nodes or expanding tiers 1–5), consider upsizing Tier 0 in advance to avoid replacing metadata devices later.
### Planning Assistance
Metadata sizing can involve multiple interdependent factors. VergeOS Sales and Authorized Reseller Partners can assist with workload evaluation and Tier 0 planning for new deployments or expansions.
