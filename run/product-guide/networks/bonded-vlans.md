---
title: "Bonded VLAN-tagged Networks"
description: "Configure bonded VLAN-tagged network interfaces with multiple bond modes for redundancy and failover. Covers mode selection, timer settings, and avoiding bond conflicts."
semantic_keywords:
  - "bonded VLAN tagged network configuration"
  - "NIC bonding modes VergeOS"
  - "network redundancy failover bond interface"
  - "VLAN bond external maintenance network"
  - "bond mode timer configuration"
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

This guide provides instructions for creating a bonded VLAN-tagged network on an External or Maintenance Network. Network-level bonding combines multiple standalone physical network interfaces into a single redundant connection. Bond modes include Active Backup, Balance ALB, Balance TLB, Balance XOR, Balance Round Robin, and Broadcast. For specific instructions related to bare-metal installations with 2 NICs per node, see the KB article: [Change External Network to Bonded with tagged VLAN](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/change-external-vlan-to-bonded).

## When to Use Network-Level VLAN Bonding

Use network-level bonding when the selected physical networks are standalone NICs. Examples include selecting two separate physical networks such as `external-1 Switch` and `external-2 Switch`, or the two core fabric NICs on 2-NIC nodes.

Do NOT use network-level bonding when the selected physical network is already an install-time bond. When the physical network is an install-time bond, select the bond as the **Interface Network** and leave **Enable Bonding** off.

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

{% hint style="warning" %}
**Do Not Select Install-Time Bond Members**

When the physical network is an install-time active-backup bond, do NOT select individual bond members as Bond Interfaces. Selecting both the bond and a bond member creates a second bond on top of the first. On primary-side failure, the install-time bond fails over to the backup member, but the VLAN bond does not. Inbound tagged frames arrive on the backup member and are dropped because they reach the bare NIC copy, not the bond. Outbound traffic continues to work, but inbound traffic fails.

Do not select **All** on systems with install-time bonds.
{% endhint %}

1. Enable Bonding by selecting the checkbox
2. Under **Bond Interfaces**:
    - Select specific physical networks (for example, `core-fabric-1 Switch`, `core-fabric-2 Switch`) OR
    - Select specific interfaces if the physical networks are standalone NICs
    - Do NOT select **All** if any physical network is an install-time bond
3. Select **Bond Mode** from the dropdown:

| Bond Mode             | Description                                                                                                  | Switch Configuration Required            |
| --------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| Active Backup         | One NIC remains active while others stand ready as backup. Recommended default.                               | None                                     |
| Balance ALB           | Adaptive load balancing distributes outbound traffic across NICs and balances inbound traffic by MAC address. | None                                     |
| Balance TLB           | Transmit load balancing distributes outbound traffic across NICs. Inbound traffic uses one NIC.               | None                                     |
| Balance XOR           | Distributes traffic based on source and destination MAC XOR. Requires static LAG configuration.               | Static LAG (port-channel, trunk group)   |
| Balance Round Robin   | Distributes traffic evenly across all NICs in sequence. Requires static LAG configuration.                    | Static LAG (port-channel, trunk group)   |
| Broadcast             | Transmits all traffic on all NICs.                                                                            | None                                     |

4. Configure **MII Link Monitoring** (milliseconds):
    - Interval for checking NIC link status
    - Recommended value: `100`
    - Setting this to `0` disables failover detection
5. Configure **Bond Up Delay** (milliseconds):
    - Time to wait before activating a link after it comes up
    - Recommended value: `200`
6. Configure **Bond Down Delay** (milliseconds):
    - Time to wait before deactivating a link after it goes down
    - Recommended value: `200`

{% hint style="info" %}
- Selecting specific interfaces provides more control over which NICs are bonded
- Active Backup is recommended for most deployments
- Balance Round Robin and Balance XOR require switch-side static LAG configuration
- Switch ports for VLAN-bond members must be independent trunk ports, not a port-channel
{% endhint %}

### LACP Clarification

The network configuration UI states that 802.3ad/LACP is not supported for VLAN bonds. LACP applies to install-time bonds configured with a switch-side LAG (Link Aggregation Group), not to the network-level **Enable Bonding** option. When configuring network-level VLAN bonding, switch ports for bond members must be independent trunk ports, not a port-channel.

### Additional Network Settings

See KB article: [How to Create an External Network](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/create-external-network) for information on configuring other external network options.

## Testing and Verification

### Basic Connectivity Test

1. Verify the network has connectivity using the [Network Diagnostics Tool](network-diagnostics.md)
2. Common diagnostic tests include:
    - Ping test to verify basic connectivity
    - DNS lookup to verify name resolution
    - TCP connection test to verify specific port connectivity

### Bond Failover Testing

{% hint style="warning" %}
**Important**

Before disconnecting any network cable, verify:

- It is not a core network cable OR
- Proper core network redundancy is in place
{% endhint %}

1. Navigate to the modified network dashboard
2. Select NICs to view the network adapters
3. Establish inbound and outbound traffic before testing:
    - Verify outbound connectivity using the [Network Diagnostics Tool](network-diagnostics.md)
    - Verify inbound traffic by pinging into the network from an external host
4. Test failover:
    - Physically disconnect one of the associated network cables
    - UI should indicate the disconnected NIC is in **Down** status
    - Verify outbound network connectivity is maintained through the backup NIC
    - Verify inbound traffic is maintained by pinging into the network from an external host while the primary link is down
5. Reconnect the cable and verify the NIC returns to normal operation

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