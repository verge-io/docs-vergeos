---
title: UCS vNIC Core fabric MTU (NIC cannot exceed 9000)
description: Set the installer physical MTU to 9000 when the server NIC cannot exceed 9000. Keep switch MTU at 9216.
semantic_keywords:
  - VergeOS core fabric installer MTU 9000
  - NIC MTU cap 9000 UCS vNIC
  - jumbo frames encapsulation overhead 50 bytes
  - switch MTU 9216 core fabric
use_cases:
  - install_core_mtu_nic_capped_9000
  - ucs_vnic_core_fabric_mtu
  - avoid_incorrect_core_mtu_8976
tags:
  - networking
  - core-fabric
  - mtu
  - installation
  - jumbo-frames
categories:
  - Installation
---

# Core fabric MTU when the NIC cannot exceed 9000

Set the installer **MTU** to **9000** when the physical NIC cannot exceed 9000 (e.g., UCS vNICs). Do not leave the installer at 9192.

## Prerequisites

- Read [Network design](network-design.md) and [Switch configuration](switch-configuration.md).
- Set switch MTU on core fabric ports. VergeOS requires **9216** on switch ports.
- Confirm the server NIC maximum MTU.

## Installer MTU

The **MTU** specified during installation pertains to the physical network (default is 9192).   When configuring physical networks that handle the core, **enter an MTU size supported by the NIC and switching hardware.**  If the NIC cannot exceed 9000, the MTU size should be set accordingly.
The installation will automatically account for necessary overhead and create the Core (vxlan fabric network) with an MTU size 50 bytes less. 

## Set the installer value

1. Open the installer physical network settings for a core fabric NIC.
2. Set **Core-Network** to yes.
3. Set **MTU** to `9000`.
4. Repeat for each core fabric network on the node.
5. Set the same installer **MTU** on every node in the system.

When installer core network **MTU** is set to 9000, the created 'Core' network MTU is set to 8950.  Switch port MTU stays 9216. A capped NIC does not change the switch requirement.


## After install

Verify fabric health. See [Core Fabric Status](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/core-fabric-status).
