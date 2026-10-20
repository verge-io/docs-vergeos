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

A virtual layer bond lets a VLAN-tagged External network fail over between two physical network paths (with optional load balancing in version 26.2 and later). This is a virtual-layer bond configured on the network itself — it is separate from the LACP bond you can define on physical interfaces at install time, and it doesn't require LACP on the switch. 


{% hint style="info" %} 
**Common Use Case - Bare-metal Installations**

Using a virtual layer bond in deployments where each node is limited to 2 NICs, e.g., bare-metal installations, allows for independent redundant core fabric paths and bonded External network paths on the same NICs as a tagged VLAN. Bonding the External network across both paths allows it to stay up if either NIC, cable, or switch fails.

{% endhint %}


## Prerequisites

- Verify the associated switch ports are configured for the VLAN tag.
- Confirm you know the password for the built-in **admin** account (user ID 1), or another administrator account with console access. If the UI becomes unreachable, you'll need it to log in at the node console and work from the command line.

{% hint style="danger" %}
**Make this change from the node console**

Changing an External network's bonding or VLAN settings can cut off remote access to the VergeOS UI. Make the change from the node's physical console or an IPMI console session, so you can revert it right away if you lose access.

If you make the change remotely, have physical console or IPMI access open and ready before you make changes.

{% endhint %}


## Configuration Steps

### Basic Network Settings

1. Create or edit the network (**Networks** > **Externals** > Click **Edit** or **New** to create one.)
2. Configure Layer 2 settings:
   - Set Layer 2 Type to vLAN
   - Enter the VLAN ID number in Layer 2 ID field

### Bonding Configuration

1. Select the **Enable Bonding** option. 
2. Under **Bond Interfaces:**  Select specific physical networks for the bond. 
3. Select **Bond Mode** (Version 26.2 and later; prior versions automatically use active-backup mode for virtual layer bonding.)
 
{% hint style="danger" %}
**Choose a bond mode carefully**

* Some bond modes only work if the physical switches are set up for them, such as a port-channel/LAG or fully separate layer 2 networks. If you pick a mode your switches don't support, traffic can drop, and you can lose the entire network, including remote access to the VergeOS UI. Before you pick any mode other than **Active Backup**, check the mode's requirements below and verify with your network administrator that the switches support it. If you're not sure, use **Active Backup**: it works with any switch setup.

* **Two-NIC bare-metal nodes:** both NICs also carry core fabric traffic, and core fabric ports can't be placed in a port-channel. Use **Active Backup**, **Balance TLB**, or **Balance ALB** only.

{% endhint %}
    
  - ***Active Backup*** (default): Only one interface is active at a time; if it fails, another interface takes over automatically. Pure redundancy; no load balancing. Most compatible option - works with any switch topology.
  - ***Balance TLB (Adaptive Transmit)***: Outgoing traffic is load balanced across all bond interfaces. Incoming traffic stays on one interface at a time (advertised MAC). Very compatible - switch only needs to handle normal MAC learning.
  - ***Balance ALB (Adaptive Load)***: Balances outbound traffic by interface load and inbound traffic by answering ARP requests with different MACs.  No switch configuration needed; works with most switches, but features like dynamic ARP inspection or port-security MAC limits can interfere.
  - ***Balance XOR***: Uses a hashing algorithm to choose which interface handles each flow. Switch must support static EtherChannel/port-channel; MLAG required across multiple switches.  Only use when switches are already configured for it.
  - ***Balance Round Robin***: Sends packets sequentially across all bond interfaces.  Requires static port-channel. Typically only appropriate for lab environments - not recommended for general VM networking.
  - ***Broadcast***: Sends every packet out every interface. Maximum redundancy/no load balancing.  Each underlying physical network must be a separate layer 2 with no connection between them; otherwise duplicate frames and MAC flapping will occur. **Almost never an appropriate option - only for very niche legacy HA environments.**

4. Select a **Primary Bond Interface** (version 26.2 and later) to specify the preferred physical network for the bond.  Set a primary if you need traffic to use a known path. 

{% hint style="info" %}
**Primary Bond Interface Selection**
- This only applies to *Active Backup*, *Balance TLB*, and *Balance ALB* modes.
- In *Active Backup* mode, selected interface carries all traffic whenever it is available. 
- When left at *--None--*, the system automatically selects a primary interface each time the external network is started. 

{% endhint %}

5. Optionally, adjust the link failure and recovery settings. The defaults work for most environments.
   - **MII link monitoring (ms)**: How often the bond checks each bond interface's link state.  Setting it to **0** turns off MII link monitoring. 
   - **Bond Up Delay (ms)**: How long a recovered link must stay up before the bond uses it again. A higher value keeps a flapping link from being put back into service too soon.
   - **Bond Down Delay (ms)**: How long to wait after a link failure before the bond stops using that link. 


  For other fields on this form, see KB article: [How to Create an External Network](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/create-external-network). 

6. Click **Submit.**  


{% hint style="warning" %}
**Restarting the network applies the bond.** If the new settings break the External network, you'll lose remote access to the VergeOS UI. Restart the network from the node console or IPMI, or have console access open and ready, so you can revert the settings right away.
{% endhint %}

7. Click **Restart** in the top banner (on the network dashboard) to apply the bond.  



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
3. Test failover/redundancy:
{% hint style="danger" %}

**Before disconnecting any cable:**

 If the bond cables also carry core fabric networks (as on two-NIC nodes), confirm both core networks are healthy before you start: the node stays in the cluster over the remaining core network while one cable is out. Test one cable at a time.
{% endhint %}

    - Physically disconnect the cable for the **primary** interface network (Active Backup), or either network (ALB/TLB)
    - In the UI, confirm the NIC shows **Down** and the network stays reachable.
    - Reconnect the cable and confirm the NIC returns to **Up**. In Active Backup, traffic moves back to the primary — expect a brief interruption.
    - Repeat for the other bond network(s).


## Troubleshooting

{% hint style="warning" %}
**Common Issues**

* **Connectivity works until failover, then drops**: VLAN not tagged on one of the interface network switch ports; verify correct VLAN configuration on all interface paths.

* **Intermittent loss/ MAC flapping alerts on switch**:  Load-balancing mode used without required port-channel; switch to *Active Backup* mode or configure the port-channel.

{% endhint %}

**If you encounter issues:**

1. Verify switch configuration matches VLAN settings
2. Check physical cable connections
3. Confirm bond interface selections are correct
4. Check the external network's logs (Diagnostics > select Query: Logs > Send.)
5. Review switch logs for error messages
6. Test connectivity from multiple points in the network

## Related Articles

- [How to Create an External Network](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/networking/create-external-network)
- [Network Diagnostics Tool](network-diagnostics.md)
