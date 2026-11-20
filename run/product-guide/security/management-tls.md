---
title: "Management Access and TLS Hardening"
description: "Harden VergeOS management access: install trusted certificates, restrict TLS cipher suites, remove unneeded HTTP listeners, and limit trusted root CAs."
semantic_keywords:
  - "VergeOS management TLS certificate hardening"
  - "restrict HTTPS listener cipher suites"
  - "disable HTTP port 80 listener"
  - "trusted root CA inventory"
use_cases:
  - install_trusted_management_certificate
  - restrict_tls_cipher_suites
  - disable_plaintext_http_listener
  - limit_trusted_root_cas
tags:
  - security
  - hardening
  - tls
  - certificates
  - listeners
  - ciphers
  - root-ca
categories:
  - Security
---

# Management Access and TLS Hardening

This page covers the certificates, listeners, and trusted root CAs that protect access to the VergeOS management UI. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

## TLS01: Configure management TLS certificates

Clients must authenticate the management hostname before they send credentials.

**Default:** Installation creates a self-signed certificate. HTTPS uses port 443.

**Configure:** In **System > Certificates**, click **New**. Select **Manual** and enter the certificate, private key, and issuing chain, or select **Let's Encrypt** to issue through an approved ACME service. Cover every management and tenant hostname. Keep the default local access certificate. Set an expiry alert, for example 30 days before expiration. Make sure ACME challenge access does not expose the management UI.

**Verify:** From each supported client, confirm the chain, hostname, lifetime, and SNI. A wrong CA or hostname must fail before credentials are sent. Check the certificate with strict parsing:

```bash
openssl verify -x509_strict -CAfile CA.pem -verify_hostname MANAGEMENT_DNS server.pem
```

Then check the live listener. Run this command for each hostname, with your approved trust roots. The handshake must fail on any verification error. Do not assume that you can select a certificate per listener.

```bash
openssl s_client -connect MANAGEMENT_DNS:443 -servername MANAGEMENT_DNS -CAfile CA.pem -verify_hostname MANAGEMENT_DNS -verify_return_error </dev/null
```

## TLS02: Limit management TLS cipher suites

Remove static RSA key exchange and CBC suites where clients support forward-secret AEAD suites.

**Default:** **Cipher** is empty, which uses the built-in cipher set.

{% hint style="warning" %}
Test the cipher string on a separate listener first. A string your clients cannot negotiate blocks management access.
{% endhint %}

**Configure:** In **System > Certificates > Listeners**, edit the HTTPS listener and set **Cipher**, for example `ECDHE+AESGCM:ECDHE+CHACHA20`. This field controls TLS 1.2 suites only, not TLS 1.3 suites or protocol versions.

**Verify:** A TLS 1.2 handshake with a CBC or static RSA suite fails. ECDHE AEAD and TLS 1.3 clients still connect.

```bash
openssl s_client -connect MANAGEMENT_DNS:443 -tls1_2 -cipher AES128-SHA </dev/null
```

## TLS03: Remove unnecessary HTTP entry points

**Default:** Two listeners exist: HTTPS on port 443 and HTTP on port 80, which redirects to HTTPS.

**Configure:**

1. In **System > Certificates > Listeners**, edit the HTTP listener and clear **Enabled**.
2. In the External network's **Rules**, remove unneeded port 80 rules and click **Apply Rules**.

Keep port 80 only for an approved dependency, such as ACME HTTP validation.

**Verify:**

- **Listener disabled:** From each network zone, port 80 is unreachable and HTTPS works.
- **Port 80 kept for ACME validation:** The challenge is reachable from outside, and a certificate renewal succeeds. An HTTP request to the management UI gives no plain-text access. Filter port 80 by source only if your CA publishes its validation addresses. Let's Encrypt does not, so a source filter can break a later renewal.

## TLS04: Limit trusted CA roots and certificate renewal exposure

Control which issuers VergeOS trusts to authenticate other services.

**Default:** Depends on the environment.

{% hint style="warning" %}
Test each trust-store change against the identity provider, Site Sync, and other outbound integrations. A missing root breaks those connections.
{% endhint %}

**Configure:** In **System > Certificates > Root CAs**, add only roots and intermediates that your PKI team approves. Check the fingerprint, subject, issuer, and validity first. Do not add a server certificate as a trust anchor. Record the owner, purpose, and expiry of each CA, and remove retired CAs.

Do not add broad roots in case they are needed later.

**Verify:** Compare **Root CAs** with your trusted inventory. A service from an approved issuer connects. An untrusted, expired, or wrong-hostname certificate fails. Test certificate renewal, and confirm the certificate each listener presents after renewal.

## Related pages

- [Server Certificates](../system/certificates.md)
- [Configuring the Sites Dashboard (Adding Sites)](../system/site-dashboard-add-sites.md)
