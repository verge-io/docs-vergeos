# Configuring PTP in VergeOS
This article explains how to configure Precision Time Protocol (PTP) as an alternative to the default NTP-based time synchronization in VergeOS. These settings allow a VergeOS system to synchronize time using hardware or software timestamping depending on hardware capabilities.

## Overview

{% hint style="caution" %}
**Critical Caution Before Enabling PTP in VergeOS**

Precision Time Protocol (PTP) should **only** be enabled in environments that have the **proper, PTP‑capable hardware**, a validated timing architecture, and administrators who **fully understand the implications** of replacing the default NTP configuration.  
{% endhint %}

{% hint style="info" %}

**Key Points**

* VergeOS supports using PTP, in place of NTP, for time sychronization.
* PTP is used in environments requiring extremely precise timing, such as industrial automation, broadcast, financial trading, and telecom systems. 
* VergeOS provides a full set of PTP configuration options

{% endhint %}


---

## Configuring PTP

1. Set the system’s time synchronization mode to **PTP**
This disables NTP entirely, so ensure your environment is prepared for PTP operation.
* Navigate to **System > Time Settings**
* Select **Edit Settings**


2. Configure PTP Settings to align with your PTP hardware and infrastructure 
## Basic Settings


* **PTP Interface Network**
Select the physical network interface that will carry PTP traffic.  
This must be a network connected to PTP‑capable switches or timing devices.

* **PTP Transport**
Choose the transport mechanism (e.g., `UDPv4`).  
Select the transport appropriate for your PTP profile and network design.

* **PTP Domain**
Defines the logical PTP domain.  
Use the domain required by your timing architecture.

* **PTP Delay Mechanism**
Select the delay measurement mechanism (e.g., `E2E`).  
Different network designs may require different mechanisms.

* **Use Hardware Timestamps**
Enable if your NICs support hardware timestamping.  
Hardware timestamping provides significantly higher accuracy.  
If unavailable, software timestamping can be used with reduced precision.

---

## Advanced Settings

These options allow fine‑tuning of PTP behavior. Correct values depend entirely on your timing architecture, switch capabilities, and PTP profile.

* **Clock Priority 1 / Priority 2**
Used by the Best Master Clock Algorithm (BMCA).  
Lower values indicate higher priority.

* **Two-Step Clock**
Controls whether Sync messages are sent in one-step or two-step mode.  
Match this to your PTP network’s expectations.

* **Log Sync Interval**
Sets the logarithmic interval between Sync messages.  
Choose a rate appropriate for timing accuracy and network load.

* **Announce Interval**
Controls how frequently Announce messages are sent.  
Affects BMCA responsiveness and master selection.

* **Delay Request Intervals**
Configure how often delay measurement messages are sent.  
Values depend on whether you use E2E or P2P mechanisms.

* **Unicast Transmission**
Enable if your PTP peers require unicast messaging instead of multicast.

* **DSCP Event / General Messages**
Allows marking PTP packets with DSCP values for QoS handling.

* **Always Master (Disable BMCA)**
Forces VergeOS to act as the master clock.  
Use only when VergeOS is intended to be the authoritative time source.

* **Inhibit Announce / Delay Request Messages**
Suppresses specific message types if required by your timing design.

* **Include Follow-Up Information**
Adds TLVs to Follow_Up messages when required by certain profiles.

* **Transport Specific Field**
Used for specialized PTP profiles requiring non-default values.

* **PTP Hyperperiod**
Defines the hyperperiod used by certain profiles (e.g., 802.1AS).

* **Mean Message Propagation Delay**
Allows manual configuration of expected propagation delay (in nanoseconds).

* **Sync and Announce Receipt Timeouts**
Controls how many intervals must pass before timing messages

3. **Submit** changes.


## After enabling PTP

* Monitor the VergeOS Time Settings dashboard to confirm expected synchronization activity.
* Validate Timestamp Behavior: Confirm NICs support the selected timestamp mode and that the system is receiving hardware timestamps.
* Monitor Network Timing Devices: Confirm VergeOS is recognized as a participant. Verify message intervals and messages match your design
* Observe Application-level Timing: Validate that latency, jitter, or synchronization-dependent functions behave normally.