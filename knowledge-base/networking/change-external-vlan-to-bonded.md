---
title: Change External Network to VLAN Bonded
slug: change-external-vlan-to-bonded
description: Instructions to change an existing external network to a VLAN bonded configuration across physical networks for redundancy and/or load balancing.
author: VergeOS Documentation Team
date: 2024-11-24T18:38:59.908Z
semantic_keywords:
  - "bond external network vlan physical networks"
  - "software-based bond redundancy two nics"
  - "change external network bonded vlan configuration"
  - "network bonding failover bare-metal"
use_cases:
  - configure_bonded_external_network
  - enable_vlan_bonding_redundancy
  - test_bond_failover
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

## Overview

{% hint style="info" %}
**Key Points**

- This procedure creates a software-based bond across vlanned physical networks.
- It is recommended for bare-metal installations with a limitation of 2 NICs per node.
- System downtime is not required to make this change.
{% endhint %}

This guide outlines the process to create a bonded external network across vlanned physical networks.  The outlined method provides optimal redundancy for bare-metal installations that are limited to two NICs per node, allowing for two independent core-fabric networks and a single-VLAN, bonded external network.

## Prerequisites

{% hint style="warning" %}
**Warning**
    - This process should be performed with local server access because external network changes can affect remote UI access. This will also allow you to test the bond configuration by removing one of the network cables to verify expected bond failover.
    - Before making any significant system changes confirm you have the name/password for the "admin" user (user ID #1), in case command-line operations become needed.
    (Hint: "Key=1" parameter is in the URL of the user's dashboard.)
    
{% endhint %}

## Steps

1. Navigate to the **External Network dashboard** 
    - Networks > Dashboard > Externals
    - Double-click External Network
    - Click **Edit** on the left menu 
2. Verify **Layer 2 Type**: ***vLAN*** and appropriate **Layer 2 ID** (VLAN number).
3. **Select** the option to **Enable Bonding**.
3. **Select** the **Physical Networks** you want to participate in the bonding.
4. **Select** desired **Bond Mode**:
    {% hint style="warning"}
    Some modes require switch support
    {% endhint %}
    - *Active Backup*: Only one NIC is active at a time. If it fails, another NIC takes over automatically. Pure Redundancy; no load balancing. Most compatible option - works with any switch.
    - *Balance ALB (Adaptive Load)*: Load balances outgoing traffic automatically based on NIC load. Incoming traffic stays on one NIC (advertised MAC).
    - *Balance Round Robin*: sends packets sequentially across all physical switch paths. Typically only appropriate for lab environments - not recommended for general VM networking.
    - *Balance TLB (Adaptive Transmit)*
    - *Balance XOR*: Uses a hashing algorithm to choose which NIC handles each flow. Switch must support static EtherChannel/port-channel.  Predictable load distribution
    - *Broadcast*: Sends every packet out every NIC. Maximum redundancy/no load balancing. Almost never an appropriate option - only for very niche legacy HA environment
5. Click **Submit** to save the change.
  
## Post Configuration

1. Check the external network by accessing the UI from a remote connection.
2. Test Bond failover: Navigate to the external network dashboard and select **NICs** to view the network adapters. Physically disconnect one network cable. The UI should now indicate the NIC is in a "Down" status; verify remote UI access is still available.  
{% hint style="warning" %}
**Verify core network redundancy is in place before disconnecting network cables.**


{% endhint %}

## Troubleshooting

{% hint style="warning" %}
**Common Issues**

- Problem: Loss of remote access
  - Solution:
    1. Check correct VLAN was entered in the external network config
    2. Verify network switch ports are correctly configured for the VLAN tag.
{% endhint %}

## Additional Resources

- [Network Design Models](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/network-design)

---
