---
description: "Hands-on training for architecting, deploying, and operating VergeOS infrastructure."
icon: graduation-cap
---

# Learn the platform

This is a hands-on lab workbook for anyone architecting, deploying, and operating VergeOS infrastructure. The program follows a linear progression from foundational concepts through advanced scenario-based labs.

{% hint style="info" %}
New to VergeOS? Start with **Module 1: Architecture Fundamentals** and work through the modules in order — each one builds on the concepts before it.
{% endhint %}

## Who this is for

- **IT Administrators** deploying, configuring, and maintaining VergeOS clusters
- **Solutions Architects** scoping and designing VergeOS environments
- **Operations Staff** monitoring and troubleshooting day-to-day infrastructure
- **DevOps Engineers** automating VergeOS with APIs, Terraform, and scripting tools
- **Channel Partners** building expertise to support customer deployments

## Prerequisites

- Hands-on experience with server and network infrastructure
- Familiarity with virtualization concepts (hypervisors, virtual machines, virtual networking)
- VMware or Nutanix experience is helpful but not required — **VMware Bridge** and **Nutanix Bridge** callouts throughout the modules map VergeOS concepts to their equivalents for anyone coming from either platform
- Access to bare-metal hardware for lab exercises (or a VergeOS lab environment)

## Modules

The curriculum is organized into 10 modules that progress from architecture fundamentals through real-world deployment scenarios.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><h3><i class="fa-sitemap" style="color:#C4502D;">:triangular_ruler:</i></h3></td><td><strong>1. Architecture Fundamentals</strong></td><td>HCI vs UCI, VergeFS storage, core fabric networking, clusters and node types.</td><td><a href="01-architecture/README.md">architecture</a></td></tr><tr><td><h3><i class="fa-ruler-combined" style="color:#C4502D;">:straight_ruler:</i></h3></td><td><strong>2. Sizing &#x26; Design</strong></td><td>Hardware requirements, reference architectures, and customer scoping exercises.</td><td><a href="02-sizing-design/README.md">sizing-design</a></td></tr><tr><td><h3><i class="fa-screwdriver-wrench" style="color:#C4502D;">:wrench:</i></h3></td><td><strong>3. Installation</strong></td><td>Bare-metal install, BIOS/disk prep, network prerequisites, and post-install checklist.</td><td><a href="03-installation/README.md">installation</a></td></tr><tr><td><h3><i class="fa-network-wired" style="color:#C4502D;">:globe_with_meridians:</i></h3></td><td><strong>4. Networking</strong></td><td>VergeFabric, VLANs, firewall rules, routing (BGP/OSPF), and network design.</td><td><a href="04-networking/README.md">networking</a></td></tr><tr><td><h3><i class="fa-database" style="color:#C4502D;">:card_file_box:</i></h3></td><td><strong>5. Storage</strong></td><td>vSAN tiers, storage provisioning, NAS configuration, and best practices.</td><td><a href="05-storage/README.md">storage</a></td></tr><tr><td><h3><i class="fa-desktop" style="color:#C4502D;">:computer:</i></h3></td><td><strong>6. Virtual Machines</strong></td><td>VM creation, recipes, templates, GPU passthrough, and migration workflows.</td><td><a href="06-virtual-machines/README.md">virtual-machines</a></td></tr><tr><td><h3><i class="fa-users" style="color:#C4502D;">:busts_in_silhouette:</i></h3></td><td><strong>7. Multi-Tenancy</strong></td><td>Tenant creation, resource allocation, isolation boundaries, and tenant recipes.</td><td><a href="07-multi-tenancy/README.md">multi-tenancy</a></td></tr><tr><td><h3><i class="fa-code" style="color:#C4502D;">:gear:</i></h3></td><td><strong>8. Developer / DevOps</strong></td><td>API, Terraform provider, pyvergeos, PowerShell, automation, and cloud-init.</td><td><a href="08-developer-devops/README.md">developer-devops</a></td></tr><tr><td><h3><i class="fa-gauge-high" style="color:#C4502D;">:bar_chart:</i></h3></td><td><strong>9. Monitoring &#x26; Troubleshooting</strong></td><td>Dashboard, logs, alerts, common issues, and support escalation.</td><td><a href="09-monitoring-troubleshooting/README.md">monitoring-troubleshooting</a></td></tr><tr><td><h3><i class="fa-flask" style="color:#C4502D;">:test_tube:</i></h3></td><td><strong>10. Scenario Labs</strong></td><td>Deploy HCI/UCI/hybrid topologies and perform VMware migrations using the Terraform playground.</td><td><a href="10-scenario-labs/README.md">scenario-labs</a></td></tr></tbody></table>

## How to use this training

Each module includes:

- **Concept pages** with diagrams, explanations, and **VMware/Nutanix Bridge** callouts for readers coming from either platform
- **Hands-on lab exercises** with step-by-step instructions (early modules) progressing to guided challenges (later modules)
- **Architecture diagrams** rendered as Mermaid visualizations you can reference during labs

## Lab environment

Labs use a combination of:

- **Your own VergeOS environment** on bare-metal hardware for installation and configuration exercises
- **The [Terraform Playground](https://github.com/verge-io/vergeos-terraform-playground)** for exploring deployment topologies and automation scenarios

Specific environment requirements are listed at the beginning of each lab exercise.

## Related spaces

- Deployment planning: [Plan and deploy VergeOS](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/)
- Day-2 operations: [Run the platform](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/)
- Disaster recovery and automation: [Automate, protect, and extend](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/)
