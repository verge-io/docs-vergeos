---
description: "Hands-on training for architecting, deploying, and operating VergeOS infrastructure."
icon: graduation-cap
---

# Learn the platform

## About This Program

This training portal is a hands-on lab workbook for anyone architecting, deploying, and operating VergeOS infrastructure. The program follows a linear progression from foundational concepts through advanced scenario-based labs.

### Who Is This For?

- **IT Administrators** deploying, configuring, and maintaining VergeOS clusters
- **Solutions Architects** scoping and designing VergeOS environments
- **Operations Staff** monitoring and troubleshooting day-to-day infrastructure
- **DevOps Engineers** automating VergeOS with APIs, Terraform, and scripting tools
- **Channel Partners** building expertise to support customer deployments

### Prerequisites

- Hands-on experience with server and network infrastructure
- Familiarity with virtualization concepts (hypervisors, virtual machines, virtual networking)
- VMware or Nutanix experience is helpful but not required -- **VMware Bridge** and **Nutanix Bridge** callouts throughout the modules map VergeOS concepts to their equivalents on each platform
- Access to bare-metal hardware for lab exercises (or a VergeOS lab environment)

---

## Modules

The curriculum is organized into 10 modules that progress from architecture fundamentals through real-world deployment scenarios.

- [**1. Architecture Fundamentals**](01-architecture/README.md) — HCI vs UCI, VergeFS storage, core fabric networking, clusters and node types.
- [**2. Sizing & Design**](02-sizing-design/README.md) — Hardware requirements, reference architectures, and customer scoping exercises.
- [**3. Installation**](03-installation/README.md) — Bare-metal install, BIOS/disk prep, network prerequisites, and post-install checklist.
- [**4. Networking**](04-networking/README.md) — VergeFabric, VLANs, firewall rules, routing (BGP/OSPF), and network design.
- [**5. Storage**](05-storage/README.md) — vSAN tiers, storage provisioning, NAS configuration, and best practices.
- [**6. Virtual Machines**](06-virtual-machines/README.md) — VM creation, recipes, templates, GPU passthrough, and migration workflows.
- [**7. Multi-Tenancy**](07-multi-tenancy/README.md) — Tenant creation, resource allocation, isolation boundaries, and tenant recipes.
- [**8. Developer / DevOps**](08-developer-devops/README.md) — API, Terraform provider, pyvergeos, PowerShell, automation, and cloud-init.
- [**9. Monitoring & Troubleshooting**](09-monitoring-troubleshooting/README.md) — Dashboard, logs, alerts, common issues, and support escalation.
- [**10. Scenario Labs**](10-scenario-labs/README.md) — Deploy HCI/UCI/hybrid topologies and perform VMware migrations using the Terraform playground.

---

## How to Use This Training

Each module includes:

- **Concept pages** with diagrams, explanations, and VMware/Nutanix Bridge callouts
- **Hands-on lab exercises** with step-by-step instructions (early modules) progressing to guided challenges (later modules)
- **Architecture diagrams** rendered as Mermaid visualizations you can reference during labs

Start with **Module 1: Architecture Fundamentals** and work through the modules in order. Each module builds on concepts from previous ones.

---

## Lab Environment

Labs use a combination of:

- **Your own VergeOS environment** on bare-metal hardware for installation and configuration exercises
- **The [Terraform Playground](https://github.com/verge-io/vergeos-terraform-playground)** for exploring deployment topologies and automation scenarios

Specific environment requirements are listed at the beginning of each lab exercise.
