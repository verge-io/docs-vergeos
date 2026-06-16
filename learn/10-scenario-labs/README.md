---
description: "Capstone scenario labs deploying multiple VergeOS topologies with the Terraform playground, performing VMware-to-VergeOS migrations, and making architecture decisions based on customer requirements."
---

# Module 10: Scenario Labs

## Learning Objectives

By the end of this module, you will be able to:

- **Deploy multiple VergeOS topologies** using the Terraform playground (2-node HCI, 4-node HCI, HCI+Compute hybrid, UCI 3-cluster)
- **Perform a VMware-to-VergeOS migration** end-to-end including planning, execution, and validation
- **Design HCI+Compute hybrid architectures** that separate storage and compute scaling for workload-specific optimization
- **Build multi-tenant MSP environments** with tenant creation, resource quotas, network isolation, and audit verification
- **Make architecture decisions** based on real-world customer requirements and constraints

## Prerequisites

- Completion of all prior modules (1–9)
- Access to the [vergeos-terraform-playground](https://github.com/verge-io/vergeos-terraform-playground) repository
- A running VergeOS environment with admin access
- Terraform CLI installed and configured

## Estimated Time

**8 hours** (across 5 scenario labs)

## Scenario Labs

* [**Lab: HCI Deployment**](lab-hci.md) — Deploy 2-node and 4-node HCI topologies using the Terraform playground. Validate cluster health, storage, and networking.
* [**Lab: UCI Deployment**](lab-uci.md) — Deploy a UCI 3-cluster topology with separate compute and storage clusters. Practice scaling and resource allocation across clusters.
* [**Lab: VMware Migration**](lab-migration.md) — Plan and execute a VMware-to-VergeOS migration end-to-end, including VM import, network reconfiguration, and validation.
* [**Lab: HCI + Compute Deployment**](lab-hci-compute.md) — Deploy an HCI foundation cluster with a dedicated compute-only cluster. Configure workload placement and validate independent compute scaling.
* [**Lab: Multi-Tenancy / MSP**](lab-multi-tenancy.md) — Build a multi-tenant MSP environment with tenant creation, resource quotas, network isolation, and audit verification.
