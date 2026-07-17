---
title: Virtual Machine Management (VergeHV)
semantic_keywords:
  - VergeOS virtual machine management overview
  - VergeHV hypervisor KVM enterprise features
  - getting started with VergeOS VMs
  - server consolidation virtualization platform
  - hyperconverged VM management compute storage networking
use_cases:
  - evaluate_vergeos_vm_capabilities
  - plan_vm_deployment_strategy
  - onboard_new_vergeos_administrator
  - server_consolidation_planning
categories:
  - Virtual Machines
description: >-
  Overview of VergeOS virtual machine management capabilities powered by the
  VergeHV hypervisor, covering enterprise-grade compute, storage, networking,
  and automation features.
tags:
  - virtual-machines
  - overview
  - vergehv
  - hypervisor
  - kvm
  - getting-started
  - architecture
  - high-availability
---

# Virtual Machine Management (VergeHV)

VergeHV is the integrated hypervisor at the heart of VergeOS, providing enterprise-grade virtual machine management through a unified platform that converges compute, storage, and networking. Built on proven KVM technology and designed as a Type-1 hypervisor, VergeHV delivers near bare-metal performance while simplifying infrastructure management through a single, comprehensive interface.

## Why Choose VergeHV?

Whether you're consolidating physical servers, migrating from legacy hypervisors, or building a new virtual infrastructure, VergeHV provides the foundation for modern, scalable virtualization. Unlike traditional solutions that require separate management tools for compute, storage, and networking, VergeHV integrates all these components into a cohesive platform that reduces complexity and operational overhead.

## Prerequisites

Before creating your first virtual machines, ensure your VergeOS environment meets these requirements:

* **System Setup**: VergeOS installed with at least two nodes for high availability
* **Storage Configuration**: vSAN storage tiers properly configured and available
* **Network Configuration**: External and internal networks configured for VM connectivity
* **Media Files**: Installation ISOs uploaded to vSAN for guest operating system installation
* **Resource Planning**: Adequate CPU, memory, and storage resources allocated for planned workloads

For detailed system requirements, see the [VergeOS Installation Guide](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/installation-guide).

## Quick Start Guide

New to VergeOS VM Management? Follow this recommended path:

### 1. Create Your First VM (15 minutes)

Start with a simple virtual machine to get familiar with the interface and verify your environment is ready.

* **What you'll accomplish:** Deploy a working VM with basic configuration
* **Next step:** [Creating Your First VM](creating-vms.md)

### 2. Understand VM Configuration (10 minutes)

Learn about drives, network interfaces, and hardware settings to optimize your virtual machines.

* **What you'll accomplish:** Master VM configuration options and performance tuning
* **Next step:** [VM Configuration Guide](vm-field-descriptions.md)

### 3. Learn VM Best Practices (20 minutes)

Discover proven strategies for sizing, security, and performance optimization.

* **What you'll accomplish:** Apply enterprise-grade practices to your VM deployments
* **Next step:** [VM Best Practices](vm-best-practices.md)

### 4. Explore Migration Strategies and Import Methods (30 minutes)

Migrate existing workloads from other hypervisors or deploy from templates.

* **What you'll accomplish:** Successfully import VMs from VMware, Hyper-V, or other platforms
* **Next step:** [VM Import Methods](vm-migration-overview.md)

## Key Capabilities

### **Enterprise-Grade Performance**

* **Type-1 Hypervisor Architecture**: VergeHV runs directly on hardware using KVM technology, delivering near bare-metal performance with minimal overhead
* **Resource Optimization**: Advanced memory management, CPU scheduling, and I/O optimization ensure maximum efficiency
* **Hardware Acceleration**: Support for Intel VT-x/AMD-V virtualization extensions and hardware-assisted features

### **Comprehensive Security**

* **Network Micro-Segmentation**: Isolate workloads using virtual networks with granular access controls
* **Tenant Isolation**: Complete separation of resources and networks in multi-tenant environments
* **Secure Migration**: Encrypted live migration and secure communication between nodes

### **Flexible Storage Integration**

* **Distributed vSAN**: Integrated software-defined storage with automatic tiering and deduplication
* **Multiple Storage Tiers**: Optimize costs by placing workloads on appropriate storage tiers (NVMe, SSD, HDD)
* **Snapshot and Cloning**: Instant VM snapshots and space-efficient cloning for backup and testing

### **Advanced Networking**

* **Software-Defined Networking**: Create and manage virtual networks without additional hardware
* **VLAN Integration**: Seamless integration with existing network infrastructure
* **Traffic Management**: Quality of Service (QoS) controls, rate limiting, and bandwidth prioritization for network optimization

### **Broad Compatibility**

* **Guest Operating Systems**: Extensive support for Windows (Server 2008 R2 - 2022), Linux distributions (RHEL, Ubuntu, CentOS, SUSE), and FreeBSD
* **Virtual Appliances**: Native support for KVM-compatible virtual appliances and OVA/OVF formats
* **Legacy Support**: Hardware emulation for older operating systems when needed

### **High Availability & Migration**

* **Live Migration**: Move running VMs between nodes without downtime for maintenance or load balancing
* **Automated Failover**: Automatic VM restart on alternate nodes during hardware failures
* **Cluster Management**: Distribute workloads across multiple nodes for optimal resource utilization

### **Powerful Automation**

* **Recipe System**: Deploy standardized VM configurations using customizable templates
* **API Integration**: Complete REST API for infrastructure-as-code and automation workflows
* **Task Engine**: Schedule and automate routine operations like backups, migrations, and maintenance
* **Terraform Integration**: Infrastructure-as-code support with the official VergeOS Terraform provider for automated provisioning of VMs, networks, and storage resources

## Common Use Cases

### **Server Consolidation**

Replace multiple physical servers with virtual machines, reducing hardware costs and improving resource utilization. VergeHV's efficient resource management allows for higher consolidation ratios while maintaining performance.

### **Development and Testing**

Rapidly provision isolated environments for development teams. Use snapshots and clones to create consistent testing environments and quickly roll back changes.

### **Disaster Recovery**

Leverage VM snapshots, replication, and migration capabilities to build robust disaster recovery solutions. Test recovery procedures without impacting production systems.

### **Legacy Application Support**

Extend the life of older applications by virtualizing aging physical servers. VergeHV's broad compatibility ensures legacy systems continue running reliably.

### **Multi-Tenant Hosting**

Provide isolated virtual environments for different customers or departments using VergeOS tenant capabilities with dedicated resources and networks.

## Getting Help

### **Documentation Resources**

* [**Guest OS Compatibility**](guest-os-compatibility.md) - Supported operating systems and configurations
* [**VM Field Descriptions**](vm-field-descriptions.md) - Complete reference for VM configuration options

### **Support**

* [**Support** ](https://app.gitbook.com/s/uJc5d3O7cwI7qD8muSyG/support-and-services)- Access professional support and documentation
* [**Knowledge Base**](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/) - Searchable database of solutions and best practices

***

## Related Documentation

### Essential Getting Started

* [**VM Best Practices**](vm-best-practices.md) - Configuration guidelines and recommendations _(20 minutes)_
* [**Creating VMs**](creating-vms.md) - Step-by-step VM creation guide _(15 minutes)_
* [**Uploading Media Images**](../storage/uploading-files-to-vsan.md) - Upload ISOs and installation media _(10 minutes)_

### VM Configuration

* [**Virtual Machine Drives**](vm-drives.md) - Storage configuration and management
* [**Virtual Machine Network Interfaces**](vm-nics.md) - Network connectivity setup
* [**VM Field Descriptions**](vm-field-descriptions.md) - Complete configuration reference
* [**Guest Agent**](vm-guest-agent.md) - Enhanced VM integration and management

### Import and Migration

* [**Import Methods Overview**](vm-migration-overview.md) - Choose the right import method for your needs
* [**Import from VMware**](import-from-vmware.md) - VMware migration guide
* [**Import from Media Images**](import-from-upload.md) - Create VMs from disk images
* [**Import from NAS**](import-from-nas.md) - Import from network storage

### Advanced Operations

* [**Live Migrations**](live-migrations.md) - Zero-downtime VM movement
* [**Manual VM Migrations**](vm-manual-migration.md) - Planned migration procedures
* [**Working with VMs**](working-with-vms.md) - Day-to-day VM management

### Virtual Desktop Infrastructure

* [**VDI Overview**](vdi-overview.md) - Native VDI capabilities
* [**VDI Administration**](vdi-administrator.md) - Admin guide for VDI deployments
* [**Remote Console Access**](vm-remote-console.md) - VM console connectivity

### Backup and Recovery

* [**VM Snapshots and Restores**](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/vm-snapshots-restores) - Backup and recovery strategies

### Automation

* [**Recipes Overview**](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/automation/recipes-overview) - Automated VM deployment templates
* [**Task Engine**](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/automation/create-tasks) - Scheduled automation and workflows
* [**VergeOS API Guide**](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/automation-api/verge-api-guide) - Programmatic infrastructure management
