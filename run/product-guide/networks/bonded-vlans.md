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

1. Enable Bonding by selecting the checkbox
2. Under Bond Interfaces:
    - Select specific physical switches

{% hint style="info" %}
- The bonded configuration provides virtual layer network redundancy across multiple physical switches (active-backup and active-active mode options)
{% endhint %}

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
