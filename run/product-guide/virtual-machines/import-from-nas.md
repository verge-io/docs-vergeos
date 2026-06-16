---
title: "Importing VMs from a NAS Volume"
description: "Instructions for bulk importing virtual machines from NFS or CIFS network shares into VergeOS using the NAS volume import method."
semantic_keywords:
  - "import VMs from NFS CIFS network share"
  - "bulk VM import from NAS volume"
  - "migrate virtual machines from network storage"
  - "import VMX OVF files from remote volume"
use_cases:
  - bulk_import_vms_from_nas
  - migrate_vms_from_network_share
  - import_vmx_ovf_from_remote_volume
tags:
  - virtual-machines
  - import
  - migration
  - nas
  - nfs
  - cifs
  - bulk-import
  - remote-volume
categories:
  - Virtual Machines
---

# Importing VMs from a NAS Volume

This method allows for the import of many VMs at once. It does not require uploading any files to the vSAN, but rather, allows for pulling data from an NFS or CIFS share. Note: For production, live, VMware environments, it is best to utilize the VMware Service to [**Import from a VMware Backup Job**](import-from-vmware.md)

{% hint style="warning" %}
**Import should be performed from VMs that are powered down.**


{% endhint %}

{% hint style="info" %}
**NAS Import is only for VMs, not disks. This process is for VMX or OVF files only. Any other formats will need to [Importing VMs from Files](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/import-vms-from-files).**


{% endhint %}

## Import from Volume

1. To utilize an external NFS or CIFS share for VM import, the external source must be set up as a **Remote Volume** in the NAS. See [**Remote Volumes**](../nas/nas-remote-volumes.md) for instructions.
2. From the cloud Dashboard, select **Machines** from the menu or click the Machines quick-link on the dashboard.
3. Select **New VM** from the left menu.
4. Select Type of (on the left), **--Import from Volume--**.
5. Existing volumes are displayed on the right. Click to **select the appropriate CIFS/NFS Remote Volume**.
6. Click **Next** (bottom of the screen).
7. The screen will display existing folders within the selected NAS volume. ***Select folders*** where the desired VM files reside. VMs will also be imported from subdirectories of selected folders. (Click the top left checkbox to select all folders in the volume.)
8. Click **Next** (bottom of the screen).
9. The import job is given a default name of "Import Volume" + *NameofVolume*. **Import job Name can be changed** as desired.
10. By default, ***MAC Addresses*** will be preserved (MAC addresses will stay the same as the source VMs from which they are imported); this is typically recommended to avoid necessary reconfiguration with the guest OS. If this option is unselected, the system will generate new, unique MAC addresses for all NICs.
11. ***Preferred Tier*** can be selected or left at **--default--**. This determines the tier first attempted for VM storage. The [**Preferred Tiers**](../storage/preferred-tiers.md) page provides a detailed explanation of Preferred Tier.
12. When fields are entered as desired, click **Submit**.
13. The import is initiated and the **Import Job Dashboard** will display. The following information (as well as additional data) is provided:
    - ***Status*** (Initializing/Importing/Complete)
    - ***Created Date***
    - ***Child Import Jobs List***, a child job for each individual VM, with:
        - status, status messages if applicable, VM name, source volume, preferred tier, preserve MAC setting, Created and last update date/time
    - ***Job Logs***
    - ***Number of completed Child Jobs(VMs) / total number of Jobs (VMs) detected***

See [**Viewing Import Jobs**](view-import-jobs.md) for more information on viewing the details of an import job.
