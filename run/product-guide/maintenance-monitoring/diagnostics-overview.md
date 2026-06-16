---
title: "VergeOS Diagnostics Overview"
description: "Overview of all diagnostic tools available in VergeOS, including component-specific diagnostics for networks, nodes, vSAN, and NAS, as well as system-wide tools like subscriptions and Prometheus integration."
semantic_keywords:
  - "VergeOS diagnostics troubleshooting tools"
  - "network node vSAN NAS diagnostics"
  - "system monitoring and alerting VergeOS"
  - "Prometheus Grafana integration VergeOS"
  - "proactive monitoring best practices"
use_cases:
  - system_troubleshooting
  - performance_monitoring
  - proactive_alerting
  - diagnostic_data_collection
  - third_party_monitoring_integration
tags:
  - diagnostics
  - monitoring
  - troubleshooting
  - alerting
  - prometheus
  - subscriptions
  - network
  - vsan
  - nas
  - nodes
categories:
  - System Administration
---

# VergeOS Diagnostics Overview

VergeOS provides comprehensive diagnostic tools integrated throughout the platform to help system administrators monitor, troubleshoot, and maintain optimal performance across all virtualization components.

## Component-Specific Diagnostics

<div class="grid cards" markdown>

-   :fontawesome-solid-network-wired: __Network Diagnostics__

    ---

    Network infrastructure troubleshooting and performance analysis

    **Access:** Networks → [Select Network] → Diagnostics

    [:octicons-arrow-right-24: Network Diagnostics Guide](../networks/network-diagnostics.md)

-   :fontawesome-solid-server: __Node Diagnostics__

    ---

    Hardware and system-level troubleshooting

    **Access:** Nodes → [Select Node] → Diagnostics

    [:octicons-arrow-right-24: Node Diagnostics Guide](../system/node-diagnostics.md)

-   :fontawesome-solid-database: __vSAN Diagnostics__

    ---

    Storage system analysis and troubleshooting

    **Access:** System → vSAN Diagnostics

    [:octicons-arrow-right-24: vSAN Diagnostics Guide](../storage/vsan-diagnostics.md)

-   :fontawesome-solid-folder-open: __NAS Diagnostics__

    ---

    Network Attached Storage service troubleshooting

    **Access:** NAS → [Select NAS Service] → Diagnostics

    [:octicons-arrow-right-24: NAS Diagnostics Guide](../nas/nas-diagnostics.md)

</div>

## System-Wide Tools

<div class="grid cards" markdown>

-   :fontawesome-solid-stethoscope: __System Diagnostics__

    ---

    Comprehensive system-wide diagnostic data collection with direct support integration

    **Access:** System → System Diagnostics

    [:octicons-arrow-right-24: System Diagnostics Documentation](../system/diagnostics.md)

-   :fontawesome-solid-bell: __Subscriptions & Alerts__

    ---

    Proactive monitoring and automated notifications

    **Access:** System → Subscriptions

    [:octicons-arrow-right-24: Subscriptions Overview](../system/subscriptions-overview.md)

-   :fontawesome-solid-chart-line: __Prometheus Exporter__

    ---

    Integration with external monitoring systems (Grafana, AlertManager)

    **Access:** System → Prometheus Exporter

    [:octicons-arrow-right-24: Prometheus Exporter](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/product-guide/tools-integrations/prometheus-exporter)

</div>

## Best Practices

**Systematic Approach:**

1. Define the problem scope and timeline
2. Start with targeted component diagnostics
3. Use System Diagnostics for complex issues
4. Document findings and escalate when needed

**Proactive Monitoring:**

- Set up Subscriptions for ongoing health monitoring
- Use Prometheus integration for long-term trend analysis
- Establish performance baselines with diagnostic tools

---

{% hint style="success" %}
**Need Help?**

For complex issues or performance optimization, contact [VergeOS Support](https://app.gitbook.com/s/uJc5d3O7cwI7qD8muSyG/support-and-services) with System Diagnostics data and detailed issue descriptions.
{% endhint %}
