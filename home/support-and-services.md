---
description: Documentation to lean on before and after you go live — architecture validation, hardening, and day-two operations.
icon: life-ring
---

# Support and services

Reach the VergeOS support team, or use the guides below to lean on before and after you go live.

## Contact support

- **Email:** [support@verge.io](mailto:support@verge.io)
- **Phone:** [855-855-8300](tel:+18558558300)

## Documentation paths

{% columns %}
{% column %}
### Before you deploy

- Validate your topology against the [reference architectures](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/reference-architectures/edge)
- Check your hardware and sizing assumptions before you order or rack nodes
- Scope your VMware migration before the first install
{% endcolumn %}

{% column %}
### After you install

- Work through [post-installation](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/post-installation) as your initial hardening checklist
- Stand up [snapshots](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/snapshots-overview) and [site syncs](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/syncs-overview) to protect your data
- Standardize day-two operations with [recipes](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/automation/recipes-overview) and the [vrg CLI](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/integrations-and-apis/vrg-cli)
{% endcolumn %}
{% endcolumns %}

{% hint style="success" %}
Just getting started? Focus on your deployment design plus one data-protection workflow — snapshots or site syncs — before exploring every subsystem.
{% endhint %}
