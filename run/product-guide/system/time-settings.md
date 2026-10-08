---
title: "Time Settings"
description: "View and change how VergeOS synchronizes system time: NTP (default) or PTP. Covers the default servers, node behavior, sync status, and changing NTP servers."
semantic_keywords:
  - "VergeOS time settings NTP servers"
  - "external time synchronization NTP PTP mode"
  - "node time sync status alarm"
  - "change NTP servers internal time source"
use_cases:
  - view_time_sync_status
  - change_ntp_servers
  - choose_ntp_or_ptp_mode
  - troubleshoot_node_time_sync
tags:
  - time-settings
  - time-synchronization
  - ntp
  - ptp
  - configuration
categories:
  - System Administration
---

# Time Settings

Time settings control how VergeOS synchronizes system time. The default, NTP mode, works for almost all systems. Change these settings only to use internal NTP servers or to use PTP.

## Overview

### What you'll learn

- How VergeOS synchronizes time by default
- How to examine the sync status of each node
- How to change the NTP servers
- When to use PTP mode

### What you'll need

- VergeOS 26.2 or later
- A user with administrator permissions for the system

{% hint style="info" %}
**Time zone**

The system time zone is not a time setting. Set it in the **Timezone** field in **System > Settings**. See [System Settings](settings-overview.md).
{% endhint %}

## How VergeOS synchronizes time

VergeOS uses NTP (Network Time Protocol) by default. The installer configures these public servers: `0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org 3.pool.ntp.org`.

Node 1 synchronizes with the NTP servers. All other nodes synchronize with node 1 over the core network. Only node 1 needs access to the external NTP servers.

## Examine the time sync status

1. Navigate to **System > Time Settings**.

The page shows two panels:

- **NTP Configuration**: The current mode and settings.
- **NTP Synchronization Status**: The status of each node, its time source, and the time of the last check.

Each node shows **Synced** when it is synchronized. Node 1 shows a public server as its source. The other nodes show the core network address of node 1. VergeOS raises an alarm when a node is out of sync for more than two minutes.

## Change the NTP servers

Change the NTP servers when your network blocks public NTP or your organization requires internal time servers.

{% hint style="warning" %}
Make sure node 1 can reach the new servers before you submit the change. If node 1 cannot reach any server, the system has no time source.
{% endhint %}

1. Navigate to **System > Time Settings**.
2. Click **Edit Settings** in the left menu.
3. In the **NTP Servers** field, enter the server names or IP addresses, separated by spaces.
    For example: `ntp1.example.com ntp2.example.com`.
4. Click **Submit**.

The **NTP Configuration** panel shows the new servers. After a short time, each node shows **Synced** in the **NTP Synchronization Status** panel.

### NTP settings reference

| Field | Default | Values | Description |
|-------|---------|--------|-------------|
| **Mode** | NTP | NTP, PTP | The time synchronization protocol. |
| **NTP Servers** | `0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org 3.pool.ntp.org` | Space-separated names or IP addresses | The servers that node 1 synchronizes with. |
| **NTP Max Clocks** | 11 | 1-255 | The maximum number of time sources NTP uses. Do not change. |
| **NTP Min Clocks** | 4 | 1-255 | The minimum number of time sources NTP tries to use. Do not change. |
| **NTP Min Sane** | 1 | 1-255 | The minimum number of time sources that must agree before NTP sets the time. Do not change. |

Do not change **NTP Max Clocks**, **NTP Min Clocks**, or **NTP Min Sane** unless VergeOS support tells you to.

## PTP mode

Precision Time Protocol (PTP) gives more precise time than NTP. Use PTP only when all of these conditions are true:

- Your workloads need sub-microsecond time accuracy.
- Your NICs, switches, and cabling support PTP.
- You have a PTP grandmaster clock, and you know its domain, transport, and delay mechanism.

For the procedure and all PTP settings, see [Configuring PTP in VergeOS](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/system-administration/configuring-ptp).

## Summary

VergeOS synchronizes time with NTP by default: node 1 synchronizes with external servers, and all other nodes synchronize with node 1. The **System > Time Settings** page shows the sync status of each node.

### Next steps

- [System Settings](settings-overview.md)
- [Advanced System Settings](advanced-system-settings.md)
