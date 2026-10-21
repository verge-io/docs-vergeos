---
title: NVMe Controllers Resetting Due to AER
slug: nvme-aer-reset-loop
author: VergeOS Documentation Team
date: 2026-10-21T15:45:00.000Z
semantic_keywords:
  - nvme controller reset aer pcie error
  - multiple nvme reset loop shared path
  - installation boot failure nvme drives
use_cases:
  - troubleshoot_nvme_aer_reset
  - diagnose_shared_path_symptoms
  - stabilize_before_install_retry
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

{% hint style="info" %}
**Key Points**

- When one NVMe drive resets repeatedly, the problem is in that drive or its PCIe link.
- When several NVMe drives reset together in a short window, the problem is in a shared path component.
- Stabilize the shared path or PCIe link before you retry installation.
{% endhint %}

The console or `dmesg` shows NVMe controllers resetting repeatedly with messages like:

```
nvme nvme0: resetting controller due to AER
nvme nvme0: 80/0/0 default/read/poll queues
```

This message indicates that the PCIe link reported an error and the kernel reset the NVMe controller to recover. AER stands for Advanced Error Reporting, a PCIe feature that reports hardware-level errors to the operating system.

## Prerequisites

- Physical or remote management access to the host.

## Understanding AER Reset Patterns

The pattern of resets shows whether the problem is in one NVMe drive or in a shared path that several NVMe drives use.

### Single Controller Resetting

When one NVMe controller resets repeatedly (for example, `nvme0` resets but `nvme1` through `nvme7` remain stable):

- The problem is in that NVMe drive or its PCIe link.
- Check the drive, its PCIe slot, and the PCIe link between the drive and the host.

### Multiple Controllers Resetting Together

When several NVMe controllers (for example, `nvme0` through `nvme7`) reset together within a short window:

- This is a shared-path symptom.
- The problem is not a single failing drive.
- Check the PCIe switch, backplane, power delivery, firmware, and root complex that all the affected drives share.

{% hint style="warning" %}
**Installation and vSAN Boot Failures**

VergeOS installation and vSAN boot can fail when NVMe controllers reset repeatedly. Stabilize the shared path or PCIe link before you retry the installation.
{% endhint %}

## What to Check

### For a Single Resetting Controller

1. Check the NVMe drive.
2. Check its PCIe slot.
3. Check the PCIe link between the drive and the host.

### For Multiple Controllers Resetting Together

1. Check the PCIe switch.
2. Check the backplane.
3. Check power delivery.
4. Check firmware.
5. Check the root complex.
6. Contact your hardware vendor to diagnose the shared path.

## Additional Resources

- [Node Sizing](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/sizing): Hardware requirements for VergeOS, including NVMe and storage controller recommendations.
- [Installation Guide](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/installation-guide): Complete installation procedure for VergeOS.
- [Pre-installation Checklist](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/pre-installation): Hardware and network verification steps before installation.

{% hint style="info" %}
**Need Help?**

If the PCIe link or shared path remains unstable after checking hardware connections and firmware, contact VergeOS support for assistance.
{% endhint %}
