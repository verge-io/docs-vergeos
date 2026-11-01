---
title: VirtIO-Win Driver Compatibility with MS SQL Server Workloads
slug: virtio-win-mssql-compatibility
author: VergeOS Documentation Team
date: 2026-11-01T00:00:00.000Z
semantic_keywords:
  - virtio-win driver compatibility ms sql server
  - windows vm sql server read retry incorrect checksum
  - virtio-win 0.1.285 0.1.292 sql server bug
  - virtio-win 0.1.302+ recommended version vergeos
  - upgrade virtio-win drivers windows guest
  - vioscsi storport srb id race condition windows server 2025
use_cases:
  - resolve_mssql_read_retry_errors_on_windows_vm
  - identify_installed_virtio_win_driver_version
  - update_virtio_win_drivers_to_stable_release
categories:
  - VMs
  - Troubleshooting
editor: markdown
dateCreated: 2026-05-22T00:00:00.000Z
description: >-
 Known virtio-win driver compatibility issue affecting Windows VMs running MS SQL Server under heavy I/O, including the resolution build, verification steps, recommended upgrade path, and legacy downgrade reference.
tags:
  - virtio
  - virtio-win
  - vioscsi
  - viostor
  - windows
  - mssql
  - sql server
  - drivers
  - troubleshooting
---

# VirtIO-Win Driver Compatibility with MS SQL Server Workloads

{% hint style="success" %}
**Resolved in virtio-win v0.1.300 and Later** 
The Storport SRB ID race condition described in this article was merged upstream and resolved in virtio-win v0.1.300 and newer builds. If your VM is running affected builds (v0.1.285 or v0.1.292), follow the Upgrade Procedure below. The legacy downgrade procedure to v0.1.271 is preserved as a fallback reference.


## Overview

{% hint style="info" %}
**Key Points**

* **Resolved Upstream:** Upstream issue #1453 (a non-atomic SRB ID assignment in vioscsi and viostor) was resolved in January 2026 and released in **virtio-win v0.1.300+**.
* **Affected Releases:** virtio-win v0.1.285 and v0.1.292 contain the race condition, which surfaces as false-positive read-retry warnings or SQL Server service hangs under heavy concurrent I/O.
* **Recommended Action:** Upgrade guest drivers to v0.1.300 (or your platform's current validated release).
* **Environment Impact:** Symptoms are most pronounced on Windows Server 2025 guests due to aggressive StartIo parallelization, though earlier Windows Server releases can also trigger the issue.
* **Data Integrity:** Database files on disk remain uncorrupted; the driver delivered an incorrect buffer on an initial read attempt, which succeeded on the retry.
* **Safe Execution:** Always take a VM snapshot and quiesce SQL Server services before applying storage driver updates.

{% endhint %}

Windows VMs running MS SQL Server on VergeOS can produce a stream of SQL Server "read-retry" log entries — and in some cases a hung SQL Server service after a few days of sustained load — when the guest is using **virtio-win v0.1.285 or v0.1.292**. The root cause is a non-atomic SRB ID assignment in the `vioscsi`/`viostor` Storport miniports that allows duplicate IDs to be issued when Windows dispatches I/O across multiple CPUs in parallel (tracked upstream as [virtio-win issue #1453](https://github.com/virtio-win/kvm-guest-drivers-windows/issues/1453)).

The behavior is most reproducible on **Windows Server 2025** because its Storport implementation parallelizes `StartIo` more aggressively than earlier Windows Server releases. Older Windows guests are exposed to the same bug but trigger it less often.

## Symptoms

If you suspect this issue on a VergeOS Windows VM, look for the following in the guest's **Application** event log and **SQL Server error log**:

*   Read-retry messages where the **expected** and **actual** values are identical, for example:

    > _A read of the file '\*.mdf' at offset 0x... succeeded after failing 1 time(s) with error: incorrect checksum (expected: 0xad4c6778; actual: 0xad4c6778)_

    > _A read of the file '\*.mdf' at offset 0x... succeeded after failing 1 time(s) with error: incorrect pageid (expected 1:29669944; actual 1:29669944)_
* `No SRB found for ID` entries from the `vioscsi` source
* SQL Server services hanging after several days of sustained heavy load

{% hint style="info" %}
**These messages can look like corruption but usually aren't**

SQL Server reports the **retry** outcome, which succeeds on the second attempt. `DBCC CHECKDB` typically comes back clean — the database pages on disk are intact. The driver is delivering the wrong buffer to the first read because of the duplicate SRB ID, and the second read returns the correct data. Persistent retries still indicate a real problem and should be addressed even when no corruption is detected.
{% endhint %}

## Recommended Versions

|Version     | Status   | Operational Guidance       |
|----------- | -------- | -------------------------- |
| v0.1.300+  | Current Recommended | Upstream fix included. Stable under sustained parallel database I/O. |
| v0.1.285   | Defective (Do not use) | Contains Storport SRB race condition; causes read-retry errors on SQL VMs. |
| v0.1.292   | Defective (Do not use) | Contains Storport SRB race condition; causes read-retry errors on SQL VMs. |
| v0.1.271   | Legacy Fallback        | Precedes the defect commit. Stable fallback if newer packages cannot be applied.|



## Prerequisites

* A Windows VM running MS SQL Server (or a similarly I/O-heavy database workload) on VergeOS
* Administrative access to the Windows guest
* A snapshot of the VM taken before changing any drivers
* The **virtio-win v0.1.302 (or later) ISO** uploaded to your VergeOS environment under **Files**. Archived ISOs are available from the [stable-virtio archive on Fedora People](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/)

## Identifying the Installed VirtIO Driver Version

Before changing anything, confirm which virtio-win build the guest is currently running.

1. **Open Device Manager**
   * Right-click the Start menu and select **Device Manager**.
2. **Locate the VirtIO storage controller**
   * Expand **Storage controllers**.
   * Right-click **Red Hat VirtIO SCSI controller** (for vioscsi) or **Red Hat VirtIO SCSI pass-through controller** / **Red Hat VirtIO SCSI Disk Device** (for viostor) and choose **Properties**.
3. **Check the driver version and date**
   * Switch to the **Driver** tab.
   * Note the **Driver Version** and **Driver Date** fields.

4. **Decode Version Revision:** VirtIO builds follow the 100.<minor>.<build>.<revision> scheme:
   * A driver ending in .28500 indicates v0.1.285.
   * A driver ending in .29200 indicates v0.1.292.
   * A driver ending in .30000 or higher indicates the patched release.
If you are unsure which ISO produced the installed driver, mount the candidate ISO inside the guest and compare its `vioscsi.inf` / `viostor.inf` `DriverVer` line against the value shown in Device Manager.

{% hint style="warning" %}
**Check both vioscsi and viostor**

The defect affects both drivers. If the VM uses one bus type for the OS disk and the other for data disks, verify both controllers.
{% endhint %}

The stable virtio-win ISO downloads are available from the [Fedora People stable-virtio repository](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/), and older releases from the [archive-virtio directory](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/).


## Upgrading to virtio-win v0.1.300 or Later (Recommended)

### Prerequisites

  * A VergeOS VM snapshot taken immediately prior to the change.
  * The virtio-win-0.1.302.iso (or later validated ISO) uploaded to Files in VergeOS.
  * Administrative access to the Windows guest OS.

### Procedure

1. **Stop MS SQL Server services in the guest**
   * From an elevated PowerShell or the Services console, stop the **SQL Server (MSSQLSERVER)** service and any dependent services (SQL Agent, full-text, Reporting Services, etc.) to quiesce I/O before changing the storage driver.
2. **Take a VM Snapshot:** providing a rollback point prior to the driver upgrade.
3. **Mount the virtio-win v0.1.300 ISO**
   * In VergeOS, add a new drive with Media type: CD-ROM  (or edit an existing)   to attach the virtio ISO (**virtio-win-0.1.302.iso or later**)
   * Confirm the ISO is visible inside Windows.
4. **Attach the Updated ISO:** In VergeOS, select the virtio-win-0.1.300.iso as the Media File on an existing CD-ROM drive (or add a new CD-ROM drive) and ensure it appears within Windows Explorer.
5. **Execute In-Place Upgrade:** Run the guest installer: *virtio-win-gt-x64.msi* from the mounted media.
6. **Reboot the Guest:** Restart the Windows VM to unload legacy drivers and bind the updated Storport miniport stack.
7. **Verify Installed Build:** Open **Device Manager** → **Storage controllers** → Open the controller's **Properties** → **Driver** tab. Ensure the version stamp reflects **.30000 or higher**.
8. **Start SQL Server:** Restart the database services:
9. **Monitor Logs:** Verify normal database operations and confirm that SQL Server error logs and Windows Application event logs remain clear of checksum retry notices.  Sustained operation without retries is the success criterion.



<details>
<summary>LEGACY WORKAROUND - Downgrading to virtio-win v0.1.271</summary>

**Use this procedure only if environmental constraints prevent deploying v0.1.300+.**  Because Windows does not support native in-place driver downgrades via MSI, the existing package must be stripped first.


{% hint style="warning" %}
**Take a snapshot first**

Before changing any virtio driver in the guest, take a VergeOS snapshot of the VM. The storage stack is boot-critical — the snapshot is your rollback point if the driver swap leaves Windows unable to mount its disks.
{% endhint %}

1. **Stop MS SQL Server services in the guest**
   * From an elevated PowerShell or the Services console, stop the **SQL Server (MSSQLSERVER)** service and any dependent services (SQL Agent, full-text, Reporting Services, etc.) to quiesce I/O before changing the storage driver.
2. **Mount the virtio-win v0.1.271 ISO**
   * In VergeOS, edit the VM and attach **virtio-win-0.1.271.iso** as a CD/DVD device.
   * Confirm the ISO is visible inside Windows (typically the next available drive letter).
3. **Uninstall the current virtio-win guest tools**
   * Open **Settings → Apps & features** (or **Programs and Features** in the Control Panel) inside the guest.
   * Locate **Virtio-win-guest-tools** and choose **Uninstall**. Follow the prompts and reboot if requested.
   * If the uninstall fails or rolls back with error `0x80070643` (a known issue when removing virtio-win-guest-tools), use Microsoft's [Program Install and Uninstall troubleshooter](https://support.microsoft.com/topic/fix-problems-that-block-programs-from-being-installed-or-removed-cca7d1b6-65a9-3d98-426b-e9f927e1eb4d) to clean up the registration before continuing.
4. **Reboot the VM**
   * Reboot Windows so any in-use driver files are released. The VM should still boot — Windows retains the storage driver binaries until the new package is installed.
5. **Install virtio-win-guest-tools from the v0.1.271 ISO**
   * From the mounted v0.1.271 ISO, run `virtio-win-guest-tools.exe` (or `virtio-win-gt-x64.msi`) as an administrator.
   * Complete the installer with the default component selection. This reinstalls vioscsi, viostor, NetKVM, and the guest agent at the v0.1.271 build.
6. **Reboot the VM again**
   * Reboot Windows so the storage and network stacks reload against the downgraded drivers.
7. **Verify the new driver version**
   * Return to **Device Manager → Storage controllers**, open the VirtIO controller's **Properties → Driver** tab, and confirm the **Driver Version** now reflects the v0.1.271 build (typically ending in `.27100`).
   * Repeat for any other VirtIO controllers and for the **Red Hat VirtIO Ethernet Adapter** under **Network adapters**.
8. **Start MS SQL Server services**
   * Start the SQL Server service and any dependents and confirm the databases come online cleanly.
9. **Monitor under load**
   * Resume normal workloads and watch the SQL Server error log and Windows Application log for the read-retry messages described above. Sustained operation without retries is the success criterion.

</details>

## Troubleshooting

{% hint style="warning" %}
**Common Issues**

* **Installer reports "newer version already installed"** — The virtio-win MSI does not perform an in-place downgrade. Complete the uninstall step (and reboot) before running the v0.1.271 installer.
* **Uninstall fails with error 0x80070643** — A known virtio-win-guest-tools quirk. Use Microsoft's _Program Install and Uninstall troubleshooter_ to clear the failed installer state, reboot, and try the v0.1.271 install again.
* **VM fails to boot after driver change** — Restore the snapshot taken in the prerequisites and retry the procedure with SQL Server services fully stopped first.
* **Storage controller shows a yellow exclamation in Device Manager** — The driver did not load cleanly. Right-click the controller, choose **Update driver → Browse my computer**, and point it at the folder on the v0.1.271 ISO matching your Windows version (e.g. `vioscsi\2k25\amd64` for Windows Server 2025).
* **Read-retry messages persist after downgrading** — Verify that **both** `vioscsi` and `viostor` (whichever the VM uses) now show the v0.1.271 build in Device Manager. If they do and the messages continue, capture a fresh sample of the Application log and SQL Server error log and contact VergeOS support.
* **A newer virtio-win release is available** — Releases published after January 2026 may include the upstream fix and be a better long-term choice than staying on v0.1.271. Confirm the specific build with VergeOS support before rolling it out to production database VMs.
{% endhint %}

## Additional Resources

* [Loading Virtio Drivers in Windows Recovery Console](loading-virtio-drivers-in-windows-recovery-console.md)
* [Database Best Practices](../system-administration/database-best-practices.md)
* [VM Snapshots and Restores](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/vm-snapshots-restores)
* [virtio-win issue #1453 — upstream report of the SRB ID race](https://github.com/virtio-win/kvm-guest-drivers-windows/issues/1453)
* [Stable virtio-win ISO downloads](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/)
* [Archived virtio-win ISO downloads](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/)

## Feedback

{% hint style="info" %}
**Need Help?**

If you are seeing read-retry messages or instability on a Windows MS SQL VM and are unsure which virtio-win version is installed — or which build to upgrade to — please reach out to the [VergeOS Support Team](https://app.gitbook.com/s/uJc5d3O7cwI7qD8muSyG/support-and-services) before making driver changes in production.
{% endhint %}
