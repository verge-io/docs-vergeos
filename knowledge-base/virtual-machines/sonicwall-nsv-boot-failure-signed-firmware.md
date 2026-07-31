---
title: SonicWall NSv 7.1.1+ Will Not Boot on VergeOS
slug: sonicwall-nsv-boot-failure-signed-firmware
author: VergeOS Documentation Team
date: 2026-07-31T00:00:00.000Z
semantic_keywords:
  - sonicwall nsv virtual firewall won't boot vergeos
  - sonicwall nsv invalid firmware detected import
  - sonicos 7.1.1 signed ovmf secure boot firmware
  - import sonicwall nsv kvm qcow2 ova vhdx fails
  - custom efi firmware nvram vergeos not supported
use_cases:
  - import_sonicwall_nsv_into_vergeos
  - run_virtual_firewall_on_vergeos
  - troubleshoot_vm_boot_failure_after_import
categories:
  - Troubleshooting
  - Migration
editor: markdown
dateCreated: 2026-07-31T00:00:00.000Z
description: >-
  SonicWall NSv firewalls on SonicOS 7.1.1+ fail to boot after import into
  VergeOS because the appliance requires SonicWall's signed OVMF firmware.
  Custom EFI firmware support is coming in Q3 2026.
tags:
  - vm
  - import
  - migration
  - firewall
  - sonicwall
  - nsv
  - secure boot
  - ovmf
  - uefi
  - efi
  - firmware
  - won't boot
  - not booting
  - invalid firmware
  - troubleshooting
---

# SonicWall NSv 7.1.1+ Will Not Boot on VergeOS

SonicWall NSv virtual firewalls on SonicOS 7.1.1 and later do not currently boot after import into VergeOS. This article explains why the appliance fails to start and what your options are in the meantime.

{% hint style="info" %}
**Support coming in Q3 2026**

VergeOS will add support for custom EFI firmware in Q3 2026. This will allow the SonicWall NSv appliance to boot on VergeOS. Until that support ships, use one of the alternatives described below.
{% endhint %}

## Symptoms

- You import a SonicWall NSv appliance into VergeOS and it fails to boot.
- The console shows a firmware validation error such as `Invalid firmware detected`.
- The failure is the same no matter which source format you import from — KVM/QCOW2, VMware OVA, or Hyper-V VHDX.

## Overview

SonicWall ships the NSv image with its own custom OVMF firmware files — `OVMF_CODE.sw.fd` and `OVMF_VARS.sw.fd` — that carry SonicWall-specific Secure Boot certificates. At boot, SonicCoreX checks that it is running on exactly that firmware and aborts on anything else.

VergeOS builds and manages each VM's UEFI variable disk from standard OVMF templates. There is currently no supported way to swap the EFI disk's media source through the UI or API. The appliance cannot see SonicWall's custom firmware files, so its boot-time firmware check fails and the NSv does not start.

{% hint style="info" %}
**Why every import format fails the same way**

The block is in the appliance's firmware validation, not in any one disk format. Converting or re-importing the image — QCOW2, OVA, or VHDX — does not change the outcome, because none of those paths supply SonicWall's signed `.fd` firmware.
{% endhint %}

{% hint style="info" %}
**Applies to SonicOS 7.1.1 and later**

Earlier SonicOS builds that did not enforce the signed-firmware check are not affected in the same way. The behavior described here is specific to NSv on 7.1.1+.
{% endhint %}

## Options in the Meantime

Any virtual firewall that boots on standard UEFI firmware runs well on VergeOS, as a VM or inside a tenant. It can fill the role until NSv support arrives.

If you want to stay on SonicWall today, run the firewall on physical SonicWall hardware and connect it to your VergeOS environment over the network.

{% hint style="info" %}
**Need Help?**

If you are planning a firewall migration into VergeOS and want to talk through options, contact the VergeOS support team.
{% endhint %}
