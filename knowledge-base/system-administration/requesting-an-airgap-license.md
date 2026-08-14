---
title: Requesting an Airgap License
slug: requesting-an-airgap-license
author: VergeOS Documentation Team
date: 2026-08-12T12:00:00.000Z
semantic_keywords:
  - airgap license request air-gapped environment
  - offline licensing no internet access
  - license request file download email
  - VergeOS system licensing activation
  - upload airgap license file apply install
use_cases:
  - request_airgap_license
  - license_air_gapped_system
  - generate_license_request_file
  - offline_system_activation
  - upload_airgap_license
categories:
  - Licensing
  - System Administration
editor: markdown
dateCreated: 2024-08-19T19:08:58.594Z
description: >-
  How to request an airgap license for VergeOS systems with no outbound
  Internet access, and how to upload the license file you receive from Verge.io.
tags:
  - airgap
  - license
  - verge
  - vergeos
  - air-gapped
  - upload
---

# Requesting an Airgap License

{% hint style="warning" %}
**Air-gap licensing is not common and requires justification. Please see** [**Licensing and Software Updates**](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/licensing-and-updates) **for more information.**
{% endhint %}

## Overview

{% hint style="info" %}
**Key Points**

* VergeOS requires a valid license for operation
* Air-gapped environments need a special airgap license
* The process involves generating a license request file and emailing it to Verge.io
* Verge.io returns a license file, which you upload on the **System > Settings** page
{% endhint %}

This guide shows how to request an airgap license for VergeOS systems without outbound Internet access, and how to upload the license file you receive.

## Prerequisites

* Access to the VergeOS Cloud Dashboard
* A working email client on a machine that can send external emails
* Understanding of your system's airgapped status

## Requesting the License
**From the system you intend to license:**
1. Navigate to System Settings
  Select **System** from the top menu and then select **Settings**.
2. Initiate License Request
   * On the left menu, click **Request Offline License**
   * The **Request Generated** dialog opens and shows the name and size of the license request file
3. Download Request File
   * Click the **Download Request File** button
   * Save the license request file to your local machine
4. Prepare Email to Verge.io
   * Click the **license@verge.io** link in the dialog
   * This opens your default email client with a pre-addressed email
5. Send License Request
   * Attach the downloaded license request file to the email
   * Provide additional information in the email body (e.g., company name, purpose of license)
   * Send the email to Verge's licensing team

## What Happens Next

1. Verge.io processes your request and generates an airgap license file
2. You receive a reply email with the airgap license file attached
3. Upload the license file to your VergeOS system (see [Uploading the License](#uploading-the-license))

{% hint style="info" %}
**Processing Time**

If you haven't received a response within 2 business days, please follow up with VergeOS support team.
{% endhint %}

## Uploading the License

When you receive the license file from Verge.io, upload it to the system:

1. Navigate to **System > Settings**.
2. On the left menu, click **Add License**. The **New License** form opens.
   * If the system already has a license, the menu shows **Edit License** instead. Click it to replace the installed key.
3. Below the **License Key** field, click **Choose File** and select the license file you received.
   * The file contents fill the **License Key** field.
   * You can also open the license file in a text editor and paste its contents into the **License Key** field.
4. (Optional) Enter a **Note**, such as the request date or ticket number.
5. Click **Submit**.

The **License** section of the Settings page shows the new license and its validity dates.

## Important Considerations

* Ensure the system requesting the license is the one you intend to license
* Keep the license request file secure
* For multiple systems, repeat this process for each system individually

## Troubleshooting

{% hint style="warning" %}
**Common Issues**

* Problem: Unable to generate license request file
  * Solution: Verify your access permissions in the VergeOS Cloud Dashboard
* Problem: Email client doesn't open automatically
  * Solution: Manually compose an email to license@Verge.io and attach the downloaded request file
* Problem: The license key is rejected when you submit the form
  * Solution: Make sure the **License Key** field contains the complete, unmodified contents of the license file
{% endhint %}

## Additional Resources

* [Updating a VergeOS System with Airgap License](updating-vergeos-system-with-airgap-license.md)
* [Licensing and Software Updates](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/licensing-and-updates)

## Feedback

{% hint style="info" %}
**Need Help?**

If you encounter any issues while requesting an airgap license or have questions about this process, please don't hesitate to contact our support team.
{% endhint %}

***
