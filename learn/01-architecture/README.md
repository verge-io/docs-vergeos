---
description: "Understand the VergeOS platform architecture, deployment models, storage, networking, and cluster concepts."
---

# Module 1: Architecture Fundamentals

## Learning Objectives

By the end of this module, you will be able to:

- **Describe what VergeOS is** and how its unified operating system approach differs from traditional 3-tier infrastructure and other HCI platforms
- **Compare HCI and UCI deployment models** and recommend the right topology for a given use case
- **Explain VergeFS (vSAN) storage** including tier architecture, data distribution, and redundancy mechanisms
- **Describe the core fabric network** and how inter-node communication, vSAN replication, and VM live migration traffic flow
- **Identify VergeOS node types and cluster concepts** including controller nodes, scale-out nodes, compute-only, and storage-only roles

## Prerequisites

None -- this is the first module in the training program. No prior VergeOS experience is required.

## Estimated Time

**2 hours** (1.5 hours reading + 0.5 hours lab)

## Topics

* [**What is VergeOS?**](01-vergeos-overview.md) — The unified ultraconverged operating system: VergeHV (compute), VergeFS (storage), and VergeFabric (networking) in a single platform. How it compares to VMware, Nutanix, and traditional infrastructure.
* [**HCI vs UCI**](02-hci-vs-uci.md) — Two deployment models for different scaling needs. Hyperconverged (HCI) scales compute and storage together; Ultra Converged (UCI) scales them independently with specialized node types.
* [**vSAN & VergeFS Storage**](03-vsan-vergefs.md) — Software-defined distributed storage with tiered drives (Tier 0 for metadata, Tiers 1–5 for workload data), global deduplication, and self-healing redundancy.
* [**Core Fabric & Networking**](04-core-fabric.md) — The private inter-node mesh that carries vSAN replication, cluster coordination, and live migration traffic. Dual-switch redundancy and jumbo frame requirements.
* [**Clusters & Node Types**](05-clusters-nodes.md) — How VergeOS organizes nodes into clusters with distinct roles: controller, scale-out, compute-only, and storage-only.
* [**Lab: Explore the Architecture**](lab.md) — Hands-on exploration of the VergeOS Terraform playground to trace deployment topologies, examine infrastructure-as-code patterns, and design a deployment for a customer scenario.
