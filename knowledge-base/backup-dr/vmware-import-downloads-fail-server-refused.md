---
title: VMware Import Scans Succeed but File Downloads Fail
slug: vmware-import-downloads-fail-server-refused
author: VergeOS Documentation Team
date: 2026-07-31T12:00:00.000Z
semantic_keywords:
  - "vmware import scan works download fails server refused connection"
  - "vergeos vmware service backup paused retry error downloading file"
  - "esxi host fqdn dns resolution vmware service vm"
  - "vmware import port 902 903 nfc firewall vddk"
  - "vmware backup one cluster works another fails"
use_cases:
  - import_vms_from_vmware_into_vergeos
  - back_up_vmware_vms_with_vergeos
  - troubleshoot_vmware_import_download_failure
categories:
  - Troubleshooting
  - Backup and DR
editor: markdown
dateCreated: 2026-07-31T12:00:00.000Z
description: >-
  A VMware Service connects to vCenter and scans VMs, but backup or import jobs
  fail with "server refused connection" when pulling files. Usually DNS or port
  902 reachability to the ESXi hosts.
tags:
  - vmware
  - import
  - migration
  - backup
  - vcenter
  - esxi
  - dns
  - port 902
  - server refused connection
  - vmware service
  - troubleshooting
---

# VMware Import Scans Succeed but File Downloads Fail

## Symptoms

- The VMware Service connects to vCenter and scans VMs without errors.
- A backup or import job starts, then pauses, retries, and fails after several attempts.
- The service log shows the snapshot succeed, then a run of download errors:

```
Error: The server refused connection
Error downloading file: [<datastore>] <VM>/<VM>.nvram
Error downloading file: [<datastore>] <VM>/<VM>.vmxf
Error downloading file: [<datastore>] <VM>/<VM>.vmx
Backup job paused due to encountering an error. Will retry again in approximately Nm (#k of 10)
```

- The failure hits **every** file, including the small config files (`.vmx`, `.vmxf`, `.nvram`) — not only the large virtual disks.

{% hint style="info" %}
**Why "Every File" Matters**

If the small config files fail together with the disks, this is not a disk-specific or VDDK transport problem. It is a connection problem with the host that holds the files.
{% endhint %}

## Overview

{% hint style="info" %}
**Key Points**

- The VMware Service uses vCenter only to list VMs and locate their files.
- The actual file transfer goes directly to the ESXi host, at the FQDN vCenter returns.
- If the service cannot resolve or reach that host, the scan succeeds while every download fails.
{% endhint %}

The VMware Service uses vCenter only to enumerate VMs and locate their files. The actual transfer goes directly to the ESXi host that owns the VM's datastore, at the host FQDN that vCenter returns.

If the service can reach vCenter but not that ESXi host, vCenter looks healthy — the scan succeeds — while every download fails with "server refused connection". There are two common causes.

**1. DNS.** The VMware Service cannot resolve the ESXi host FQDNs that vCenter returns. The usual reason is a wrong or missing DNS server or search domain on the service VM's NIC. This is the most common cause. It also explains why VMs on one cluster back up fine while another cluster fails — the working cluster's hosts happen to resolve.

**2. Network or firewall.** The host name resolves, but the host is not reachable directly. The transfer needs TCP 443 (vSphere API) and TCP 902 (NFC, the disk data channel) open from the VMware Service to each ESXi host, not only to vCenter. Port 902 is the one most often missed.

## Diagnosis

1. In vSphere, note the FQDNs of the ESXi hosts in the cluster that owns the failing VM's datastore. These are the names VergeOS connects to.
2. In VergeOS, navigate to **Import/Export > VMware Services** and double-click the service.
3. Select **View Service > Diagnostics**.
4. From the Diagnostics panel, try to resolve and reach each host FQDN.
    - If a name does not resolve, the cause is DNS.
    - If a name resolves but does not connect, check the firewall and port 902.

## Solution

1. Set the VMware Service VM's NIC to a DNS server that resolves the ESXi host FQDNs, or add the correct search domain. See [Configuring VMware Service VM NIC IPv4 Settings](../networking/vmware-service-vm-nic-ipv4-configuration.md).
2. Make sure TCP 443 and 902 are open from the VMware Service to each ESXi host, not only to vCenter.
3. Run the job again. The downloads proceed past the config files and into the virtual disks.

## Additional Resources

- [Configuring VMware Service VM NIC IPv4 Settings](../networking/vmware-service-vm-nic-ipv4-configuration.md)
- [VMware Backup and DR Guide](vmwarebackupdrguide.md)

{% hint style="info" %}
**Need Help?**

If downloads still fail after you confirm DNS and the ports, contact the VergeOS support team with a copy of the VMware Service log.
{% endhint %}
