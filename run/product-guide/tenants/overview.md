---
title: Tenants (Virtual Data Centers)
semantic_keywords:
  - VergeOS multi-tenancy virtual data center overview
  - tenant isolation network encapsulation security
  - nested multi-tenant service provider infrastructure
  - virtual data center resource management delegation
use_cases:
  - evaluate_tenant_capabilities
  - plan_multi_tenant_deployment
  - understand_tenant_isolation_model
  - service_provider_virtual_data_centers
categories:
  - Tenants
description: >-
  Overview of VergeOS multi-tenancy, providing secure, encapsulated virtual data
  centers with full network isolation, nested tenancy, resource tracking, and
  portable self-contained environments.
tags:
  - tenants
  - multi-tenancy
  - virtual-data-center
  - isolation
  - security
  - resource-management
  - nested-tenants
---

# Tenants (Virtual Data Centers)

VergeOS provides native support for multi-tenancy, allowing a single installation to host multiple, encapsulated, secure enclaves called **tenants**. Each tenant is a separate and complete virtual data center that includes all the functionality of a base VergeOS environment (excluding hardware management). Every tenant has access to its own user interface via a unique URL.

Privacy and security are ensured with full network encapsulation and exclusive storage volumes, providing true isolation between tenants, unlike other strategies, such as VLAN-based segmentation.

## Getting Started

New to VergeOS tenants? Start here:

1. [**Create your first tenant**](create-tenants.md) - Set up a basic tenant environment
2. [**Assign external access**](assign-ip-to-tenant.md) - Provide network connectivity
3. [**Configure monitoring**](tenant-monitoring.md) - Set up oversight and reporting

## Key Features

* **Built-in functionality:** Comprehensive solution for tenancy (No additional licensing, tools, or applications needed)
* **Nested Multi-tenancy:** Each tenant can create sub-tenants from its own allocated resources, providing a hierarchical structure of delegation and resource management
* **Resource Tracking:** Per-tenant resource tracking, including deduplication statistics, facilitates billing and capacity planning
* **User Management Flexibility:** Optionally, a tenant can be configured for centralized identity management through: its parent, another VergeOS system, or a third-party identity provider
* **Individualized backup/DR:** DR protocols can be customized per tenant
* **Portability:** Each tenant is a portable, self-contained system that can be moved to a different location as one unit
* **Automated Deployment:** [Tenant Recipes](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/automation/tenant-recipes) allow for rapid deployment, compliance, self-service applications, etc.
* **Custom Branding:** Parent systems can permit a tenant to "brand" its user interface with its own company logos, color schemes and font selections, using [**Themes**](../system/themes.md) (can be allowed/disallowed on a per-tenant basis)

## Security & Isolation

VergeOS tenants provide enterprise-grade security through:

* **Network Encapsulation**: Complete layer 2/3 isolation between tenants
* **Storage Isolation**: Dedicated storage volumes with encryption support
* **Administrative Separation**: Independent user management and permissions
* **Resource Boundaries**: Guaranteed resource allocation and limits

## Practical Applications

Examples of VergeOS tenancy used in the field:

* A **Service Provider** creates secure, full-featured virtual data centers for their clients, which in turn can create virtual data centers for their own customers
* An **Enterprise** centralizes infrastructure management while separating workloads and delegating administration to different regions or business groups
* An **Educational Institution** provides specialized environments to separate faculties or research projects, eliminating traditional siloed, stand-alone systems

## Related Documentation

### Getting Started

* [Creating Tenants](create-tenants.md)
* [Assigning External IP Addresses](assign-ip-to-tenant.md)
* [Modifying Tenant Properties](tenant-modifications.md)

### Resource Management

* [Increasing Tenant Resources](add-tenant-resources.md)
* [Reducing Tenant Resources](reduce-tenant-resources.md)
* [Tenant Usage Reports](tenant-usagereports.md)

### Data Sharing & Protection

* [Sharing Files with Tenants](provide-files-to-tenant.md)
* [Sharing VMs with Tenants](share-vm-snapshot.md)
* [Tenant Snapshots](tenant-snapshots.md)
* [Tenant Restores](tenant-restores.md)

### Monitoring & Management

* [Monitoring Tenants](tenant-monitoring.md)
