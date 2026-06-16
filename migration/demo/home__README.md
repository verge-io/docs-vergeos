---
description: A GitBook-first view of the VergeOS platform, tuned for deployment, operations, and automation journeys.
icon: house
cover: .gitbook/assets/verge-home-cover.jpg
coverY: 0
layout:
  width: wide
  cover:
    visible: true
    size: full
---

# VergeOS docs, rebuilt for platform operators

Verge.io already has deep technical content. This demo reorganizes it into clearer operator journeys so infrastructure teams can move from evaluation to deployment to day-2 automation without fighting a large MkDocs tree.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><h3><i class="fa-compass-drafting" style="color:#C4502D;">:triangular_ruler:</i></h3></td><td><strong>Plan and deploy</strong></td><td>Implementation guidance, network design, sizing, and reference architectures.</td><td><a href="https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/">deploy</a></td></tr><tr><td><h3><i class="fa-server" style="color:#C4502D;">:desktop_computer:</i></h3></td><td><strong>Run the platform</strong></td><td>Storage, networking, system administration, and virtual machine operations.</td><td><a href="https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/">run</a></td></tr><tr><td><h3><i class="fa-robot" style="color:#C4502D;">:robot_face:</i></h3></td><td><strong>Automate, protect, and extend</strong></td><td>Backup and DR, recipes, CLI and SDKs, webhooks, and Private AI.</td><td><a href="https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/">automate</a></td></tr></tbody></table>

{% hint style="info" %}
This is a first-draft GitBook demo based on the current public Verge docs and repo structure as of June 8, 2026. The goal is to show a stronger docs product shape, not to replace Verge's source of truth.
{% endhint %}

## Why this shape works better in GitBook

{% columns %}
{% column %}
### Better top-level routing

- Clear separation between deployment, operations, and automation
- Shorter paths into the highest-value workflows
- Fewer "where do I start?" decisions for new operators
{% endcolumn %}

{% column %}
### Better sales-demo moments

- A homepage that explains the platform story up front
- Cross-space navigation for VMware migration and Private AI
- Higher-signal landing pages before the long-tail detail
{% endcolumn %}
{% endcolumns %}

## Start with the operator journey

{% stepper %}
{% step %}
### Evaluating VergeOS against VMware
Start with [Run the platform -> What is VergeOS](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/product-guide/intro/what-is-vergeos) and [Transitioning from VMware](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/product-guide/intro/transition-from-vmware).
{% endstep %}

{% step %}
### Designing a new deployment
Move into [Plan and deploy](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/) for sizing, network design, install sequencing, and reference architectures.
{% endstep %}

{% step %}
### Operationalizing the estate
Use [Automate, protect, and extend](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/) for snapshots, site syncs, recipes, API keys, CLI flows, and Private AI.
{% endstep %}
{% endstepper %}

## High-signal paths

- New deployment blueprint: [Implementation guide](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/intro)
- VMware migration story: [Transitioning from VMware](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/product-guide/intro/transition-from-vmware)
- Core platform concepts: [Platform capabilities](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/product-guide/intro/platform-capabilities)
- Built-in resilience: [Backup & disaster recovery](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/product-guide/backup-dr/overview)
- Automation surface: [VergeOS CLI](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/product-guide/tools-integrations/vrg-cli)
- Local model hosting: [Private AI overview](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/product-guide/private-ai/overview)

<a class="button primary" href="https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/">Explore the deployment path</a>
<a class="button" href="support-and-services.md">See support and service paths</a>
