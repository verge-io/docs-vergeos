---
title: Configuring PTP in VergeOS
slug: configuring-ptp
author: VergeOS Documentation Team
date: 2026-09-22T15:41:14.296Z
semantic_keywords:
  - "configure PTP precision time protocol VergeOS"
  - "replace NTP with PTP time synchronization"
  - "PTP hardware timestamps grandmaster domain delay mechanism"
  - "ptp4l phc2sys VergeOS time settings"
use_cases:
  - use_ptp_in_place_of_ntp
  - configure_ptp_for_time_synchronization
  - match_ptp_settings_to_grandmaster_profile
  - revert_from_ptp_to_ntp
categories:
  - System Administration
editor: markdown
dateCreated: 2026-09-22T15:41:14.296Z
description: >-
  Configure Precision Time Protocol (PTP) in place of NTP for VergeOS time
  synchronization, including every PTP setting, its default, and how to revert to NTP.
tags:
  - time
  - time-synchronization
  - ptp
  - ntp
  - precision-time-protocol
  - hardware-timestamps
---

# Configuring PTP in VergeOS

## Overview

{% hint style="info" %}
**Key Points**

- PTP mode replaces NTP for system time synchronization. NTP does not run while PTP mode is on.
- PTP needs a physical network connected to PTP-capable switches and a PTP grandmaster clock.
- Hardware timestamps give the highest accuracy. They are on by default.
- The **Time Settings** page shows the synchronization status of each node. VergeOS raises an alarm when a node is out of sync for more than two minutes.
- To undo the change, set **Mode** back to **NTP**.
{% endhint %}

This article explains how to switch VergeOS time synchronization from NTP to Precision Time Protocol (PTP) and how to set each PTP option. Use PTP only when your workloads need more precise time than NTP gives, for example in broadcast, financial trading, telecom, or industrial automation.

{% hint style="danger" %}
Do not enable PTP unless your NICs, switches, and grandmaster support PTP. An incorrect PTP configuration causes incorrect time on every node in the system.
{% endhint %}

## Prerequisites

- VergeOS 26.2 or later.
- A user with administrator permissions for the system.
- A physical network connected to PTP-capable switches or timing devices.
- A PTP grandmaster clock that the nodes can reach, and its PTP profile: domain, transport, and delay mechanism.
- NICs that support hardware timestamping, for the highest accuracy.

## Steps

{% hint style="warning" %}
When you set **Mode** to **PTP**, NTP stops. If the nodes cannot reach a PTP master, they have no time source.
{% endhint %}

1. Navigate to **System > Time Settings**.
2. Click **Edit Settings** in the left menu.
3. In the **Mode** list, select **PTP**.
    The PTP fields show in the **Time Settings** panel and the **Advanced PTP Settings** panel.
4. Set the basic settings to match your PTP network. See [Basic settings](#basic-settings).
5. If your PTP profile needs non-default values, set them in the **Advanced PTP Settings** panel. See [Advanced settings](#advanced-settings).
6. Click **Submit**.

The **Time Settings** page opens and shows the new mode.

## Verify the configuration

1. Navigate to **System > Time Settings**.
2. Make sure the synchronization status panel shows each node as synchronized.
    If a node stays out of sync for more than two minutes, VergeOS raises an alarm.
3. On your grandmaster or PTP switch, make sure each node shows as a PTP client on the correct domain.
4. Make sure that applications that depend on precise time operate correctly.

If synchronization does not become stable, revert to NTP. Then examine your PTP network and settings.

## Revert to NTP

1. Navigate to **System > Time Settings**.
2. Click **Edit Settings**.
3. In the **Mode** list, select **NTP**.
4. Click **Submit**.

The **Time Settings** page shows **Mode: NTP**. The **NTP Synchronization Status** panel shows each node as **Synced**.

## Guest time

VergeOS passes the kvmclock parameter through to guests. Guests that support PTP can synchronize accurately to the host clock.

## PTP settings reference

### Basic settings

These settings are in the **Time Settings** panel.

| Field | Default | Values | Description |
|-------|---------|--------|-------------|
| **PTP Interface Network** | None | A physical network | The physical network that carries PTP traffic. Required in PTP mode. Select a network connected to PTP-capable switches or timing devices. |
| **PTP Transport** | UDPv4 | UDPv4, UDPv6, L2 | The transport for PTP messages. Use the transport of your PTP profile. 802.1AS (gPTP) uses L2. |
| **PTP Domain** | 0 | 0-127 | The PTP domain number. Use the domain of your grandmaster. |
| **PTP Delay Mechanism** | E2E | E2E, P2P, Auto | How the path delay is measured: end-to-end (E2E) or peer-to-peer (P2P). Use the mechanism of your PTP network. |
| **Use Hardware Timestamps** | On | On, Off | With hardware timestamps, ptp4l steers the NIC hardware clock and phc2sys copies that time to the system clock. With software timestamps, ptp4l steers the system clock directly, with lower accuracy. If your NICs do not support hardware timestamping, turn this off. VergeOS does not fall back to software timestamps automatically. |

### Advanced settings

These settings are in the **Advanced PTP Settings** panel. The defaults work with most PTP networks. Change a value only when your PTP profile or grandmaster needs it.

| Field | Default | Values | Description |
|-------|---------|--------|-------------|
| **Clock Priority 1** | 128 | 0-255 | Priority in Best Master Clock Algorithm (BMCA) clock selection. A lower value is a higher priority. |
| **Clock Priority 2** | 128 | 0-255 | BMCA tie-breaker when Clock Priority 1 is equal. |
| **Two-Step Clock** | On | On, Off | On: the timestamp is sent in a Follow_Up message. Off: the timestamp is in the Sync message (one-step). |
| **Log Sync Interval** | 0 | -6 to 1 | Sync message rate, as log2 seconds: 0 = 1 s, -1 = 0.5 s, -3 = 0.125 s. |
| **Log Announce Interval** | 1 | -3 to 3 | Announce message rate, as log2 seconds: 0 = 1 s, 1 = 2 s, 2 = 4 s. |
| **Log Min Delay Request Interval** | 0 | -4 to 1 | Minimum delay request rate, as log2 seconds. Used with the E2E delay mechanism. |
| **Log Min P-Delay Request Interval** | 0 | -4 to 1 | Minimum peer delay request rate, as log2 seconds. Used with the P2P delay mechanism. |
| **Unicast Transmission** | Off | On, Off | Use unicast instead of multicast. Turn on only if your PTP peers support unicast. |
| **DSCP Event Messages (Port 319)** | 0 | 0-63 | DSCP value for PTP event messages, for QoS. |
| **DSCP General Messages (Port 320)** | 0 | 0-63 | DSCP value for PTP general messages, for QoS. |
| **Always Master (Disable BMCA)** | Off | On, Off | The port always acts as master and does not use BMCA. Turn on only when VergeOS is the time source for the PTP network. Do not turn on if another grandmaster uses the same domain. |
| **Inhibit Announce Messages** | Off | On, Off | Stops sending and receiving Announce messages. |
| **Inhibit Delay Request Messages** | Off | On, Off | Stops sending Delay Request messages. |
| **Include Follow-Up Information** | Off | On, Off | Adds the follow-up information TLV to Follow_Up messages. Some profiles, such as 802.1AS, need it. |
| **Transport Specific Field** | 0 | 0-255 | The PTP transportSpecific field. For 802.1AS (gPTP), this value is typically 1. |
| **Max Neighbor Propagation Delay (ns)** | 20000000 | Nanoseconds | The maximum propagation delay allowed to a neighbor. This is a limit, not an expected delay. |
| **Sync Receipt Timeout** | 0 | 0-255 | Number of sync intervals before a timeout. 0 disables the timeout. |
| **Announce Receipt Timeout** | 3 | 1-255 | Number of announce intervals before a timeout. |

## Additional Resources

- [Time Settings](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/time-settings)
- [System Settings](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/settings-overview)
- [VergeOS 26.2 release notes](https://app.gitbook.com/s/33mA7es4mQYkyUa7dMvu/2026/26-2-release-notes)

{% hint style="info" %}
**Need Help?**

If you have questions or problems with this procedure, contact the VergeOS support team.
{% endhint %}
