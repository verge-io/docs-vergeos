---
title: "SMTP"
description: "How to configure, test, and troubleshoot SMTP email settings in VergeOS, including relay configuration, TLS, queue management, mail logs, and troubleshooting delivery issues."
semantic_keywords:
  - "VergeOS SMTP email configuration relay"
  - "SMTP troubleshooting delivery failure SPF DMARC"
  - "test SMTP send email queue flush delete"
  - "TLS relay host port SASL authentication"
  - "mail log SMTP reports subscription alerts"
  - "Microsoft 365 Office 365 SMTP relay inbound connector MX record"
use_cases:
  - configure_smtp_email_settings
  - test_smtp_configuration
  - troubleshoot_email_delivery
  - manage_smtp_queue
  - configure_relay_host
  - review_smtp_logs_and_reports
tags:
  - smtp
  - email
  - configuration
  - troubleshooting
  - tls
  - relay
  - notifications
  - subscriptions
  - microsoft 365
  - office 365
categories:
  - System Administration
---

# SMTP

This page provides instructions for configuration and administration of SMTP in a VergeOS system. [Subscriptions](subscriptions-overview.md) (used for system alerts and notifications) rely on effective SMTP configuration. 

{% hint style="info" %}
**Send direct or via an SMTP Relay**

SMTP can be configured to send email directly from the built-in VergeOS mail server -OR- through a relay email server. 
{% endhint %}

{% hint style="success" %}
Because SMTP can involve inherently complex and error-prone configuration (DNS, reverse DNS records, firewall rules, etc.) some customers opt to use a commercial email relay service for ease of use, security, and compliance reasons.  The provider of this service can supply the proper relay settings for your SMTP configuration. 
{% endhint %}

## SMTP Configuration

1. Start at the **SMTP Dashboard (System > SMTP)**.
2. Click **Edit Settings** on the left menu.
3. Configure **settings:**
    * **Use TLS:** enables/disables TLS encryption; must be set to correspond with target system requirements when using an email relay host. When it is supported, always use TLS. 
    * **Hostname:** When using the built-in SMTP server, be sure to use a valid FQDN that clearly identifies its purpose, ensure the hostname resolves to the correct IP using DNS, and verify proper SPF, DMARC, and reverse DNS records are in place for the hostname. Specific hostname may also be important when using a relay, depending on requirements and policies of the relaying server. 
    * **From Name:** the display from name to appear in email messages
    * **From Address:** the source email address to appear in email messages
    * **Relay Host:** address of the email relay server (blank for direct sending)
    * **Relay Port:** TCP port used by relay host, e.g. 25 (unencrypted), 587 (TLS), 465 (SSL/legacy-deprecated); blank for direct sending
    * **Use SASL Authorization:** Typically, valid authentication credentials will be required when using a relay host; enable this option to enter username/password needed to access the relay server.
4. Click **Submit** to save the configuration.

### Relay Through Microsoft 365 (Inbound Connector)

Microsoft 365 is phasing out Basic authentication for SMTP AUTH, which **Use SASL Authorization** relies on with `smtp.office365.com`. To relay through Microsoft 365 without a username and password, use an inbound connector that identifies your VergeOS system by the public IP address its mail comes from.

1. Find the static public IP address that your VergeOS system's outbound mail comes from (after any NAT). This is the address Microsoft 365 sees as the source of the mail. It must be static and not shared with another organization.
2. In the Exchange admin center, create a connector from **Your organization's email server** to **Office 365** that authenticates mail by that IP address. Microsoft's steps are in [Configure an IP address-based connector for SMTP relay](https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365#configure-an-ip-address-based-connector-for-smtp-relay).
3. Add the same IP address to your domain's SPF record so Microsoft 365 doesn't deliver the messages to Junk. See [Set up SPF to identify valid email sources for your Microsoft 365 domain](https://learn.microsoft.com/en-us/defender-office-365/email-authentication-spf-configure).
4. In VergeOS, go to **System > SMTP** and click **Edit Settings**.
5. Set **Relay Host** to your MX endpoint, the host name in your domain's MX record (for example, `yourdomain-com.mail.protection.outlook.com`). This is not `smtp.office365.com`. To look it up, see [Find the MX record for the chosen accepted domain](https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365#appendix-find-the-mx-record-for-the-chosen-accepted-domain-in-microsoft-365-or-office-365).
6. Set **Relay Port** to **25**.
7. Enable **Use TLS** and disable **Use SASL Authorization**.
8. Set **From Address** to an address in one of your Microsoft 365 accepted domains. The address doesn't need a mailbox.
9. Click **Submit**, then [send a test email](#test-smtp-configuration).

{% hint style="warning" %}
Enter the public IP address in the connector, not the system's private address. Exchange rejects a private address (for example, 192.168.x.x or 10.x.x.x) as a reserved IP range.
{% endhint %}

{% hint style="info" %}
Outbound port 25 must be open from your VergeOS system to the internet. Microsoft doesn't support this relay from a third-party hosted service, so a VergeOS system at a hosting provider may not be able to use it. In that case, or if you can't use a static public IP, a third-party SMTP relay service that accepts a username and password works with **Use SASL Authorization**.
{% endhint %}

## Test SMTP Configuration

1. Start at the **SMTP Dashboard (System > SMTP)**.
2. Click **Send Test Email** on the left menu.
3. Enter an **email address** to send to.  
4. Click **Send**.
5. Refer to the [Troubleshooting](#smtp-troubleshooting) section if the test message is not received. 

## SMTP Queue Management

The **Mail Queue** contains email messages waiting to be sent.  

### Delete the SMTP Queue

Deleting the SMTP queue might be necessary in situations related to email delivery, such as a large backlog after a prolonged SMTP outage or when troubleshooting, to start with a clean slate.  The following instructions will wipe out all entries in the email queue and those entries will not be regenerated.

1. Start at the **SMTP Dashboard (System > SMTP)**.
2. **Assess queue entries before deleting:** the most recent entries are displayed in the ***Mail Queue*** section of this page; to view a larger queue, click the **Mail Queue** entry on the left menu. 
3. Click **Delete Queue** on the left menu.

### Flush (Expedite) the SMTP Queue

Flushing the SMTP queue expedites sending messages by forcing the mail server to re-evaluate and attempt sending each entry in the queue.  This is often used when there were numerous messages stuck from a previous issue (misconfiguration, network outage, service delay, etc.) that may now be resolved.  Flushing the queue does not delete messages, but rather, expedites the sending process. 

1. Start at the **SMTP Dashboard (System > SMTP)**.
2. Click **Flush Queue** on the left menu.
3. Click **Yes** to confirm the operation.

## SMTP Logs 

### View a Log of Sent Messages (Mail Log)
1. Start at the **SMTP Dashboard (System > SMTP)**.
2. View the most recent entries in the **Mail Log** section of the dashboard.
3. To view more entries (going farther back), click **Mail Log** on the left menu.  **Next/Prev** buttons at the bottom of the page allow you to scroll through pages of large logs. 

### View SMTP System Events
1. Start at the **SMTP Dashboard (System > SMTP)**.
2. View the most recent entries in the **Logs** section at the bottom of the dashboard.
3. To view more entries (going farther back), click **Logs** on the left menu.  **Next/Prev** buttons at the bottom of the page allow you to scroll through 
pages of large logs. 

## SMTP Reports

SMTP reports provide a **summary of recent SMTP activity**, containing information such as warnings, errors, bytes sent/received, number of messages by recipients and senders, etc. Use the left menu options to run **Today's Report** or **Yesterday's Report**. 

## SMTP Troubleshooting

### Check SPAM folders

Verify messages are not being sent to the recipient's SPAM/Junk folder.   

### Check Logs 

Error messages in the SMTP log can provide information when email messages fail, such as warnings about incorrect SMTP settings or STMP disabled, etc. Check the ***Logs* section at the bottom** of the SMTP page.

### Verify Appropriate Firewall Rules and Network Policies

Outgoing SMTP connections are commonly blocked by default.  Make sure port 25, 587, or 465 (depending on your configuration) are open and allowed; in some cases, this may require contacting your service provider.  

### Using a Relay: 

**Confirm Relay settings**

* Some email servers require explicit relay permissions.  Ensure the email server allows your VergeOS system to relay messages, typically by enabling authentication or whitelisting IP addresses.
  
* You may need to configure the “From Address” field to use the same domain you are sending emails to. Typically, your relay host has the correct SPF/DMARC/reverse DNS records for your domain but is not authorized to send emails from the default system@cloud.verge.io address.

* Confirm the correct server address and port are configured for the relay server. Verify you are using the name/address expected by the relaying mail system.

* Confirm TLS setting conforms to relay server requirements.  Many email servers require a TLS secure connection.
{% hint style="success" %}
**Some email servers will utilize STARTTLS where the connection starts unencrypted on a standard SMTP port (25 or 587) with encryption negotiated after the connection is established.**


{% endhint %}

### Sending Direct:

**Verify SPF/ DMARC/ reverse DNS records**  
If emails are marked as spam or fail to deliver, ensure proper reverse DNS records and that your domain has correct SPF (Sender Policy Framework) and DMARC (Domain-based Message Authentication, Reporting & Conformance) records.  When these records do not correspond correctly to your system, attempted messages can be detected as impersonation, resulting in delivery failures and/or emails flagged as suspicious. Repeated impersonation can get your domain/IP blacklisted which can affect future email deliveries. 
