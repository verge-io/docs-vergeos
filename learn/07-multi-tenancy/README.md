---
description: "Design multi-tenant environments with proper isolation, create tenants, allocate resources, and configure tenant recipes for standardized provisioning."
---

# Module 7: Multi-Tenancy

## Learning Objectives

By the end of this module, you will be able to:

- **Design a multi-tenant environment** with proper isolation and resource boundaries
- **Create tenants and allocate resources** using the VergeOS tenant management system
- **Configure tenant recipes** for standardized, repeatable tenant provisioning

## Prerequisites

- Completion of [Module 1: Architecture Fundamentals](../01-architecture/README.md) -- understanding of VergeOS platform architecture
- Completion of [Module 4: Networking](../04-networking/README.md) -- understanding of virtual networks and tenant network isolation
- Completion of [Module 5: Storage](../05-storage/README.md) -- understanding of vSAN tiers and storage allocation
- Completion of [Module 6: Virtual Machines](../06-virtual-machines/README.md) -- understanding of VM provisioning and recipes

## Estimated Time

**3 hours** (1.5 hours reading + 1.5 hours lab)

## Topics

* [**Virtual Data Center Concepts**](01-vdc-concepts.md) — Understanding VergeOS tenants as isolated virtual data centers, resource allocation models, and tenant hierarchy.
* [**Creating & Configuring Tenants**](02-creating-tenants.md) — Creating tenants, assigning compute, memory, and storage quotas, and configuring tenant-level networking.
* [**Tenant Recipes**](03-tenant-recipes.md) — Building reusable tenant recipes for standardized provisioning, including pre-configured networks, VMs, and settings.
* [**Resource Allocation & Scaling**](04-resource-allocation.md) — Tenant node planning, right-sizing strategies, and scaling paths for single-node and multi-node tenant deployments.
* [**Tenant Isolation & Security**](05-isolation-security.md) — Network isolation between tenants, resource guarantees, and security boundaries in a multi-tenant deployment.
* [**Lab: Multi-Tenant Environment**](lab.md) — Create tenants, allocate resources, deploy from a tenant recipe, and verify tenant isolation.
