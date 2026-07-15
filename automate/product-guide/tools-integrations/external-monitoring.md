---
title: External Monitoring
semantic_keywords:
  - VergeOS SNMP support, SNMP not supported, MIB trap agent
  - external monitoring integration VergeOS, observability tooling
  - Prometheus Exporter ioMetrics, vSAN cluster node metrics
  - VergeOS REST API monitoring, custom HTTP collector polling
  - IPMI hardware sensors per-node monitoring BMC
  - SolarWinds LogicMonitor VergeOS, SNMP-first monitoring tools
use_cases:
  - external_monitoring_integration
  - prometheus_metrics_collection
  - rest_api_polling_for_metrics
  - hardware_health_monitoring
  - snmp_tool_workaround
categories:
  - Automation
description: >-
  VergeOS does not support SNMP. This guide covers the supported paths for
  external monitoring — the Prometheus Exporter (ioMetrics), the REST API, and
  IPMI — plus SNMP-first tools like SolarWinds.
tags:
  - monitoring
  - observability
  - snmp
  - prometheus
  - api
  - ipmi
  - integrations
---

# External Monitoring

## Overview

This page describes how to integrate VergeOS with external monitoring and observability platforms. VergeOS is API-first and exposes platform health, performance, and hardware sensor data through three supported paths.

{% hint style="warning" %}
**SNMP is not supported**

VergeOS does not include an SNMP agent, MIB, or trap mechanism. SNMP was designed in the late 1980s for managing hardware network devices, such as routers, switches, and printers, not modern software-defined platforms. VergeOS is API-first: every metric and resource an SNMP agent would expose is already available through the REST API and the Prometheus Exporter, which provide richer structured data over standard HTTP. This mirrors the broader industry shift, with Microsoft deprecating the SNMP service in Windows Server 2012, and cloud-native and hypervisor platforms standardizing on the Prometheus exposition format. If your legacy monitoring tool requires SNMP, see [SNMP-First Tools](external-monitoring.md#snmp-first-tools) below for the available workarounds.
{% endhint %}

### Supported Monitoring Paths

| Path                                                                                    | Use For                                 | Audience                                         |
| --------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------ |
| [Prometheus Exporter (ioMetrics)](external-monitoring.md#prometheus-exporter-iometrics) | vSAN, cluster, and node metrics         | Recommended starting point for most environments |
| [REST API](external-monitoring.md#rest-api)                                             | Custom collectors, polling any resource | Tool-specific integrations, scripted checks      |
| [IPMI](external-monitoring.md#ipmi)                                                     | Per-node hardware health and sensors    | Hardware-level monitoring outside VergeOS        |

***

## Prometheus Exporter (ioMetrics)

The **VergeOS Prometheus Exporter (ioMetrics)** is the recommended path for platform-level metrics. It collects vSAN tier, cluster, and node-level metrics from VergeOS and exposes them in standard Prometheus format, ready for scraping by Prometheus, Grafana, VictoriaMetrics, or any Prometheus-compatible system.

### Why This Is the Recommended Path

* **First-party** — maintained in the verge-io organization
* **Standards-based** — any Prometheus-compatible monitoring tool can consume the output

See the [Prometheus Exporter (ioMetrics)](prometheus-exporter.md) page for the in-product overview, exposed metrics, and links to the open-source project.

***

## REST API

The VergeOS REST API exposes every resource the UI can read, which makes it the right path for custom collectors, scripted health checks, or integrating with tools that don't speak Prometheus.

### Authentication

External monitoring collectors are long-running and should authenticate with an API Key rather than a session token. API Keys are created per user and can be IP-scoped and given an expiration. See [API Keys](../system/api-keys.md) for setup and the [API Guide](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/automation-api/verge-api-guide) for the full list of supported authentication methods.

### Swagger Documentation

The complete, version-accurate API reference is available inside VergeOS:

1. Click the **user icon** in the top-right of the VergeOS UI.
2. Select **System**.
3. Select **API Documentation**.

The Swagger page lists every table and operation, with examples that can be run directly against the system.

{% hint style="success" %}
**Where to Start**

For background on HTTP conventions, filtering, sorting, and example requests, see the [API Guide](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/automation-api/verge-api-guide) in the knowledge base.
{% endhint %}

### When to Use the REST API for Monitoring

* The monitoring tool supports HTTP polling but not Prometheus
* A specific metric or resource is not exposed by the Prometheus Exporter
* A custom collector is needed to integrate with an in-house observability platform

***

## IPMI

For **per-node hardware health and sensor data** — temperature, fan speed, voltage, power draw, hardware errors — VergeOS surfaces the node's IPMI interface directly.

1. Navigate to **Infrastructure > Nodes** from the top menu.
2. Double-click the desired node to open the node dashboard.
3. Under the **IPMI** submenu, click **Connect** to open the IPMI web interface in a new tab, or **Test** to verify connectivity from VergeOS.

{% hint style="info" %}
**Hardware-Only**

IPMI exposes the **physical hardware** state of a host node — not VergeOS application-layer metrics. Most monitoring platforms already include IPMI collectors that can poll the node BMCs directly, in parallel with the Prometheus Exporter and REST API paths above.
{% endhint %}

For configuring stored IPMI credentials and testing connectivity, see the [IPMI](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/ipmi) page.

***

## SNMP-First Tools

Tools such as **SolarWinds**, **LogicMonitor**, **PRTG**, and **Nagios** are often configured to monitor infrastructure over SNMP. VergeOS has no turnkey integration for these tools because there is no SNMP agent to point them at.

{% hint style="success" %}
**Check for Native Prometheus Support First**

Some of these platforms now ingest Prometheus metrics natively — **LogicMonitor** (OpenMetrics DataSource) and **SolarWinds Observability** (Prometheus integration). If your platform is one of them, point it at the [Prometheus Exporter](external-monitoring.md#prometheus-exporter-iometrics) and skip the rest of this section. The two options below cover tools that don't speak Prometheus — including the on-prem **SolarWinds Platform / SAM**, **PRTG**, and **Nagios**.
{% endhint %}

### Option 1 — Custom REST Collector

Most enterprise monitoring platforms allow custom HTTP/REST collectors:

| Platform     | Mechanism                           |
| ------------ | ----------------------------------- |
| SolarWinds   | API Poller (SAM)                    |
| LogicMonitor | Scripted DataSource (Groovy / HTTP) |
| PRTG         | HTTP XML/REST Custom Sensor         |
| Nagios       | `check_http` / custom plugin        |

Point the collector at the VergeOS REST API, authenticate per the [API Guide](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/automation-api/verge-api-guide), and parse the JSON response. This is the lowest-overhead path — no intermediate process to maintain, and the collector talks directly to the source of truth.

### Option 2 — Prometheus-to-SNMP Bridge

If the monitoring tool only speaks SNMP and a custom collector is not an option, the community pattern is to run the [Prometheus Exporter](external-monitoring.md#prometheus-exporter-iometrics) and place a Prometheus-to-SNMP bridge in front of it. The bridge re-exposes Prometheus metrics as SNMP OIDs that an SNMP poller can scrape.

{% hint style="warning" %}
**Not Verge-Supported**

Prometheus-to-SNMP bridges are community projects and are not built, tested, or supported by Verge. We do not endorse a specific bridge — the choice depends on which subset of Prometheus metrics needs to be re-exposed and how the downstream tool consumes SNMP. Treat this path as a stopgap, not a long-term integration.
{% endhint %}

***

## Choosing a Path

| Scenario                                                  | Recommended Path                                                                                                                                                                               |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| New monitoring deployment, no existing tooling commitment | [Prometheus Exporter](external-monitoring.md#prometheus-exporter-iometrics) + Grafana                                                                                                          |
| Existing Prometheus / Grafana / VictoriaMetrics stack     | [Prometheus Exporter](external-monitoring.md#prometheus-exporter-iometrics)                                                                                                                    |
| Monitoring tool that polls HTTP but not Prometheus        | [REST API](external-monitoring.md#rest-api) custom collector                                                                                                                                   |
| Hardware health (temperature, fans, power)                | [IPMI](external-monitoring.md#ipmi)                                                                                                                                                            |
| SolarWinds / LogicMonitor / PRTG / Nagios (SNMP-first)    | [Custom REST Collector](external-monitoring.md#option-1-custom-rest-collector) preferred, [Prometheus-to-SNMP Bridge](external-monitoring.md#option-2-prometheus-to-snmp-bridge) as a fallback |

## Next Steps

* [Prometheus Exporter (ioMetrics)](prometheus-exporter.md) — in-product overview and links to the open-source project
* [API Guide](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/automation-api/verge-api-guide) — authentication, HTTP conventions, and example requests
* [IPMI](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/ipmi) — testing connectivity, managing credentials, and accessing the IPMI web interface

## Documentation and Resources

| Resource                                                                                        | Description                                 |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------- |
| [vergeos-exporter](https://github.com/verge-io/vergeos-exporter)              | Open-source Prometheus exporter for VergeOS |
| [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/) | Upstream Prometheus docs                    |
| [Grafana Documentation](https://grafana.com/docs/)                            | Building dashboards on Prometheus metrics   |
