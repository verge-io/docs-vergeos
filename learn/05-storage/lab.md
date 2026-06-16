---
description: "Configure vSAN storage tiers, provision NAS shares, and validate storage performance and redundancy in VergeOS."
---

# Lab: Storage Configuration

## Objective

Configure a complete storage environment in VergeOS, including vSAN tier setup, NAS share provisioning, and storage health validation.

## Prerequisites

- Completed Module 1: Architecture Fundamentals
- Completed Module 3: Installation
- Completed Module 5 reading (vSAN Architecture, Storage Tiers, NAS Shares, Best Practices)
- A running VergeOS cluster with at least 2 nodes and available physical disks

## Difficulty

**Intermediate** -- Requires understanding of storage concepts (disk tiers, redundancy, file shares)

## Estimated Time

**1.5 hours**

## Steps

### Part 1: vSAN Tier Configuration

Set up storage tiers to organize physical disks by performance characteristics.

1. Navigate to the Storage section in the VergeOS UI
2. Review the physical disks available in your cluster:
   - Identify SSD vs HDD drives
   - Note drive sizes and current assignments
3. Configure storage tiers:
   - Assign NVMe / high-endurance SSDs to Tier 1, SATA/SAS SSDs to Tier 2, standard HDDs to Tier 4, and archive HDDs to Tier 5 — leave any unpopulated tier empty
   - The UI's auto-detected tier is the starting point; override only when needed
4. Verify the vSAN pool shows correct disk assignments and available capacity
5. Review the configured redundancy level on each vSAN tier (Infrastructure > vSAN Tiers > tier dashboard > Status card) and confirm it reports Redundant. Changing redundancy levels on an existing system requires Verge.io Support and is not part of this lab.

### Part 2: NAS Share Provisioning

Create file-level shares for workload access.

1. Create a CIFS/SMB share:
   - Name the share (e.g., "app-data")
   - Configure the storage allocation and tier placement
   - Set permissions for user/group access
2. Create an NFS share:
   - Name the share (e.g., "backup-target")
   - Configure export settings and allowed networks
   - Set appropriate access permissions
3. Verify both shares are accessible from a test VM or client

### Part 3: Storage Monitoring

Validate storage health and performance.

1. Navigate to the Storage dashboard
2. Review key metrics:
   - Capacity utilization per tier
   - IOPS and throughput statistics
   - Deduplication ratios
3. Verify redundancy status shows healthy across all nodes
4. Identify any alerts or warnings in the storage health view

### Part 4: Storage Best Practices Validation

Confirm your configuration follows recommended guidelines.

1. Review tier assignments against workload requirements
2. Confirm each vSAN tier reports Redundant in its Status card
3. Check that the vSAN has at least 30% free capacity (the documented scale-up minimum and a reasonable operational floor); per-tier alerts trigger at 80% utilization, critical at 90%
4. Document your storage configuration for future reference

## Verification

Your storage lab is complete when you can answer **yes** to all of the following:

- [ ] vSAN tiers are configured with appropriate disk assignments
- [ ] At least one CIFS/SMB share is provisioned and accessible
- [ ] At least one NFS share is provisioned and accessible
- [ ] Storage dashboard shows healthy status across all nodes
- [ ] Per-tier deduplication ratio is reported on the storage tier dashboard
- [ ] Redundancy settings are appropriate for the cluster size
