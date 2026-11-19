---
title: Configuring Microsoft 365 SMTP Relay with an Inbound Connector
slug: smtp-add-ms365-relay-inbound-connector
description: >-
  Relay VergeOS SMTP email through Microsoft 365 using an IP address-based
  inbound connector instead of SMTP AUTH (Basic authentication).
author: VergeOS Documentation Team
date: 2026-11-19T00:00:00.000Z
semantic_keywords:
  - "Microsoft 365 Office 365 SMTP relay inbound connector VergeOS"
  - "SMTP AUTH Basic authentication deprecated smtp.office365.com alternative"
  - "IP address-based connector MX endpoint mail.protection.outlook.com port 25"
  - "SPF record public IP VergeOS alerts email Exchange Online"
use_cases:
  - relay_smtp_through_microsoft_365
  - replace_smtp_auth_with_inbound_connector
  - configure_vergeos_email_for_exchange_online
tags:
  - smtp
  - email
  - relay
  - microsoft 365
  - office 365
  - exchange online
  - inbound connector
  - spf
categories:
  - System Administration
editor: markdown
dateCreated: 2026-11-19T00:00:00.000Z
---

# Configuring Microsoft 365 SMTP Relay with an Inbound Connector

Microsoft 365 is phasing out Basic authentication for SMTP AUTH, which **Use SASL Authorization** relies on with `smtp.office365.com`. To relay through Microsoft 365 without a username and password, use an inbound connector that identifies your VergeOS system by the public IP address its mail comes from.

For general SMTP settings, testing, and troubleshooting, see [SMTP](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/smtp) in the product guide.

## Steps

1. Find the static public IP address that your VergeOS system's outbound mail comes from (after any NAT). This is the address Microsoft 365 sees as the source of the mail. It must be static and not shared with another organization.
2. In the Exchange admin center, create a connector from **Your organization's email server** to **Office 365** that authenticates mail by that IP address. Microsoft's steps are in [Configure an IP address-based connector for SMTP relay](https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365#configure-an-ip-address-based-connector-for-smtp-relay).
3. Add the same IP address to your domain's SPF record so Microsoft 365 doesn't deliver the messages to Junk. See [Set up SPF to identify valid email sources for your Microsoft 365 domain](https://learn.microsoft.com/en-us/defender-office-365/email-authentication-spf-configure).
4. In VergeOS, go to **System > SMTP** and click **Edit Settings**.
5. Set **Relay Host** to your MX endpoint, the host name in your domain's MX record (for example, `yourdomain-com.mail.protection.outlook.com`). This is not `smtp.office365.com`. To look it up, see [Find the MX record for the chosen accepted domain](https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365#appendix-find-the-mx-record-for-the-chosen-accepted-domain-in-microsoft-365-or-office-365).
6. Set **Relay Port** to **25**.
7. Enable **Use TLS** and disable **Use SASL Authorization**.
8. Set **From Address** to an address in one of your Microsoft 365 accepted domains. The address doesn't need a mailbox.
9. Click **Submit**, then [send a test email](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/smtp#test-smtp-configuration).

{% hint style="warning" %}
Enter the public IP address (where the outbound mail comes from) in the connector, not the system's private address. Exchange rejects a private address (for example, 192.168.x.x or 10.x.x.x) as a reserved IP range.
{% endhint %}

{% hint style="info" %}
Outbound port 25 must be open from your VergeOS system to the internet. Microsoft doesn't support this relay from a third-party hosted service, so a VergeOS system at a hosting provider may not be able to use it. In that case, or if you can't use a static public IP, a third-party SMTP relay service that accepts a username and password works with **Use SASL Authorization**.
{% endhint %}
