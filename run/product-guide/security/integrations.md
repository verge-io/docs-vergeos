---
title: "Integrations Hardening"
description: "Harden VergeOS integrations: validate certificates for repositories and VMware services, restrict catalog publishing, and protect webhooks, SMTP, and auth source logging."
semantic_keywords:
  - "VergeOS allow insecure certificate validation"
  - "catalog publishing scope private"
  - "webhook HTTPS authorization hardening"
  - "SMTP TLS SASL relay for MFA email"
  - "authentication source debug logging"
use_cases:
  - validate_external_endpoint_certificates
  - restrict_catalog_publication
  - secure_outbound_webhooks
  - secure_smtp_relay
  - disable_auth_source_debug
tags:
  - security
  - hardening
  - integrations
  - certificates
  - catalogs
  - webhooks
  - smtp
  - authentication
categories:
  - Security
---

# Integrations Hardening

This page covers certificate validation for external endpoints, catalog publishing, webhooks, SMTP, and authentication source logging. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

## INT01: Validate external repository and migration endpoints

Certificate validation stops an impersonated service from capturing credentials or supplying untrusted content.

**Default:** **Allow Insecure Certificates** is off for catalog repositories and VMware services.

**Configure:** Use approved HTTPS endpoints and keep **Allow Insecure Certificates** clear on each repository and VMware service. For an internal CA, register it in **System > Certificates > Root CAs > New** instead of turning on **Allow Insecure Certificates**.

**Verify:** Against a test endpoint, confirm a wrong or untrusted certificate fails before authentication or download. Confirm the approved endpoint works with its trusted chain.

## INT02: Restrict catalog publication

**Default:** **Publishing Scope** is **Private**.

**Configure:** Edit each catalog that must not reach tenants or other systems and set **Publishing Scope** to **Private**. Control who can edit or publish catalogs with IAM06 in [Identity and Access Hardening](identity-access.md).

**Verify:** Confirm an identity or tenant outside the permitted audience cannot see the catalog, and an authorized administrator can still use it. Separately, test publication changes under the IAM06 permissions.

## INT03: Protect outbound webhooks

**Default:** **Allow Insecure Certificates** is off. **Authorization Type** is none. The URL accepts HTTP or HTTPS.

**Configure:** In **System > Tasks Dashboard**, edit each webhook:

1. Use an approved HTTPS **URL** and keep **Allow Insecure Certificates** clear.
2. Set the **Authorization Type** the receiver requires, with a credential scoped to alert ingestion.
3. Keep **Timeout** and **Retries** finite. The defaults are 5 seconds and 3 retries.

Send only the event data the receiver needs, and restrict who can change webhooks.

**Verify:** Send a test event with no real secrets to the receiver. Test receiver authentication. Confirm a server with an untrusted certificate is rejected.

## INT04: Protect SMTP when used for security notifications or MFA

**Default:** SMTP **Enabled** is on. **Use TLS** and **Use SASL Authorization** are not set.

{% hint style="warning" %}
Test mail delivery before you depend on email MFA. A failed relay blocks MFA codes.
{% endhint %}

**Configure:** In **System > SMTP > Edit Settings**, set the approved **Relay Host** and **Relay Port** (587 with STARTTLS; port 465 with implicit TLS does not work). Turn on **Use TLS** and **Use SASL Authorization**, and protect the relay credential. **Use TLS** requires encryption, so delivery fails instead of falling back to plain text. Confirm **Hostname** and **From Address** with the mail owner. A port change alone does not prove encryption.

**Verify:** Click **Send Test Email** and check the **Mail Queue** and **Mail Log**. On the relay, confirm the session used TLS. Alert on SMTP failure through a separate channel.

## INT05: Disable authentication source debug logging

**Default:** **Debug** is off. When on, it stops automatically after one hour.

**Configure:** In **System > Auth Sources**, keep **Debug** clear on each source during normal operation.

**Verify:** Confirm normal successful and failed login events still appear in the logs without verbose provider diagnostics. **Debug** does not configure external MFA or group authorization.

## Related pages

- [Server Certificates](../system/certificates.md)
- [SMTP](../system/smtp.md)
- [Authorization Sources - Overview](../auth/auth-sources-general.md)
- [Two-Factor Authentication (MFA)](../auth/multifactor-auth.md)
- [Transitioning from VMware to VergeOS](../intro/transition-from-vmware.md)
- [Webhooks](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/automation/webhooks)
- [Recipe catalogs and repositories](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/automation/recipes-organization)
