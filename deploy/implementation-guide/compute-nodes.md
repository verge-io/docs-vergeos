---
title: "Compute Only Node Installation Guide"
description: "Step-by-step instructions for installing compute-only nodes in VergeOS to expand processing capacity without impacting existing storage infrastructure."
semantic_keywords:
  - "VergeOS compute only node installation"
  - "add compute resources without storage"
  - "compute node USB installer VergeOS"
  - "expand processing power VergeOS cluster"
use_cases:
  - compute_node_installation
  - processing_capacity_expansion
  - compute_cluster_creation
tags:
  - installation
  - compute-node
  - compute-cluster
  - expansion
  - processing
categories:
  - Installation
---

# Compute Only Node Installation Guide

## Introduction

Welcome to the Compute Only Node Installation Guide for VergeOS. This guide provides step-by-step instructions for installing Compute Only nodes using a USB installer. 

By deploying Compute Only nodes, you augment the computational capabilities of your hyper-converged environment without impacting existing storage infrastructures. This type of deployment can optimize operations that require high processing power, such as data analysis, machine learning workloads, or graphics rendering.

This guide will help ensure that your addition of Compute Only nodes is executed smoothly and effectively, maintaining the high standards of efficiency and reliability expected in your VergeOS environment.

---

## Prerequisites

Ensure the following before starting the installation of a Compute Only node:

* A VergeOS cluster is installed and fully operational.
* All network configurations, including VLANs and physical NIC assignments, have been set up according to the main installation guide.

{% hint style="warning" %}
**If this will be the first node in a new compute cluster**

A compute-only node cannot join a cluster that has storage enabled. Before you install the first compute-only node, navigate to **Infrastructure** > **Clusters** in the VergeOS UI and create a new cluster with only **Compute** selected.
{% endhint %}

---

## Installation Steps

1. **Boot from the VergeOS USB Installer:**
   - Insert the VergeOS USB installer into the server designated as the Compute Only node.
   - Reboot the server and select the USB drive as the boot device from the boot menu.

2. **Select Node Type:**
   - When prompted by the installer, select the "Compute Only" option. This indicates that the node is being installed specifically to enhance computational resources without adding storage capacity.

3. **Enter Admin Credentials:**
   - You will be prompted to enter the admin credentials for the VergeOS cluster. These credentials are necessary to authenticate and authorize the addition of the new node to the existing cluster.

4. **Network Configuration:**
   - Allow the installer to auto-detect the network configuration, ensuring that NICs are correctly cabled and match the configuration documented during the initial setup.

5. **Cluster Selection:** (OPTIONAL)
   - If prompted, select the cluster your Compute Only node is joining.
   - Select the node this new node resembles the most.

6. **Complete Installation:**
   - The installer will configure the necessary network settings, install VergeOS, and integrate the node into your cluster without configuring local storage.
   - The node will automatically reboot upon the completion of the installation process.

7. **Verify Installation:**
   - After rebooting, log into the VergeOS web UI using the cluster’s IP address.
   - Check the Nodes page to ensure that the Compute Only node has been successfully added and is operational.

8. **Review the Storage Buffer:**
   - The compute cluster has its own *Storage buffer per node* value, separate from the storage cluster. A cluster added after the first one defaults to 1 GB.
   - Review this value on the compute cluster. See [Cluster Settings](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/system-administration/cluster-settings) for guidance.

---

## Troubleshooting & Support

If issues arise during installation:
- Press `Esc` to cancel and get a command prompt.
- Type `yb-install` to resume or `yb-install --restart` to start over.

### No clusters available to join

If the installer shows this message, the system has no compute-only cluster for the node to join, or the wrong install option was selected at the first menu:

```
There are no clusters in the system that this node is able to join, ensure you selected the correct install option (compute, scale-out, etc) at the first menu. If you believe you selected the correct entry, log into the user interface and verify you have a cluster that matches this config. (Compute: No storage checked, and compute checked. Scale-out: Requires storage checked)
```

1. In the VergeOS UI, navigate to **Infrastructure** > **Clusters** and create a new cluster with only **Compute** selected.
2. On the node, type `yb-install --restart` to start the installation again.
