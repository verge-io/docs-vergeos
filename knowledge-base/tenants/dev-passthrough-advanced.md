---
title: Device Passthrough Advanced Configuration
slug: dev-passthrough-advanced
author: VergeOS Documentation Team
date: 2024-11-10T16:53:09.094Z
semantic_keywords:
  - pci device passthrough resource rules
  - sriov sr-iov nvidia vgpu configuration
  - resource group filter device pool
  - usb pci passthrough virtual machine
  - manual resource rule creation editing
use_cases:
  - manually_create_device_passthrough_rules
  - edit_existing_resource_rules
  - configure_sriov_nvidia_vgpu_passthrough
  - filter_pci_usb_devices_for_vms
  - manage_device_resource_groups
categories:
  - System Administration
  - VM
  - Virtual Machines
  - Tenant
editor: markdown
dateCreated: 2024-11-10T16:53:09.094Z
description: >-
  Advanced configuration information for device passthrough including manual
  creation and editing of resource rules for PCI, USB, SR-IOV, and NVIDIA vGPU
  devices.
tags:
  - device passthrough
  - passthrough
  - sriov
  - vgpu
  - nvidia
  - pci
  - resource rules
  - device pool
---

# Device Passthrough Advanced Configuration

Although allowing auto-generation of resource rules (e.g. when you select a device and use the _Make Resource_ menu option) is easiest and usually recommended, there may be situations where it may be useful to manually create a resource rule or to modify an auto-generated resource rule.

{% hint style="danger" %}
**It is important to read and be familiar with** [**PCI Passthrough Risks and Precautions**](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/device-pass-overview#pci-passthrough-risksprecautions) **before making passthrough configurations.**
{% endhint %}

## Manually Create a New Resource Rule

1. Navigate to Infrastructure > Resources.
2. Click **Rules** (ui card or on the left menu).
3. Click **New** on the left menu.
4. Provide a **Name** for the Rule; it is recommended to use a descriptive name can be helpful in future administration.
5. Select the **Resource Group** to which the resource rule will apply.
6. Select a specific **Node** or select _--None--_ to apply the rule to all nodes.
7. Select the **Type** (PCI, USB, SR-IOV, or NVIDIA vGPU).
8. Leave the default value set to **--None--** in the field labeled _Automatically created based on PCI Device._
9. Configure device filters as desired; filter fields will vary depending on the device type selected; see below. (_Advanced Entry_ option also available)

{% hint style="success" %}
**Information on installed PCI devices, for use in filters, you can use the PCI devices listing: navigate to Infrastructure > Resources > PCI Devices. To show additional fields, right-click in the heading section to select from the full list of available columns that can be displayed.**
{% endhint %}

## Edit an Existing Resource Rule

1. Navigate to the Associated **Resource Group dashboard** (Infrastructure > Resources > Groups > double-click the particular group).
2. In the _**Rules**_ section, locate and **click the desired resource rule**.
3. Click **Edit** on the left menu.
4. Node selection and PCI Filters can be modified as needed. (_Advanced Entry_ option also available)

The _Advanced Entry_ section allows you to manually input filter syntax rather than using the filter entry fields. Generally, it is preferable to allow system-generated syntax based on your filter field selections.
