---
title: Pass Guest-Tagged VLANs to a VM
slug: pass-guest-tagged-vlans-to-a-vm
description: Use an external network with Layer 2 Type none to pass an 802.1Q VLAN trunk into a VM so the guest OS can tag its own traffic.
author: VergeOS Documentation Team
date: 2026-11-11
semantic_keywords:
  - "pass vlan trunk to vm guest tagging"
  - "802.1q guest-tagged vlans external network layer 2 type none"
  - "vm creates its own vlan interfaces tagged frames"
  - "vlan trunk to virtual machine without physical bridged"
  - "virtual guest tagging vgt vlan"
use_cases:
  - pass_vlan_trunk_to_vm
  - configure_guest_vlan_tagging
  - verify_vlan_tags_with_tcpdump
tags:
  - networking
  - vlan
  - trunk
  - 802.1q
  - guest-tagging
  - external
  - vm
categories:
  - Networking
editor: markdown
dateCreated: 2026-11-11
---

# Pass Guest-Tagged VLANs to a VM

An external network with **Layer 2 Type** ***none*** can carry a VLAN trunk into a VM. The guest OS creates its own VLAN interfaces and tags its own traffic, and the network passes 802.1Q-tagged frames in both directions with the tags intact: from the physical switch to the VM, from the VM to the physical switch, and between VMs on the same network.

## When to Use Guest Tagging

{% hint style="info" %}
**Most VMs do not need this**

For most VMs, let VergeOS manage VLANs: create a ***vLan*** external network for each VLAN, as described in [How to Create an External Network](create-external-network.md), and attach a VM NIC to each one.
{% endhint %}

**VergeOS-managed VLANs are the better choice in most cases:**

- **Isolation**: Each VM receives only the VLANs its NICs are attached to. A ***none*** network delivers every unclaimed VLAN on the trunk to the VM.
- **Visibility**: Each VLAN is its own network in VergeOS, with its own rules and statistics. VLANs tagged inside a guest are not visible to VergeOS.
- **Simpler guests**: The guest OS needs no VLAN configuration, so there is nothing VLAN-related to set up again if the VM is rebuilt.
- **Less broadcast traffic**: The VM does not receive broadcasts from VLANs it does not use.

Use guest tagging only when the guest itself needs to handle VLANs, for example:

- A virtual router or firewall, such as pfSense, OPNsense, or VyOS, that routes between VLANs on a single interface. See also [Best Practices - Running a pfSense Virtual Firewall](running-a-pfsense-virtual-firewall.md).
- A nested hypervisor that tags traffic for its own VMs.
- A network appliance, such as an IDS/IPS sensor, that expects a trunk port.
- A VM that needs more VLANs than is practical to provide with one NIC per VLAN.
- A VM migrated from VMware that used Virtual Guest Tagging (VGT, VLAN 4095) and is not being reconfigured.

## Set Up the External Network

{% hint style="info" %}

Physical bridge mode (**Physical Bridged**) is not required on the physical network.

{% endhint %}

{% hint style="danger" %}
**Untagged traffic and every unclaimed VLAN reach the VM**

The ***none*** network carries all untagged traffic on the physical network, plus every VLAN that is not claimed by another network on that same physical network. Before using this setup, limit the VLANs allowed on the switch port to the ones the guest needs, and consider the security and broadcast-traffic impact on the VM.
{% endhint %}

1. Confirm the physical switch port is a trunk that allows every VLAN ID the guest needs, and only those VLAN IDs.
2. In **Networks**, look for any network (typically an external network) whose **Interface Network** is the same physical network and whose **Layer 2 Type** is ***vLan***. If any has a **Layer 2 ID** that matches a VLAN ID the guest needs, move that network to a different VLAN ID or have the guest use another one.

    {% hint style="warning" %}
    **VLAN IDs already defined as vLan networks are not passed through**

    If a VLAN ID is also defined as its own ***vLan*** network on the same physical network, that network receives the frames for that ID from the physical switch, and they never reach the ***none*** network.
    {% endhint %}

3. Create a new external network as described in [Create a New External Network](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/connect-lan-wan#create-a-new-external-network), with these settings:
    - **Layer 2 Type**: ***none***
    - **Interface Network**: the physical network that carries the trunk
    - **IP Address Type**: ***None***
    - **DHCP**: unchecked
4. Power on the network.
5. Attach the VM's NIC to the new network.
6. Inside the guest OS, create a VLAN interface for each VLAN ID the guest uses (for example, on Linux: `ip link add link eth0 name eth0.210 type vlan id 210`).

## Verify the Tags

To check that tags arrive intact, run a [TCP Dump](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/node-diagnostics#tcp-dump) from **Node Diagnostics** on the node running the VM, select the VM's TAP device or the network's bridge, and check **Show Link-Level Header (VLAN, MAC)**.
