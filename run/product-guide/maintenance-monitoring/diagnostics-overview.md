---
title: VergeOS Diagnostics Overview
semantic_keywords:
  - VergeOS diagnostics troubleshooting tools
  - network node vSAN NAS diagnostics
  - system monitoring and alerting VergeOS
  - Prometheus Grafana integration VergeOS
  - proactive monitoring best practices
use_cases:
  - system_troubleshooting
  - performance_monitoring
  - proactive_alerting
  - diagnostic_data_collection
  - third_party_monitoring_integration
categories:
  - System Administration
description: >-
  Overview of diagnostic tools in VergeOS, including component-specific
  diagnostics for networks, nodes, vSAN, and NAS, plus system-wide tools like
  subscriptions and Prometheus integration.
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
---

# VergeOS Diagnostics Overview

VergeOS provides comprehensive diagnostic tools integrated throughout the platform to help system administrators monitor, troubleshoot, and maintain optimal performance across all virtualization components.

## Component-Specific Diagnostics

*   **Network Diagnostics**

    Network infrastructure troubleshooting and performance analysis

    **Access:** Networks → \[Select Network] → Diagnostics

    [Network Diagnostics Guide](../networks/network-diagnostics.md)
*   **Node Diagnostics**

    Hardware and system-level troubleshooting

    **Access:** Nodes → \[Select Node] → Diagnostics

    [Node Diagnostics Guide](../system/node-diagnostics.md)
*   **vSAN Diagnostics**

    Storage system analysis and troubleshooting

    **Access:** System → vSAN Diagnostics

    [vSAN Diagnostics Guide](../storage/vsan-diagnostics.md)
*   **NAS Diagnostics**

    Network Attached Storage service troubleshooting

    **Access:** NAS → \[Select NAS Service] → Diagnostics

    [NAS Diagnostics Guide](../nas/nas-diagnostics.md)

## System-Wide Tools

*   **System Diagnostics**

    Comprehensive system-wide diagnostic data collection with direct support integration

    **Access:** System → System Diagnostics

    [System Diagnostics Documentation](../system/diagnostics.md)
*   **Subscriptions & Alerts**

    Proactive monitoring and automated notifications

    **Access:** System → Subscriptions

    [Subscriptions Overview](../system/subscriptions-overview.md)
*   **Prometheus Exporter**

    Integration with external monitoring systems (Grafana, AlertManager)

    **Access:** System → Prometheus Exporter

    [Prometheus Exporter](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/integrations-and-apis/prometheus-exporter)

## Best Practices

**Systematic Approach:**

1. Define the problem scope and timeline
2. Start with targeted component diagnostics
3. Use System Diagnostics for complex issues
4. Document findings and escalate when needed

**Proactive Monitoring:**

* Set up Subscriptions for ongoing health monitoring
* Use Prometheus integration for long-term trend analysis
* Establish performance baselines with diagnostic tools

***

{% hint style="success" %}
**Need Help?**

For complex issues or performance optimization, contact [VergeOS Support](https://app.gitbook.com/s/uJc5d3O7cwI7qD8muSyG/support-and-services) with System Diagnostics data and detailed issue descriptions.
{% endhint %}
