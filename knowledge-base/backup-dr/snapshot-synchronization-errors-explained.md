---
title: Snapshot Synchronization Errors Explained
slug: snapshot-synchronization-errors-explained
author: VergeOS Documentation Team
date: 2023-01-24T19:17:04.187Z
semantic_keywords:
  - snapshot sync error messages
  - site sync troubleshooting connection timeout
  - sync-back configuration errors
  - CBT changed block tracking sync failures
use_cases:
  - troubleshoot_snapshot_sync_errors
  - diagnose_site_sync_failures
  - resolve_sync_back_configuration_issues
  - fix_snapshot_naming_conflicts
categories:
  - Snapshot
  - Troubleshooting
editor: markdown
dateCreated: 2022-09-02T15:54:31.531Z
description: >-
  Reference guide explaining common VergeOS site sync error messages, their
  causes, and recommended resolutions for snapshot synchronization issues.
tags:
  - snapshot
  - error
---

# Snapshot Synchronization Errors Explained

The VergeOS platform provides a feature known as **Site Syncs** to replicate a copy of a system snapshot.

{% hint style="info" %}
**For more information on Snapshots and Site Syncs, refer to our** [**Product Guide on Sync Configuration**](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/sync-configuration)**.**
{% endhint %}

Occasionally, the system may generate a system alert from a new Message Log entry related to the Site Sync functionality. Below is a list of common errors along with a brief explanation:

### ybvsan: Error walking tier 3 refs: (2) No such file or directory

* This error can occur if the VergeOS software version is mismatched between the sending side and the destination side.

### Unable to delete snapshot that no longer exists: Resource '/v4/cloud\_snapshots/1' not found during delete

* This error is usually the result of a timing issue when a snapshot is being deleted, and the reference is deleted in the metadata of the system.

### Error notifying client with 'notify\_complete' Error (403) while communicating with server

* The snapshot successfully synchronized, but this error appeared during the sync clean-up process. If this error occurs on multiple snapshot synchronizations, the handshake credentials between the two systems may have stopped working. In that case, consult VergeOS support for assistance.

### Error - Sync back not found and no registration code supplied

* This error occurs when requesting a snapshot back from the destination site to the source site. If this message appears, Sync Back is not configured between the two systems. Refer to the [Guide on Sync Back](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/sync-back) for instructions on setting up Sync-Back between the systems.

### Error - Sync Request for 'system name' Error notifying client with 'notify\_start' Connection timed out

* This error occurs when requesting a snapshot back from the destination site to the source site, similar to the previous error. Ensure that Sync Back is configured properly between the two systems.

### An error has occurred while syncing 'snapshot name': Resource temporarily unavailable. Retrying 1 of 10

* This error typically results from an interruption of the transfer connection between the source site and the destination site. The sync will automatically retry following the Retry interval setting. The retry count will increase until the connection is re-established or until the maximum Queue retry count has been reached.

### Error- Unable to create tenant snapshot 'snapshotinterval\_yyyymmdd': This name already exists

* The local snapshot schedule is naming snapshots the same as the inbound snapshots from the site sync. A simple fix is to rename the origin (sending) side snapshot by editing the auto-sync configuration. Use the field **Prefix the snapshot name with this on the destination** and add something unique, such as **remote-**.

### Unable to update system snapshot: No such file or directory

* This error indicates a possible timing issue with snapshots. Review the **Outgoing Sync** configuration on the sending site for any setting mismatches.

### Error notifying client with 'notify\_start' Connection timed out

* The sync task was unable to start because the connection timed out. Typically, this error occurs when requesting a snapshot back from the destination side to the original sending side. In most cases, this is caused by a firewall blocking the traffic or missing traffic rules on the destination side. Refer to the [Guide on Sync Configuration](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/sync-configuration) for the required traffic rules.

### Error notifying client with 'notify\_start' / 'notify\_complete' Error (500) while communicating with server

* The bulk data transfer still completes — snapshots appear Normal on both ends and data keeps flowing — but the start and finish notification calls return HTTP 500 on every sync cycle. This typically indicates a major version mismatch between the source and destination systems (for example, a pre-26.x system syncing with a 26.x system). The underlying data path is more version-tolerant than the notification API, so snapshots land on both sides while the notifications error out. To resolve, upgrade the lagging side to a release compatible with the other end. For a large version gap, you may need to step through intermediate release branches rather than jumping straight to the target version. Once the versions align, the errors stop on the next sync cycle.
