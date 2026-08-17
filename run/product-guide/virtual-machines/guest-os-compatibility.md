---
title: "VergeOS Guest OS Compatibility"
description: "Reference guide for supported guest operating systems on VergeOS, including Windows, Linux, and FreeBSD versions with recommended interfaces and minimum requirements."
semantic_keywords:
  - "supported operating systems for VergeOS VMs"
  - "Windows server guest compatibility KVM"
  - "Linux distribution support VirtIO drivers"
  - "FreeBSD virtual machine compatibility"
  - "guest OS minimum RAM and interface requirements"
use_cases:
  - verify_os_compatibility
  - select_disk_interface_for_guest
  - plan_vm_resource_requirements
  - evaluate_legacy_os_support
tags:
  - compatibility
  - guest-os
  - windows
  - linux
  - freebsd
  - virtio
  - kvm
  - drivers
  - virtual-machines
categories:
  - Virtual Machines
---

# VergeOS Guest OS Compatibility

VergeOS, built on Linux KVM technology, provides extensive compatibility for x86_64 guest operating systems. This includes Windows, Linux distributions, FreeBSD, and virtual appliances designed for KVM environments. While any x86_64-compatible operating system should work without issues, this guide outlines commonly tested configurations.

{% hint style="info" %}
**OS Support**

While this list represents commonly tested configurations, VergeOS's KVM foundation enables **support for nearly any x86_64 operating system or KVM-compatible virtual appliance**. Contact support for guidance on specific operating systems or virtual appliances not listed here.
{% endhint %}


{% hint style="success" %}
**Virtual Appliances**

Virtual appliances packaged for KVM environments are fully compatible with VergeOS. This includes OVA/OVF formats from vendors who support KVM-based deployments.
{% endhint %}

## Microsoft Windows 

### Windows Desktop Versions

| Version | Recommended Interface | Minimum RAM | Notes |
|---------|---------------------|-------------|--------|
| Windows 11 | VirtIO | 4 GB | Best performance with latest VirtIO drivers |
| Windows 10 | VirtIO | 2 GB | Supports all editions (Home, Pro, Enterprise) |
| Windows 8.1 | VirtIO/IDE | 2 GB | May require legacy hardware support |
| Windows 7 | IDE/SATA | 2 GB | Legacy OS - Limited driver support |

### Windows Server Versions

| Version | Recommended Interface | Minimum RAM | Notes |
|---------|---------------------|-------------|--------|
| Server 2025 | VirtIO | 2 GB | Optimal performance with latest drivers |
| Server 2022 | VirtIO | 2 GB | Optimal performance with latest drivers |
| Server 2019 | VirtIO | 2 GB | Supports all roles and features |
| Server 2016 | VirtIO | 2 GB | Recommended for production use |
| Server 2012 R2 | VirtIO/IDE | 2 GB | Extended support ends 2023 |
| Server 2008 R2 | IDE/SATA | 2 GB | Legacy support only |

## Linux

### Enterprise Linux Distributions

| Distribution | Versions | Recommended Interface | Minimum RAM | Notes |
|-------------|----------|---------------------|-------------|--------|
| RHEL | 7, 8, 9, 10 | VirtIO | 2 GB | Native VirtIO support |
| SUSE Enterprise | 11, 12, 15, 16 | VirtIO | 2 GB | Built-in driver support |
| Oracle Linux | 6, 7, 8, 9, 10 | VirtIO | 2 GB | UEK kernel recommended |

### Community Enterprise Linux

| Distribution | Versions | Recommended Interface | Minimum RAM | Notes |
|-------------|----------|---------------------|-------------|--------|
| AlmaLinux | 8, 9, 10 | VirtIO | 2 GB | RHEL binary compatible |
| Rocky Linux | 8, 9, 10 | VirtIO | 2 GB | Native driver support |
| CentOS | 7, 8 | VirtIO | 2 GB | Built-in VirtIO support |
| CentOS Stream | 8 | VirtIO | 2 GB | Rolling release model |

### Debian-based Distributions

| Distribution | Versions | Recommended Interface | Minimum RAM | Notes |
|-------------|----------|---------------------|-------------|--------|
| Debian | 8, 9, 10, 11, 12, 13 | VirtIO | 1 GB | Native driver support |
| Ubuntu LTS | 20.04, 22.04, 24.04, 26.04 | VirtIO | 2 GB | Recommended for production |
| Ubuntu | 12.04 - 19.04 | VirtIO | 1 GB | Older releases - limited support |

## FreeBSD

| Version | Support Status | Recommended Interface | Minimum RAM | Notes |
|---------|---------------|---------------------|-------------|--------|
| FreeBSD 14 | Full | VirtIO | 1 GB | Best performance with VirtIO |
| FreeBSD 13 | Full | VirtIO | 1 GB | Production ready |
| FreeBSD 12 | Full | VirtIO | 1 GB | Production ready |
| FreeBSD 11 | Limited | VirtIO/SATA | 1 GB | Legacy support |
| FreeBSD 10 | Limited | SATA | 1 GB | Basic compatibility |

{% hint style="info" %}
**Driver Support**

For optimal performance, VirtIO drivers are recommended where supported. Windows guests may require additional driver installation, while most modern Linux distributions include native VirtIO support.
{% endhint %}


## Technical Considerations

{% hint style="info" %}
**System Requirements**

- RAM requirements vary by operating system and workload
- Always consult vendor documentation for production sizing
- Consider additional overhead for virtualization
{% endhint %}

{% hint style="success" %}
**Storage Interface Options**

- VirtIO: Modern interface offering best performance (recommended)
- SATA: Compatible with most operating systems, requires Q35 machine type
- IDE: Available for legacy operating system support, requires i440FX machine type
{% endhint %}

{% hint style="warning" %}
**Architecture Support**

- VergeOS supports 64-bit (x86_64) operating systems
- 32-bit operating systems are not officially supported
{% endhint %}

{% hint style="info" %}
**Performance Optimization**

- Install and configure VirtIO drivers where supported
- Windows guests require additional VirtIO driver installation
- Most modern Linux distributions include VirtIO support
- Keep guest operating systems and drivers updated
{% endhint %}
