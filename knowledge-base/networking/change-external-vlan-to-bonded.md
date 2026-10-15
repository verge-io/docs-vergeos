---
title: Change External Network to Bonded with Tagged VLAN
slug: change-external-vlan-to-bonded
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

# Change External Network to Bonded with Tagged VLAN

On a bare-metal node with only two NICs, each NIC carries its own core fabric network. Because both NICs are in use by the core fabric, the External network runs on those same NICs as a tagged VLAN. Bonding that VLAN across both physical networks keeps the External network, including remote access to the VergeOS UI, available if either NIC, cable, or switch fails.

## When to use this configuration

Use a bonded, VLAN-tagged External network when:

- Each node has exactly two NICs.
- Both NICs are dedicated to core fabric networks.
- The External network needs redundancy across both physical paths.

## Configure the bond

{% hint style="warning" %}
Changing the External network can interrupt remote access to the VergeOS UI. Before you start, make sure you have local console or IPMI access to the nodes.
{% endhint %}

For the full procedure, including bond mode selection, failover testing, and troubleshooting, see [Bonded VLAN-tagged Networks](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/bonded-vlans).



## Related articles

- [Bonded VLAN-tagged Networks](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/bonded-vlans)
- [Network Design Models](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/network-design)
