---
title: Site Syncs
semantic_keywords:
  - VergeOS site syncs overview offsite backup replication
  - block-level sync deduplication compression encryption
  - disaster recovery migration offsite archival
  - site sync repair server ioGuardian features
use_cases:
  - evaluate_site_sync_capabilities
  - plan_offsite_backup_strategy
  - understand_sync_features
  - plan_system_migration
categories:
  - Backup and DR
description: >-
  Overview of VergeOS site sync capabilities for offsite backup, disaster
  recovery, and system migration through block-level snapshot replication with
  encryption and compression.
tags:
  - site-syncs
  - replication
  - backup
  - disaster-recovery
  - migration
  - encryption
---

# Site Syncs

Site Syncs replicate system snapshots to another VergeOS system, simplifying and streamlining:

* **Offsite Backup and Archival** - recover data in a granular level at the remote site or on the source system after syncing back
* **Emergency Preparedness** - ensure your entire system can be ready for quick and complete recovery at a remote site to minimize downtime and ensure operational continuity
* **Migrations** - easily move and spin up a complete system, individual tenants, or select workloads at a new location

## Key Features

* **Complete-system, Off-site Backup** - replicates system snapshots that include your networking, VMs, tenants, NAS, and system configuration
* **Minimized Bandwidth Usage/Shorter Transfer Times** - block-level synchronization (only transferring changed data), in-flight deduplication and compression
* **In-flight Encryption** - automatic AES 256-bit encryption
* **Flexible Operations** - scheduling, queuing, and manual sync options
* **Repair Server (ioGuardian)** - sync sites can be used for automatic inline healing (e.g. after multiple concurrent drive failures or power issues)

## Recovery Granularity

Site syncs replicate system snapshots to the remote site — either full-system snapshots that capture everything, or partial snapshots limited to tagged objects such as specific tenants, VMs, or NAS services. Full-system snapshots support complete environment failover, enabling you to bring your entire environment online at the DR site after a catastrophic failure. In either case full or partial), any VMs and tenants captured at the top system level can be selectively restored directly from the replicated snapshots.

Tenants within a system snapshot are recoverable as single objects. Individual objects inside a tenant — such as VMs, sub-tenants, and NAS volumes — cannot be selectively restored from the system-level snapshot. Recovering a specific item within a tenant requires first restoring the tenant as a whole to the DR site, then logging into that restored tenant with valid tenant credentials to access and restore individual objects.

If direct, granular recovery of individual tenant objects at the remote site is required — for example, failing over a single VM without restoring the entire tenant first — site syncs can be configured from within the tenant itself. A site sync originated at the tenant level replicates that tenant to a pre-configured tenant on the remote site. Users with tenant credentials can then browse the replicated tenant's snapshots and restore specific VMs, sub-tenants, or NAS volumes directly, without any prior host-level restore step.

{% hint style="success" %}
**You can run both.** A top-system level sync for full-system failover and a tenant-to-tenant sync for per-VM recovery granularity can coexist. Replicating the same tenant at both levels increases sync overhead.
{% endhint %}

## Related Links

* [**Sites Dashboard**](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/sites-overview)
* [**Configuring a Site Sync**](sync-configuration.md)
* [**Monitoring Site Syncs**](monitoring-site-syncs.md)
* [**Manual Site Syncs**](manual-site-syncs.md)
* [**Retrieving a Sync Back** (for local data recovery)](sync-back.md)
* [**Repair Server (ioGuardian)**](repair-server.md)
