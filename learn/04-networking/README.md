---
description: "Configure external and internal networks, VLANs, firewall rules, and dynamic routing in VergeOS."
---

# Module 4: Networking

## Learning Objectives

By the end of this module, you will be able to:

- **Configure external and internal networks** in VergeOS for production workloads
- **Set up VLANs and firewall rules** to segment and secure network traffic
- **Configure dynamic routing** (BGP/OSPF) for enterprise environments
- **Troubleshoot common networking issues** using VergeOS diagnostic tools

## Prerequisites

- Completion of [Module 1: Architecture Fundamentals](../01-architecture/README.md) -- understanding of core fabric networking
- Completion of [Module 3: Installation](../03-installation/README.md) -- a running VergeOS cluster to configure

## Estimated Time

**3 hours** (1.5 hours reading + 1.5 hours lab)

## Topics

* [**Network Concepts & Types**](01-network-concepts.md) — The VergeOS networking model: network types (internal, external, core, DMZ, maintenance), default-secure isolation, and software-defined networking fundamentals.
* [**External Networks**](02-external-networks.md) — Connecting VergeOS to upstream physical networks, IP addressing, gateway configuration, bonding modes, and provider network integration.
* [**Internal Networks & DHCP/DNS**](03-internal-networks.md) — Creating isolated virtual networks for workloads, built-in DHCP and DNS services, inter-network routing via DMZ, and tenant self-service networking.
* [**Firewall Rules, NAT & VLANs**](04-firewall-nat-vlans.md) — Rule types (accept/drop/reject, NAT/PAT translate), rule processing order, VLAN trunking, VPN overview (WireGuard/IPsec), and micro-segmentation.
* [**Lab: Network Configuration**](lab.md) — Build a multi-network environment with external access, internal segmentation, and firewall rules.
