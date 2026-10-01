---
title: "VergeOS Time Settings Overview"
description: "Overview of VergeOS Time Settings that control external time synchronization (NTP/PTP). Nearly all systems should use the installed default settings. 
semantic_keywords:
  - "Time Settings"
  - "External time synchronization"
use_cases:
  - view NTP settings
  - adjust NTP system settings
tags:
  - settings
  - configuration
  - time synchronization
  - real-world time
categories:
  - System Administration
---

# VergeOS Time Settings Overview

## Overview 

{% hint style="info" %}

* VergeOS defaults to NTP and configures servers automatically

* Most users should never change time settings

* PTP mode is available for advanced, hardware‑specific use cases

* Keeping the defaults ensures a predictable, and well‑synchronized VergeOS environment.


{% endhint %}

Time settings determine how your VergeOS system accesses external time synchronization services to avoid drifting from real-world time. In nearly all environments, the default configuration is already optimized and should not be changed.

{% hint style="info" %}

**Time Zone**
The System *Timezone* setting is available in **System > Settings**.

{% endhint %}


## Default Behavior

VergeOS uses NTP (Network Time Protocol) by default. During installation, the system automatically configures a set of reliable public time servers. These defaults are appropriate for almost all deployments.

Unless you are an advanced user with a specific requirement, do not modify time settings.



## NTP Mode (Default)

NTP mode provides:

*  Automatic synchronization to trusted external time sources

*  Multi‑server redundancy

* Safe, predictable behavior for general-purpose clusters

*  Most users should leave the mode set to NTP and allow VergeOS to manage synchronization automatically.

## PTP Mode (Advanced)

Precision Time Protocol (PTP) is available for environments that require extremely precise timing and have the proper network hardware to support it.

**PTP should only be used when:**

- Your infrastructure explicitly requires sub‑microsecond timing

- You have compatible NICs, switches, and cabling

- You understand PTP domains, delay mechanisms, and hardware timestamping

For more information about PTP see the KB article: PTP Mode Requirements & Usage

## When to Change Time Settings

**Only adjust time settings if:**

* You are implementing PTP for a specialized workload

* You have a controlled environment with dedicated timing hardware

* You fully understand the implications of modifying NTP or PTP parameters

For all other cases, keep the defaults.
