---
description: "Create and manage VMs in VergeOS, deploy from recipes and templates, configure GPU passthrough, and import VMs from VMware and other platforms."
---

# Module 6: Virtual Machines

## Learning Objectives

By the end of this module, you will be able to:

- **Create and manage VMs** in VergeOS using the UI and API
- **Deploy VMs from recipes and templates** to standardize provisioning workflows
- **Configure GPU passthrough** for specialized workloads (VDI, AI/ML, rendering)
- **Import VMs from VMware and other platforms** using built-in migration tools

## Prerequisites

- Completion of [Module 1: Architecture Fundamentals](../01-architecture/README.md) -- understanding of VergeOS platform architecture
- Completion of [Module 4: Networking](../04-networking/README.md) -- understanding of virtual networks and network configuration
- Completion of [Module 5: Storage](../05-storage/README.md) -- understanding of vSAN tiers and storage provisioning

## Estimated Time

**3 hours** (1.5 hours reading + 1.5 hours lab)

## Topics

* [**VM Creation & Lifecycle**](01-vm-creation-lifecycle.md) — Creating VMs, configuring CPU/memory/disk, managing VM lifecycle (start, stop, snapshot, clone), live migration between nodes, and HA failover.
* [**Recipes & Marketplace**](02-recipes-marketplace.md) — Building reusable VM recipes for standardized deployments, organizing catalogs, Cloud-Init integration, and the VergeOS Marketplace.
* [**GPU & Device Passthrough**](03-gpu-passthrough.md) — Configuring PCI, NVIDIA vGPU, SR-IOV NIC, and USB device passthrough using resource groups and resource rules.
* [**VM Migration & Import**](04-vm-migration-import.md) — Migrating workloads from VMware, Hyper-V, KVM, and physical machines using the VMware Connector, file uploads, NAS volumes, and the Clone Utility.
* [**Lab: Virtual Machine Operations**](lab.md) — Create VMs, deploy from recipes, configure GPU passthrough, and import a VM from an external format.
