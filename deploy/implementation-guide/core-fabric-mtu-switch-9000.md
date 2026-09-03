---
title: Core fabric MTU for physical networks supporting less than 9050 bytes
description: Set installer MTU to correspond to the physical network constraints. Do not leave at default (9192) if the switch/NIC does not support it. 

semantic_keywords:

VergeOS core fabric installer MTU
switch port MTU cap 9000
Core NIC MTU cap 9000
jumbo frames encapsulation overhead 50 bytes
Physical core MTU less than 9050 

use_cases:
install_core_mtu_switch_capped_9000 tags:
networking
core-fabric
mtu
installation
jumbo-frames categories:
Installation
---

# Core fabric MTU when the physical network cannot support 9050 bytes

## Overview

{% hint style="info" %}
**Key Points**

Physical switch ports and core NICs must support at least 50 bytes more than the desired guest MTU. The core fabric network always operates at physical MTU − 50 to accommodate packet encapsulation. For the default 9000-byte guest MTU, the physical network minimum is 9050.

Do not leave the installer at the default 9192 if your hardware cannot support frames of that size. During installation, set the MTU field to your actual hardware maximum. VergeOS will set the core fabric MTU to 50 bytes below that value, up to a maximum of 9000.

Each layer of tenancy adds 50 bytes of overhead. If tenants will host nested tenants, account for the full overhead depth. Three levels of nesting consume 200 bytes total above the guest payload.

{% endhint %}

Prerequisites
Read Network design and Switch configuration before beginning installation.
Confirm the maximum supported MTU for every switch port and core NIC in the physical core path. All nodes in the system must use the same value.



By default, the VergeOS Core network targets a 9000-byte MTU to support jumbo frames for guest-to-guest, inter-system communications. For this to work, every physical component in the core path — all core switch ports and core NICs — must support frames at least 50 bytes larger to accommodate encapsulation overhead. If any component in that path is capped below 9050, the MTU must be set accordingly during installation.

Example: When your core switch port or NIC is capped at 9000 bytes, set the MTU to 9000 for all core physical networks. VergeOS will configure the core fabric network at 8950 — 50 bytes below the physical maximum — to ensure encapsulation headers fit within the link's capacity.
Encapsulation overhead per tenant layer
Each layer of the VergeOS stack consumes 50 bytes of the physical MTU budget. Your physical hardware can support the MTU your switch ports and NICs allow — the higher the physical MTU, the more overhead headroom you have for nested tenant layers while still delivering full 9000-byte jumbo frames to guests.

The core fabric network MTU is capped at 9000 regardless of the physical MTU. Any physical MTU at or above 9050 results in the same core fabric MTU of 9000. The benefit of a higher physical MTU (for example, 9216) is that it provides sufficient overhead for deeper tenant nesting at full guest MTU.

Layer
Cumulative overhead
Min. physical MTU for 9000 guest MTU
Guest MTU when physical = 9000
Core fabric network
−50 B
9050
8950
Tenant — level 1
−100 B
9100
8900
Tenant — level 2
−150 B
9150
8850
Tenant — level 3
−200 B
9200
8800


A physical MTU of 9216 — a common NIC and switch maximum — satisfies the overhead requirement for three tenant levels with room to spare.

Set the installer value
During the VergeOS installation, configure each physical core network as follows. Repeat for every node in the system —** the MTU value must be consistent across all nodes.**

Set Core-Network to yes.
Set MTU to the maximum MTU your physical switch port and NIC can support. Do not leave the default 9192 if your hardware cannot carry frames of that size.
Repeat for each core fabric network interface on the node.
Apply the same MTU value on every node in the system. A mismatch across nodes will destabilize the core fabric.
After install
Verify that VergeOS applied the expected MTU values to both the physical and core fabric networks.

Physical core networks

Navigate to Networks > List.
Filter by Type = Physical.
Double-click a core physical network (for example, core1 Switch) to open its dashboard.
Confirm the MTU Size: This is the value you entered during installation and should not exceed the limits of the physical switch or core NIC. 

Core fabric network

In Networks > List, filter by Type = Core.
Double-click the Core network to open its dashboard.
Confirm the MTU Size field shows the expected value. The core fabric MTU defaults to 9000 — it will not exceed this regardless of the physical MTU entered during installation.
Physical MTU ≥ 9050 → Core fabric MTU = 9000
Physical MTU < 9050 → Core fabric MTU = physical MTU − 50 (e.g., physical 9000 → core fabric 8950)

Fabric health

Verify overall fabric connectivity and node status. See Core Fabric Status.

