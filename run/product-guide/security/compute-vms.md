---
title: "Compute and VM Hardening"
description: "Harden VergeOS compute and VMs: keep CPU mitigations on, limit nested virtualization and passthrough, use Secure Boot and vTPM, and restrict consoles and exports."
semantic_keywords:
  - "VergeOS CPU security mitigations cluster"
  - "nested virtualization device passthrough risk"
  - "VM Secure Boot virtual TPM"
  - "restrict VM console and snapshot export"
use_cases:
  - keep_cpu_mitigations_enabled
  - limit_nested_virtualization
  - enable_guest_secure_boot_vtpm
  - restrict_vm_console_access
  - constrain_sriov_vgpu_passthrough
tags:
  - security
  - hardening
  - virtual-machines
  - clusters
  - passthrough
  - secure-boot
  - tpm
  - sr-iov
categories:
  - Security
---

# Compute and VM Hardening

This page covers cluster CPU protections and the VM settings that control guest isolation, boot integrity, console access, and exports. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

## HV01: Keep CPU security mitigations enabled

Mitigations stop speculative execution attacks from leaking data between guests.

**Default:** **Disable CPU Security Mitigations**, **Disable Speculative Store Bypass**, and **Disable SMT** are cleared.

**Configure:** In **System > Clusters**, edit the cluster and keep **Disable CPU Security Mitigations** cleared. For mixed-trust workloads, decide on the speculative store bypass and SMT options from your CPU risk assessment. Do not disable mitigations for a benchmark. Disabling SMT costs significant performance and is not a baseline requirement.

**Verify:** After any required reboot, check `/sys/devices/system/cpu/vulnerabilities/*` on every node against the CPU vendor advisories.

## HV02: Limit nested virtualization and device passthrough

**Default:** **Nested Virtualization** is off for the cluster and each VM. Passthrough requires an explicit device assignment.

**Configure:**

1. Keep **Nested Virtualization** cleared on the cluster and on each VM that does not need it.
2. In each VM's **Devices**, remove passthrough devices that are not in use.
3. Restrict who can edit VMs and devices (IAM06 in [Identity and Access Hardening](identity-access.md)).

**Verify:** After a power cycle, the guest does not report hardware virtualization. An ordinary VM operator cannot assign a host device.

## HV03: Verify guest boot integrity and protect guest encryption keys

Secure Boot and a virtual TPM let a compatible guest verify its boot chain and seal encryption keys.

**Default:** **UEFI** and **Secure Boot** are cleared. A VM has no TPM until you add one.

{% hint style="warning" %}
Save the guest's encryption recovery keys before you change the boot mode or TPM. A change can lock the guest out of its encrypted disks.
{% endhint %}

**Configure:**

1. If the guest boots with legacy BIOS, convert the guest OS to UEFI first.
2. Edit the VM and select **UEFI** and **Secure Boot**.
3. In **Devices**, click **New** and add a **Trusted Platform Module (vTPM)**. Set **Version** to **2.0** and **Model** to **CRB**, if the guest supports it.

Guest encryption is separate from vSAN encryption. A vTPM alone does not prove measured boot.

**Verify:** In the guest, Secure Boot is on and the TPM is present. On a test guest, an unsigned boot image is rejected.

## HV04: Restrict VM consoles and VM exports

**Default:** **Console Type** is **VNC**. **Console Password Enabled** is cleared. **Allow Export** is selected.

**Configure:**

1. Grant VM permissions only to approved console operators. VM read permission includes console access.
2. To add a second challenge, power off the VM and select **Console Password Enabled**. You cannot change this setting while the VM runs.
3. On VMs with protected data, clear **Allow Export**. This removes the VM from NAS VM Export jobs. It does not control access to existing snapshots; use permissions for that.

**Verify:** An unauthorized account cannot open the console. New NAS VM Export runs do not include the VM. Console ports are unreachable from untrusted zones. Check other export paths separately.

## HV05: Constrain SR-IOV, vGPU, and direct-device privileges

Passthrough hardware can bypass virtual device isolation.

**Default:** Depends on the device, hardware, and driver.

**Configure:**

- Require approval for each PCI, USB, GPU, direct-disk, and NAS passthrough.
- On SR-IOV NICs, keep **Spoof Checking** on and **Trust** off. Set VLAN and rate limits where needed.
- Keep vGPU debugging, profiling, and unified memory off unless a workload needs them.
- Attach ISO and recovery media read-only.
- Do not use NFS or CIFS passthrough to get around NAS access policy.

Passthrough can block live migration. Check migration and recovery for each affected VM.

**Verify:** Check the VM's **Devices**, **NICs**, and **Drives**. On an isolated test VM, an unauthorized MAC address, VLAN, or rate above the limit fails.

## Related pages

- [Cluster Settings](../system/cluster-settings.md)
- [Device Passthrough Overview](../system/device-pass-overview.md)
- [SR-IOV NICs](../system/sriov-nics.md)
- [NVIDIA vGPU Configuration](../system/nvidia-vgpu-configuration.md)
- [Virtual Machine Fields](../virtual-machines/vm-field-descriptions.md)
- [Using the Virtual Machine Remote Console](../virtual-machines/vm-remote-console.md)
- [VM Export Volume](../virtual-machines/vm-export-volume.md)
- [Permissions](../system/permissions.md)
