---
title: Configuring Remote Log Forwarding (Syslog)
slug: configuring-remote-log-forwarding
description: How to configure VergeOS to forward system logs to a remote syslog server for centralized log management, archival, and compliance.
author: VergeOS Documentation Team
date: 2023-08-30T18:05:00.332Z
semantic_keywords:
  - "remote syslog log forwarding configuration"
  - "centralized log management archival compliance"
  - "rsyslog tcp udp template format"
  - "advanced settings syslog server setup"
use_cases:
  - remote_syslog_configuration
  - centralized_log_management
  - compliance_log_archival
  - log_retention_extension
tags:
  - logs
  - troubleshooting
  - support
categories:
  - Troubleshooting
editor: markdown
dateCreated: 2022-08-23T19:19:56.461Z
---

# Configuring Remote Log Forwarding (Syslog)

VergeOS can be configured to forward logs to a remote Syslog server, an important capability for organizations leveraging log aggregation for centralized management, log archival, and compliance. 

{% hint style="success" %}
**Log Retention**

Logged activity is typically available within the VergeOS user interface for a maximum of **45 days**. Configure remote log forwarding to retain logs for longer periods.
{% endhint %}

## Prerequisites

- Network connectivity between VergeOS and the remote syslog server
- Appropriate firewall rules to allow syslog traffic (typically port 514)
- Access to VergeOS System Settings

## Configuration Steps

To configure log forwarding to a remote syslog server:

### 1. Navigate to Advanced Settings

Navigate to **System > Settings > Advanced Settings**.

### 2. Configure the Remote Syslog Server

1. Under the "Setting" column heading, type `syslog` and press **Enter** to search
2. Select and edit **Remote syslog server (tcp: @@name/ip:port, udp: @name/ip:port)**
3. Configure this setting according to the syntax expected by your remote server:

{% hint style="info" %}
**Server Configuration Examples**

- **For TCP:** `@@10.10.10.10:514`
- **For UDP:** `@10.10.10.10:514`
{% endhint %}

{% hint style="info" %}
**Choosing TCP or UDP**

- **TCP (`@@`)** provides guaranteed delivery; use it for audit and compliance logging.
- **UDP (`@`)** is fire-and-forget: lower overhead, but messages can drop under load.
{% endhint %}

{% hint style="info" %}
**Collector Port**

Listening on port 514 requires root privileges on the collector. Many collectors run unprivileged (for example, in containers) and listen on port **1514** instead. Enter the port your collector listens on.
{% endhint %}

4. Click **Submit** at the bottom of the page to save

### 3. Configure the Format Template

1. Search for `syslog` again in the settings
2. Select and edit **Template to define for syslog server (See rsyslog for format)**
3. Enter a syslog template format that is compatible with your remote syslog server

{% hint style="info" %}
**Template Example**

```plaintext
   RFC5424,"<%PRI%>1 %TIMESTAMP:::date-rfc3339% %HOSTNAME%.your-hostname-here %APP-NAME% %PROCID% %MSGID% %STRUCTURED-DATA% %msg%\n"
```
{% endhint %}

{% hint style="warning" %}
Use the literal `1` after `<%PRI%>` — it is the RFC 5424 version field. Do not use `%PROTOCOL-VERSION%`: it renders as `0` on the wire, and strict RFC 5424 collectors (Promtail/Loki, Fluent Bit, modern Graylog) reject version 0 with parse errors.
{% endhint %}

{% hint style="info" %}
Replace `your-hostname-here` with your actual hostname, or leave as `.HOSTNAME_HERE` to use the default system hostname.
{% endhint %}

{% hint style="info" %}
**Forwarding from Multiple VergeOS Systems**

`%HOSTNAME%` resolves to the bare node name (`node1`, `node2`), which is ambiguous when several VergeOS systems forward to the same collector. Common hostname patterns:

| Pattern | Example output | Use |
|---------|----------------|-----|
| `%HOSTNAME%` | `node1` | A single system |
| `mycluster-%HOSTNAME%` | `mycluster-node1` | A prefix per system; recommended for multiple systems |
| `%HOSTNAME%.mycluster.example.com` | `node1.mycluster.example.com` | FQDN style |
{% endhint %}

4. Click **Submit** at the bottom of the page to save the format

## Collector Notes

The RFC 5424 template above works with common collectors:

| Collector | Configuration notes |
|-----------|---------------------|
| Graylog | Use a **Syslog TCP** or **Syslog UDP** input. |
| Loki | Use a Promtail `syslog` scrape job; Promtail requires strict RFC 5424 (the literal `1` version). |
| Splunk | Use a TCP or UDP data input, or Splunk Connect for Syslog. |
| Elasticsearch | Ingest through Logstash with the `syslog` input plugin. |
| rsyslog relay | Use a standard `imtcp` or `imudp` listener. |

## Additional Resources

For more information on syslog templates and formatting options, visit the [Rsyslog Documentation](https://www.rsyslog.com/doc/master/configuration/examples.html).

## Verification

After you save the configuration, VergeOS begins forwarding logs to the specified server. Check the collector to confirm VergeOS logs arrive.

If logs do not arrive:

1. On the collector host, capture traffic on the configured syslog port to confirm packets arrive:

    ```bash
    tcpdump -i any -A port 514
    ```

2. Inspect the captured messages to verify the wire format. An RFC 5424 message starts with `<PRI>1` (for example, `<30>1 2026-04-15T...`); a version of `0` means the template still uses `%PROTOCOL-VERSION%` — see the template warning above.
3. Make sure firewall rules between VergeOS and the collector allow the configured port and protocol.
