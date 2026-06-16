---
description: "Bare-metal preparation, VergeOS installation walkthrough, and post-install verification for production deployments."
---

# Module 3: Installation

## Learning Objectives

By the end of this module, you will be able to:

- **Prepare bare-metal hardware** for VergeOS installation (BIOS settings, disk controllers, networking)
- **Perform a complete 2-node VergeOS installation** from USB boot media
- **Complete the post-installation verification checklist** to confirm a healthy system
- **Troubleshoot common installation issues** and know when to escalate

## Prerequisites

- Completion of [Module 1: Architecture Fundamentals](../01-architecture/README.md) -- understanding of node roles, core fabric, and cluster concepts
- Completion of [Module 2: Sizing & Design](../02-sizing-design/README.md) -- hardware has been selected and scoped

## Estimated Time

**2.5 hours** (1 hour reading + 1.5 hours lab)

## Topics

* [**Pre-Installation Checklist**](01-pre-installation.md) — BIOS configuration, disk controller modes, network interface identification, and boot media preparation.
* [**Controller Installation**](02-controller-installation.md) — Step-by-step installation of Node 1 (controller) and Node 2 (controller), including network configuration and cluster formation.
* [**Adding Nodes**](03-adding-nodes.md) — Scale-out nodes, storage-only nodes, and compute-only nodes. Expanding your cluster beyond the initial 2-node deployment.
* [**Post-Install Verification**](04-post-install-verification.md) — Dashboard health checks, vSAN verification, network connectivity, initial configuration, and final deployment testing.
* [**Lab: 2-Node Installation**](lab.md) — Perform a complete VergeOS installation on a 2-node cluster using the Terraform playground or physical hardware.
