---
title: "Tenant Isolation Hardening"
description: "Harden VergeOS tenant isolation: limit Layer 2 network grants, control tenant access to system snapshots, and prepare a tested network containment plan."
semantic_keywords:
  - "VergeOS tenant isolation hardening"
  - "tenant layer 2 network grants"
  - "expose system snapshots tenant"
  - "tenant network containment isolate"
use_cases:
  - restrict_tenant_layer2_networks
  - control_tenant_snapshot_access
  - plan_tenant_network_containment
tags:
  - security
  - hardening
  - tenants
  - multi-tenancy
  - isolation
  - layer-2
  - snapshots
categories:
  - Security
---

# Tenant Isolation Hardening

This page covers tenant network attachments, snapshot access, and network containment. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

## TEN01: Authorize tenant Layer 2 attachments

**Default:** A tenant has no Layer 2 grants until you add one. A new grant is enabled.

**Configure:** In the tenant's **Layer 2 Networks**, add only approved parent networks. Disable or delete grants that are no longer needed.

**Verify:** Only approved networks show in the list. From the tenant, a NIC cannot attach to an ungranted network, and other tenants' management addresses are not reachable.

## TEN02: Control tenant access to historical snapshots

**Default:** **Expose System Snapshots** is on, so tenant administrators can restore from the provider's system snapshots.

**Configure:** Edit the tenant and clear **Expose System Snapshots** unless the tenant is authorized to do its own recovery.

**Verify:** As the tenant administrator, snapshot visibility matches your policy. A parent administrator can still restore the tenant.

## TEN03: Prepare tenant network containment

**Default:** Depends on the tenant's networks and upstream connections.

{% hint style="warning" %}
**Isolate Network** blocks network traffic only. It does not freeze storage or remove a compromise. Do not test it on a production tenant.
{% endhint %}

**Configure:** Keep tenant network rules, permissions, quotas, and service exposure current. Document when to use **Isolate Network** and how to restore the network.

**Verify:** On a disposable tenant, run **Isolate Network**. Traffic that worked before is blocked. Record the guest power state and whether guest storage writes continue. After you restore the network, traffic returns.

## Related pages

* [Tenants (Virtual Data Centers)](../tenants/overview.md)
* [Configure Tenant Layer 2 Networks](../tenants/layer-2-networks.md)
* [Modifying Tenants](../tenants/tenant-modifications.md)
* [Tenant Snapshots](../tenants/tenant-snapshots.md)
* [Tenant Restores](../tenants/tenant-restores.md)
