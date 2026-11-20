---
title: "Storage and Recovery Hardening"
description: "Harden VergeOS storage and recovery: encrypt vSAN at install, use immutable snapshots, secure Site Sync replication, and test restores safely."
semantic_keywords:
  - "VergeOS vSAN encryption at install"
  - "immutable snapshot retention ransomware"
  - "Site Sync encryption intersite authority"
  - "disaster recovery restore validation"
use_cases:
  - encrypt_vsan_at_installation
  - protect_snapshots_with_immutability
  - secure_site_sync_replication
  - validate_recovery_procedures
tags:
  - security
  - hardening
  - vsan
  - encryption
  - immutable-snapshots
  - site-sync
  - disaster-recovery
categories:
  - Security
---

# Storage and Recovery Hardening

This page covers vSAN encryption, immutable snapshots, Site Sync replication, and recovery testing. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

This baseline has no STO02 control.

## STO01: Encrypt vSAN during initial installation

vSAN encryption protects stored data if someone removes the physical drives.

**Default:** The installer's vSAN AES256 encryption prompt defaults to **No**.

{% hint style="danger" %}
You can turn on vSAN encryption only during installation. To encrypt an existing vSAN, move the data you want to keep and reinstall.
{% endhint %}

**Configure:** During the initial controller installation, select **Yes** at the encryption prompt and complete the key steps before you add protected data. See the [Installation Guide](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/installation-guide).

**Verify:** Every physical vSAN data drive on every node shows encryption enabled (key devices excluded). On a test installation, the system starts with the correct key and does not unlock without it.

## STO03: Protect recovery points with immutability

An immutable snapshot cannot be deleted while it is locked. If someone removes the immutable flag, deletion stays blocked for up to 7 more days. That delay is your time to respond.

**Default:** The hourly period of the **System Snapshots** profile keeps snapshots for 3 hours and is immutable. Other periods are not immutable until you select **Immutable**. An immutable snapshot stays locked until it expires. If someone removes the immutable flag, the snapshot stays locked for 7 days or until it expires, whichever comes first. For example, a snapshot with 30-day retention that is unlocked on day 2 can be deleted on day 9.

**Configure:** In **System > Snapshot Profiles > System Snapshots**, edit each period that must resist deletion. Select **Immutable** and set a retention long enough to detect and recover from an attack. Plan capacity for snapshots that you cannot delete.

An unlock request is accepted while a snapshot is locked. Its status changes to unlocking and an alarm fires. Deletion stays blocked during the unlock delay. Route that alarm to an owner (AUD05).

**Verify:** In **System > System Snapshots**, the required snapshots show as locked. A test snapshot cannot be deleted while it is locked. An unlock request raises an alarm.

## STO04: Encrypt replication and restrict intersite authority

**Default:** Outgoing syncs have **Encryption** and **Network Integrity** on. **Allow Insecure SSL Connection** is cleared. Machine management and cloud snapshot management between sites are disabled.

**Configure:** In **System > Sites**, keep **Allow Insecure SSL Connection** cleared and enable only the management directions you need. Keep **Encryption** on for each outgoing sync. Restrict network access between peers. **Network Integrity** is a checksum, not authentication.

**Verify:** A peer with the wrong certificate fails to connect. Replication completes with encryption. With a management direction disabled, the peer cannot manage VMs on this system.

## STO05: Define immutable snapshot schedules and consistency boundaries

**Default:** Depends on the assigned snapshot profile.

**Configure:** In **System > Snapshot Profiles**, set **Retention**, **Minimum Snapshots**, **Private**, **Immutable**, and scope for each period. Assign the profile with **System > System Snapshots > Set Snapshot Profile**. Keep snapshot-count warnings on and check capacity cost. Example policy:

| Period | Retention | Minimum |
| ------ | --------- | ------- |
| Hourly | 24 hours | 2 |
| Daily | 7 days | 2 |
| Weekly | 30 days | 2 |
| Monthly | 365 days | 1 |

Treat system snapshots as crash-consistent. A guest agent or quiesce tag does not prove a snapshot was quiesced. Use application-native backups for transactional consistency. Local snapshots do not replace off-site recovery.

**Verify:** The created snapshots have the expected lock, expiry, visibility, and scope. A restore to an isolated target passes application and data integrity checks. Record whether each snapshot actually quiesced.

## STO06: Protect Site Sync queues and the separate recovery domain

**Default:** Depends on the configured sites and syncs.

**Configure:**

1. Use trusted HTTPS endpoints. Keep machine management and repair authority disabled unless needed.
2. Create the incoming sync on the destination, then register the outgoing sync on the source. Protect the registration code.
3. Tune threads, retries, and throttle for the workload. The defaults are 8 data threads, 4 file threads, 10 retries, and no send throttle. On a shared WAN link, set a throttle, for example 50–80% of the link.
4. Link each snapshot period to **Auto Sync** with remote retention, priority, and immutability.
5. If local retention is shorter than the transfer time, select **Do not expire snapshot**.

Sync-back creates a return path. It does not fail back automatically.

**Verify:** Each site authenticates, and every intended snapshot period is linked. Remote snapshots are locked, private, and expire as planned. Investigate any persistent **Error**, **Retry**, retention skip, or **Not Ready** status. Confirm whether a queue is idle or its destination is unavailable, and watch source capacity while transfers fail. Test returning an isolated recovery point without touching production.

## STO07: Validate recovery without treating a system restore as a harmless test

A completed snapshot or sync does not prove you can recover.

**Default:** No restore schedule or recovery target exists.

{% hint style="danger" %}
Do not use a full system restore as a recovery drill. It rolls back the whole system, and it is supported only on the system that took the snapshot. You cannot restore one system over another. At the final confirmation, **Proceed** starts the restore immediately. If you do nothing, the restore starts by itself after 60 seconds. To stop it, click **Cancel** within those 60 seconds. After the restore starts, with **Auto Reboot All Nodes** selected (the default), every node resets and you cannot stop the restore.
{% endhint %}

**Configure:** Schedule restores of representative VMs, volumes, and applications, for example quarterly. If disaster recovery is in scope, plan a separately approved failover exercise, for example yearly. Document identity, network, and DNS cutover, and how you protect the recovered primary.

For routine drills, restore selected VMs or tenants from a system snapshot. A selective restore creates a copy and leaves the original in place. Test a full system restore only on a disposable system, from its own snapshot. Clear **Auto Reboot All Nodes** if you must control when the nodes restart.

**Verify:** A restored test dataset passes integrity checks within the recovery objective. Record the release, source snapshot, target, and cleanup.

## Related pages

- [VergeOS Installation Guide](../operations/sop-verge-install.md)
- [Configuring the Sites Dashboard (Adding Sites)](../system/site-dashboard-add-sites.md)
- [Tenant Snapshots](../tenants/tenant-snapshots.md)
- [Immutable Snapshots](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/immutable-snapshots)
- [Snapshot Profiles](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/snapshot-profiles)
- [Configuring a Site Sync](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/sync-configuration)
- [Sync-Back](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/sync-back)
- [System Snapshot Restores](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/system-snapshot-restores)
