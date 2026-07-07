---
title: System Snapshots
semantic_keywords:
  - system snapshots full partial VergeOS
  - automated system snapshot schedule profile
  - manual system snapshot before maintenance
  - partial system snapshot custom tagging include exclude
use_cases:
  - configure_automated_system_snapshots
  - take_manual_system_snapshot
  - setup_partial_system_snapshots
  - manage_system_snapshot_retention
categories:
  - Backup and DR
description: >-
  How to manage system snapshots in VergeOS including full and partial snapshots
  with custom tagging, automated scheduling via profiles, manual snapshot
  creation, and storage best practices.
tags:
  - snapshots
  - system-snapshots
  - scheduling
  - automation
  - data-protection
  - storage
  - tagging
---

# System Snapshots

{% hint style="info" %}
**New in 26.1 - Partial System Snapshots Based on Custom Tagging**

Partial system snapshots allow you to selectively include only the VMs, tenants, VMware services, or volumes you choose, giving you far more flexibility in designing replication and retention strategies.

Full system snapshots remain the foundation of protection and are still required for full‑system recovery. However, you can now include partial system snapshots within your schedule to give specific VMs or tenants their own replication and retention cadence.

Adding partial snapshots alongside your regular full system snapshots enables you to:

* Replicate high‑priority VMs or tenants more frequently
* Retain targeted workloads for longer without expanding system‑wide retention
* Sync different subsets of workloads to different locations

This approach preserves the reliability of full system snapshots while giving you finer‑grained control over how individual workloads are protected.
{% endhint %}

## Full vs. Partial

Both Full and Partial system snapshots can be used in VergeOS Site syncs to replicate data to a remote system

### Full System Snapshots:

* Contain a backup of everything in a system, including all tenants, VMs, NAS volumes, networks, and settings
* supports full-system restore
* supports selective object restores, including:
  * Tenants
  * NAS volumes
  * VMs
* VergeOS Site Sync support
* Select: Snapshot Type=_Full_

{% hint style="success" %}
**Default settings on a new system are configured to perform&#x20;**_**Full**_**&#x20;system snapshots at multiple intervals with different retentions.**
{% endhint %}

### Partial System Snapshots:

* Include or exclude VMs, tenants, VMware services, and volumes based on custom tagging
* Allow more frequent backup and sync replication of select workloads
* Support longer retention for specific workloads _without increasing system‑wide retention_
* VergeOS Site Sync support
* Select: \*_Snapshot Type=Partial - Exclude Tags_ or _**Partial - Include Tags**_

***

### Full vs. Partial System Snapshots — Quick Reference

| Feature / Behavior                  | **Full System Snapshots**                                          | **Partial System Snapshots**                                                           |
| ----------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| **What they capture**               | Entire system: tenants, VMs, NAS volumes, networks, settings       | Only selected VMs, tenants, VMware services, and volumes based on include/exclude tags |
| **Primary purpose**                 | Full‑system recovery and broad protection                          | Targeted protection for specific workloads                                             |
| **Supports selective restores**     | Yes — tenants, NAS volumes, VMs                                    | Yes — only for objects included in the partial snapshot                                |
| **Use cases**                       | System‑wide rollback, disaster recovery                            | Higher‑frequency protection or longer retention for specific workloads                 |
| **Retention impact**                | Affects system‑wide retention                                      | Allows extended retention without increasing system‑wide retention                     |
| **Replication behavior**            | Can be used in Site Syncs                                          | Can also be used in Site Syncs                                                         |
| **Snapshot Type selection**         | `Full`                                                             | `Partial - Exclude Tags` or `Partial - Include Tags`                                   |
| **Default behavior on new systems** | Preconfigured with multiple Full snapshot intervals and retentions | Not enabled by default; added as needed                                                |

***

## Automated System Snapshots

By default, system snapshots run according to the included _**System Snapshots**_ profile. It is recommended to keep this profile assigned. The periods within this default profile can be tailored to meet your schedule and retention needs.

{% hint style="success" %}
**To change which profile is assigned for system snapshots, navigate to System > System Snapshots and click Set Snapshot Profile on the left menu.**
{% endhint %}

{% hint style="success" %}
**Default Schedule**

The default _**"System Snapshots"**_ profile includes the following schedule of Full snapshots

* hourly snapshots retained for 3 hours
* a daily snapshot at midnight retained for 3 days
* a daily snapshot at noon retained for 1 day.

This provides a solid starting point for most environments, balancing system protection with storage usage.
{% endhint %}

### Modifying Your System Snapshot Schedule

To modify the system snapshot schedule:

1. Navigate to **System** > **System Snapshots**.
2. Click **View Snapshot Profile** on the left menu.\
   This opens the profile currently assigned for automatic system snapshots (default: "_**System Snapshots**_").
3. Scroll to the **Periods** section.\
   Each period listed defines a frequency and retention. You can add, modify, and remove periods to customize the schedule.

For detailed instructions on configuring periods, see [Snapshot Profiles - Profile Periods](snapshot-profiles.md#profile-periods).

## Manual System Snapshots

A manual system snapshot can be taken at any time. Creating a short‑term manual snapshot before major configuration changes or maintenance provides a rollback point if needed.

### Take a Manual System Snapshot

1. Navigate to **System** > **System Snapshots**.
2. Select **New** from the left menu.
3.  Configure snapshot options:

    * **Name** (required): Provide a descriptive name (e.g. 'before drive maintenance')
    * **Description** (optional):
    * **Expiration Type**: Select _Set Date_ to specify an expiration date/time, or _Never Expire_ to retain the snapshot indefinitely.
    * **Expires** (when _Set Date_ is selected): Select/enter a date and time for expiration.

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p><strong>Consider vSAN usage when setting expirations. Initially, source and snapshot are identical, but as they diverge, deduplication decreases between the two and storage usage increases. Avoid </strong><em><strong>Never Expire</strong></em><strong> unless necessary.</strong></p></div>

    * **Snapshot Type**:
      * _**Full**_: capture of entire system; required for system-wide recovery
      * _**Partial - Exclude Tags**_: captures all VMs, tenants, VMware services, and volumes _except_ those with specified tags
      * _**Partial - Include Tags**_: captures only VMs, tenants, VMware services, and volumes with the specified tags
        * **Exclude/Include Tags** (Partial snapshots only): Click the ellipse button \[] to select one or more tags.
        * **Quiesce Tags**: (optional; Partial snapshots only); Click the ellipse button \[] to select one or more tags. VMs with the specified tags will temporarily freeze disk activity during capture to provide an application-consistent snapshot. Requires [VM Guest Agent](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/virtual-machines/vm-guest-agent) support.
    * **Private** (default:enabled): This option can be deselected to allow tenants access to their own data within this snapshot.
    * **Immutable** (default:disabled): Prevents deletion until unlocked, with a mandatory waiting period.

{% hint style="warning" %}
**Immutable snapshots cannot be deleted (even by administrators) until unlocked, and the waiting period has elapsed. Ensure retention settings align with available storage. For more guidance, refer to the** [**Immutable Snapshots Guide**](immutable-snapshots.md)**.**
{% endhint %}

4. Click **Submit** to take the snapshot.

## Best Practices

### Storage Considerations

* Retaining an excessive number of snapshots can significantly increase storage consumption and operational overhead. A well‑designed retention policy preserves essential restore points while automatically pruning older, less relevant snapshots, helping you meet recovery objectives without accumulating unnecessary historical data.
* Monitor storage utilization regularly to ensure that snapshot growth remains aligned with your retention strategy.
* Reevaluate retention settings after major environment changes, such as adding new VMs, expanding tenants, or increasing workload churn, to confirm that storage usage remains predictable and sustainable.
* Avoid creating overly granular snapshot periods unless they are required for specific workloads. High‑frequency snapshots can increase metadata and storage overhead without providing meaningful recovery benefits for all systems.

### System Protection

{% hint style="warning" %}
**Ensure your System Snapshots profile includes scheduled periods that&#x20;**_**take full snapshots**_**. Full system snapshots provide the system‑wide recovery point needed to restore from unpredictable hardware failures or configuration errors.**
{% endhint %}

* Add partial snapshot periods when specific VMs or tenants require more frequent protection or longer retention.

## Related Documentation

* [Snapshots Overview](snapshots-overview.md)
* [Snapshot Profiles](snapshot-profiles.md)
* [Restores from System Snapshot](system-snapshot-restores.md)
* [Tenant Snapshots](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/tenants/tenant-snapshots)
* [Tenant Restores](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/tenants/tenant-restores)
* [VM Snapshots and Restores](vm-snapshots-restores.md)
* [NAS Volume Snapshots and Restores](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/nas/volume-snapshots-restores)
* [Site Syncs](syncs-overview.md)
