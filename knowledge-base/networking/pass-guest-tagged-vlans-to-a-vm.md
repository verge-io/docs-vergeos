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

