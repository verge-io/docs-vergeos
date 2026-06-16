---
description: Key handoff paths for implementation support, architecture validation, and operational follow-through.
icon: life-ring
---

# Support and services

This demo is strongest when it pairs product depth with a clear adoption path.

{% columns %}
{% column %}
### Pre-production

- Validate topology with [reference architectures](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/reference-architecture/edge)
- Check hardware and sizing assumptions
- Align VMware migration scope before first install
{% endcolumn %}

{% column %}
### Post-install

- Use [post-installation](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/post-installation) as the initial hardening checklist
- Stand up [snapshots](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/product-guide/backup-dr/snapshots-overview) and [site syncs](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/product-guide/backup-dr/syncs-overview)
- Standardize day-2 operations with [recipes](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/product-guide/automation/recipes-overview) and [vrg](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/product-guide/tools-integrations/vrg-cli)
{% endcolumn %}
{% endcolumns %}

{% hint style="success" %}
For a prospect demo, the strongest follow-up is usually a scoped walkthrough of deployment design plus one automation or DR workflow, not a tour of every subsystem.
{% endhint %}
