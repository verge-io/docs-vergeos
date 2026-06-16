---
description: "Hardware requirements, reference architectures, and customer scoping exercises for VergeOS deployments."
---

# Module 2: Sizing & Design

## Learning Objectives

By the end of this module, you will be able to:

- **Evaluate customer requirements** and recommend an appropriate VergeOS topology (HCI or UCI -- including the hybrid two-cluster UCI variant, HCI + Dedicated Compute)
- **Size hardware** for HCI and UCI deployments based on workload profiles
- **Use reference architectures** as starting points for customer designs
- **Create a bill of materials** for a VergeOS deployment proposal

## Prerequisites

- Completion of [Module 1: Architecture Fundamentals](../01-architecture/README.md) -- you should understand HCI vs UCI trade-offs, node types, and cluster concepts

## Estimated Time

**2 hours** (1 hour reading + 1 hour lab)

## Topics

* [**Hardware Requirements**](01-hardware-requirements.md) — Minimum and recommended specs for controller nodes, storage nodes, and compute-only nodes. CPU, memory, disk, and NIC considerations.
* [**Reference Architectures**](02-reference-architectures.md) — Three deployment models -- HCI, HCI + Dedicated Compute (the hybrid two-cluster UCI variant), and UCI -- plus guidance for edge and CSP scenarios.
* [**Customer Scoping**](03-customer-scoping.md) — How to gather requirements, translate workload profiles into resource estimates, and select the right topology.
* [**Lab: Design Exercise**](lab.md) — Given a customer scenario, produce a hardware recommendation and topology diagram.
