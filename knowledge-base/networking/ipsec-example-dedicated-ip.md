---
title: IPsec Example - Dedicated Public IP
slug: ipsec-example-dedicated-ip
author: VergeOS Documentation Team
date: 2025-04-04T15:19:47.449Z
semantic_keywords:
  - ipsec tunnel dedicated public ip bridged network
  - vpn network configuration phase 1 phase 2
  - translate route rules vpn internal network
  - static lease vpn router bridged internal
use_cases:
  - configure_ipsec_with_dedicated_public_ip
  - bridge_vpn_to_internal_network
  - create_vpn_translate_and_route_rules
  - assign_public_ip_to_vpn_network
categories:
  - VPN
editor: markdown
dateCreated: 2025-01-31T14:48:12.332Z
description: >-
  IPsec tunnel configuration example using a dedicated public IP address with a
  bridged internal network for workload connectivity.
tags:
  - vpn
  - networking
---

# IPsec Example - Dedicated Public IP

The following IPsec example utilizes a dedicated public IP address for a VPN tunnel. The VPN router is bridged to an existing internal network to provide Layer 2-connectivity to that network.

{% hint style="info" %}
**IPsec is a complex framework that supports a vast array of configuration combinations with many ways to achieve the same goal, making it impossible to provide one-size-fits-all instructions. Sample configurations are given for reference and should be tailored to meet the particular environment and requirements.**
{% endhint %}

{% hint style="info" %}
**Consult the** [**IPsec Product Guide Page**](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/vpn/ipsec) **for step-by-step general instructions on creating an IPsec tunnel.**
{% endhint %}

* **VPN Network Name:** _vpn-ipsec_
* **VPN Router address:** _192.168.0.254_
* **Local VPN network:** _192.168.0.0/24_
* **Remote VPN network:** _10.10.0.0/16_
* **Bridged Internal Network Name:** _Internal-xyz_
* **External Network Name:** _External_

## Static Lease

We navigate to _**Internal-xyz** > IP Addresses > New_\* to reserve a static address for the VPN router on this internal network in order avoiding another entity from taking the same IP address. Full instructions for creating a static lease can be found here: [Create a DHCP Static Lease](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/dhcp-static-lease).

![VPN Static Lease](../.gitbook/assets/ipsec-dedicated-bridged-staticlease.png)

## VPN Network Configuration

![VPN Network Config](../.gitbook/assets/ipsec-dedicated-bridged-vpn-network.png)

## Phase 1

![Phase 1 Configuration](../.gitbook/assets/ipsec-dedicated-bridged-phase1.png)

## Phase 2

![Phase 2 Configuration](../.gitbook/assets/ipsec-dedicated-bridged-phase2.png)

## Assigned Public IP Address

The public address must be [Assigned from the External network](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/assign-external-ip) to the VPN network.

![Assign Public IP](../.gitbook/assets/ipsec-dedicated-bridged-provide-public.png)

## Default VPN Network Rules

**Default Firewall Rules** - The following necessary firewall rules are **created automatically** when a VPN network is created:

* **Allow IKE**: Accept incoming UDP traffic on port 500 to **My Router IP**
* **Allow IPsec NAT-Traversal**: Accept incoming UDP traffic on port 4500 to **My Router IP**
* **Allow ESP**: Accept incoming ESP protocol traffic to **My Router IP**
* **Allow AH**: Accept incoming AH protocol traffic to **My Router IP**

![Review Rules](../.gitbook/assets/ipsec-defaultrules.png)

{% hint style="success" %}
**These rules can be modified to restrict to specific source addresses, where appropriate.**
{% endhint %}

## Additional VPN Network Rules

Additional rules need to be created on our new VPN network:

**Translate Rule:** ![VPN Translate to Router](../.gitbook/assets/ipsec-dedicated-bridged-vpn-translate.png)

{% hint style="info" %}
**The translate rule must be moved to the top of the rules list, before the&#x20;**_**Accept**_**&#x20;Rules. Instructions for changing the order of rules can be found in the Product Guide:** [**Network Rules - Change the Order of Rules**](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/network-rules#change-the-order-of-rules)
{% endhint %}

**Default Route Rule:** ![VPN Default Route Rule](../.gitbook/assets/ipsec-dedicated-bridged-vpn-defroute.png)

## Internal Network Rule

A routing rule is needed on _Internal-xyz_ to route its VPN traffic to the VPN network.

![VPN Default Route Rule](../.gitbook/assets/ipsec-dedicated-bridged-internal-route.png)

{% hint style="success" %}
**New rules must be applied on each network to put them into effect.**
{% endhint %}
