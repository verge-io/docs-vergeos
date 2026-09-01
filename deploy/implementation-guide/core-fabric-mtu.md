---
title: Core fabric MTU when the NIC cannot exceed 9000
description: Set the installer physical MTU to 9000 when the server NIC cannot exceed 9000. Overlay is then 8950. Keep switch MTU at 9216.
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

Set the installer **MTU** to **9000** when the physical NIC cannot exceed 9000 (for example some UCS vNICs). Do not leave the installer at 9192.

## Prerequisites

- Read [Network design](network-design.md) and [Switch configuration](switch-configuration.md).
- Set switch MTU on core fabric ports. VergeOS requires **9216** on switch ports.
- Confirm the server NIC maximum MTU.

## Installer MTU and overlay

The installer **MTU** is the physical NIC and switch-facing MTU. Enter a value the NIC and switching hardware support. The default is 9192. This field is not the post-encapsulation overlay payload. The overlay is derived. VXLAN overlay equals physical NIC MTU minus 50.

## Set the installer value

1. Open the installer physical network settings for a core fabric NIC.
2. Set **Core-Network** to yes.
3. Set **MTU** to `9000`.
4. Repeat for each core fabric network on the node.
5. Set the same installer **MTU** on every node in the system.

{% hint style="danger" %}
Do not enter 8950 in the installer **MTU** field. Overlay then becomes 8900. Do not enter 8976.
{% endhint %}

When installer **MTU** is 9000, overlay is 8950. Switch port MTU stays 9216. A capped NIC does not change the switch requirement.

## Why not 8976

8976 is 9000 minus 24, not 9000 minus 50. VXLAN overhead is 50, not 24. If 8976 is used as overlay, 8976 plus 50 equals 9026. That value overruns a 9000-capped NIC.

## After install

Verify fabric health. See [Core Fabric Status](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/core-fabric-status).
