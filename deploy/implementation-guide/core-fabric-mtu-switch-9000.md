---
title: Core fabric MTU when the switch port cannot exceed 9000
description: Set the installer MTU to 8950 when the core fabric switch port cannot exceed 9000. Do not leave 9192.
semantic_keywords:
  - VergeOS core fabric installer MTU 8950
  - switch port MTU cap 9000
  - jumbo frames encapsulation overhead 50 bytes
  - core NIC MTU 8950
use_cases:
  - install_core_mtu_switch_capped_9000
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

# Core fabric MTU when the switch port cannot exceed 9000

When the core fabric switch port cannot exceed 9000, set the installer **MTU** to **8950**. Do not leave 9192.

## Prerequisites

- Read [Network design](network-design.md) and [Switch configuration](switch-configuration.md).
- Confirm the switch port maximum MTU.

## Set the installer value

1. Open the installer physical network settings for a core fabric NIC.
2. Set **Core-Network** to yes.
3. Set **MTU** to `8950`.
4. Repeat for each core fabric network on the node.
5. Set the same installer **MTU** on every node in the system.

Do not subtract 50 again. Type **8950** once.

{% hint style="danger" %}
Do not enter 8976. 8976 is 9000 minus 24. Encapsulation overhead is 50. 9000 minus 50 equals 8950. Use 8950 so the frame fits a 9000-capped switch port.
{% endhint %}

## After install

Verify fabric health. See [Core Fabric Status](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/core-fabric-status).
