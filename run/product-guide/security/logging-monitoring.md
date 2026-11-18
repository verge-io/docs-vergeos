---
title: "Logging and Monitoring Hardening"
description: "Harden VergeOS logging and monitoring: export logs off the cluster, keep timestamps trustworthy, limit API abuse, route alarms, and watch protection freshness."
semantic_keywords:
  - "VergeOS remote syslog export security logs"
  - "audit log retention and collector outage"
  - "API rate limit max connections hardening"
  - "alarm and sync event notification tasks"
  - "snapshot freshness ransomware indicator monitoring"
use_cases:
  - export_security_logs_to_external_collector
  - preserve_node_log_timestamps
  - limit_api_connection_and_rate_abuse
  - route_alarms_through_event_tasks
  - monitor_recovery_point_freshness
tags:
  - security
  - hardening
  - logging
  - syslog
  - monitoring
  - alarms
  - audit
  - api-limits
categories:
  - Security
---

# Logging and Monitoring Hardening

This page covers log export, timestamps, API abuse limits, alarm routing, and external monitoring of protection state. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

## AUD01: Export security logs outside the cluster

An off-cluster copy keeps security events safe from a compromised platform administrator.

**Default:** `remote_syslog_server` and `syslog_template` are empty.

**Configure:** In **System > Settings > Advanced Settings**, set `remote_syslog_server` to an external collector: `@@host:port` for TCP or `@host:port` for UDP. Authenticated TLS transport was not verified.

**Verify:** Make a failed test login and a harmless configuration change. At the collector, confirm the timestamp, source, and actor of each event.

## AUD02: Capture node logs and preserve trustworthy timestamps

**Default:** Node log capture has no explicit default. NTP uses time.nist.gov plus four pool hosts.

**Configure:** In **System > Nodes**, edit each node and keep **Capture Logs** on. In **System > Time Settings**, use approved, reachable time sources (see NET13 in [Networking Hardening](networking.md)).

**Verify:** Confirm logs from each node reach the collector with matching timestamps. In **System > Time Settings**, confirm each node shows as synchronized. Check the actual time peers on every node; one status sample does not prove time service behavior.

## AUD03: Retain finite API abuse limits

Finite limits on connections and per-session API load protect the management plane from exhaustion.

**Default:** `max_connections` is 500, `max_api_commands` is 50, and `max_sess_api_rate` is 50.

**Configure:** In **System > Settings > Advanced Settings**, keep all three values finite. Lower them only after you measure legitimate administrative and integration traffic.

{% hint style="warning" %}
Test lower limits on an isolated system first. Limits that are too low can block integrations and administrator access.
{% endhint %}

**Verify:** On an isolated system, lower `max_sess_api_rate` and compare a request sample before and after. Excess requests are delayed, not rejected, and still return success. Confirm that a separate administrator session stays responsive. Test the connection and command limits separately, then restore the original values.

## AUD04: Export application audit tables separately from node syslog

Remote syslog does not export every application log. Collect high-value logs separately so evidence outlives local retention and collector outages.

**Default:** Retention and export coverage vary by log and release.

**Configure:**

1. List the logs to keep: **System > Logs**, user **Logs** and **Current Sessions**, task **Logs**, SMTP logs, outgoing sync **Logs**, **NAS > Antivirus**, and archived alarms. Include per-user authentication and API key events, and session and permission changes.
2. Collect the logs that syslog does not export through a read-only integration.
3. Use a protected transport. The TCP `@@` syntax is not TLS, even on port 6514.
4. Set collector retention by policy (for example, 90 days).
5. If events from a collector outage are not replayed, add a second collection path.

**Verify:** Make test events in each selected log and compare counts, timestamps, and redaction at the collector. Stop the collector briefly and check for gaps. Check the actual retention period and record cap of each selected log. Confirm collection runs before local records expire or reach their cap. Confirm that a retention change takes effect before you rely on it.

## AUD05: Route alarms and exact-owner sync events through tested tasks

**Default:** Recipients, events, and delivery paths depend on the configured groups, tasks, and integrations.

**Configure:**

1. In **System > Tasks Dashboard**, use the built-in Send Event Email or a webhook task. Set **Enabled** to yes, **Delete Task After Running** to no, **Object Type** to Script, and **Action** to Run. Send to a group that has an owner.
2. Make separate events for **Critical Raised**, **Error Raised**, and **Critical Lowered**. Route completion messages elsewhere.
3. Bind **Outgoing Sync Error** (and optionally **Completed**) to each sync.
4. Add events for snapshot profile, task, and cluster changes, and for **User Logged In** on high-value accounts. Add **Critical System Log New** where the release supports it.
5. Where supported, add audit object filters for Snapshot Profile, Task, Cluster, User, Permission, Group, Site, VNet, and System.

Per-user audit entries do not necessarily trigger a global log task. Confirm whether the group sends to its group address, to members as BCC, or both, and protect its membership.

**Verify:** Send test mail and webhook events and confirm the severity, owner, recipient, and task log. Test **Raised** and **Lowered** separately. A cleared alarm does not close an incident. Test tampering with the notification path and a mail failure, and confirm you detect both through a separate route.

## AUD06: Monitor protection freshness and ransomware indicators externally

Error events do not show missing jobs or abnormal change. Watch for these from outside the platform.

**Default:** Thresholds depend on the workload and recovery policy.

**Configure:** Track the newest good local and remote recovery point for each protected scope. Also track sync queue progress, retries and retention skips, volume sync errors and deletes, antivirus results, write-rate changes, policy edits, and storage health. Set per-workload thresholds (for example, 1.5 times the snapshot interval, 80% tier use, 20% I/O wait). Confirm which conditions the product exposes before you design alert rules. Use [external monitoring](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/integrations-and-apis/external-monitoring) for conditions the product does not alert on, and do not give the collector write access.

Sources include **System Snapshots**, the outgoing sync **Snapshot Queue** and **Statistics**, **NAS > Volume Syncs**, **NAS > Antivirus**, and the storage tier and node dashboards.

**Verify:** Test missing-job detection separately from error alerts, and measure detection time. Match a harmless test event to its source record and to the receiver acknowledgment. Check immutable and remote snapshot availability, capacity, no-redundancy, bad-drive, and repair conditions. Test antivirus detection with a safe test file, and confirm a manual scan works before you rely on automatic protection.

## Related pages

- [Advanced System Settings](../system/advanced-system-settings.md)
- [Time Settings](../system/time-settings.md)
- [Nodes Overview](../system/nodes-overview.md)
- [Alarms](../operations/alarms.md)
- [SMTP](../system/smtp.md)
- [Volume Syncs](../nas/volume-syncs.md)
- [Webhooks](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/automation/webhooks)
- [Monitoring Site Syncs](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/monitoring-site-syncs)
- [System Snapshots](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/system-snapshots)
