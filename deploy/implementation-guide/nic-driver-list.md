---
title: "VergeOS Included Ethernet Drivers"
description: "Reference list of Ethernet drivers packaged with VergeOS for host nodes."
semantic_keywords:
  - "VergeOS network drivers"
  - "Ethernet driver list"
use_cases:
  - review_included_drivers
  - plan_vm_network_interface_selection
  - understand_driver_inventory
tags:
  - networking
  - drivers
  - ethernet
  - kernel
  - virtualization
categories:
  - Virtual Machines
  - Networking
---

# VergeOS Included Ethernet Drivers

VergeOS includes a broad set of Ethernet drivers as part of its Linux-based virtualization stack, and this page reflects the drivers packaged within the platform for the current release.

{% hint style="info" %}
**Need hardware not shown?**

If you do not see a network adapter family you plan to use, contact **VergeOS Sales** for guidance.  
They can help evaluate your requirements and confirm whether your hardware aligns with recommended deployment practices.
{% endhint %}

---

## Broadcom

| Family / Series | Driver |
|-----------------|--------|
| NetXtreme — BCM5700–5789, BCM570x/571x/572x/575x/576x, BCM5780–5788, BCM5901, BCM5906, BCM5776x–5779x | `tg3` |
| NetXtreme II GbE — BCM5706, BCM5708, BCM5709, BCM5716 | `bnx2` |
| NetXtreme II 10/20G — BCM577xx | `bnx2x` |
| NetXtreme‑C/E — BCM573xx, BCM574xx, BCM575xx, BCM576xx, BCM5880x | `bnxt_en` |
| BCM57708 (50–800G) | `bng_en` |
| BCM4401/4402 | `b44` |

---

## Cavium / Marvell Octeon

| Family / Series | Driver |
|-----------------|--------|
| ThunderX NIC PF/VF, BGX, XCV | `nicpf`, `nicvf`, `thunder_bgx`, `thunder_xcv` |
| LiquidIO — CN23XX, CN65XX, CN68XX (+VF) | `liquidio`, `liquidio_vf` |
| Octeon endpoint (+VF) | `octeon_ep`, `octeon_ep_vf` |

---

## Chelsio

| Family / Series | Driver |
|-----------------|--------|
| T3 — T302, T310, T320, S310, S320, N320 | `cxgb3` |
| T4/T5/T6 Unified Wire — T4xx, T5xx, T6xx (PF4 and PF0–3 variants) | `cxgb4` |
| T4/T5/T6 virtual functions | `cxgb4vf` |
| T1/T2 — T210 Protocol Engine and early adapters | `cxgb` |

---

## Intel

| Family / Series | Driver |
|-----------------|--------|
| PRO/100 — 8255x, 82562, ICH3–ICH5 LOM | `e100` |
| PRO/1000 PCI/PCI‑X — 82542, 82543–82547 | `e1000` |
| PCIe GbE — 82571–82574, 82583, ICH8–ICH10 LOM, 82577/78/79, I217, I218, I219 | `e1000e` |
| Server GbE — 82575, 82576, 82580, I210, I211, I350, I354, DH8900CC | `igb` (+`igbvf`) |
| 2.5G — I225, I226, Killer E3100X | `igc` |
| 10G — 82598, 82599, X520, X540, X550, X552, X553, X557, E610 | `ixgbe` (+`ixgbevf`) |
| 10/25/40G — X710, XL710, XXV710, X722, I710 | `i40e` (+`iavf`) |
| 25/100/200G — E810, E822, E823, E825, E830, E835 | `ice` |
| IPU / Infrastructure Data Path Function | `idpf` |
| FM10000 switch host interface | `fm10k` |

---

## Marvell / SysKonnect

| Family / Series | Driver |
|-----------------|--------|
| Yukon II — 88E80xx PCIe/PCI‑X, SK‑9Exx, SK‑9Sxx, DGE‑5xx | `sky2` |
| Genesis / Yukon — 88E8001, SK‑98xx, 3c940 | `skge` |

---

## Mellanox / NVIDIA Networking

| Family / Series | Driver |
|-----------------|--------|
| ConnectX‑2, ConnectX‑3, ConnectX‑3 Pro (+VFs) | `mlx4_core` |
| Connect‑IB, ConnectX‑4/4 Lx, ‑5/5 Ex, ‑6/6 Dx/6 Lx, ‑7, ‑8, ‑9, ‑10 (+VFs) | `mlx5_core` |
| Spectrum, Spectrum‑2, ‑3, ‑4 switch ASICs | `mlxsw_spectrum` |

---

## QLogic

| Family / Series | Driver |
|-----------------|--------|
| FastLinQ QL41000, QL45000 (+VFs) | `qede` |
| cLOM8214, ISP8324 converged | `qlcnic` |
| ISP4022, ISP4032 | `qla3xxx` |
| BCM57840 (QLogic‑branded) | `bnx2x` |

---

## Realtek

| Family / Series | Driver |
|-----------------|--------|
| RTL8168/8169/811x GbE, RTL8125 2.5G, RTL8126 5G, RTL8127 10G, Killer E2600/E3000/E5000 | `r8169` |
| RTL8139 / RTL8129 Fast Ethernet | `8139too`, `8139cp` |
| RTL90xx automotive Ethernet switch | `rtase` |

---

{% hint style="info" %}
**Release Variability**

Driver availability may vary across VergeOS releases as the Linux kernel evolves.  
This list reflects the drivers included at build time for the current release.
{% endhint %}
```

---
