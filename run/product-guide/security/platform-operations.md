---
title: "Platform Operations Hardening"
description: "Harden VergeOS platform operations: apply supported updates safely, isolate and manage BMC access, and keep owner inventory and recurring security reviews."
semantic_keywords:
  - "VergeOS supported update process hardening"
  - "BMC IPMI out-of-band network isolation"
  - "security owner inventory and review cadence"
  - "pre-update snapshot rollback planning"
use_cases:
  - apply_supported_updates_safely
  - isolate_bmc_management_network
  - manage_bmc_credentials
  - schedule_recurring_security_reviews
tags:
  - security
  - hardening
  - updates
  - ipmi
  - bmc
  - out-of-band
  - operations
categories:
  - Security
---

# Platform Operations Hardening

This page covers software updates, out-of-band (BMC) access, and the ownership and review work that keeps a hardened system hardened. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

## OPS01: Use supported updates with bounded rollback exposure

**Default:** Update checks, installation, and reboot behavior depend on the cluster settings.

{% hint style="danger" %}
Do not manually replace packaged components or stop appserver, vSAN, or service VM services as hardening. Either action can cause an outage.
{% endhint %}

**Configure:**

1. In **System > Updates > Edit Settings**, keep **Auto Check For Updates** on. Keep **Auto Update** and automatic reboots off unless a change process governs them. Use **Warm Reboot (Fast)** only if you tested it.
2. Before each update, review the release notes and pre-install checks, and confirm cluster and tenant health.
3. Turn on **Take System Snapshot on Update**. Its snapshot expires after 6 hours by default. Set a longer expiration if your checks take longer, for example 24 to 72 hours.
4. Keep spare capacity. Keep **Max vSAN Usage Percentage** at 80, the default.
5. Update multiple clusters in stages.

**Verify:** In **System > Updates**, confirm the version and status. After an update, confirm the pre-update recovery point exists and storage, VMs, networks, and applications are healthy. These checks do not prove that a rollback works.

## OPS02: Isolate BMC access and manage BMC credentials at their source

A BMC controls node power and console, so protect it separately from tenant networks.

**Default:** BMC accounts and access settings are managed on the BMC.

**Configure:**

1. Put BMCs on a dedicated out-of-band VLAN or physical network, reached only through ACLs, VPN, or jump hosts. Do not NAT a BMC to a public address.
2. On each BMC, set non-default accounts, strong passwords, HTTPS, MFA where supported, and current firmware.
3. In **Infrastructure > Nodes**, edit each node and enter the matching IPMI address, user, and password. Keep **Capture System Logs** on, turn off **Send/Receive LLDP Advertisements** on nodes that connect to untrusted Layer 2 networks, and keep **PXE Network** on the provisioning network.

VergeOS does not create or rotate the BMC account. Rotate it on the BMC, then update the node. If a BMC falls back from IPMI LANplus to legacy LAN, plan to update or replace it.

**Verify:** Confirm BMCs are reachable from approved paths only, not from workload or public networks. With authorization, run **IPMI > Test** on the node (no power operations) and confirm **IPMI Status** shows **OK**. Check SEL capacity. Test the BMC login itself; isolation and a saved password do not prove the BMC enforces authentication.

## OPS03: Maintain owner inventory and recurring boundary reviews

One configuration pass cannot prevent drift.

**Default:** The operating policy sets ownership, review frequency, and physical access rules.

**Configure:**

1. Assign an owner to each public IP and NAT rule, service account and API key, VPN peer, certificate and CA, BMC, and recovery target.
2. Keep these boundaries separate per the design: Core and vSAN, management, out-of-band, tenant and VM, DMZ, NAS, backup, and replication.
3. Protect racks, consoles, BIOS/UEFI, and USB boot. Keep server, NIC, HBA, BMC, switch, and drive firmware current.
4. Store encryption, recovery, and break-glass secrets under separate roles.
5. Schedule reviews, for example monthly access, exposure, and log-delivery reviews, and quarterly restore, VPN, and break-glass exercises.

**Verify:** Compare the inventory with the services that are actually reachable. Confirm no public port forward exposes node SSH, API, or vSAN ports without an approved exception. Record review evidence and open deviations.

## Related pages

- [Licensing and Software Updates](../system/update-settings.md)
- [VergeOS Version Update Guide](../operations/sop-update.md)
- [IPMI](../system/ipmi.md)
- [The System Event Log (SEL)](../system/sel.md)
- [Nodes Overview](../system/nodes-overview.md)
- [API Keys](../system/api-keys.md)
- [Server Certificates](../system/certificates.md)
