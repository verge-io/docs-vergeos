---
title: Filtering Syslog Messages from the System Logs View
slug: filtering-syslog-messages
author: VergeOS Documentation Team
date: 2026-07-31T12:00:00.000Z
semantic_keywords:
  - "filter syslog messages vergeos system logs view"
  - "hide repeating kernel driver message from system logs"
  - "syslog_regex_list filter configuration vergeos"
  - "stop failed ioctl HBA message flooding the logs"
  - "filter cosmetic log noise out of the system logs ui"
use_cases:
  - filter_syslog_messages
  - suppress_cosmetic_log_noise
  - quiet_repeating_driver_message
categories:
  - Troubleshooting
editor: markdown
dateCreated: 2026-07-31T12:00:00.000Z
description: >-
  Filter confirmed-cosmetic hardware and driver messages out of the System Logs
  view with the System Log Filter cluster setting. The filter hides lines from
  the UI only — the kernel still writes them to the raw syslog.
tags:
  - logs
  - syslog
  - log filtering
  - syslog_regex_list
  - troubleshooting
  - hardware
  - driver
  - regex
---
# Filtering Syslog Messages from the System Logs View

## Overview

{% hint style="info" %}
**Key Points**
- The **System Log Filter** cluster setting hides matching lines from the **System > Logs** view.
- The filter hides messages from the UI only — the kernel still writes them to the raw syslog.
-Systems are installed with a default set of System Log Filter entries that should be kept intact; additional entries can be appended to the comma-delimited list to suppress messages that have been confirmed as non-fault conditions.
- Patterns use POSIX Extended Regular Expression (ERE) syntax.
{% endhint %}

Some hardware and driver messages repeat constantly in **System > Logs** without indicating a real fault. A storage HBA driver that logs a failed ioctl on every poll is a common example. These messages bury the log entries you care about. This article shows how to hide them with the **System Log Filter** cluster setting.

{% hint style="danger" %}
**Confirm the message is cosmetic before suppressing it.**

Suppressing a log entry hides it from the Logs view permanently until the filter is removed.  If the message later changes character — for example, an HBA firmware bug that begins returning a different error code — you will not see it.

Before adding a filter:
- Verify with the hardware vendor or VergeOS support that the specific message is a known non-fault condition.
- Record the full original message text, the reason it was deemed cosmetic, and notify other administrators so they are aware the filter exists and why it was added.
- Note the firmware version, driver version, and hardware model so you can re-evaluate if any of those change.

**When in doubt, do not suppress.** Contact the VergeOS support team before filtering any message you are not fully certain is harmless.
{% endhint %}

## Prerequisites

- A repeating log message that you have **confirmed is not a real fault**.
- A user with administrator access to the cluster settings.

## Step 1: Get the Exact Message Text

1. Navigate to **System > Logs**.
2. Copy the repeating line.
3. Keep the part of the message that stays the same each time it fires.
4. Remove the parts that vary — instance numbers, hex status codes, and timestamps.
5. Carefully use ERE syntax expressions to include relevant variations of the message. 

Example message:

```
kernel: mpi3mr1: Issue IOUCTL time_stamp: Failed ioc_status(0x000d) Loginfo(0x00000000)
```

{% hint style="warning" %}
Do not include the `kernel:` prefix in your pattern. The Logs view prepends this identifier for display — it is not part of the message the filter sees. A pattern anchored on `kernel:` never matches.
{% endhint %}

## Step 2: Build the Pattern

Patterns use POSIX Extended Regular Expression (ERE) syntax, not PCRE. Start with a plain substring and then **make it as specific as possible**:

```
Issue IOUCTL time_stamp: Failed ioc_status
```

This minimal substring matches every controller instance and every status code. In most cases, you should add specificity to reduce the risk of accidentally suppressing a different message that happens to share part of the same text. A more specific pattern that anchors on the driver prefix and escapes literal parentheses is safer:

```
mpi3mr[0-9]*: Issue IOU?CTL time_stamp: Failed ioc_status\(0x000[124d]\)
```

- `mpi3mr[0-9]*`  
  Matches: mpi3mr/mpi3mr0/mpi3mr1/mpi3mr12/etc.

- `Issue IOU?CTL time_stamp`  
  Anchors specifically on IOCTL failures (U? means the U is optional, to match both 'IOCTL' and 'IOUCTL')

- `ioc_status\(0x000[124d]\)`
  Matches only these benign codes: 0x0001/0x0002/0x0004/0x000d
  (The bracket expression [124d] is POSIX ERE shorthand.)
  Parentheses escaped because ERE treats them as grouping operators.


{% hint style="warning" %}
**Prefer the More Specific Pattern**

Avoid overly short or broad substrings. A pattern that is too general can inadvertently suppress a related but distinct message that *does* indicate a real fault. Use the most specific string that reliably matches the known-cosmetic message and nothing else. If variable fields like Loginfo codes are meaningful — for example, only one particular code is cosmetic — include them in the pattern.
{% endhint %}

## Step 3: Add the Pattern to the System Log Filter (via Cluster Settings) 

{% hint style="warning" %} Do not clear or replace the installed default System Log Filter value.

VergeOS populates the System Log Filter field with a default set of entries at installation. These defaults suppress a large volume of routine kernel and service messages that would otherwise make the Logs view unreadable. Deleting or overwriting them will cause that noise to flood back into the Logs view. Always append your new pattern to the end of the existing value. 
{% endhint %}


1. Navigate to **Clusters** in the main menu.
2. Click on the cluster name to select it, then click **Edit**.
3. Scroll down to the **System Log Filter** field. You will see the default entries already populated — for example:
   `*:3,ipmievd:5,rasdaemon,!ntpd,!postfix`
4. Place your cursor at the end of the existing value, **add a comma**, then append your new pattern:
   e.g. `*:3,jpmievd:5,rasdaemon,!ntpd,!postfix,mpi3mr[0-9]*: Issue IOU?CTL time_stamp: Failed ioc_status\(0x000[124d]\)`
6. Click **Submit** to save.

{% hint style="info" %} If you need to filter multiple distinct messages, add each pattern as its own comma-delimited entry, all appended to the end of the existing value. {% endhint %}

## Step 4: Reload the Filter on Each Node

Log capture reads the filter when you toggle it. Do this one node at a time:

1. Edit the node.
2. Disable the **Capture System Logs** option and click **Submit**.
3. Wait 15 to 30 seconds.
4. Edit the node again, enable the **Capture System Logs** option, and click **Submit**.

If a node still shows the message after you toggle log capture, reboot that node to force the reload.

## Step 5: Verify the Filter

Wait until the message would normally recur, then check **System > Logs**. The line no longer appears.

{% hint style="info" %}
**Verify in the Logs View, Not the Raw Syslog**
The raw syslog inside a system diagnostics file still contains the message by design. Only the Logs view reflects the filter.
{% endhint %}

## Troubleshooting

### The message still appears in the Logs view

**Cause**: The pattern does not match, or a node has not reloaded the filter.

**Solution**:
1. Make sure the pattern does not include the `kernel:` prefix.
2. Make sure the pattern uses ERE syntax — escape literal parentheses as `\(` and `\)`.
3. Toggle **Capture System Logs** on the node again.
4. The node may need to be rebooted. Always **Follow proper** [**Maintenance Mode**](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/operations/maintenance-mode) **procedures when rebooting a node to avoid workload disruptions.**

### The message still appears in a system diagnostics file

**Cause**: The filter hides lines from the UI Logs view only. The kernel still writes them to the raw syslog.

**Solution**: This is expected behavior. Verify the filter in **System > Logs**, not in a system diagnostics file.

## Additional Resources

- [Cluster Settings](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/cluster-settings)
- [Node Diagnostics](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/node-diagnostics)
- [System Logs](system-logs.md)
- [Generating System Diagnostics](generating-system-diagnostics.md)

{% hint style="danger" %}
**Need Help?**
If you are not certain whether a repeating log line is cosmetic or a real fault, contact the VergeOS support team **before** suppressing it. Suppressing an active fault message can delay diagnosis of a serious hardware problem.
{% endhint %}
