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

## Choosing the Right Sync Scope for DR Granularity

The sync source you choose — whole-system or tenant-level — determines how you recover workloads at the DR site. Decide the scope before you configure replication.

| Sync source | What replicates | What you can recover at the DR site |
|---|---|---|
| **Whole-system site sync** | The entire system, including tenants, as one object | The full system; individual system-level VMs from a received system snapshot; tenants only as whole objects |
| **Tenant-to-tenant sync** | The tenant as one object | Individual VMs within that tenant |

**Whole-system site sync** replicates your entire production system to the DR site. This is ideal for full-system failover — spinning up your entire environment at the DR site after a catastrophic failure. Individual VMs that run at the system level can be recovered from a received system snapshot; see [Recovering a Single VM from a Remote System Snapshot](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/backup-dr/recovering-a-single-vm-from-a-remote-cloud-snapshot). Tenants inside the snapshot replicate as single objects — recovering an individual VM from inside a tenant requires recovering the tenant first.

**Tenant-to-tenant sync** (syncing a production tenant into a DR tenant) preserves per-VM recovery granularity for that tenant. At the DR site you can browse the tenant's snapshots, recover a specific VM, and leave everything else untouched.

**If your DR plan includes per-VM recovery for tenant workloads** — for example, failing over a single database VM without affecting the rest of the tenant — configure a tenant-to-tenant sync for that tenant.

{% hint style="success" %}
**You can run both.** A whole-system sync for full-system failover and a tenant-to-tenant sync for per-VM granularity can coexist. Replicating the same tenant both ways doubles sync overhead with no additional benefit — use a tenant-to-tenant sync for that tenant and rely on the whole-system sync for everything else.
{% endhint %}

## Related Links

* [**Sites Dashboard**](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/sites-overview)
* [**Configuring a Site Sync**](sync-configuration.md)
* [**Monitoring Site Syncs**](monitoring-site-syncs.md)
* [**Manual Site Syncs**](manual-site-syncs.md)
* [**Retrieving a Sync Back** (for local data recovery)](sync-back.md)
* [**Repair Server (ioGuardian)**](repair-server.md)
