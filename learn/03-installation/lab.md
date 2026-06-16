---
description: "Install VergeOS on a 2-node cluster, configure core fabric networking, and verify system health."
---

# Lab: 2-Node VergeOS Installation

## Objective

Perform a complete VergeOS installation on a 2-node cluster, including hardware preparation, Node 1 bootstrap, Node 2 join, and post-installation verification.

## Prerequisites

- Completed Module 1: Architecture Fundamentals
- Completed Module 2: Sizing & Design
- Completed Module 3 reading (Pre-Installation Checklist, Installation Walkthrough, Post-Install Verification)
- Access to either physical hardware or the VergeOS Terraform playground for a virtual deployment

## Difficulty

**Beginner** -- Step-by-step guidance provided

## Estimated Time

**1.5 hours**

## Steps

### Part 1: Pre-Installation Hardware Preparation

Prepare your target hardware (or virtual environment) for installation.

1. Verify BIOS settings:
   - Virtualization extensions enabled (VT-x / AMD-V)
   - Boot mode set to UEFI
   - Disk controller in HBA/passthrough mode (not RAID)
2. Identify network interfaces and their MAC addresses
3. Prepare VergeOS USB boot media
4. Document the planned IP addressing for core fabric and external networks

### Part 2: Node 1 Installation

Install the first controller node, which bootstraps the cluster.

1. Boot Node 1 from USB media
2. Follow the installation prompts:
   - Select boot drive
   - Configure core fabric network interface (name, MTU, core=Yes, VLAN if applicable — no IP address is assigned to core fabric interfaces)
   - Configure external network interface and IP
   - Set admin credentials
3. Wait for installation to complete and the node to reboot
4. Verify Node 1 is accessible via the web UI

### Part 3: Node 2 Installation

Install the second controller node, which joins the existing cluster.

1. Boot Node 2 from USB media
2. Follow the installation prompts:
   - Select **Standard Install**, then choose **Controller** as the node role
   - When asked "is this a new system?" answer **No**. (Answering **Yes** creates a separate cluster instead of joining the existing one — the most common install mistake.)
   - Enter the admin/root password from Node 1 to authenticate the join
   - Confirm the auto-detected core fabric networks (no manual core fabric IP is needed — the installer discovers the existing system by listening on the core fabric)
   - Match the **Encryption** settings from Node 1
   - Select boot/data drives and confirm Drive Tier assignments match Node 1
3. Wait for Node 2 to join the cluster and synchronize
4. Verify Node 2 appears in the cluster dashboard

### Part 4: Post-Installation Verification

Confirm the cluster is healthy and ready for workloads.

1. Log in to the VergeOS web UI
2. Check the dashboard for overall system health
3. Verify both nodes show as online with correct roles
4. Confirm vSAN storage tiers are initialized and healthy
5. Test network connectivity between nodes (core fabric)
6. Verify external network access

## Verification

Your installation is complete when you can answer **yes** to all of the following:

- [ ] Both nodes are online and visible in the cluster dashboard
- [ ] vSAN storage tiers show a healthy status with expected capacity
- [ ] Core fabric network connectivity is established between nodes
- [ ] External network access is functional
- [ ] The web UI is accessible and responsive
- [ ] No critical alerts or errors appear in the system log
