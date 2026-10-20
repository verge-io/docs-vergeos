---
title: Create Bonded External Network on a Bare-metal system
slug: bond-external-vlan-bare-metal
description: On bare-metal nodes with only two NICs, bond the External network's VLAN across both physical networks for failover.
author: VergeOS Documentation Team
date: 2026-10-14T12:00:00.000Z
semantic_keywords:
  - "bond external network vlan physical networks"
  - "virtual layer bond redundancy two nics"
  - "change external network bonded vlan configuration"
  - "network bonding failover bare-metal"
use_cases:
  - configure_bonded_external_network
  - enable_vlan_bonding_redundancy
  - ui_redundancy_bare-metal
tags:
  - bonded
  - network
  - bonding
  - redundant
  - external
  - bond
categories:
  - Network
  - Network Configuration
editor: markdown
dateCreated: 2024-11-24T18:38:59.908Z
---

# Create Bonded External Network on a Bare-metal System

On a bare-metal node with only two NICs, each NIC carries its own core fabric network. Because both NICs are in use by the core fabric, the External network runs on those same NICs as a tagged VLAN. Bonding that VLAN across both physical networks keeps the External network, including remote access to the VergeOS UI, available if either NIC, cable, or switch fails.

## When to use this configuration

Use a bonded, VLAN-tagged External network when:

- Each node has exactly two NICs.
- Both NICs already carry core fabric networks.
- The External network needs redundancy across both physical paths.

## Before you start

{% hint style="warning" %}
- Changing the External network can interrupt remote access to the VergeOS UI. Make this change from the node console or IPMI so you can revert it if you lose external UI access. 

- If the External network is currently untagged, the **VLAN must be added to the ports on both core switches** before the network's Layer 2 settings are changed.

{% endhint %}

For the full procedure, including bond mode selection, failover testing, and troubleshooting, see [Bonded VLAN-tagged Networks](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/bonded-vlans).

## Related articles

- [Network Design Models](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/network-design)
- [Bonded VLAN-tagged Networks](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/bonded-vlans)
