---
title: "VergeOS Security Baseline"
description: "A baseline of hardening controls for VergeOS: what each control protects, the setting to choose, where to configure it, and how to verify the result."
semantic_keywords:
  - "VergeOS security baseline hardening guide"
  - "harden VergeOS administrative access network storage"
  - "security configuration controls and verification"
  - "VergeOS security checklist compliance review"
use_cases:
  - harden_new_vergeos_deployment
  - review_existing_security_configuration
  - prepare_security_audit
  - track_hardening_progress
tags:
  - security
  - hardening
  - baseline
  - compliance
  - best-practices
  - checklist
categories:
  - Security
---

# VergeOS Security Baseline

The security baseline is a set of hardening controls for VergeOS. Each control tells you what it protects, the setting to choose, where to configure it, and how to verify the result.

## How to use this baseline

1. Select the areas that apply to your deployment.
2. For each control, compare the default to your security policy.
3. Configure the control in the VergeOS UI.
4. Complete the **Verify** steps for the control.
5. Record the result in the [Hardening Checklist](checklist.md).

Example values are starting points, not required settings. Select values that agree with your security policy and workload requirements.

{% hint style="info" %}
Defaults can change between releases. Before you change a setting, confirm its current value on the installed release.
{% endhint %}

## Before you start

{% hint style="warning" %}
Keep a working recovery path while you change identity, certificate, or routing settings. A mistake in these areas can lock all administrators out of the system.
{% endhint %}

- Make sure a second administrator account with tested access exists.
- Use test accounts and isolated workloads for lockout, denial, and recovery tests.
- For each control, test the action that must succeed and the action that must fail.

## Control areas

| Area | Controls | Covers |
| --- | --- | --- |
| [Identity and access](identity-access.md) | IAM01–IAM13 | MFA, passwords, lockout, sessions, roles, API keys, OIDC, break-glass access |
| [Management access and TLS](management-tls.md) | TLS01–TLS04 | Certificates, cipher suites, HTTP listeners, trusted CAs |
| [Networking](networking.md) | NET01–NET13 | Management and replication sources, firewall rules, IPv6, DNS, VPN, routing, NTP |
| [Compute and VMs](compute-vms.md) | HV01–HV05 | CPU mitigations, nested virtualization, passthrough, secure boot, consoles |
| [Tenant isolation](tenants.md) | TEN01–TEN03 | Layer 2 attachments, tenant snapshots, network containment |
| [Storage and recovery](storage-recovery.md) | STO01, STO03–STO07 | vSAN encryption, immutable snapshots, replication, Site Sync, recovery tests |
| [NAS](nas.md) | NAS01–NAS11 | Volume encryption, SMB, NFS, antivirus, NAS sync |
| [Logging and monitoring](logging-monitoring.md) | AUD01–AUD06 | Log export, timestamps, API rate limits, alarms |
| [VergeIQ](vergeiq.md) | AI01–AI02 | AI permissions, chat history retention |
| [Integrations](integrations.md) | INT01–INT05 | Repositories, catalogs, webhooks, SMTP, authentication sources |
| [Platform operations](platform-operations.md) | OPS01–OPS03 | Updates, BMC access, inventory and reviews |
