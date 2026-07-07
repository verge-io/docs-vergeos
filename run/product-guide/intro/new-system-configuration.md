---
title: New System Configuration
semantic_keywords:
  - VergeOS new system setup checklist
  - post-installation configuration production readiness
  - SMTP certificates licensing initial setup
  - authentication MFA alerting snapshot configuration
  - VergeOS first-time system configuration
use_cases:
  - initial_system_setup
  - production_readiness_checklist
  - security_configuration
  - alerting_and_reporting_setup
  - snapshot_schedule_configuration
  - authentication_setup
categories:
  - Getting Started
description: >-
  Post-installation checklist for preparing a new VergeOS system for production,
  covering cluster settings, licensing, SMTP, certificates, alerting, snapshots,
  and authentication configuration.
tags:
  - configuration
  - setup
  - post-installation
  - licensing
  - smtp
  - certificates
  - alerting
  - snapshots
  - authentication
  - mfa
---

# New System Configuration

This page will guide you through preparing your installed VergeOS system for production; including configuration steps to ensure optimum performance, security, and reliability. For instructions on planning and completing an installation, refer to the [VergeOS Implementation Guide](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/intro).

## System and Network Verification

{% hint style="info" %}
**Before proceeding:**

* **Verify system status** (all green status indicators)
* **Ensure correct networking configuration**

Refer to [**Implementation Guide - Post-Installation**](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/post-installation) for instructions on verifying system status and networking.
{% endhint %}

## New System Task List

* [ ] [Review/Adjust Cluster Settings](new-system-configuration.md#cluster-settings)
* [ ] [Confirm Licensing/Updates](new-system-configuration.md#licensingupdates)
* [ ] [Configure SMTP](new-system-configuration.md#smtp)
* [ ] [Register a Server Certificate](new-system-configuration.md#server-certificate)
* [ ] [Establish Alerting/Reporting](new-system-configuration.md#alerting-and-reporting)
* [ ] [Verify System Snapshot Settings](new-system-configuration.md#system-snapshot-settings)
* [ ] [Configure Authorization/Authentication Settings](new-system-configuration.md#authenticationauthorization-settings)
* [ ] [Optional - Enable Third-party Logging](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/troubleshooting/configuring-remote-log-forwarding)

## Cluster Settings

For each cluster, it's advisable to review and fine-tune settings during initial configuration because:

* Most cluster changes require node reboots
* Some cluster settings will be important to establish before putting your system into production

The [**Cluster Settings Guide**](../system/cluster-settings.md) provides detailed information regarding available settings.

{% hint style="success" %}
**Learn about VergeOS Cluster Basics here:** [**Clusters Overview Guide**](../system/clusters-overview.md)
{% endhint %}

## Licensing/Updates

1. [**Verify Your VergeOS Licensing**](../system/license-updates-verify.md): This will ensure your system will be able to run VMs, start NAS services, and run updates.
2. [**Update your System**](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/system-administration/updating-vergeos-system): Perform an update if your system is not running the most up-to-date version. Running the newest version of VergeOS will guarantee you have all the latest features and improvements.

{% hint style="success" %}
[**VergeOS Release Notes**](https://app.gitbook.com/o/FpusSnrkRHyZiVEsXf9X/s/33mA7es4mQYkyUa7dMvu/) **provides information about the current latest version.**
{% endhint %}

## SMTP

Proper SMTP configuration is necessary for receiving email-based reports and alerts. See the [**SMTP Product Guide** ](../system/smtp.md)for instructions.

## Server Certificate

By default, your VergeOS system is installed with a self-signed certificate. For public-facing and production systems it is important to install a trusted, CA-issued certificate to provide security and ensure trust between your system, browsers, and external platforms (for integrations). See [**Server Certificates**](../system/certificates.md) for related instructions.

{% hint style="success" %}
**A CA-issued certificate may be less important for home labs, or other non-critical systems that are used solely within a private infrastructure.**
{% endhint %}

## Alerting and Reporting

Configuring [**Subscriptions**](../system/subscriptions-overview.md) allows you to receive alerts and reports for effective system monitoring. Alerts (on-demand subscriptions) are essential for immediate notification when specific events occur (e.g. high storage usage percentage, drive warnings, system log errors, etc.), allowing for rapid response. Reports (scheduled subscriptions) enable you to receive summarized information on a specified schedule.

## System Snapshot Settings

_Full_ System Snapshots provide a point-in-time backup of your entire system. By default, your VergeOS system is configured to perform regular full system snapshots. You can customize this schedule to align with your organizational needs. See [**System Snapshots**](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/system-snapshots) for instructions on adjusting the default frequency and retention of system snapshots.

{% hint style="success" %}
**After creating tenants, VMs and NAS volumes, you can also create individualized snapshot frequency and retention for these items where needed.**
{% endhint %}

## Authentication/Authorization Settings

1. **Third-party Authorization Sources:** [**Configure an Authorization Source**](../auth/auth-sources-overview.md) for any external identity service (such as Google SSO or Microsoft Entra ID) you wish to utilize for VergeOS logins.
2. **Multifactor Authentication (MFA):** MFA adds a critical security layer to your user accounts, ensuring that even if a password is compromised, unauthorized access is nearly impossible. With cyber threats on the rise, enabling MFA helps protect your systems and data. It is strongly advised that you require multifactor authentication for all user logins. [**Configure Multifactor Authentication for direct VergeOS logins**](../auth/multifactor-auth.md).

{% hint style="info" %}
**When using external authorization sources (Google, Entra, etc.) for VergeOS, multifactor authentication should also be configured within those systems to ensure secure logins; consult the provider's related documentation for instructions.**

. **Password Complexity:** The default password complexity requirement is a minimum length of 8 characters. Additional requirements (e.g.lowercase letters, uppercase letters, numbers, symbols) can also be added in [**Advanced Settings**](../system/advanced-system-settings.md) - _**Password Complexity Requirement**_
{% endhint %}

{% hint style="warning" %}
**User Security**

Strong user security practices are essential for protecting systems and data from unauthorized access and potential breaches. By assigning unique accounts to each user, limiting permissions to only what's necessary, and regularly reviewing audit logs, organizations can reduce risks and ensure accountability across their environments.
{% endhint %}
