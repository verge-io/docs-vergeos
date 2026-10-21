---
title: NVMe Controllers Resetting Due to AER
slug: nvme-aer-reset-loop
author: VergeOS Documentation Team
date: 2026-10-21T15:45:00.000Z
semantic_keywords:
  - nvme controller reset aer pcie error
  - advanced error reporting hardware troubleshooting
  - multiple nvme reset loop shared path
  - installation boot failure nvme devices
use_cases:
  - troubleshoot_nvme_aer_reset
  - diagnose_pcie_link_errors
  - stabilize_nvme_storage_path
  - resolve_installation_boot_failure
categories:
  - Troubleshooting
  - Storage
editor: markdown
dateCreated: 2026-10-21T15:45:00.000Z
description: >-
  How to interpret NVMe controller AER reset messages and diagnose hardware
  issues when one or multiple controllers reset repeatedly during installation
  or operation.
tags:
  - nvme
  - storage
  - hardware
  - troubleshooting
  - aer
  - pcie
  - installation
  - boot
---

# NVMe Controllers Resetting Due to AER

## Overview

The console or `dmesg` shows NVMe controllers resetting repeatedly with messages like:

```
nvme nvme0: resetting controller due to AER
nvme nvme0: 80/0/0 default/read/poll queues
```

This message indicates that the PCIe link reported an error and the kernel reset the NVMe controller to recover. AER stands for Advanced Error Reporting, a PCIe feature that reports hardware-level errors to the operating system.

## Understanding AER Reset Patterns

The pattern of resets determines whether the problem is isolated to a single device. It also shows whether multiple devices share a hardware path and are affected together.

### Single Controller Resetting

When one NVMe controller resets repeatedly (for example, `nvme0` resets but `nvme1` through `nvme7` remain stable):

- The problem is likely specific to that NVMe device or its direct connection.
- Investigate the device itself, its PCIe slot, and the link between the device and the host.

### Multiple Controllers Resetting Together

When several NVMe controllers (for example, `nvme0` through `nvme7`) reset together within a short window:

- This is a shared-path symptom.
- The problem is not a single failing drive.
- Check the PCIe switch, backplane, power delivery, system firmware, or root complex that all the affected controllers share.

{% hint style="warning" %}
**Installation and vSAN Boot Failures**

VergeOS installation and vSAN boot can fail when NVMe controllers are resetting. The installer cannot reliably write to the drives while the controllers cycle. Stabilize the PCIe or storage path before you retry the installation.
{% endhint %}

## What to Check

### For a Single Resetting Controller

1. Check the physical connection between the NVMe device and its slot.
2. Verify the device is fully seated.
3. Check for physical damage to the device or slot.
4. Check the PCIe slot health in the BIOS or system management interface.
5. Check firmware versions for the NVMe device.

### For Multiple Controllers Resetting Together

1. Check the PCIe switch that connects the NVMe devices to the CPU.
2. Verify the backplane firmware and connections.
3. Check power delivery to the drives and the PCIe switch.
4. Check system firmware (BIOS and BMC) for updates.
5. Check for PCIe root complex errors in the system event log.

{% hint style="info" %}
**Firmware and Configuration**

Firmware updates and BIOS configuration changes should be tested in a non-production environment when possible. Contact your hardware vendor for specific guidance on firmware versions and settings for your configuration.
{% endhint %}

## Prerequisites

- Physical access to the host or remote management interface access.
- Administrative access to the system BIOS or BMC.

## Additional Resources

- [Node Sizing](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/sizing) — Hardware requirements for VergeOS, including NVMe and storage controller recommendations.
- [Installation Guide](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/installation-guide) — Complete installation procedure for VergeOS.
- [Pre-installation Checklist](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/pre-installation) — Hardware and network verification steps before installation.

{% hint style="info" %}
**Need Help?**

If the PCIe link or storage path remains unstable after checking hardware connections and firmware, contact VergeOS support for assistance.
{% endhint %}
