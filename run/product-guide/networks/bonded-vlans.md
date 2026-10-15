---
title: "Bonded VLAN-tagged Networks"
description: "Create virtual layer bonded network interfaces (not LACP) with VLAN tagging on external networks for network redundancy and failover."
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

A virtual layer bond lets an External network fail over between two physical network paths (optional load balancing in version 26.2 and later).  This allows two-NIC nodes e.g., bare-metal installations, to simultaneously carry two independent redundant core fabric paths and bonded External network paths on the same NICs as a tagged VLAN. Bonding the External network across both paths means it stays up if either NIC, cable, or switch fails.

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

1. Create or edit the network (**Networks** > **Externals**. Click **Edit** or **New** to create one.)
2. Configure Layer 2 settings:
   - Set Layer 2 Type to vLAN
   - Enter the VLAN ID number in Layer 2 ID field

### Bonding Configuration

1. Select the **Enable Bonding** option. 
2. Under **Bond Interfaces:**  Select specific physical networks for the bond. 
3. Select **Bond Mode** (Version 26.2 and later; prior versions automatically use active-backup mode for virtual layer bonding.)
 
{% hint style="danger" %}
**Choose a bond mode carefully**

Some bond modes only work if the physical switches are set up for them, for example with a port-channel/LAG or a particular network layout. If you pick a mode your switches don't support, traffic can drop, and you can lose the entire network, including remote access to the VergeOS UI. Before you pick any mode other than **Active Backup**, check with your network administrator that the switches support it. If you're not sure, use **Active Backup**: it works with any switch setup.

{% endhint %}
    
  - *Active Backup*(default): Only one NIC is active at a time; if it fails, another NIC takes over automatically. Pure Redundancy; no load balancing. Most compatible option - works with any switch topology.
  - *Balance TLB (Adaptive Transmit)*: Outgoing traffic is load balanced across all switch paths. Incoming traffic stays on one NIC at a time (advertised MAC). Very compatible - switch only needs to handle normal MAC learning.
  - *Balance ALB (Adaptive Load)*: Balances outbound traffic by NIC load and inbound traffic by answering ARP requests with different NIC MACs.  No switch configuration needed; works with most switches, but features like dynamic ARP inspection or port-security MAC limits can interfere.
  - *Balance XOR*: Uses a hashing algorithm to choose which NIC handles each flow. Switch must support static EtherChannel/port-channel; MLAG required across multiple switches.  Only use when switches are already configured for it.
  - *Balance Round Robin*: Sends packets sequentially across all physical switch paths.  Requires static port-channel. Typically only appropriate for lab environments - not recommended for general VM networking.
  - *Broadcast*: Sends every packet out every NIC. Maximum redundancy/no load balancing.  Each underlying physical network must be a separate layer 2 with no connection between them; otherwise duplicate frames and MAC flapping will occur. **Almost never an appropriate option - only for very niche legacy HA environments.**

4. Select a **Primary Bond Interface** (version 26.2 and later) to specify the preferred physical network for the bond. 

{% hint style="info" %}
- Primary Bond Interface only applies to *Active Backup*, *Balance TLB*, and *Balance ALB* modes.
- In *Active Backup* mode, the primary interface carries all traffic whenever it is available. 
- When *Primary Bond Interface* selection is left at --None-- the first network in the list is automatically selected as primary. 

{% endhint %}

For other fields on this form, see KB article: [How to Create an External Network](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/create-external-network). 

5. **Submit Changes**


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

### Common Issues

#### Connectivity works until failover, then drops

* **VLAN not tagged on the backup path's switch ports**: verify correct VLAN configuration on backup path

#### Intermittent loss/ MAC flapping alerts on switch

* **Load-balancing mode used without required port-channel**: switch to Active Backup mode or configure the port-channel.


**If you encounter issues:**

1. Verify switch configuration matches VLAN settings
2. Check physical cable connections
3. Confirm bond interface selections are correct
4. Check the external network logs (Select Diagnostics on the left menu > select Query: Logs and click Send.)
5. Review switch logs for error messages
6. Test connectivity from multiple points in the network

## Related Articles

- [How to Create an External Network](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/create-external-network)
- [Network Diagnostics Tool](network-diagnostics.md)
