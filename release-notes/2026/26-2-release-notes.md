---
title: "26.2"
description: "Release notes for VergeOS 26.2: shared multi-writer disks, updated kernel and OS packages, graphical boot, advanced BGP configuration, PTP support, native vSAN alarms, and restored full chassis node replacement."
semantic_keywords:
  - "VergeOS 26.2 release notes new features"
  - "VergeOS shared disks multi-writer clustering"
  - "VergeOS kernel update 6.18"
  - "VergeOS BGP configuration vtysh"
  - "VergeOS Precision Time Protocol PTP"
  - "VergeOS vSAN alarms monitoring"
  - "VergeOS node replacement chassis swap"
use_cases:
  - review_26_2_new_features
  - plan_upgrade_to_26_2
  - configure_shared_disks
  - enable_ptp
  - configure_advanced_bgp
  - monitor_vsan_alarms
  - perform_node_replacement
tags:
  - release-notes
  - vergeos-26
  - shared-disks
  - kernel-update
  - bgp
  - ptp
  - vsan
  - monitoring
  - installer
  - node-replacement
categories:
  - Release Notes
---

# 26.2


{% hint style="info" %}
**Release Information**

- **Release Date**: October 2026  
- **Latest Version**: 26.2.2.1 (October 2026)
- **Previous Version**: 26.1.8 (August 2026)  
- **Upgrade Floor**: 26.1.6 or later  
- **End-of-Life**: TBD
{% endhint %}

## Summary

VergeOS 26.2 is a major feature release. The headline capability is **shared (multi-writer) disks**, which let a single disk be attached to multiple VMs at once and unlock guest-clustered workloads such as Windows Failover Clustering and Cluster Shared Volumes. The release also rebases the platform on an updated kernel and core OS packages, reworks VergeFabric for scale and adds advanced BGP configuration and VLAN load-balancing bond modes, brings full Precision Time Protocol (PTP) support, and significantly expands visibility with a native vSAN alarm framework and per-core CPU statistics. Alongside these, 26.2 includes a large set of stability, security, and usability fixes carried in on the 26.2.x patches.

## Highlights

- **Shared disks for clustered workloads** -- Attach one disk to multiple VMs concurrently for guest-level clustered filesystems and shared-disk HA (Microsoft CSV, Windows Failover Clustering). Shared disks present proper NAA/WWN identity and support SCSI-3 Persistent Reservations.
- **Updated kernel and core OS packages** -- Refreshed base OS packages including a newer 6.18.x kernel, updated firmware and networking drivers, and a modern graphics stack.
- **Graphical boot** -- Nodes now show a clean, branded boot screen with system name and vSAN mount progress, replacing scrolling service logs.
- **Advanced BGP configuration** -- Configure BGP directly from a secured console shell inside the virtual network, with configuration persisted across restarts.
- **Precision Time Protocol (PTP)** -- Enable PTP on the host and pass kvmclock through to guests, with per-node time-sync status on the time dashboard.
- **Super Users group for physical access** -- Physical-access capability is now governed by group membership rather than a standalone user flag.
- **Native vSAN alarms and expanded monitoring** -- A vSAN alarm framework, per-core CPU utilization, and a snapshot-retention alarm improve day-to-day visibility.
- **Node replacement with drives is back** -- Full chassis replacement is supported again through a rebuilt, guided installer flow.

## 26.2.2.1 (October 2026)

VergeOS 26.2.2.1 is a maintenance release focused on storage reliability, cluster availability, and security. It includes a kernel update that
addresses a critical virtualization escape vulnerability, a set of vSAN fixes for shared-disk clustering and node maintenance, improved
update behavior for large environments and PXE nodes, and a collection of UI, audit-log, and permissions corrections.

{% hint style="danger" %}
**Security fix**

The Linux kernel in 26.2.2 is updated to 6.18.57, which includes the fix for [CVE-2026-99999](https://nvd.nist.gov/vuln/detail/CVE-2026-99999) (PWNEscape), a critical vulnerability.
{% endhint %}

### Update Process

{% hint style="warning" %}
**Upgrade Paths to 26.2.2**

Systems on 26.1.6, 26.1.7, or 26.1.8 can upgrade directly to 26.2.2. Systems on 26.0, or on 26.1 earlier than 26.1.6, must first update to [26.1.8.1](26-1-release-notes.md#id-26.1.8.1-october-2026). Release 26.1.8.1 includes a fabric hotfix so systems with 50 or more networks upgrade reliably.
{% endhint %}
on shared disks, and repeated validations no longer leave a VM unable to detect newly attached shared disks


#### Update Process

- **Upgrades to 26.2 must come from 26.1.6 or later.** Systems on earlier releases must first update to a 26.1.6-or-newer build before they can upgrade; the update package enforces this.
- **Optional packages can now be installed with their dependencies and uninstalled cleanly.** Installing an optional package automatically pulls in everything it depends on, and uninstalling one cascades to dependents, so the system is never left in an inconsistent state. This also fixed a regression where a fresh install was incorrectly flagged as needing a reboot.
- **The Private AI service is now an optional download package** rather than being bundled in the ISO, following the same pattern as oVirt. This significantly reduces the base ISO size and download footprint for environments that do not use Private AI; the service can be downloaded and installed on demand.
- **Packages can run a pre-flight script when installed.** Before a package is installed, a script shipped with it can check for conditions such as use of deprecated features and indicate whether the install should proceed. A similar pre-flight check already runs before system updates.
- **Packages now use customer-facing names.** Package aliases were finished and surfaced in the UI: `yb` is now **vergeos-ui**, `ybos` is now **vergeos**, and `yb-help` is now **help**.
- **A hotfix was added so that node1 reboots after node2 during an update.**

Key Changes
Security
Updated the kernel to address PwnEscape (CVE-2026-99999), a critical Linux networking vulnerability that could allow an
untrusted guest virtual machine to escape to the host. Affected systems should be updated as soon as practical.
Fixed an issue where a rejected user creation could still leave a working login. A create request rejected with a validation error no
longer leaves behind an enabled identity with a credential.
Corrected the root permission guard, which determined physical access from the user's internal key rather than the user's actual
physical-access setting. This caused permission edits to fail for some users and left others inadequately protected.
Storage (vSAN)
Fixed an issue where .snap_ snapshots being synced could become stuck in an endless repair loop and lose data. This affected
site syncs in some environments.
Fixed an issue where running VMs on the surviving node of a two-node cluster could fail with I/O errors while the other node was
down for a maintenance reboot. VMs now continue running normally through the maintenance window.
Prevented a node from entering maintenance mode before it is actually redundant, which could occur when reference walks were
long and replays missed their window.
Shared disks now pass I/O errors through to the guest instead of stopping the VM, allowing clustered guests to make their own
failover decisions.
Fixed a case where concurrent boot-partition updates stalled on a vSAN master handoff timeout and then produced SQUASHFS read
errors, even though the update reported success.
Fixed Windows failover-cluster VMs losing recognition of newly attached shared disks after repeated cluster validations.
Fixed SCSI-3 persistent reservation validation failures on shared virtio-scsi disks during Windows cluster validation.
Fixed Fibre Channel device-path mismatches during some HBA failures, where LUNs could end up associated with the wrong device
path.
Increased the multipath read timeout when all nodes are online, so a path that recovers quickly is no longer abandoned prematurely.
Fixed vSAN errors when removing a node from a cluster.
Restored accurate CPU IO Wait reporting. Idle cores no longer display inflated IO Wait values, and the temporary workaround that
suppressed these statistics is no longer needed.
Update & Installation
Systems with 50 or more networks are now handled correctly during upgrade — the network fabric is updated before the main
update begins, avoiding fabric contention on large environments.
A node interrupted by a hard reboot during an upgrade now repairs its kernel mismatch automatically on boot.
Fixed PXE nodes losing network visibility during the update process, which could cause QMP socket errors on VMs.
Optional packages are now correctly marked after an upgrade, so previously installed AI packages can be uninstalled.
Networking
Corrected the bonding options shown when creating or editing an external network, including the primary bond interface field and
bridged-mode selection.
Snapshots
Fixed a snapshot error when a VM has two tags in the same category whose names differ only by letter case. The snapshot now
completes without logging an error.
System & Logging
Cluster edits now write an audit entry to the System Log, including changes such as disabling CPU sleep states and KVM nesting.
User Interface
Fixed column dragging in the VM list view, which could remove columns or leave visual artifacts.
10/26/26, 3:23 PM Release notes 26.2.2 · Wiki · yb / yb · GitLab

Comments
Fixed modal menus stacking on top of each other when opened from the kebab menu.
Improved WebUI and API upload throughput, which had regressed relative to 26.0 in some environments.
Upgrade Notes
PwnEscape is addressed by the kernel included in this release; no manual kernel action is required.
Environments with 50 or more networks should apply this release before attempting further version upgrades, as the fabric update
ordering change is required for a clean upgrade path.

