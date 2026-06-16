---
description: "Automate VergeOS infrastructure using the REST API and vrg CLI, pyvergeos, the PSVergeOS PowerShell module, the Terraform provider, Ansible, the Task Engine, and Kubernetes/Rancher."
---

# Module 8: Developer & DevOps

## Learning Objectives

By the end of this module, you will be able to:

- **Use the VergeOS REST API** to automate common infrastructure operations via REST endpoints and CLI tools
- **Script with pyvergeos and PowerShell** to automate bulk VM, network, and tenant operations
- **Manage infrastructure with the Terraform provider** for declarative, version-controlled deployments
- **Automate configuration with Ansible** using the VergeOS collection for playbook-driven orchestration
- **Build event-driven workflows with the Task Engine** using webhooks and automated task chains
- **Deploy Kubernetes on VergeOS** using the Docker Machine Driver, Rancher integration, and VergeOS CSI/CCM components

## Prerequisites

- Completion of [Module 1: Architecture Fundamentals](../01-architecture/README.md) -- understanding of VergeOS platform architecture
- Completion of [Module 6: Virtual Machines](../06-virtual-machines/README.md) -- understanding of VM provisioning and management
- Completion of [Module 7: Multi-Tenancy](../07-multi-tenancy/README.md) -- understanding of tenant creation and resource allocation
- Basic familiarity with REST APIs, command-line tools, and at least one scripting language (Python, PowerShell, or HCL/Terraform)

## Estimated Time

**4 hours** (2 hours reading + 2 hours lab)

## Topics

* [**REST API & CLI Tools**](01-api-cli.md) — Authenticating with the VergeOS API, exploring endpoints, performing CRUD operations, and using the `vrg` CLI for scripted automation.
* [**Python SDK (pyvergeos)**](02-python-sdk.md) — Automating VergeOS operations with pyvergeos: VM lifecycle, network management, tenant provisioning, and bulk operations.
* [**PowerShell Module**](03-powershell-module.md) — Managing VergeOS from Windows environments using the PSVergeOS PowerShell module for scripting and orchestration.
* [**Terraform & Packer**](04-terraform-packer.md) — Declarative infrastructure-as-code with the VergeOS Terraform provider and immutable image builds with Packer.
* [**Ansible Collection**](05-ansible.md) — Playbook-driven configuration management and orchestration using the VergeOS Ansible collection.
* [**Task Engine & Webhooks**](06-task-engine.md) — Event-driven automation with the built-in task engine, scheduled tasks, and webhook integrations.
* [**Kubernetes & Rancher**](07-kubernetes-rancher.md) — Running Kubernetes on VergeOS with the Docker Machine Driver, Rancher integration, CSI driver, and Cloud Controller Manager.
* [**Lab: Infrastructure Automation**](lab.md) — Use the REST API, Terraform, and scripting tools to automate VM and tenant provisioning end-to-end.
