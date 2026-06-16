---
description: "Configure vSAN storage tiers, provision NAS shares, and apply storage best practices for performance and redundancy in VergeOS."
---

# Module 5: Storage

## Learning Objectives

By the end of this module, you will be able to:

- **Configure vSAN storage tiers** for different workload profiles (performance, capacity, archive)
- **Provision and manage NAS shares** for file-level storage access across workloads
- **Apply storage best practices** for performance tuning and redundancy configuration
- **Monitor storage health** and respond to capacity or performance alerts

## Prerequisites

- Completion of [Module 1: Architecture Fundamentals](../01-architecture/README.md) -- understanding of VergeFS and vSAN concepts
- Completion of [Module 3: Installation](../03-installation/README.md) -- a running VergeOS cluster with disks available

## Estimated Time

**3 hours** (1.5 hours reading + 1.5 hours lab)

## Topics

* [**vSAN Architecture**](01-vsan-architecture.md) — How VergeOS vSAN organizes physical disks into tiered storage pools, redundancy models, and the role of VergeFS.
* [**Storage Tiers**](02-storage-tiers.md) — Configuring Tier 1 (high-performance NVMe), Tier 2 (mixed-workload SSD), Tier 3 (read-optimized SSD), Tier 4 (capacity HDD), and Tier 5 (archive HDD) for different workload profiles.
* [**NAS Service & Shares**](03-nas-shares.md) — Provisioning CIFS/SMB and NFS shares, remote volumes, VM export volumes, and Active Directory integration.
* [**Snapshots & Data Protection**](04-snapshots-data-protection.md) — Snapshot architecture, quiesced snapshots, clones, snapshot profiles, site sync replication, and disaster recovery.
* [**Storage Monitoring & Troubleshooting**](05-storage-monitoring.md) — vSAN diagnostics, vcmd commands, health monitoring, NAS troubleshooting, and Fibre Channel integration.
* [**Lab: Storage Configuration**](lab.md) — Configure vSAN tiers, provision NAS shares, and validate storage performance and redundancy.
