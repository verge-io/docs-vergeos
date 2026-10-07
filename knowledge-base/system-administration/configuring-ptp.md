---
title: Configuring PTP in VergeOS
slug: configuring-ptp
description: Instructions for configuring PTP (replacing NTP) for system time synchronization.
author: VergeOS Documentation Team
date: 2026-09-22T15:41:14.296Z
semantic_keywords:
  - "configure PTP time synchronization"
use_cases:
  - use_ptp_in_place_of_NTP
  - configure_ptp_for_time_synchronization
tags:
  - time
  - time synchronization
  - ptp
categories:
  - System Administration
editor: markdown
dateCreated: 2025-09-22T19:08:58.594Z
---

# Configuring PTP in VergeOS
This article explains how to configure Precision Time Protocol (PTP) as an alternative to the default NTP-based time synchronization in VergeOS. These settings allow a VergeOS system to synchronize time using hardware or software timestamping depending on hardware capabilities.

## Overview

{% hint style="danger" %}
**Critical Caution Before Enabling PTP in VergeOS**

Precision Time Protocol (PTP) replaces the default NTP configuration and should **only** be enabled in environments that have the **proper, PTP‑capable hardware**, a validated timing architecture, and administrators who **fully understand PTP configuration settings**.

PTP is a highly specialized timing mechanism. Misconfiguration can lead to **system instability**, **incorrect application time**, or **cluster‑wide timing faults**.  
If you are not certain your network equipment supports PTP—or you are unsure how PTP behaves in your environment, **do not enable it**.

{% endhint %}

{% hint style="info" %}

**Key Points**

* VergeOS supports using PTP, in place of NTP, for time synchronization.
* PTP is used in environments requiring extremely precise timing, such as industrial automation, broadcast, financial trading, and telecom systems. 
* VergeOS provides a full set of PTP configuration options

{% endhint %}


---

## Configuring PTP

### 1. Set the system’s time synchronization **Mode**

This disables NTP entirely; ensure your environment is prepared for PTP operation.
* Navigate to **System > Time Settings**
* Select **Edit Settings**
* In the **Mode** field select ***PTP*** 


### 2. Configure PTP Settings to align with your PTP hardware and infrastructure 

#### Basic Settings

* **PTP Interface Network**  
Select the physical network that carries PTP traffic. This field is required in PTP mode.  
This must be a network connected to PTP‑capable switches or timing devices.

* **PTP Transport**  
Select **UDPv4** (default), **UDPv6**, or **L2**.  
Select the transport appropriate for your PTP profile and network design.

* **PTP Domain**  
Defines the logical PTP domain.  
Use the domain required by your timing architecture.

* **PTP Delay Mechanism**  
Select **E2E** (end-to-end, default), **P2P** (peer-to-peer), or **Auto**.  
Different network designs may require different mechanisms.

* **Use Hardware Timestamps**  
Enabled by default. Leave it enabled if your NICs support hardware timestamping. Hardware timestamping provides significantly higher accuracy.  
If your NICs do not support hardware timestamping, disable this option to use software timestamping. VergeOS does not fall back to software timestamping automatically.

---

#### Advanced Settings

These options allow fine‑tuning of PTP behavior. Correct values depend entirely on your timing architecture, switch capabilities, and PTP profile.

* **Clock Priority 1**  
Used by the Best Master Clock Algorithm (BMCA) to select the master clock.  
Lower values indicate higher priority (0-255, default 128).

* **Clock Priority 2**  
BMCA tie-breaker when Clock Priority 1 is equal (0-255, default 128).

* **Two-Step Clock**  
Enabled by default. Two-step sends the timestamp in a Follow_Up message. One-step embeds it in the Sync message.  
Match this to your PTP network’s expectations.

* **Log Sync Interval**  
Sync message rate as log2 seconds: 0 = 1 s, -1 = 0.5 s, -2 = 0.25 s, -3 = 0.125 s (-6 to 1, default 0).  
Choose a rate appropriate for timing accuracy and network load.

* **Log Announce Interval**  
Announce message rate as log2 seconds: 0 = 1 s, 1 = 2 s, 2 = 4 s (-3 to 3, default 1).  
Affects BMCA responsiveness and master selection.

* **Log Min Delay Request Interval**  
Minimum delay request rate as log2 seconds, used with the E2E delay mechanism (-4 to 1, default 0).

* **Log Min P-Delay Request Interval**  
Minimum peer delay request rate as log2 seconds, used with the P2P delay mechanism (-4 to 1, default 0).

* **Unicast Transmission**  
Disabled by default. Enable if your PTP peers require unicast messaging instead of multicast.

* **DSCP Event Messages (Port 319)**  
DSCP value for PTP event messages, for QoS handling (0-63, default 0).

* **DSCP General Messages (Port 320)**  
DSCP value for PTP general messages, for QoS handling (0-63, default 0).

* **Always Master (Disable BMCA)**  
Disabled by default. Forces this port to always act as master and skips the Best Master Clock Algorithm.  
Use only when VergeOS is intended to be the authoritative time source.

* **Inhibit Announce Messages**  
Disabled by default. Suppresses Announce message transmission and reception.

* **Inhibit Delay Request Messages**  
Disabled by default. Suppresses Delay Request message transmission.

* **Include Follow-Up Information**  
Disabled by default. Sends the follow-up information TLV in Follow_Up messages when required by certain profiles.

* **Transport Specific Field**  
The PTP transportSpecific field (0-255, default 0). Used with 802.1AS/gPTP, where it is typically set to 1.

* **Max Neighbor Propagation Delay (ns)**  
The maximum allowed propagation delay to a neighbor, in nanoseconds (default 20000000). This is a threshold, not an expected delay value.

* **Sync Receipt Timeout**  
Number of sync intervals before a timeout is declared (0-255, default 0 = disabled).

* **Announce Receipt Timeout**  
Number of announce intervals before a timeout is declared (1-255, default 3).


### 3. **Submit** changes

* Click **Submit** to implement the changes.

### 4. Verify Configuration

**After enabling PTP:**

* **Monitor the VergeOS Time Settings dashboard:** Confirm expected synchronization activity.
* **Validate Timestamp Behavior:** Verify NICs support the selected timestamp mode and that the system is receiving hardware timestamps.
* **Monitor Network Timing Devices:** Confirm VergeOS is recognized as a participant. Verify message intervals and messages match your design.
* **Observe Application-level Timing:** Validate that latency, jitter, or synchronization-dependent functions behave as expected.

{% hint style="warning" %}
If PTP synchronization does not stabilize, revert to NTP until the timing architecture is validated.

{% endhint %}

