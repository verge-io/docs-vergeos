---
description: >-
  Hands-on training for architecting, deploying, and operating VergeOS
  infrastructure.
icon: graduation-cap
---

# Learn the platform

This is a hands-on lab workbook for anyone architecting, deploying, and operating VergeOS infrastructure. The program follows a linear progression from foundational concepts through advanced scenario-based labs.

{% hint style="info" %}
New to VergeOS? Start with **Module 1: Architecture Fundamentals** and work through the modules in order — each one builds on the concepts before it.
{% endhint %}

## Who this is for

* **IT Administrators** deploying, configuring, and maintaining VergeOS clusters
* **Solutions Architects** scoping and designing VergeOS environments
* **Operations Staff** monitoring and troubleshooting day-to-day infrastructure
* **DevOps Engineers** automating VergeOS with APIs, Terraform, and scripting tools
* **Channel Partners** building expertise to support customer deployments

## Prerequisites

* Hands-on experience with server and network infrastructure
* Familiarity with virtualization concepts (hypervisors, virtual machines, virtual networking)
* VMware or Nutanix experience is helpful but not required — **VMware Bridge** and **Nutanix Bridge** callouts throughout the modules map VergeOS concepts to their equivalents for anyone coming from either platform
* Access to bare-metal hardware for lab exercises (or a VergeOS lab environment)

## Modules

The curriculum is organized into 10 modules that progress from architecture fundamentals through real-world deployment scenarios.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><h3><i class="fa-sitemap">:sitemap:</i></h3></td><td><strong>1. Architecture Fundamentals</strong></td><td>HCI vs UCI, VergeFS storage, core fabric networking, clusters and node types.</td><td><a href="01-architecture/">01-architecture</a></td></tr><tr><td><h3><i class="fa-ruler-combined">:ruler-combined:</i></h3></td><td><strong>2. Sizing &#x26; Design</strong></td><td>Hardware requirements, reference architectures, and customer scoping exercises.</td><td><a href="02-sizing-design/">02-sizing-design</a></td></tr><tr><td><h3><i class="fa-screwdriver-wrench">:screwdriver-wrench:</i></h3></td><td><strong>3. Installation</strong></td><td>Bare-metal install, BIOS/disk prep, network prerequisites, and post-install checklist.</td><td><a href="03-installation/">03-installation</a></td></tr><tr><td><h3><i class="fa-network-wired">:network-wired:</i></h3></td><td><strong>4. Networking</strong></td><td>VergeFabric, VLANs, firewall rules, routing (BGP/OSPF), and network design.</td><td><a href="04-networking/">04-networking</a></td></tr><tr><td><h3><i class="fa-database">:database:</i></h3></td><td><strong>5. Storage</strong></td><td>vSAN tiers, storage provisioning, NAS configuration, and best practices.</td><td><a href="05-storage/">05-storage</a></td></tr><tr><td><h3><i class="fa-desktop">:desktop:</i></h3></td><td><strong>6. Virtual Machines</strong></td><td>VM creation, recipes, templates, GPU passthrough, and migration workflows.</td><td><a href="06-virtual-machines/">06-virtual-machines</a></td></tr><tr><td><h3><i class="fa-users">:users:</i></h3></td><td><strong>7. Multi-Tenancy</strong></td><td>Tenant creation, resource allocation, isolation boundaries, and tenant recipes.</td><td><a href="07-multi-tenancy/">07-multi-tenancy</a></td></tr><tr><td><h3><i class="fa-code">:code:</i></h3></td><td><strong>8. Developer / DevOps</strong></td><td>API, Terraform provider, pyvergeos, PowerShell, automation, and cloud-init.</td><td><a href="08-developer-devops/">08-developer-devops</a></td></tr><tr><td><h3><i class="fa-gauge-high">:gauge-high:</i></h3></td><td><strong>9. Monitoring &#x26; Troubleshooting</strong></td><td>Dashboard, logs, alerts, common issues, and support escalation.</td><td><a href="09-monitoring-troubleshooting/">09-monitoring-troubleshooting</a></td></tr><tr><td><h3><i class="fa-flask">:flask:</i></h3></td><td><strong>10. Scenario Labs</strong></td><td>Deploy HCI/UCI/hybrid topologies and perform VMware migrations using the Terraform playground.</td><td><a href="10-scenario-labs/">10-scenario-labs</a></td></tr></tbody></table>

## How to use this training

Each module includes:

* **Concept pages** with diagrams, explanations, and **VMware/Nutanix Bridge** callouts for readers coming from either platform
* **Hands-on lab exercises** with step-by-step instructions (early modules) progressing to guided challenges (later modules)
* **Architecture diagrams** rendered as Mermaid visualizations you can reference during labs

## Lab environment

Labs use a combination of:

* **Your own VergeOS environment** on bare-metal hardware for installation and configuration exercises
* **The** [**Terraform Playground**](https://github.com/verge-io/vergeos-terraform-playground) for exploring deployment topologies and automation scenarios

Specific environment requirements are listed at the beginning of each lab exercise.

## Related spaces

* Deployment planning: [Plan and deploy](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/)
* Day-2 operations: [Run the platform](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/)
* Disaster recovery and automation: [Automate, protect, and extend](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/)
