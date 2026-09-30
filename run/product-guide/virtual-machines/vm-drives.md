---
title: "Virtual Machine Drives"
description: "Guide to adding, modifying, erasing, and removing virtual machine drives in VergeOS, including disk types, interfaces, media options, and storage tier selection."
semantic_keywords:
  - "add drive to virtual machine VergeOS"
  - "VM disk interface VirtIO SCSI SATA IDE"
  - "non-persistent golden image drive VDI"
  - "import disk clone disk CD-ROM drive"
  - "modify resize erase delete VM drive"
use_cases:
  - add_drive_to_vm
  - configure_drive_interface
  - create_non_persistent_drive
  - import_disk_image
  - modify_vm_drive_settings
tags:
  - virtual-machines
  - drives
  - storage
  - virtio
  - disk
  - vdisk
  - cd-rom
  - non-persistent
  - golden-image
  - preferred-tier
categories:
  - Virtual Machines
---


# Virtual Machine Drives

This page describes how to add, configure, modify, erase, and remove virtual machine drives in VergeOS. Drive configuration is field‑based: depending on the **Media** type, **Interface**, and other selections, different fields will appear.

---

## Adding a Drive

From the **VM dashboard**, click **New Drive** on the left menu.  
You will be presented with the **Drive Configuration** panel, which contains all fields relevant to the selected Media type and Interface.

After configuring the fields, click **Submit**.  
Repeat as needed to add additional drives.

---

# Drive Configuration Fields

## Basic Fields

* **Enabled**
Toggle to enable or disable the drive.  
Useful when temporarily attaching a drive or staging a configuration change.

* **Name**  
Optional.  
If omitted, VergeOS auto‑generates names (`drive_x`) in order, as created, where x is an integer starting with 0.    
Using a distinctive name is strongly recommended for Golden Images, Shared Disks, or any drive that needs easy identification.  


* **Read Only**  
Default: Off  
Useful for recovery scenarios or drives that should not be modified.  

* **Description**  
Optional but recommended when multiple drives exist. 


---

## Media

* **Disk** (default option)  
Standard virtual disk, creates a new empty raw file as source 
Requires selecting **Disk Size** and optionally **Preferred Tier**.

* **CD-ROM**  
Read‑only. Uses an ISO file.  Typically used for installing OS or other software. 
ISO can be selected now or after virtual drive creation.  


* **Clone Disk**  
Creates a duplicate of an existing VergeOS disk (`.raw` file) within the same system.  
Requires making a selection in the *Media File* dropdown list. 

* **EFI Disk**  
Typically system‑generated; can be created manually for custom use cases.   


* **Import Disk**  
Imports external disk (`.raw`, `.qcow`, `.qcow2`, `.vhd`, `.vhdx`, `.vmdk`). Creates a new `.raw` file as disk source.
Requires making a selection in the *Media File* dropdown list. Source file must be [Uploaded Files to the vSAN](product-guide/storage/uploading-files-to-vsan.md)    


* **Non-Persistent**  
Drive reverts to the referenced `.raw` file on each boot.  
Ideal for Golden Image / VDI deployments where all updates and modifications can be made centrally. 
Requires selecting an existing VergeOS `.raw` file.  


---

## Interface

* ***Virtio‑SCSI***  
Recommended option. High performance, para‑virtualized SCSI.  
Linux supports it natively; Windows requires Virtio drivers.  


* ***Virtio (Legacy)***  
Maximum I/O performance but lacks some SCSI features. Requires guest compatibility.   


* ***Virtio‑SCSI (Dedicated Controller)***  
Provides a para-virtualized SCSI device with its own controller (new PCI bridge within the guest). Use when adding a Virtio‑SCSI drive on a different storage tier than existing Virtio‑SCSI drives. Keeps tiered drives on separate virtual controllers.  


* ***LSI***  
native VMware‑compatible controller options provided for compatibility, where needed. 

* ***SATA (AHCI)***  
Provided as a legacy compatibility fallback - scenarios that require native OS support without paravirtualized drivers, such as installing older guest operating systems, running legacy recovery environments, etc. **Only for Q35 machine type.**  

* ***IDE***  
Provided for extreme legacy support.  **Only for PC (i440FX) machine type.** 

---

## Size & Storage Fields

* **Disk Size**  
Only appears for **Disk** media type.

* **Media File**  
Appears for **CD-ROM**, **Clone Disk**, **Import Disk**, **Non-Persistent**, and **Shared Disk**  
Select the ISO or disk image appropriate for the media type.  

* CD-ROM: Select *.iso (files uploaded to vSAN) Note: *.iso file can also be selected after VM creation.

* Clone Disk: Select *.raw file (existing disks on this VergeOS system)

* Import Disk: Select disk image (files uploaded to vSAN) Supported file types: (.raw,.qcow,.qcow2,.vhd, .vhdx,.vmdk)

* Non-Persistent Disk: Select *.raw file (existing disks on this VergeOS system).

* Shared Disk: Select *.raw file (existing virtual SCSI disks on this VergeOS system)


* **Preferred Tier**  
Appears for **Disk** and **EFI Disk**.  
Choose a storage tier or leave as **Default** (*Default VM drive tier* configured in system settings)

* **Override Preferred Tier**  
Appears for **Clone Disk**, **Import Disk**, and **Non-Persistent**.  
Allows placing the drive on a different tier than the media file’s current tier.


---

## Advanced Fields

* **Shared Disk**  
Allows attaching an existing disk to multiple VMs.  Useful for clustered applications or shared data volumes. 
  * Option only applies to Media: ***Disk***
  * Option only applies to ***Virtio SCSI*** and ***Virtio SCSI (Dedicated Controller)*** interfaces.  
  * Requires making a selection in the *Media File*  (select an existing virtual SCSI disk; does not allow sharing disks attached to the same VM)

{% hint style="info" %}
KB article: [Using Shared Disks for Windows Clustering](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/using-shared-disks-windows-clustering) provides step-by-step instructions for configuring a shared disk for Windows clustering use within VergeOS.

{% endhint %}


* **Serial Number**
Appears for **Disk** only. Alphanumeric logical identifier exposed through virtual storage controller to guest OS. 


* **Asset**  
A unique identifier for the drive (e.g., “OS”, “Data”).  
Used in Recipes and automation.  


* **Strict Fsync**
  * ***System Default*** (default)
  * ***On***
  * ***Off**

{% hint style="info"}
* System default=disabled (vSAN conf setting)
* When enabled no throttle imposed on meta writes

{% endhint %}


* **Discard** (default on)

Provided for backward compatibility only. 


* **Optimize For**  
  
* ***General Usage*** – 64 KB chunks with read‑ahead (default)  
* ***Large Files*** – up to 1 MB chunks; beneficial only for sequential access of very large files  

{% hint style="info" %}
The default *Optimize For* choice is General Usage, which should be the preferred choice for most use cases. Large Files could be beneficial for workloads exclusively (or nearly exclusively) working with very large files accessed sequentially.

{% endhint %}

* **Advanced Properties**  

Allows adding custom key/value properties for specialized configurations or integrations.


---

# Drive Operations

{% hint style="caution" %}
**Caution:** Erasing or removing a drive can render a VM unusable.  Take special care to ensure an erase operation is being applied to the intended drive on the intended VM. Consider taking a short-term VM snapshot first.  

{% endhint %}

## Erase a Drive

The VM must be powered off.

1. VM dashboard → **Drives**  
2. Select drive(s)  
3. Click **Erase** 
4. Confirm

---

## Remove a Drive

Drive must be offline (VM powered off or hot‑unplugged).

1. VM dashboard → **Drives**  
2. Select drive(s)  
3. Click **Delete** 
4. Confirm

---

## Modify a Drive

### Considerations

  * Media type cannot be changed after creation  
  * Drives cannot be reduced in size  
  * Interface or size changes may require guest OS adjustments  


1. VM dashboard → **Drives**  
2. Select drive  
3. Click **Edit**  
4. Modify fields  
5. Submit

---

