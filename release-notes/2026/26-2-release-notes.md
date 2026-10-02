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
- **Previous Version**: 26.1.8 (August 2026)  
- **Upgrade Floor**: 26.1.6 or later  
- **End-of-Life**: TBD
{% endhint %}

## Summary

VergeOS 26.2 is a major feature release. The headline capability is **shared (multi-writer) disks**, which let a single disk be attached to multiple VMs at once and unlock guest-clustered workloads such as Windows Failover Clustering and Cluster Shared Volumes. The release also rebases the platform on an updated kernel and core OS packages, reworks VergeFabric for scale and adds advanced BGP configuration and VLAN load-balancing bond modes, brings full Precision Time Protocol (PTP) support, and significantly expands visibility with a native vSAN alarm framework and per-core CPU statistics. Alongside these, 26.2 includes a large set of stability, security, and usability fixes carried in on the 26.2.0.x and 26.2.1 patches.

## Highlights

- **Shared disks for clustered workloads** -- Attach one disk to multiple VMs concurrently for guest-level clustered filesystems and shared-disk HA (Microsoft CSV, Windows Failover Clustering). Shared disks present proper NAA/WWN identity and support SCSI-3 Persistent Reservations.
- **Updated kernel and core OS packages** -- Refreshed base OS packages including a newer 6.18.x kernel, updated firmware and networking drivers, and a modern graphics stack.
- **Graphical boot** -- Nodes now show a clean, branded boot screen with system name and vSAN mount progress, replacing scrolling service logs.
- **Advanced BGP configuration** -- Configure BGP directly from a secured console shell inside the virtual network, with configuration persisted across restarts.
- **Precision Time Protocol (PTP)** -- Enable PTP on the host and pass kvmclock through to guests, with per-node time-sync status on the time dashboard.
- **Super Users group for physical access** -- Physical-access capability is now governed by group membership rather than a standalone user flag.
- **Native vSAN alarms and expanded monitoring** -- A vSAN alarm framework, per-core CPU utilization, and a snapshot-retention alarm improve day-to-day visibility.
- **Node replacement with drives is back** -- Full chassis replacement is supported again through a rebuilt, guided installer flow.

## OS, Installer & Update Process

### Operating System

- **VergeOS 26.2 is rebased on an updated kernel and core OS packages.** The underlying operating system was refreshed including a newer kernel (6.18.x), updated firmware and networking drivers, and a modern graphics stack. This brings newer hardware support and a more current set of system utilities.
- **The boot process is now graphical.** Nodes display a clean, branded boot screen instead of scrolling service logs, showing the system name and vSAN mounting progress. If a vSAN needs to be interrupted while mounting, or an encryption key must be entered because no USB key is present, the boot screen now prompts for it properly — the encryption key prompt on an encrypted node no longer overlays the boot status text.

### Installer

- **Node replacement now supports a full chassis replacement (drives and all).** The installer's node-replace path has been rebuilt as a guided flow: choose **Node Replace**, pick the node to replace, then explicitly choose the drive disposition (new drives, keep existing drives, or PXE boot). The previous dead-end that blocked the "no, do not keep drives" answer is gone, and drives are matched to tiers with size validation so a chassis swap can be completed self-service.
- **The installer's Controller role label no longer implies a two-node limit.** The `(node1/node2)` wording was dropped, since any node can be added as a Controller — which is how an N+1 system is converted to N+2.
- **The installer now reports licensing limits when adding nodes.** Attempting to install more nodes than a license permits now produces a clear message identifying the license restriction, instead of a generic failure that looked like a configuration problem.
- **Single-node installations no longer require a core network.** VergeOS can be deployed on a single node using only two physical NICs, with both available for external and workload networking instead of dedicating one to a core-network loopback. There is no peer node, so no inter-node traffic path is needed.
- **Fixed PXE boot on UEFI nodes**, and fixed an issue where a PXE install could appear to fail when it had actually succeeded.

### Update Process

- **Upgrades to 26.2 must come from 26.1.6 or later.** Systems on earlier releases must first update to a 26.1.6-or-newer build before they can upgrade; the update package enforces this.
- **Optional packages can now be installed with their dependencies and uninstalled cleanly.** Installing an optional package automatically pulls in everything it depends on, and uninstalling one cascades to dependents, so the system is never left in an inconsistent state. This also fixed a regression where a fresh install was incorrectly flagged as needing a reboot.
- **The Private AI service is now an optional download package** rather than being bundled in the ISO, following the same pattern as oVirt. This significantly reduces the base ISO size and download footprint for environments that do not use Private AI; the service can be downloaded and installed on demand.
- **Packages can run a pre-flight script when installed.** Before a package is installed, a script shipped with it can check for conditions such as use of deprecated features and indicate whether the install should proceed. A similar pre-flight check already runs before system updates.
- **Packages now use customer-facing names.** Package aliases were finished and surfaced in the UI: `yb` is now **vergeos-ui**, `ybos` is now **vergeos**, and `yb-help` is now **help**.
- **A hotfix was added so that node1 reboots after node2 during an update.**

## Storage (vSAN)

- **Shared disks are now supported for clustered workloads.** A disk can be marked as shared and attached to multiple VMs at once, allowing guest-level clustered filesystems and shared-disk HA stacks such as Microsoft Cluster Shared Volumes (CSV) and Windows Failover Clustering to run on VergeOS. Shared disks use a SCSI interface, and I/O is no longer serialized or exclusively locked when a disk is flagged shared — write coordination is left to the guest cluster.
- **Fixed a vSAN instability when deleting a node at the same time as a repair-count query.** Resolved a timing scenario in which removing a node at the exact moment the system queried repair counts could crash the instability.
- **Improved Fibre Channel path failover.** vSAN devices now fail over to a surviving, fully-available FC fabric path on a read error instead of remaining closed until the original path returns, and a background health monitor now tracks alternate paths.
- **SSD health is now based on remaining endurance rather than power-on hours alone.** The drive health alarm now evaluates remaining endurance (percentage life used) reported by SMART, using power-on hours only when a drive provides no endurance data. The power-on-hours gauge on the node drive dashboard now shows raw hours instead of a percentage scaled against a misleading threshold.
- **Fixed SMART statistics getting stuck as unavailable.** A drive with a healthy SMART feed could permanently show no SMART stats after a transient controller failure, because a later write in the same scan reverted the recovery. The recovery path was corrected so the flag clears without requiring an appserver restart.
- **vSAN can now raise alarms.** The vSAN gained a native alarm capability with dedicated alarm types, exposed for use in the UI and logged to syslog.
- **Improved vSAN diagnostics.** vSAN diagnostics now use vcmd for inode lookups instead of the legacy find command, and more vSAN directories are included in diagnostic bundles.
- **Volumes with a stale file handle are now reported in the UI.** Added error handling and reporting around the stale file handle condition on export volumes, so a volume that needs to be reset is surfaced to the user instead of silently failing scheduled exports.

## Virtual Machines & Compute

- **VMs now report unique serial numbers instead of sharing the host serial.** Each VM is given its own deterministic SMBIOS serial number, so asset-management and inventory tools can distinguish VMs that previously all appeared as a single device.
- **Pass-through and vGPU devices now work beyond PCI domain 0000.** Systems with more than one PCI domain can pass through devices on every domain; devices in domain 0000 continue to display without the domain prefix, while other domains show the full address.
- **Removed unsupported NVIDIA vGPU driver versions.** Following the kernel update, only 16.14+, 19.4+, and 20.0+ drivers are supported — 17.x and 18.x no longer function. Updates to this release are blocked while an unsupported version is installed in a resource group.
- **Editing a vGPU resource group no longer overwrites its description.** The saved description is preserved instead of being replaced by the driver-file name.
- **Added the CPU types introduced with QEMU 11.** ClearwaterForest, Diamond Rapids, EPYC-Turin, and SierraForest are now selectable, and the CPU flag warning for emulated types was corrected.
- **VRAM size can now be configured per VM.** A new field on the video adapter settings allows more than the adapter default.
- **Fixed a migration stall when workloads sharing an HA group outnumbered nodes.** A VM belonging to an HA group could fail to finish migrating when the group had more members than the system had nodes.
- **VM clones now honor the preserve options when quiescing.** Cloning a running VM with a guest agent no longer reuses the source MAC address when the preserve option is not selected.
- **A Preferred Node column is available in the VM list**, hidden by default.
- **The VM list can now show an IP Address column** populated from the Guest Agent, with sorting and filtering.
- **Power-on failures due to insufficient resources now list the reasons**, naming the nodes considered and why each was unable to host the VM.
- **Added a grace period for guest agent warnings.** A VM that is powering off no longer logs a guest agent warning during the normal shutdown window.

## Networking & Fabric

- **BGP advanced configuration.** Administrators configuring BGP can now drop into a vtysh shell within the virtual network and run BGP commands directly, providing a flexible path for the complex configurations that are hard to express through the UI. Shell access is secured to prevent breaking out, and manual configuration is saved to disk so it persists across restarts.
- **Fabric performance with hundreds of networks.** Reworked the fabric to keep up on systems running large numbers of networks (reproduced at 600). Previously, fabric change processing could take long enough to miss the heartbeat window, allowing the core to time out and fail over.
- **Fabric alarms no longer fire for nodes that are intentionally gone.** Deleting a node or shutting it down gracefully no longer generates fabric alarms across the remaining nodes. Previously the fabric monitor was not notified when a node departed, and every node raised alarms for a node that was no longer part of the system.
- **New alarm for stranded virtual wires.** When a virtual wire connecting two networks cannot be co-located because the two network halves land in different clusters, VergeOS now raises a "Wired Network on Different Cluster" alarm instead of leaving the wire silently stranded and the layer-2 link broken. Wired partner networks are now strictly co-located during power-on and migration where possible.
- **Large firewall rulesets no longer mark a vnet unresponsive.** Action-triggered firewall rule refreshes now run asynchronously, so a network applying thousands of rules no longer stalls its heartbeat and gets flagged unresponsive and power-cycled. Only one refresh runs per vnet at a time, and per-rule processing yields so other work continues to be scheduled during very large rulesets.
- **NIC multi-queue now enabled on hotplug.** Hotplugging a NIC onto a VM with multi-queue enabled now correctly configures multiple receive and transmit queues in the guest, matching the behavior of a NIC present at power-on.
- **Raised NIC limit for tenant nodes.** Tenant nodes (and other non-VM machines) can now attach up to 255 NICs, up from the previous blanket 31-NIC cap, supporting the L2 tenant networks feature that needs to attach many interfaces. The 31-NIC limit is retained for VMs.
- **DHCP broadcast option for dynamic external networks.** Added an opt-in option (off by default) that makes a dynamic external network's DHCP client request broadcast replies. This lets networks behind cable/ISP DHCP servers that only answer broadcast-flagged BOOTP requests obtain a lease, with default behavior unchanged.
- **Advanced network options collected into a collapsible section.** The network form now groups less-frequently-used options — probe/statistics, tracing, mirror logs, rate limiting, proxy, PXE, and VXLAN multicast — into a collapsible Advanced card placed after the Network DHCP section, matching the pattern used on the VM page. DHCP-specific options appear only when the network IP type is Dynamic.
- **VLAN load balancing bond modes for external networks.** Added software bond modes to VergeFabric External Networks beyond the existing active-backup mode, starting with Balance-SLB (source load balancing), which rebalances VM traffic across physical uplinks by measured per-source-MAC load with no switch-side configuration required. This delivers both redundancy and bandwidth aggregation without guest OS configuration.

## VMware / Veeam / oVirt Integration

- **VMware backup transfers are significantly faster.** The VMware service now uses asynchronous NFC I/O buffers (nfcAio) for NBD transfers, alongside broader performance tuning when retrieving VM lists.
- **VMware tags and categories are now carried across with imported backups.** Tag and category associations are preserved on import, tag and category descriptions are imported with the objects, tags that share a name but belong to different categories are kept distinct, and a category's "one tag per object" cardinality is mapped to Single Tag Selection.
- **The oVirt SSO endpoint now enforces two-factor authentication.** Password-only logins through the oVirt-compatible OAuth endpoint are rejected for accounts with TOTP enabled, matching the standard interactive login path.
- **Fixed the UUID not being preserved when restoring an oVirt VM over its source.** Restoring a VM back over itself previously produced a new UUID and broke subsequent Veeam backup jobs; the original UUID is now retained.
- **Fixed restores of VMs with special characters in their names.** Restoring such a VM to a tenant no longer fails with a null-value error, and the translated name shown in Veeam is now handled consistently.
- **VMware imports can now flag the QEMU Guest Agent per batch.** When importing a batch of VMs whose guest OS already has the agent installed, the Guest Agent setting can be applied at creation time for the whole batch rather than per VM afterwards.
- **OVA and VMware imports no longer select a deprecated machine type.** Imported VMs with a SCSI controller are created with a current machine type instead of a deprecated Q35 version, including when cloning from OVF and VMX sources.

## Users, Security & Access Control

- **Introduced a dedicated Super Users group to manage physical access.** Physical-access capability (console, BMC/IPMI, and hardware-level operations) is now governed by membership in a Super Users group rather than by a standalone user flag. The existing physical-access toggle is retained for backwards compatibility, but it now simply adds or removes the user from that group, and granting it no longer implicitly confers built-in administrator permissions.
- **Deleted users no longer leave orphaned VM favorites behind.** When a user was deleted and later recreated with the same name, their profile previously inherited the favorite VMs from the deleted account. Favorite records are now cleaned up when either the user or the favorite VM is removed.
- **The warning shown when deleting a user now only appears when that user actually owns VMs**, and the owned VMs are listed. Deleting multiple users expands this warning across all affected accounts.
- **Added a configurable idle session timeout for shell and SSH sessions.** Administrators can now set an idle timeout for CLI sessions via an advanced system setting, supporting hardening requirements such as CIS, DISA STIG, and NIST 800-53 session-termination controls. Sessions default to remaining open until this setting is configured.

## Alarms & Monitoring

- **Raised an alarm when system snapshots are held well past their expiration.** A snapshot that should have expired but is being retained — for example due to the minimum-snapshot setting or a non-redundant system — now generates an alarm so it can be investigated.
- **Fixed snoozed alarms permanently showing as snoozed in the alarms list view.** Once a snooze period expired, the alarm correctly reappeared on its dashboard, but the overall alarms list continued to display it as snoozed until the page was reloaded.
- **Acknowledging a snoozable alarm now suspends it indefinitely.** Acknowledging an alarm previously snoozed it only for the maximum snooze period; it now remains acknowledged permanently while still being visible in the list.
- **Added per-core CPU utilization to the UI.** Node CPU views now break utilization down by individual physical core, making it possible to spot a single pegged core, NUMA imbalance, or a runaway service without SSHing to the node and running a third-party tool.

## Time Sync

- **PTP (Precision Time Protocol) support.** VergeOS can now enable PTP on the host and pass the kvmclock parameter through to guests, allowing guests that support PTP to synchronize accurately to the host clock. This extends the earlier PTP startup work into full end-to-end support.
- **Time sync status on the time dashboard.** The Time Settings dashboard now shows time sync status for each node for both NTP and PTP, and raises an alarm when a node has been out of sync for more than two minutes. NTP settings for Max Clocks, Min Clocks, and Min Sane were also added.

## User Interface & Files

- **Enhanced table views with resizable and reorderable columns.** Column widths and ordering can now be adjusted and are retained per browser via local storage. Resetting a view restores both the sizing/order and the hide/show column state.
- **Fixed Tags column rendering in list views.** The Tags column now displays all tags that fit the available column width rather than capping the list at five, handles tags whose names contain commas correctly, and no longer misdirects clicks on the overflow indicator to an unrelated tag.
- **Subtenants now correctly inherit themes they have been granted access to.** A subtenant created under a tenant with read-only access to a host theme previously did not pick up the theme's styling; it now renders consistently with its parent.
- **The node serial console is now resizable.** A control in the console window lets physical-access users set the console dimensions, and the chosen size persists in the browser. The console page also enforces a hard maximum size so it cannot be sized beyond the browser window.
- **Improved SR-IOV resource group rule editing.** Administrators can now select which nodes supply SR-IOV devices without having to choose "None" and force a driver reload on every node in the system.
- **Added a Count field for USB devices shared to a tenant.** USB passthrough device assignments now support selecting multiple devices, matching the behavior of other passthrough types.
- **Fixed file-access filters.** Filtering in the tenant file access view now returns correct results instead of ignoring the selected criteria.
- **Added a breadcrumb showing the file when viewing references.** The references view now indicates which file it belongs to, and clearly distinguishes a file that has no references rather than showing a blank list.
- **Added an audit log entry when a file is given to a tenant.** Adding a file to a tenant now records what was added, when, and by whom — useful for tracking sensitive file transfers.
- **Expired and deleted public file links no longer remain usable.** Previously, a public link could still be used to download the file after it was deleted or after its expiration passed. Links now stop working as intended, and the associated audit log entry for an expired link now reads "Link Expired" rather than "Link Deleted."
- **Fixed capitalization of CPU and RAM usage history labels** for consistency across the usage pages.
- **Fixed webhook retries being silently ignored.** Webhook deliveries now honor the configured retry count instead of making exactly one attempt regardless of the setting.
- **Fixed loader spinner behavior.** The branded spinner now renders above page content rather than behind text, and now appears when an action is applied to more than one selected item rather than only for single-item actions.

## Recipes, Tenants & Sites

- **Recipes remain editable after a referenced object is deleted.** Previously, if an object referenced by a recipe (such as a network) was deleted, the VM or object built from that recipe became permanently unmodifiable. Recipe-tracked fields can now be edited even when a referenced object no longer exists.
- **Fixed recipe questions being attached to the wrong recipe.** Cloned questions could carry a section belonging to a different recipe, so the same question appeared on one recipe and was missing from the other — and the affected recipe could not remove it. Questions are now validated against their recipe and section.
- **A sync destination that is not actively syncing now shows as "Idle" instead of "Offline."** The previous wording implied the sync was broken or non-functional, prompting unnecessary troubleshooting when the destination was healthy and simply waiting for its next scheduled run.
- **Fixed remote snapshot expiration edits on the remote site not persisting.** Changing a remote snapshot's expiration now updates the remote expiration record alongside the local edit, so the value no longer reverts on the next refresh.
- **Changed how tenant snapshots are cleaned up within system snapshots**, improving consistency of snapshot cleanup during site and system operations.

## System Stability & Performance

- **Fixed a controller crash when backup replication filled storage.** The controller now handles out-of-space conditions on a backup system gracefully instead of crashing and taking production down with it, preventing any cascading outages seen during site-to-site replication.
- **Fixed fabric heartbeat failures on systems with many networks.** Reworked the fabric so it processes topology changes quickly enough to keep up when a node accumulates hundreds of networks. Previously a node with too many vxlan devices could miss the heartbeat window, get fenced, and cascade the failure across the cluster as its workloads migrated.
- **Fixed the appserver unexpectedly exiting on update or node1 reboot.** Addressed appserver shutdown timeouts observed across several builds; shutdown timeouts are now clearly reported as such and stale shutdown messages are cleared.
- **Fixed tenant migrations getting stuck during an upgrade.** If tenant nodes updated out of order, they could fail to migrate workloads back once the upgrade started, leaving a node looping in maintenance.
- **Fixed a group create/delete race condition.** A group created within a few seconds of a group deletion could never accept members while appearing healthy in every field. Group membership state is now correct.
