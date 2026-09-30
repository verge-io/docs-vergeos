---
title: "VergeOS Included Storage Drivers"
description: "Reference list of storage, RAID, SAS, NVMe, Fibre Channel, and offload drivers packaged with VergeOS."
semantic_keywords:
  - "VergeOS storage drivers"
  - "RAID controller drivers"
  - "SAS HBA drivers"
  - "NVMe drivers"
  - "Fibre Channel drivers"
  - "iSCSI offload drivers"
use_cases:
  - review_included_drivers
  - plan_storage_interface_selection
  - understand_driver_inventory
tags:
  - storage
  - drivers
  - raid
  - sas
  - nvme
  - fibre-channel
  - iscsi
categories:
  - Virtual Machines
  - Storage
---

# VergeOS Included Storage Drivers

VergeOS includes a broad set of storage-related drivers as part of its Linux-based virtualization stack. This page reflects the drivers packaged within the platform for the current release.

{% hint style="info" %}
**Need hardware not shown?**

If you do not see a storage controller family you plan to use, contact **VergeOS Sales** for guidance.  
They can help evaluate your requirements and confirm whether your hardware aligns with recommended deployment practices.
{% endhint %}

---

## RAID Controllers

| Family | Driver |
|--------|--------|
| Microchip/Adaptec SmartRAID, SmartHBA, HPE Smart Array Gen10+ | `smartpqi` |
| Adaptec/Microsemi aacraid series | `aacraid` |
| HPE Smart Array Gen8/Gen9 | `hpsa` |
| Broadcom/LSI MegaRAID SAS — incl. Aero/9560 tri-mode (`1000:10e0`–`10e7`) | `megaraid_sas` |
| LSI MegaRAID legacy (mbox/v1) | `megaraid_mbox`, `megaraid` |
| IBM Power RAID | `ipr` |
| HighPoint RocketRAID (IOP series) | `hptiop` |
| Areca | `arcmsr` |
| Promise SuperTrak | `stex` |
| 3ware 9xxx / SAS / legacy | `3w-9xxx`, `3w-sas`, `3w-xxxx` |
| ATTO ExpressSAS | `esas2r` |
| Mylex / IBM ServeRAID / Marvell UMI | `myrb`, `myrs`, `ips`, `mvumi` |

---

## SAS / SATA Host Bus Adapters

| Family | Driver |
|--------|--------|
| Broadcom SAS2/SAS3 (9200/9300/9400) and 9500 tri-mode | `mpt3sas` |
| Broadcom 24G tri-mode (9600, SAS40xx/41xx/50xx/51xx) | `mpi3mr` |
| PMC/Microsemi PM8001/PM80xx SAS | `pm80xx` |
| Marvell SAS | `mvsas` |
| Intel C600 on-board SAS | `isci` |
| Adaptec SAS | `aic94xx` |
| LSI Fusion legacy (SAS/SPI/FC) | `mptsas`, `mptspi`, `mptfc` |

---

## Fibre Channel and FCoE

| Family | Driver |
|--------|--------|
| Emulex LightPulse — through LPe35000/LPe36000 (G7/G7P) | `lpfc` |
| QLogic/Marvell FC — 2400/2500/2600/2700/2800 series | `qla2xxx` |
| Chelsio T4/T5/T6 FCoE | `csiostor` |
| Brocade/Cavium | `bfa` |
| Cisco VIC FC | `fnic` |
| Marvell FastLinQ FCoE | `qedf` |
| Emulex EFCT target | `efct` |

---

## iSCSI Offload

| Family | Driver |
|--------|--------|
| Emulex OneConnect iSCSI | `be2iscsi` |
| QLogic iSCSI | `qla4xxx` |
| Marvell FastLinQ iSCSI | `qedi` |
| Chelsio / Broadcom iSCSI offload | `cxgb4i`, `cxgb3i`, `bnx2i` |

---

## NVMe, PCIe SSD, and Virtual Storage

| Family | Driver |
|--------|--------|
| Any NVMe SSD | `nvme` (class match) |
| NVMe behind Intel VMD | `CONFIG_VMD=m` |
| Micron P320/P420 PCIe SSD | `mtip32xx` |
| VMware PVSCSI | `vmw_pvscsi` |
| virtio-scsi | `CONFIG_SCSI_VIRTIO=m` |
| NVMe over TCP / FC | `CONFIG_NVME_TCP=m`, `CONFIG_NVME_FC=m` |

---

{% hint style="info" %}
**Release Variability**

Driver availability may vary across VergeOS releases as the Linux kernel evolves.  
This list reflects the drivers included at build time for the current release.
{% endhint %}
```

---
