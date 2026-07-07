---
description: >-
  Minimum and recommended hardware specifications for VergeOS controller nodes,
  storage nodes, and compute-only nodes, plus maximum supported limits.
---

# Hardware Requirements

## Overview

Sizing a VergeOS deployment starts with understanding the hardware requirements for each node role. Because VergeOS is a complete infrastructure operating system -- not a collection of separate products -- its base overhead is remarkably low. There is no management appliance VM, no per-node controller VM, and no separate storage software to feed. The specifications below cover what VergeOS itself needs; you will add capacity on top for your workloads.

{% hint style="info" %}
**Coming from VMware or Nutanix?**

VergeOS has no management appliance VM and no per-node storage VM (no CVM), so the 16 GB minimum RAM is the entire management-plane footprint per node. vSAN RAM (1 GB per 1 TB of storage) is additional, sized to the disk capacity each node contributes.
{% endhint %}

## Generic Requirements (All Node Types)

Every node in a VergeOS cluster -- regardless of role -- must meet these baseline requirements:

| Component             | Minimum Specification                                                                                |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| **CPU**               | AMD or Intel x86-64 with hardware virtualization support (VT-x / AMD-V)                              |
| **RAM**               | 16 GB dedicated to VergeOS (additional RAM sized for workloads)                                      |
| **Remote Management** | IPMI, iDRAC, iLO, or equivalent out-of-band management                                               |
| **Disk Controller**   | NVMe direct-attached (preferred), or HBA / RAID controller in JBOD / IT mode -- **no hardware RAID** |
| **External NIC**      | 1 x 1 GbE (Intel, NVIDIA Mellanox, or Broadcom)                                                      |
| **Core Fabric NIC**   | 1 x 10 GbE (Intel, NVIDIA Mellanox, or Broadcom)                                                     |

{% hint style="warning" %}
**No Hardware RAID**

VergeOS manages data redundancy through its built-in vSAN (VergeFS). Hardware RAID controllers must be placed in **JBOD or IT mode** so that VergeOS can see and manage individual disks. Using RAID arrays hides disk health information and prevents VergeOS from performing its own data protection.
{% endhint %}

### BIOS Settings Checklist

Before installation, verify these BIOS settings on every node:

* **Boot mode:** UEFI (required if all drives are NVMe)
* **Hardware-assisted virtualization:** Enabled (VT-x / AMD-V)
* **Hyper-threading / SMT:** Enabled
* **All processor cores:** Enabled
* **System clocks:** Synchronized across all nodes (within seconds)
* **Secure Boot:** Disabled

## Controller Nodes (Node 1 and Node 2)

The first two nodes in any VergeOS system are the **controller nodes**. They host the vSAN metadata (Tier 0), manage cluster orchestration, and serve as the system's management plane. Every VergeOS installation requires at least two controller nodes: two controllers provide N+1 redundancy (the default). Surviving the simultaneous loss of two controllers — N+2 (RF3, three copies of every data block) — requires three controller nodes, and five is recommended for N+2 to provide a witness and avoid split-brain scenarios.

### Minimum Specifications

| Component           | Specification                                  | Notes                                           |
| ------------------- | ---------------------------------------------- | ----------------------------------------------- |
| **CPU**             | 1 x 2.7 GHz+                                   | Higher clock speed benefits metadata operations |
| **RAM**             | 16 GB + 1 GB per 1 TB of storage               | The 1 GB/TB ratio is for vSAN metadata overhead |
| **Tier 0 Storage**  | 1 x Enterprise NVMe SSD (3 DWPD or equivalent) | Stores the vSAN hash map and filesystem index   |
| **Tier 0 Capacity** | 5 GB per 1 TB of usable capacity               | Dedicated metadata storage                      |

### Recommended Specifications

| Component           | Specification                                  | Notes                                           |
| ------------------- | ---------------------------------------------- | ----------------------------------------------- |
| **CPU**             | 1 x 3.0 GHz+                                   | Improves metadata and orchestration performance |
| **Tier 0 Storage**  | 2 x Enterprise NVMe SSD (3 DWPD or equivalent) | Redundant metadata configuration                |
| **Tier 0 Capacity** | 10 GB per 1 TB of usable capacity              | Additional headroom for metadata growth         |

{% hint style="success" %}
**Tier 0 Is Metadata Only**

Tier 0 stores the vSAN hash map and filesystem index -- it is **not** a workload data tier. It lives on fast NVMe specifically for performance: keeping the dedup hash map and filesystem index on low-latency media is what ensures fast lookups across the entire storage pool. Tier 0 is write-intensive, so the drives need high endurance — **3 DWPD or equivalent**. Endurance scales with capacity (DWPD × capacity = writes/day), so a larger drive at a lower DWPD is equivalent: a 1 TB drive at 3 DWPD and a 3 TB drive at 1 DWPD both absorb 3 TB of writes/day. The larger, lower-DWPD drive is often the better choice — typically cheaper and more available, with capacity headroom as a bonus.
{% endhint %}

## Storage Nodes

Storage nodes participate in the vSAN and contribute disk capacity to the shared storage pool. In an HCI deployment, storage nodes also run workloads. In a UCI deployment, they may be dedicated exclusively to storage.

### Minimum Specifications

| Component                           | Specification                                     | Notes                                                                                                                                                                                                                               |
| ----------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CPU**                             | 2.7 GHz+                                          | Handles vSAN I/O processing                                                                                                                                                                                                         |
| **RAM**                             | 16 GB + 1 GB per 1 TB of raw storage              | Per-node; scales with disk capacity                                                                                                                                                                                                 |
| **Primary Storage**                 | 1 x Enterprise NVMe or SAS/SATA SSD per node      | For workload I/O (primary storage tier)                                                                                                                                                                                             |
| **Capacity/Archive Tier (Tier 4+)** | Enterprise HDDs (optional)                        | For snapshots, archives, or file-based services. VergeOS does not auto-tier (no automatic data movement), but an administrator can change a volume's or file's preferred tier, which triggers a non-disruptive background migration |
| **Redundancy**                      | At least 2 nodes with matching disk configuration | Required for vSAN data redundancy                                                                                                                                                                                                   |

### Recommended Specifications

| Component           | Specification                                     | Notes                                           |
| ------------------- | ------------------------------------------------- | ----------------------------------------------- |
| **CPU**             | 3.0 GHz+, 1 core per disk                         | Dedicated core per disk improves I/O throughput |
| **RAM**             | 1.5 GB per 1 TB of storage per node               | Better performance under heavy workloads        |
| **Primary Storage** | 2+ NVMe or SAS/SATA SSDs per node                 | More spindles = more IOPS                       |
| **Redundancy**      | At least 2 nodes with matching disk configuration | Required for vSAN data redundancy               |

### RAM Sizing Example

To illustrate the RAM calculation for a storage node:

```
Base VergeOS requirement:          16 GB
Storage overhead (8 TB raw x 1 GB): 8 GB
Workload VMs (example):           96 GB
─────────────────────────────────────────
Total RAM per node:              120 GB
```

At the recommended 1.5 GB/TB ratio, the storage overhead would be 12 GB instead of 8 GB, bringing the total to 124 GB.

{% hint style="info" %}
**Account for the Target Max RAM % (default 80%)**

VergeOS targets no more than **80% of physical RAM** in use per node under normal conditions (the `Target Max RAM %` cluster setting), leaving headroom that failover and live migration can draw on. Size physical RAM so that overhead **plus** workloads fit within that 80%. In the example above, \~120 GB of normal usage should land on a node with at least \~150 GB of physical RAM (120 ÷ 0.80) to stay within the target.
{% endhint %}

## Compute-Only Nodes

Compute-only nodes run workloads but do **not** participate in the vSAN. They have no local storage requirements beyond a boot device (or can PXE boot). This makes them ideal for scaling CPU and RAM independently from storage in UCI and HCI+Compute architectures.

| Component      | Specification                                               |
| -------------- | ----------------------------------------------------------- |
| **CPU**        | Sized for workload requirements                             |
| **RAM**        | Sized for workload requirements (16 GB minimum for VergeOS) |
| **Storage**    | Boot device only (or PXE boot) -- no vSAN disks             |
| **Networking** | Same generic NIC requirements as all nodes                  |

Compute-only nodes are the simplest to size: determine the aggregate CPU and RAM your workloads need, divide by the per-node capacity, and round up to maintain N+1 availability.

## Networking Recommendations

The minimum networking configuration (1 GbE external + 1 x 10 GbE core) is suitable for small or proof-of-concept deployments. For production environments, follow these recommendations:

### Core Fabric NICs

**2 x 25/40/100 GbE** (Intel, NVIDIA Mellanox, or Broadcom). Dual NICs provide redundancy for the core fabric -- the high-speed mesh that carries vSAN replication, VM migration, and inter-node traffic. Jumbo frames are required on the core fabric: VergeOS sets node NICs to \~9192, and the switch ports they connect to must be configured for ≥9216 so those frames pass without fragmentation.

### External NICs

**2 x 10/25/40/100 GbE** (Intel, NVIDIA Mellanox, or Broadcom). Dual external NICs support bonding for redundancy and bandwidth to the upstream network. These carry management UI access and tenant external traffic.

### Supported NIC Vendors

VergeOS supports network adapters from three vendors:

* **Intel** -- Broad compatibility across different series
* **NVIDIA Mellanox** -- High-performance ConnectX series
* **Broadcom** -- Enterprise-grade NICs

{% hint style="warning" %}
Consumer-grade or off-brand NICs are not supported. Using unsupported NICs may result in driver compatibility issues, poor performance, or system instability.
{% endhint %}

## Maximum Supported Specifications

The following table outlines the maximum supported hardware specifications as of VergeOS version 4.12:

| Resource                          | Maximum | Notes                                                                                                          |
| --------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------- |
| **Nodes per system**              | 200     | Across all clusters                                                                                            |
| **Individual physical disk size** | 64 TB   | Per physical drive                                                                                             |
| **RAM per host**                  | 5 TB    | vSAN nodes require 1 GB RAM per 1 TB storage                                                                   |
| **vDisk size**                    | 256 TB  | Per virtual disk                                                                                               |
| **Disks per VM**                  | 2,000   | Requires Virtio-SCSI interface                                                                                 |
| **Clusters per system**           | 100     | Mix of compute, storage, and HCI clusters                                                                      |
| **Storage tiers per system**      | 5       | 5 workload tiers (Tier 1 high-performance through Tier 5 archive); Tier 0 metadata is separate and system-only |
| **vSAN fault domains per system** | 2       | Provides data redundancy                                                                                       |

These limits accommodate extremely large-scale deployments. Most production environments operate well within these boundaries.

## Storage Warnings and Considerations

### Consumer-Grade Disks

{% hint style="danger" %}
**Consumer-Grade Disks Not Supported**

VergeOS does **not** officially support consumer-grade disks. Only enterprise-grade storage devices should be used in production environments and backups of production data. Consumer-grade disks may be acceptable for test, development, or proof-of-concept environments where data loss is tolerable. Some consumer-grade devices may not function properly due to firmware limitations, non-standard command implementations, or compatibility issues with VergeOS.
{% endhint %}

### Large HDD Considerations

HDDs larger than **8 TB** are not recommended outside of archive-specific environments. The concern is **rebuild time**. vSAN does not rebuild automatically when a drive fails — an operator kicks off a repair that rebuilds the lost data onto a hot spare or replacement drive. With an 8 TB+ drive, that rebuild can take many hours — often days — during which:

* **System performance is degraded** as rebuild I/O competes with production workloads
* **Availability risk increases** because a second drive failure during rebuild could cause data loss
* **The rebuild window grows** proportionally with drive size

For primary workload tiers, prefer smaller, faster SSDs. Reserve large HDDs for snapshot retention, archival storage, or file-based service tiers where rebuild time is an acceptable trade-off.

### Fibre Channel LUNs as Storage

VergeOS vSAN can also consume **Fibre Channel (FC) LUNs** as storage devices within its tiers, which is useful for integrating existing SAN investments. VergeOS treats each FC LUN like a local physical disk, so native redundancy and deduplication still apply. Key requirements:

* Present **unique LUNs per node** — never share the same LUN across multiple nodes
* FC HBAs in at least two nodes; a redundant FC fabric is recommended
* **Disable RAID and auto-tiering on the SAN** — VergeOS handles redundancy natively
* Keep **Tier 0 metadata on direct-attached NVMe** — external storage is not recommended for Tier 0

Verge.io still recommends direct-attached disks for best performance and simplicity; use FC LUNs primarily when you have existing SAN infrastructure or specific compliance requirements. See [Using Fibre Channel Storage with vSAN](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/fibre-channel) for setup details.

## Dedicated vs. Shared Controller Nodes

For production environments, VergeOS recommends **dedicated controller nodes** -- nodes that handle only the vSAN metadata (Tier 0) and system management, without running guest workloads or contributing to workload storage tiers.

```mermaid
graph LR
    subgraph shared["Shared Controllers (Small / PoC)"]
        N1S["Node 1<br/>Controller + Storage + Compute"]
        N2S["Node 2<br/>Controller + Storage + Compute"]
    end

    subgraph dedicated["Dedicated Controllers (Production)"]
        N1D["Node 1<br/>Controller Only<br/>(Tier 0 metadata)"]
        N2D["Node 2<br/>Controller Only<br/>(Tier 0 metadata)"]
        N3["Node 3+<br/>Storage + Compute"]
        N4["Node 4+<br/>Storage + Compute"]
    end

    style shared fill:#fef3c7,stroke:#d97706
    style dedicated fill:#d1fae5,stroke:#059669
```

| Approach                  | When to Use                    | Trade-off                                                         |
| ------------------------- | ------------------------------ | ----------------------------------------------------------------- |
| **Shared controllers**    | 2-node clusters, PoC, dev/test | Fewer nodes, but metadata I/O competes with workloads             |
| **Dedicated controllers** | Production, 4+ nodes           | Extra nodes, but metadata operations are isolated and predictable |

## Sizing Quick Reference

Use this quick-reference card when scoping a new deployment:

| Question                         | Guidance                                                                  |
| -------------------------------- | ------------------------------------------------------------------------- |
| How much RAM per storage node?   | 16 GB base + 1 GB per 1 TB raw (minimum) or 1.5 GB per 1 TB (recommended) |
| How many Tier 0 drives?          | 1 per controller (minimum), 2 per controller (recommended)                |
| How large should Tier 0 be?      | 5 GB per 1 TB usable (minimum), 10 GB per 1 TB usable (recommended)       |
| What DWPD for Tier 0?            | 3 DWPD or equivalent (enterprise NVMe)                                    |
| How many cores per storage disk? | 1 core per disk (recommended)                                             |
| Minimum nodes for vSAN?          | 2 nodes with matching disk configuration                                  |
| Maximum nodes per system?        | 200                                                                       |
| Core fabric NIC speed?           | 10 GbE minimum; 25/100 GbE recommended                                    |

## Next Steps

Now that you understand the hardware requirements for each node role, continue to:

* [**Reference Architectures**](02-reference-architectures.md) -- See how these requirements map to real-world deployment topologies (HCI, HCI+Compute, UCI)
* [**Customer Scoping**](03-customer-scoping.md) -- Learn the methodology for translating customer workloads into hardware specifications
