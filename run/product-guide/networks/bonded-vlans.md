---
title: "Bonded VLAN-tagged Networks"
description: "Create virtual layer bonded network interfaces (not LACP) with VLAN tagging on external or maintenance networks for network redundancy and failover."
semantic_keywords:
  - "bonded VLAN tagged network configuration"
  - "virtual layer NIC bonding VergeOS"
  - "network redundancy failover bond interface"
  - "VLAN bond external maintenance network"
use_cases:
  - configure_bonded_vlan_network
  - enable_nic_failover_redundancy
  - setup_active_backup_bonding
  - test_bond_failover
tags:
  - networking
  - vlan
  - bonding
  - redundancy
  - failover
  - external-network
  - high-availability
categories:
  - Networking
---

# Bonded VLAN-tagged Networks

## Overview

This guide provides instructions for creating a virtual layer bond (not LACP) on an External or Maintenance Network. For specific instructions related to bare-metal installations with 2 NICs per node, see the KB article: [Change External Network to Bonded with tagged VLAN](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/change-external-vlan-to-bonded).

## Prerequisites

{% hint style="warning" %}
**Before Making Network Changes**

- Verify associated network switch ports are configured for the VLAN tag
- Ensure you have an alternative method to reach the nodes: physical console access or IPMI access
- Confirm the name/password for the "admin" user (user ID #1)
Note: The user ID can be found in the URL of the user's dashboard (Key=1 parameter)
{% endhint %}

## Configuration Steps

### Basic Network Settings

1. Create or edit the network
2. Configure Layer 2 settings:
   - Set Layer 2 Type to vLAN
   - Enter the VLAN ID number in Layer 2 ID field

### Bonding Configuration

1. Select the **Enable Bonding** option. 
{% hint style="info" %}
- The bonded configuration provides virtual layer network redundancy across multiple physical networks 
{% endhint %}
2. Under **Bond Interfaces:**
    - Select specific physical networks for the bond.
3. Select **Bond Mode**
{% hint style="warning"}
    Some modes require configuration on the switching hardware to support specific link‑level behaviors.  
    {% endhint %}
    - *Active Backup*(default): Only one NIC is active at a time. If it fails, another NIC takes over automatically. Pure Redundancy; no load balancing. Most compatible option - works with any switch.
    - *Balance ALB (Adaptive Load)*: Load balances outgoing traffic automatically based on NIC load. Incoming traffic is balanced using ARP negotiation. Maximum throughput, but requires the switch to tolerate ARP manipulation. Very compatible with most switch configurations.
    - *Balance Round Robin*: Sends packets sequentially across all physical switch paths. Typically only appropriate for lab environments - not recommended for general VM networking.
    - *Balance TLB (Adaptive Transmit)*: Outgoing traffic is load balanced across all switch paths. Incoming traffic stays on one NIC at a time (advertised MAC). Very compatible - switch only needs to handle normal MAC learning
    - *Balance XOR*: Uses a hashing algorithm to choose which NIC handles each flow. Switch must support static EtherChannel/port-channel.  Predictable load distribution
    - *Broadcast*: Sends every packet out every NIC. Maximum redundancy/no load balancing. Almost never an appropriate option - only for very niche legacy HA environments.

4. Select a **Primary Bond Interface** to specify the preferred physical network for the bond. In *Active Backup* mode, the primary interface carries all traffic whenever it is available. 

{% hint style="info" %}
When *Primary Bond Interface* selection is left at --None-- a network is automatically selected based on registration order. 

{% endhint %}

5. **Configure Additional Network Settings**

See KB article: [How to Create an External Network](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/create-external-network) for information on other external network configuration options.

6. **Submit Changes**


## Testing and Verification

### Basic Connectivity Test

1. Verify the network has connectivity using the [Network Diagnostics Tool](network-diagnostics.md)
2. Common diagnostic tests include:
    - Ping test to verify basic connectivity
    - DNS lookup to verify name resolution
    - TCP connection test to verify specific port connectivity

### Bond Failover Testing

1. Navigate to the modified network dashboard
2. Select NICs to view the network adapters
3. Test failover:
    - Physically disconnect one of the associated network cables
    - UI should indicate the disconnected NIC is in "Down" status
    - Verify network maintains connectivity through the backup NIC

{% hint style="warning" %}
**Important**

Before disconnecting any network cable, verify:

- It is not a core network cable OR
- Proper core network redundancy is in place
{% endhint %}

## Troubleshooting

If you encounter issues:

1. Verify switch configuration matches VLAN settings
2. Check physical cable connections
3. Confirm bond interface selections are correct
4. Review network logs for error messages
5. Test connectivity from multiple points in the network

## Related Articles

- [How to Create an External Network](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/create-external-network)
- [Change External Network to Bonded with tagged VLAN](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/change-external-vlan-to-bonded)
- [Network Diagnostics Tool](network-diagnostics.md)
