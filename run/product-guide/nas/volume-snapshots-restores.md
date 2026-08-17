---
title: NAS Volume Snapshots and Restores
semantic_keywords:
  - NAS volume snapshot and restore procedures
  - quiesced snapshot freeze filesystem for consistent backup
  - schedule automated volume snapshots with profiles
  - restore volume from snapshot to new or overwrite existing
use_cases:
  - take_manual_volume_snapshots
  - schedule_automated_snapshots
  - restore_volume_from_snapshot
  - import_snapshots_from_system_snapshots
  - create_quiesced_snapshots
categories:
  - NAS
description: >-
  How to create, schedule, and restore NAS volume snapshots in VergeOS,
  including quiesced snapshots, snapshot profiles, and restore-to-new or
  restore-over-source options.
tags:
  - nas
  - snapshot
  - restore
  - backup
  - quiesce
  - volume
  - snapshot profile
  - data protection
---

# NAS Volume Snapshots and Restores

Volume-level snapshots allow for customizing snapshot schedule and retention rules per individual NAS volume and provide the option for a quiesced snapshot.  Non-quiesced NAS volumes can be imported from full system snapshots and used for restore.

## Quiesced Snapshots

Quiesced volume snapshots freeze file system I/O during the snapshot process. The quiesce option can be selected when taking a manual volume snapshot and can be enabled within the snapshot profile used for automated snapshots.

## Schedule Volume Snapshots

[Snapshot Profiles](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/snapshot-profiles) are used to schedule snapshots; assign a profile to a volume to perform automated snapshots.

### Assign a Snapshot Profile to a Volume

{% hint style="info" %}
**Snapshots can only be performed on volumes of type=local.**
{% endhint %}

1. From the **volume dashboard**, click **Edit** on the left menu.
2. In the _**Snapshot profile**_ field, select the desired profile from the dropdown list.
3. Click **Submit** at the bottom of the page.

## Manual Volume Snapshots

### Take a Manual Snapshot of a Volume

{% hint style="info" %}
**Snapshots can only be performed on volumes of type=local.**
{% endhint %}

1. From the volume dashboard, click **Take Snapshot** on the left menu.
2. Enter a _**Name**_ for the snapshot (required).
3. Enter a _**Description**_ (optional).
4. The _**Quiesce**_ option can be selected to freeze I/O during the snapshot process.
5. In the _**Expires**_ field, select/enter a date and time for expiration.
6. Click **Submit** at the bottom of the page.

{% hint style="warning" %}
**Always consider vSAN Usage**

When selecting expiration for a snapshot it is important to consider vSAN space utilization. Initially source and snapshot are the same and thus there is no impact on storage utilization; however, as source data diverges more from the snapshot data, there is less deduplication between the two and thus more vSAN usage. The _Never Expires_ option is not recommended unless necessary.
{% endhint %}

## Restore a Volume from Snapshot

{% hint style="info" %}
**To restore a volume from a system snapshot, the volume must first be imported from the system snapshot as detailed below. To restore from an individual volume snapshot, skip the import section of instructions and continue to Restore to overwrite -OR- Restore to create new instructions**

Individual volume snapshots can only be imported from a full system snapshot or a partial system snapshot that included the intended volume. 
{% endhint %}

### _Import Volume Snapshot from a System Snapshot (to make it available for a volume restore)_

1. From the **volume dashboard**, click **System Snapshots** (left menu or UI tile).
2. Click to **select desired system snapshot**.
3. Click **Import Snapshot** on the left menu.
4. \***Name, Description and Expiration fields** will default to the values from the system snapshot; make changes if desired; changes made will only apply to the import and will not affect the underlying system snapshot.
5. Click **Submit** to continue.
6. (If the process was continued) a message should appear stating the import process has begun. Click the **Ok** button to acknowledge.
7. When the import is complete, the snapshot will be available for restore using instructions below.


### _Restore a Volume (to overwrite existing current version of volume)_

1. From the **volume dashboard**, click **Snapshots** on the left menu.
2. A listing of available snapshots is displayed. Click to **select the desired snapshot**.
3. Select **Restore over Source** from the left menu.
4. A warning message will appear to caution that this will overwrite the existing volume and all of its data. _By default, **Restore Data Only** is selected; this option will restore over data within the volume, but not modify any current volume settings. The alternate option: **Restore Data and Settings** will both restore over volume data and will replace volume settings with those in the snapshot._
5. Click the **Proceed** button to continue/ or **Cancel** to abort.

### _Restore a Volume (to create a new volume)_

1. From the volume dashboard, click **Snapshots** on the left menu.
2. A listing of available snapshots is displayed. Click to **select the desired snapshot**.
3. Click **Restore To New** on the left menu.
4. The **Destination Service VM** defaults to the NAS service of the source volume; if multiple NAS services exist on the system, a different service can be selected on which to restore the volume.
5. The **Volume Name** (for the new volume instance) will default to ORIGINALVOLUMENAME\_restored; change name if desired.
6. Click the **Submit** button to create the new volume from snapshot. The new volume is brought online automatically. To view the new volume's dashboard, return to _Volumes_ and double-click on the volume in the listing.
