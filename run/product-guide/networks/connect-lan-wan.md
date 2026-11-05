---
title: "Connect VergeOS to an Existing LAN/WAN"
description: "Create and configure external networks to connect VergeOS to existing LAN, WAN, or other physical network infrastructure with full Layer 2 and Layer 3 options."
semantic_keywords:
  - "connect VergeOS to existing LAN WAN network"
  - "create external network physical connection"
  - "external network VLAN DHCP configuration"
  - "integrate VergeOS with corporate network infrastructure"
use_cases:
  - create_external_network
  - connect_to_existing_lan
  - configure_wan_connectivity
  - setup_vlan_external_network
  - integrate_with_physical_infrastructure
tags:
  - networking
  - external-network
  - lan
  - wan
  - vlan
  - dhcp
  - routing
  - configuration
categories:
  - Networking
---

# Connect VergeOS to an Existing LAN/WAN

## How to Connect to an Existing Network

Connecting to a network that exists outside your VergeOS environment, such as an existing company LAN, or a WAN connection, requires a VergeOS external network. Typically, one external network is created during the VergeOS system install and mapped to a physical network that is also defined during installation. Multiple externals can be created to take advantage of multiple available physicals. More than one external network can be mapped to the same physical network, with each utilizing a different VLAN. The following instructions walk through creating an external network after install, from the VergeOS UI. Additionally, an external network created during installation can be modified using the settings information provided.

## Create a New External Network

1. From the Cloud Dashboard, select **Networks** from the left menu.
2. Select **New External** from the left menu.
3. Enter a **Name** for the network (required). The name should be something helpful for future administration. Note: spaces are not permitted.
4. Optionally, a **Description** can be entered for the network.
5. Optionally, a **HA Group** can be defined for the network. HA Groups define two or more networks to provide high availability. When multiple networks are assigned to the same HA Group, the system attempts to run the networks across different physical nodes to increase availability.
6. Select the appropriate **Layer 2 Type**:
    - ***vLan*** (VLAN id specified in Layer 2 ID field)
    - ***Bond*** - supports switch ports configured for lag group-active/main physical device
    - ***Bond Slave*** - supports switches configured for lag group-secondary device
    - ***none*** - simple direct connect (also passes guest-tagged 802.1Q VLANs to VMs; see [Pass Guest-Tagged VLANs to a VM](#pass-guest-tagged-vlans-to-a-vm))
    - ***vxLan*** (VXLAN id specified in Layer 2 ID field)
7. Enter a **Layer 2 ID**, if applicable (VLAN/VXLAN)
8. Enter the appropriate **MTU size** for the existing network.
9. Optionally, a specific **Cluster** can be selected to specify the primary cluster where this VNet will run.
10. Optionally, a specific **Failover Cluster** can be selected to specify a cluster on which to run if the primary is not available.
11. Optionally, a **Preferred node** can be selected to specify a particular node as a "first-choice" on which to run the VNet.
12. Optionally, this network can be set to allow **PXE** boot for VergeOS nodes (by default PXE is not enabled.)
13. Select the appropriate **Interface Network** from the dropdown list of physical and external networks. Typically, a physical network would be selected here; selecting an external (rather than a physical) would be for Q-in-Q (VLAN inside VLAN).
14. Select the appropriate **IP Address Type**:
    - ***Static*** - to specify a particular address for the network
    - ***Dynamic*** - to configure the network as a DHCP client (This is only used in small test or archive systems as it will limit the network to a single address.)
    - ***BGP/OSPF***
    - ***None*** - Layer 2 network connection
15. Enter **IP Address** (Does not apply if Type Dynamic is selected.)
16. Enter **Network Address** (in CIDR format) for the network, ex: 192.168.2.0/24
17. Specify a **DNS server list**; each entry separated by a comma. (ex: 10.10.25.3, 10.10.25.4)
18. Select a **DNS** Setting:
    - ***Disabled*** - no DNS management provided
    - ***Bind*** - for networks that will act as an authoritative DNS
    - ***Simple*** - DNS provided for the network without holding actual DNS records
19. Optionally, check the **DHCP** checkbox to run a DHCP server for the network's clients:
    - ***Domain Name*** for this network (optional)
    - ***Gateway***
    - ***Hostname*** (for this VNet's router)
    - ***Dynamic DHCP*** option (checkbox) - when selected, DHCP start/stop addresses can be entered to specify the scope for dynamic allocation. Additionally, DHCP sequential Addresses option (checkbox) can be selected to allocate addresses in a consecutive manner.
20. Select action to be taken when power is restored to the network **On Power Loss** (This would be after a physical node power loss or for a tenant: after the tenant is powered off/on.)
    - ***Last State*** - network will only be powered on if it was on at the time of power loss
    - ***Leave Off*** - network will not be powered on when power is restored (regardless of its state at the time of power loss)
    - ***Power On*** - network will be powered on when power is restored (regardless of its state at the time of power loss)
21. Optionally, the following options (checkboxes) can be selected:
    - **Track Statistics** for All Rules to automatically turn on tracking for all rules applied to this network.
    - **Track DMZ Statistics** to track total packets/bytes from this network through the DMZ network.
    - **Enable Rate Limiting on Routing** to define limits on this overall network. (Example usage: consumption-based billing, etc.)
    - **Rate Limit** overall throttle on network traffic
    - **Rate Type** (ex: Packets per second, Megabytes per day, Bytes per Hour, etc.)
    - **Rate Limit Burst** - allow this burst rate as long as the rate limit is staying within the averages defined.
22. Click **Submit** to finish creation of the new network.
23. The dashboard for the new network appears. Click **Power on** from the left menu to start the network.

## Pass Guest-Tagged VLANs to a VM

An external network with **Layer 2 Type** ***none*** can carry a VLAN trunk into a VM. The guest OS creates its own VLAN interfaces and tags its own traffic, and the network passes 802.1Q-tagged frames in both directions with the tags intact: from the physical switch to the VM, from the VM to the physical switch, and between VMs on the same network.

Physical bridge mode (**Physical Bridged**) is not required.

1. Confirm the physical switch port is a trunk that allows every VLAN ID the guest needs.
2. Create a new external network as described above, with these settings:
    - **Layer 2 Type**: ***none***
    - **Interface Network**: the physical network that carries the trunk
    - **IP Address Type**: ***None***
    - **DHCP**: unchecked
3. Power on the network.
4. Attach the VM's NIC to the new network.
5. Inside the guest OS, create a VLAN interface for each VLAN ID the guest uses (for example, on Linux: `ip link add link eth0 name eth0.210 type vlan id 210`).

{% hint style="warning" %}
**VLAN IDs already defined as vLan networks are not passed through**

If a VLAN ID is also defined as its own ***vLan*** external network on the same physical network, that vLan network receives the frames for that ID from the physical switch, and they never reach the ***none*** network. Any VLAN ID the guest needs from the physical network must not also exist as a ***vLan*** external network on that physical network.
{% endhint %}

{% hint style="danger" %}
**Every unclaimed VLAN on the trunk reaches the VM**

The ***none*** network passes every VLAN on the switch trunk that is not claimed by a ***vLan*** network on that physical network. This can include VLANs that VergeOS uses for other networks. Before using this setup, limit the VLANs allowed on the switch port to the ones the guest needs, and consider the security and broadcast-traffic impact on the VM.
{% endhint %}

To check that tags arrive intact, run a [TCP Dump](../system/node-diagnostics.md#tcp-dump) from **Node Diagnostics** on the node running the VM, select the VM's TAP device or the network's bridge, and check **Show Link-Level Header (VLAN, MAC)**.

