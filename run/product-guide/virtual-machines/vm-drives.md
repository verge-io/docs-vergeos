---
title: "Virtual Machine Drives"
description: "Guide to adding, modifying, erasing, and removing virtual machine drives in VergeOS, including disk types, interfaces, media options, shared disks, and storage tier selection."
semantic_keywords:
  - "add drive to virtual machine VergeOS"
  - "VM disk interface VirtIO SCSI SATA IDE"
  - "non-persistent golden image drive VDI"
  - "import disk clone disk CD-ROM drive"
  - "shared disk multiple VMs clustering"
use_cases:
  - add_drive_to_vm
  - configure_drive_interface
  - create_non_persistent_drive
  - import_disk_image
  - configure_shared_disk
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
  - shared-disk
  - preferred-tier
categories:
  - Virtual Machines
---

# Virtual Machine Drives

This page describes how to add, configure, modify, erase, and remove virtual machine drives in VergeOS. The drive form is conditional: the **Media** type, **Interface**, and other selections determine which fields appear.

## Adding a Drive

1. From the VM dashboard, click **New Drive** on the left menu.
2. Configure the fields described below. Less-common options are in the collapsible **Advanced** section of the form.
3. Click **Submit**.

Repeat to add more drives.

## Drive Configuration Fields

### Basic Fields

* **Enabled**  
Default: on. Disable to stage a drive without presenting it to the guest.

* **Name**  
Optional. When omitted, VergeOS names drives `drive_x` in creation order, starting at 0.  
Give a distinctive name to any drive that must be easy to identify later — Golden Images, shared disks, data volumes.

* **Read Only**  
Default: off. Use for drives that must not be modified, such as a restored disk used only to recover data.

* **Description**  
Optional. Recommended when a VM has more than one drive.

### Media

* **Disk** (default)  
Standard virtual disk. Creates a new, empty `.raw` file as the source.  
Set **Disk Size** and, optionally, **Preferred Tier**.

* **CD-ROM**  
Read‑only; presents an ISO file as inserted media. Used to install an OS or other software.  
Select the ISO now or after the drive is created.

* **Clone Disk**  
Creates a duplicate of an existing disk (`.raw` file) on the same system.  
Select the source in **Media File**.

* **EFI Disk**  
Normally system‑generated. Create manually only for custom use cases, such as a vendor-supplied UEFI firmware image.

* **Import Disk**  
Imports a disk image (`.raw`, `.qcow`, `.qcow2`, `.vhd`, `.vhdx`, `.vmdk`) and creates a new `.raw` file as the disk source.  
The source file must be [uploaded to the vSAN](../storage/uploading-files-to-vsan.md) first; select it in **Media File**.

* **Non-Persistent**  
The drive reverts to the referenced `.raw` file on each boot.  
Designed for Golden Image / VDI deployments where all updates are made centrally.  
Select the referenced disk in **Media File**.

### Interface

* ***Virtio‑SCSI***  
Recommended. High-performance, para‑virtualized SCSI with a standard command set.  
Most Linux distributions include the driver; Windows requires the [virtio drivers](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso).

* ***Virtio (Legacy)***  
Maximum I/O performance, but lacks some SCSI features such as TRIM. Requires guest driver support.

* ***Virtio‑SCSI (Dedicated Controller)***  
A para-virtualized SCSI device with its own controller (a new PCI bridge in the guest).  
Use when a Virtio‑SCSI drive must live on a different storage tier than the VM's existing Virtio‑SCSI drives — it keeps tiered drives on separate virtual controllers.

* ***LSI controllers***  
Four VMware‑compatible controller options provided for compatibility: **LSI53C895A SCSI**, **LSI MegaRAID SAS 1078**, **LSI MegaRAID SAS 2108**, and **LSI SAS 1608**.

* ***SATA (AHCI)***  
Legacy fallback for guests without para-virtualized drivers, such as older operating systems and recovery environments. **Only for the Q35 machine type.**

* ***USB***  
Presents the drive as a USB storage device.

* ***IDE***  
Legacy support. **Only for the PC (i440FX) machine type.**

### Size & Storage Fields

* **Disk Size**  
Appears for **Disk** media only.

* **Media File**  
Appears for **CD-ROM**, **Clone Disk**, **Import Disk**, **Non-Persistent**, and **Shared Disk**.  
Select the ISO or disk appropriate for the media type:
  * CD-ROM: Select a \*.iso file (files uploaded to the vSAN). The \*.iso file can also be selected after drive creation.
  * Clone Disk: Select a \*.raw file (existing disks on this VergeOS system).
  * Import Disk: Select a disk image (files uploaded to the vSAN). Supported file types: .raw, .qcow, .qcow2, .vhd, .vhdx, .vmdk.
  * Non-Persistent Disk: Select a \*.raw file (existing disks on this VergeOS system).
  * Shared Disk: Select an existing disk on this VergeOS system (grouped by VM, shown as drive name and description).

* **Preferred Tier**  
Appears for **Disk** and **EFI Disk**.  
Select a [storage tier](../storage/storage-tiers.md) or leave **-- Default --** to use the system default VM drive tier.

* **Override Preferred Tier**  
Appears for **Clone Disk**, **Import Disk**, and **Non-Persistent**.  
Check it to place the new drive on a different tier than the media file's current tier.

* **OVMF Vars / OVMF Code File** *(VergeOS 26.2 or later)*  
Appear for **EFI Disk**.  
Leave **-- Default --** for the system-managed firmware, or select an imported vendor-supplied OVMF image for appliances that ship their own signed UEFI firmware.

### Advanced Fields

* **Shared Disk** *(VergeOS 26.2 or later)*  
Attaches an existing disk to multiple VMs at the same time, for clustered applications or shared data volumes. Shared disks support SCSI-3 Persistent Reservations.
  * Must be set when the drive is created.
  * Applies to *Media:* ***Disk***. When enabled, *Interface* choices are limited to ***Virtio-SCSI*** and ***Virtio-SCSI (Dedicated Controller)***.
  * Select the disk to attach in *Media File* (existing disks, grouped by VM; a disk cannot be shared with the same VM twice).

{% hint style="info" %}
The KB article [Using Shared Disks for Windows Clustering](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/using-shared-disks-windows-clustering) provides step-by-step instructions for configuring VMs with shared disks for Windows clustering.
{% endhint %}

* **Serial Number**  
Appears for **Disk** only. An alphanumeric identifier the virtual storage controller exposes to the guest OS.

* **Asset**  
A unique identifier for the drive (for example `OS` or `Data`), used to reference the drive in Recipes and automation.

* **Strict Fsync**  
Options: **System Default** (default), **On**, **Off**.  
When on, metadata writes are not throttled for this drive, which affects performance. The system default is off (a vSAN configuration setting). Leave at **System Default** unless directed by support.

* **Discard**  
Default: on. Frees unused blocks on the vSAN when the guest deletes data. Leave enabled unless directed otherwise by support. See [VM Disk Discard](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/virtual-machines/vm-disk-discard) for details.

* **Optimize For**  
  * ***General Usage*** – 64 KB chunks with read‑ahead (default). The right choice for most workloads.
  * ***Large Files*** – up to 1 MB chunks. Only benefits workloads that access very large files sequentially.

* **Advanced Properties**  
Custom key/value properties for specialized configurations or integrations.

## Drive Operations

{% hint style="warning" %}
Erasing or removing a drive can render a VM unusable. Verify the operation targets the intended drive on the intended VM. Take a short-term VM snapshot first.
{% endhint %}

### Erase a Drive

Power off the VM before you erase a drive.

1. From the VM dashboard, click **Drives**.
2. Select the drive(s) to erase.
3. Click **Erase**.
4. Click **Yes** to confirm.

### Remove a Drive

The drive must be offline: power off the VM, or hot-unplug the drive where the guest supports it.

1. From the VM dashboard, click **Drives**.
2. Select the drive(s) to delete.
3. Click **Delete**.
4. Click **Yes** to confirm.

### Modify a Drive

{% hint style="info" %}
**Considerations**

- The **Media** type and the **Shared Disk** setting cannot be changed after the drive is created.
- Drives cannot be reduced in size.
- Interface or size changes can require corresponding changes inside the guest OS.
{% endhint %}

1. From the VM dashboard, click **Drives**.
2. Select the drive to modify.
3. Click **Edit**.
4. Modify the fields.
5. Click **Submit**.
