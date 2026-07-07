---
title: Volume Syncs
semantic_keywords:
  - synchronize data between NAS volumes in VergeOS
  - volume sync for file-level backup and data transfer
  - configure recurring volume sync schedules
  - rsync and VergeOS sync methods with ACL preservation
  - remote and local volume data synchronization
use_cases:
  - sync_data_between_volumes
  - transfer_external_data_to_vsan
  - schedule_recurring_file_backups
  - configure_sync_advanced_options
  - migrate_data_between_storage_systems
categories:
  - NAS
description: >-
  How to create and configure volume syncs in VergeOS to synchronize data
  between local and remote NAS volumes, including scheduling, advanced sync
  options, and destination delete policies.
tags:
  - nas
  - volume sync
  - data transfer
  - backup
  - rsync
  - synchronization
  - scheduling
  - acl
  - remote volume
---

# Volume Syncs

Volume syncs allow for synchronizing data between two volumes. A volume sync can be used as a one-time transfer or recurring in order to synchronize data on a regular schedule. Volume syncs can involve both [**Remote Volumes**](nas-remote-volumes.md) and [**Local Volumes**](nas-local-volumes.md), providing the ability to:

* Easily transfer an external file system into VergeOS storage.
* Use VergeOS as a target for file-level backups of an external system.
* Transport data from a VergeOS NAS to an external storage system.
* Perform regular backups of VergeOS native-NAS data to another VergeOS system or a third-party storage.

## Create a Volume Sync

1. Navigate to **NAS** > **Volume Syncs**.
2. Click **New** on the left menu.
3. Select the _**NAS Service**_ (the NAS service hosting the volumes to be synchronized)
4. Specify a _**Name**_ for the new volume sync. Note: no spaces allowed.
5. Select _**Volume Sync**_ in the _**Type**_ dropdown list.
6. Enter a _**Description**_ for the volume sync (optional).
7. Specify _**Max Run Time**_ by entering an integer and selecting _**Units**_ (Hours/Days) from the dropdown list, **-or-** select **'Forever'** in the Units field to set an unlimited run time.
8. The _**Max Errors**_ setting will default to 1000. This will determine at what number of errors the sync job will automatically abort.
9. Verge.io sync is the default sync _**Method**_. While this method may provide better performance, alternately, the **rsync** method can be selected to include synchronization of CIFS file permissions.
10. Select _**Destination Delete**_ setting from the dropdown list. This setting specifies how files are handled that exist at the destination, but (no longer) exist at the source.
    * **Delete after transfer** - Files are deleted from the destination after all data is transferred; the delete part of the sync operation will entail an additional walk of the filesystem.
    * **Never delete (default)** - Files are not deleted (even when they no longer exist on the source).
    * **Delete before transfer** - Files are deleted before data is transferred.
    * **Delete after transfer (find during)** - Files to delete are found during transfer, but not actually deleted until after data is transferred. (This does not involve multiple walks of the source data.)
    * **Delete during transfer** - Files are deleted as they are encountered during the transfer process.
    * **Delete files from Destination** - Files are deleted in a manner automatically determined by the particular system.
11. Select _**Source Volume**_ from the dropdown list. Source volume can be either a local volume or a remote volume.
12. Specify a _**Source Start Directory**_ (or leave blank to sync the entire volume from the root). A trailing slash will copy only the contents of the directory; no trailing slash will copy the directory by name. For example: /data/ will copy everything under the data folder, not creating the data folder on the destination; /data will copy the data folder and all its contents.
13. Specify _**Include Files/Directories**_ (optional), to only synchronize particular files, directories, and/or file patterns. Example pattern: /foldername/
14. Specify _**Exclude Files/Directories**_ (optional), to skip particular files, directories, and/or file patterns. Note: the snapshots, lost+found, and quarantine folders are excluded by default.

{% hint style="info" %}
**Paths used in&#x20;**_**Source Start Directory**_**&#x20;and&#x20;**_**Include/Exclude**_**&#x20;entries always use forward slash ('/'), not backslash. This includes paths involving remote CIFS volumes.**
{% endhint %}

15. Select _**Destination Volume**_ from the dropdown list. (can be either a local volume or remote volume.)
16. Specify a _**Destination Start Directory**_ (or leave blank to sync to the root of the volume).
17. _**Start Profile**_ option should be enabled to provide a recurring, regularly-scheduled sync; disable Start Profile for a one-time sync or a sync that can only be started manually. Select a _**Start Time Profile**_ from the dropdown list **-or-** leave the **-- Default -** setting to utilize the start time of the built-in **"NAS Volume Syncs"** Profile. The _**Start Time Profile**_ determines when the recurring sync will start. [Snapshot Profiles](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/snapshot-profiles) are used to control volume sync Start Profiles.

{% hint style="warning" %}
**The&#x20;**_**Start Time Profile**_**&#x20;setting determines the start time of the sync only; it does not control snapshots for the volume!**
{% endhint %}

18. **Advanced Options**

* Specify a _**Run As User**_ (optional). By default, the sync operation is run as "root"
* _**Freeze Filesystem**_ (default - disabled) - Applies only when source volume is a local VergeOS volume; temporarily blocks write operations while buffers are flushed, the filesystem is branched and a clean-state snapshot is taken for the sync operation. Although not as instantaneous as a crash-consistent snapshot operation, a filesystem freeze can be a relatively quick operation.
* _**Preserve ACLs**_ (default - enabled) - Can be disabled for performance, when ACLs are unnecessary on the destination (for example: converting Linux volume to Windows)
* _**Preserve Extended Attributes**_ (default - enabled) - Can be disabled to omit extended attributes from sync transfer.
* _**Copy Symlinks**_ (default - enabled) - Can be disabled where symlinks point to external/separate file systems.
* _**Preserve Permissions**_ (default - enabled) - Applies to Linux permissions; can be disabled to avoid transferring to destination.
* _**Preserve Modification Time**_ (default - enabled) - Can be disabled to force complete transfer of all data on subsequent sync operations.
* _**Preserve Groups**_ (default - enabled) - Can be disabled to avoid transfer of group setting to destination.
* _**Preserve Owner**_ (default - enabled) - Can be disabled to avoid transfer of owner setting to destination.
* _**Preserve Device Files**_ (default - disabled) - Can be enabled to facilitate machine backups, etc. **This option should be used with caution!** Requires superuser permissions.
* _**Omit setting directory time**_ (default - disabled) - Directory times are assigned based on time of backup rather than from source data.
* _**Omit setting symlink time**_ (default - disabled) - Symlink times are not transferred from source data.
* _**Update destination files in-place**_ (default - disabled) - When a file needs to be updated, the sync will update the data directly rather than the default method of creating a new copy of the file and moving it into place when it is complete.
* _**Preserve CIFS ACLs**_ (default - enabled) - Sync will update destination ACLs to be the same as the source ACLs. The source and destination system must have compatible ACL entries for this option to work properly.
* _**Extended properties**_ - Extended properties can be specified to provide additional features/constraints for this sync; contact VergeOS Support for assistance with extended properties.
* _**Number of simultaneous workers**_ (default - 4) - Specifies the number of threads to be used for the sync operation. Increasing this number can improve sync completion times, particularly where syncs are performed over high-latency connections.

19. Click **Submit** to save the settings and create the new volume sync.

The dashboard for the new volume sync will appear. The sync job will be offline until either run manually or automatically started per the specified start profile.

## Start a Volume Sync

To start the sync manually select **Start Sync** from the left menu of the volume sync dashboard.
