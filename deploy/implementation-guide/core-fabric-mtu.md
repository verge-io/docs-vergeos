---
title: Core fabric MTU when the NIC cannot exceed 9000
description: Set the installer core MTU to 8950 when the server NIC cannot exceed 9000. Keep switch MTU at 9216 when the switch allows it.
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

Set the installer **MTU** for each core fabric network to **8950** when the physical NIC cannot exceed 9000. Keep switch port MTU at **9216** when the switch allows it.

## Audience

Administrators who install VergeOS on hosts whose NIC MTU cannot exceed 9000 (for example a Cisco UCS vNIC).

## Prerequisites

- Read [Network design](network-design.md) and [Switch configuration](switch-configuration.md).
- Set switch MTU on core fabric ports. Use **9216** when the switch allows it.
- Confirm the server NIC maximum MTU. If the NIC cannot exceed 9000, use this page.

## Default vs this special case

The installer **MTU** field default for a core fabric network is **9192**. Typical NIC MTU is 9192. Switch port MTU is >= 9216. VXLAN overlay MTU is NIC MTU minus 50 bytes.

Use this page only when the physical NIC cannot exceed 9000.

## Set the installer value

1. Open the installer physical network settings for a core fabric NIC.
2. Set **Core-Network** to yes.
3. Set **MTU** to `8950`.
4. Repeat for each core fabric network on the node.

{% hint style="danger" %}
Do not set the installer core MTU to 8976. Use 8950.
{% endhint %}

Subtract 50 bytes for encapsulation from the 9000-byte NIC payload. 9000 minus 50 equals 8950.

The 9000-byte payload is for the endpoints (NICs). The switched network can still use 9216 for frame-header padding when the switch allows it.

## After install

Verify fabric health. See [Core Fabric Status](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/core-fabric-status).

## Related

- [Installation guide](installation-guide.md)
- [Network design](network-design.md)
- [Switch configuration](switch-configuration.md)
