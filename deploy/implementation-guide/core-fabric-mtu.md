---
title: Core fabric MTU when the NIC cannot exceed 9000
description: Set the installer core MTU to 8950 when the server NIC cannot exceed 9000. Keep switch MTU at 9216.
semantic_keywords:
  - VergeOS core fabric installer MTU 8950
  - NIC MTU cap 9000 Cisco UCS vNIC
  - jumbo frames encapsulation overhead 50 bytes
  - switch MTU 9216 core fabric
use_cases:
  - install_core_mtu_nic_capped_9000
  - cisco_ucs_vnic_core_fabric_mtu
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

Set the installer **MTU** to **8950** when the physical NIC cannot exceed 9000 (for example a Cisco UCS vNIC).

## Prerequisites

- Read [Network design](network-design.md) and [Switch configuration](switch-configuration.md).
- Set switch MTU on core fabric ports. VergeOS requires **9216** on switch ports.
- Confirm the server NIC maximum MTU.

## Default values

The installer **MTU** field default for a core fabric network is **9192**. Typical NIC MTU is 9192. Switch port MTU is >= 9216. VXLAN overlay MTU is NIC MTU minus 50 bytes.

## Set the installer value

1. Open the installer physical network settings for a core fabric NIC.
2. Set **Core-Network** to yes.
3. Set **MTU** to `8950`.
4. Repeat for each core fabric network on the node.
5. Set the same installer **MTU** on every node in the system.

{% hint style="danger" %}
Do not set the installer core MTU to 8976. Use 8950.
{% endhint %}

## Why not 8976

An installer value of 8976 was used in the field and is wrong. VergeOS encapsulation overhead is 50 bytes. From a 9000-byte NIC payload, 9000 minus 50 equals 8950.

The 9000-byte payload is for the endpoints (NICs). The switched network uses 9216 to accommodate the 9000-byte payload plus VLAN tags, headers, and overhead.

## After install

Verify fabric health. See [Core Fabric Status](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/core-fabric-status).
