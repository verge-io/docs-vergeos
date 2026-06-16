---
description: "Real-time system visibility from the VergeOS UI -- node dashboards, hardware resources, fabric status, event logs, and cluster-level monitoring."
---

# Dashboard & System Health

## Monitoring Philosophy

VergeOS takes a **single-pane-of-glass** approach to infrastructure monitoring. Every component -- compute, storage, networking, and hardware health -- is visible from the built-in UI without any external monitoring tools. The system provides real-time metrics, historical trends, and event logs at every level: individual nodes, clusters, vSAN tiers, networks, VMs, and tenants.

This page covers the primary monitoring surfaces you will use daily to assess system health and troubleshoot issues.

```mermaid
graph TB
    subgraph ui["VergeOS UI — Monitoring Hierarchy"]
        direction TB
        MAIN["Main Dashboard<br/>System-wide overview"]
        CLUSTER["Cluster Views<br/>Aggregate resource pools"]
        NODE["Node Dashboards<br/>Per-node hardware & metrics"]
        VSAN["vSAN Status<br/>Tier health & capacity"]
        NET["Network Status<br/>Connectivity & traffic"]
        VM["VM / Tenant Dashboards<br/>Per-workload metrics"]

        MAIN --> CLUSTER
        MAIN --> VSAN
        MAIN --> NET
        CLUSTER --> NODE
        NODE --> VM
    end

    style ui fill:#f0f4ff,stroke:#336
```

## Node Dashboard

The **Nodes dashboard** is your primary interface for monitoring individual physical (or virtual) servers in the environment. Navigate to it via **Infrastructure → Nodes**, then select a specific node.

### Node Status Information

At the top of the node dashboard, you will find key status fields:

| Field                    | Description                                                                                                                                   |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**               | Current operational state -- Running or Offline; during maintenance workflows it may show Migrating, Maintenance Mode, or Leaving Maintenance |
| **Maintenance Mode**     | Whether the node is in maintenance state (workloads migrated away)                                                                            |
| **Last Powered On**      | Timestamp of the most recent boot                                                                                                             |
| **IPMI Status**          | Status of the Intelligent Platform Management Interface                                                                                       |
| **IPMI Network Address** | BMC/iDRAC/iLO management IP for remote access                                                                                                 |
| **System Version**       | VergeOS version breakdown -- OS, vSAN, Appserver, and Kernel versions                                                                         |

### Hardware Configuration

The dashboard also displays the physical hardware profile:

- **CPU** -- Processor model and generation
- **CPU Cores** -- Number of physical cores
- **RAM** -- Total physical memory capacity
- **Failover RAM** -- Memory reserved for failover scenarios
- **Overcommit RAM** -- Memory available for oversubscription
- **Cluster** -- Which cluster this node belongs to
- **Model / Asset Tag** -- Hardware platform and inventory asset tag

### CPU Usage Graph

The CPU usage graph is one of the most frequently consulted metrics. It provides real-time and historical trend visualization with multiple breakdown categories:

| Metric        | What It Shows                                                                 |
| ------------- | ----------------------------------------------------------------------------- |
| **Total CPU** | Aggregate CPU utilization across all cores                                    |
| **Core Peak** | The single highest-utilized core (helps identify single-threaded bottlenecks) |
| **User**      | Time spent in user-space processes                                            |
| **System**    | Time spent in kernel-space operations                                         |
| **IO Wait**   | Time the CPU is idle waiting for I/O operations to complete                   |
| **VM Usage**  | CPU consumed by virtual machines running on this node                         |
| **IRQ**       | Time spent handling hardware and software interrupts                          |

### Node Statistics Cards

Below the CPU graph, the dashboard presents quick-reference metric cards:

- **Physical RAM** -- Current memory utilization percentage and total capacity
- **Virtual RAM** -- Allocated virtual memory (typically 0% when not overcommitted)
- **Temperature** -- Current node temperature with a color-coded indicator (green / yellow / red based on thresholds)
- **Running Machines** -- Count of active VMs, vNet containers, and system services on this node
- **Cores Usage** -- Percentage of CPU cores currently in use
- **RAM Usage** -- Memory consumption across all running machines

## Hardware Resources Panel

The lower section of the node dashboard provides detailed views of every physical hardware component.

### Drives

All physical drives attached to the node are listed with full health data:

| Column                | Purpose                                            |
| --------------------- | -------------------------------------------------- |
| **Status**            | Online / Offline indicator                         |
| **Name**              | Device identifier (e.g., `nvme0n1`, `sda`)         |
| **Model**             | Manufacturer and model number                      |
| **Tier**              | vSAN storage tier assignment (set at install time) |
| **vSAN Drive ID**     | Unique identifier within the vSAN                  |
| **Firmware**          | Current drive firmware version                     |
| **Bus**               | Hardware bus connection type (NVMe, SATA, SAS)     |
| **Usage**             | Capacity utilization with visual progress bar      |
| **Repairing**         | Whether the drive is currently being rebuilt       |
| **Read/Write Errors** | Error counters for proactive health monitoring     |

You can click any drive to access its **S.M.A.R.T.** diagnostics -- reallocated sectors, temperature, power-on hours, wear leveling, and other predictive failure indicators.

### Network Interface Cards (NICs)

Every NIC in the node is displayed with operational and fabric status:

- **Status** -- Up or Down
- **Fabric Status** -- Core fabric connectivity. **Confirmed** indicates the NIC is properly integrated; **No Path** and **Degraded** are the problem statuses to watch for; **None** appears for NICs that are not part of the core fabric. A globe icon indicates NICs connected to the core fabric
- **Port** -- Physical port identifier on the NIC
- **Name** -- Interface identifier (e.g., `enp2s0f0`)
- **Model / Vendor / Driver** -- Hardware and software details
- **Speed** -- Negotiated link speed (e.g., 10000 Mb/s, 25000 Mb/s)
- **MAC** -- Hardware MAC address
- **Network** -- Associated VergeOS network
- **RX / TX** -- Total data received and transmitted
- **RX / TX Rate** -- Current transfer rates

### Additional Hardware Sections

| Section                 | What It Shows                                                                           |
| ----------------------- | --------------------------------------------------------------------------------------- |
| **Memory Modules**      | Installed RAM -- module count, capacity, type, and specifications                       |
| **LLDP Neighbors**      | Link Layer Discovery Protocol data -- connected switch, port mappings, network topology |
| **PCI Devices**         | All PCI/PCIe devices with bus assignments and passthrough availability                  |
| **SR-IOV NIC Devices**  | Virtual function count and assignment status for SR-IOV capable NICs                    |
| **NVIDIA vGPU Devices** | GPU model, vGPU profiles available, and allocation status                               |
| **USB Devices**         | Connected USB devices with passthrough capability                                       |

## Fabric Status Monitoring

The **core fabric** is the backbone network connecting all VergeOS nodes. Monitoring fabric health is critical because fabric degradation impacts vSAN replication, VM live migration, and inter-node communication.

On each node's NIC table, look for the **Fabric Status** column:

- **Confirmed** -- The NIC is properly integrated into the core fabric and communicating with peer nodes
- **No Path** or **Degraded** -- Problem statuses indicating the NIC is not successfully participating in the fabric. May indicate a cable issue, switch misconfiguration, or NIC failure
- **None** -- Displayed for NICs that are not part of the core fabric (e.g., external-network NICs)

{% hint style="success" %}
**Quick Fabric Health Check**

From the main dashboard, navigate to **Infrastructure → Nodes** and scan the NIC fabric status across all nodes. Every core fabric NIC should show **Confirmed**. Any **No Path** or **Degraded** status warrants immediate investigation -- check physical cabling, switch port configuration, and NIC driver status.
{% endhint %}

## Event Logs

Every node dashboard includes an **Event Logs** section that displays system events scoped to that node. Events are classified by severity level:

| Level        | Description                                              | Examples                                                         |
| ------------ | -------------------------------------------------------- | ---------------------------------------------------------------- |
| **Critical** | System-threatening conditions requiring immediate action | Node offline, vSAN degraded                                      |
| **Error**    | Failures that impact functionality                       | Drive failure, failed operations                                 |
| **Warning**  | Conditions that may escalate if unaddressed              | Temperature threshold exceeded, drive errors increasing          |
| **Message**  | Normal operational events                                | Power state changes, maintenance mode transitions, VM migrations |

### Common Log Entries

- **Temperature warnings** -- `"Core has reached warning temperature '96 / 95'"` indicates a CPU core exceeded the configured threshold. The two numbers are the current reading and the computed warning threshold for that CPU. By default (`max_core_temp = 0` in Cluster Settings → Node Temperature), VergeOS queries each CPU's hardware-rated maximum and fires the warning at `max_core_temp_warn_perc` (default **10%**) below that maximum
- **Drive status events** -- Notifications when drives go offline, begin repairing, or report new read/write errors
- **Power state changes** -- Records of node reboots, shutdowns, and power-on events
- **Maintenance mode transitions** -- Logs when a node enters or exits maintenance mode

Each log entry includes the **timestamp**, **source** (e.g., `node1`), and a **detailed message**. Click **View More** to access the full log history.

## Node Management Actions

The left-side menu on the node dashboard provides essential management operations:

### Power Control

- **Power On / Off** -- Standard power operations via IPMI
- **Reboot** -- Graceful restart of the node
- **Kill Power** -- Force shutdown (use only when graceful methods fail)

### Maintenance Mode

**Always enable maintenance mode before performing hardware changes or system updates.** When you place a node in maintenance mode, VergeOS live-migrates eligible running workloads to other nodes in the cluster. VMs with GPU passthrough or a host-passthrough CPU type (also USB passthrough or SR-IOV NICs) are not migratable and must be powered off -- manually, or automatically if the VM's Migration Method is set to Automatic.

### Remote Console

Provides direct console access to the node via IPMI/iDRAC/iLO. Use this for troubleshooting scenarios where the VergeOS UI is unreachable or you need BIOS-level access.

### Additional Actions

- **Edit** -- Modify node settings (failover RAM, overcommit, tags)
- **Scale Up** -- Add resources to the cluster from this node
- **Diagnostics** -- Access node-level diagnostic tools (ARP scan, ethtool, IPMI sensors, S.M.A.R.T. tests, and more)
- **Refresh** -- Force an update of all dashboard data

## Cluster-Level Views

While node dashboards show individual server health, **cluster views** provide aggregate resource utilization across all nodes in a cluster.

Navigate to **System → Clusters** to see:

- **Total CPU** -- Combined processing capacity and utilization across all nodes
- **Total RAM** -- Aggregate memory with utilization breakdown
- **Node Count** -- Number of active vs. total nodes in the cluster
- **Workload Distribution** -- How VMs and services are spread across nodes

Cluster views are essential for capacity planning -- they help you identify when a cluster is approaching resource limits and when it is time to scale out with additional nodes.

## vSAN Status Overview

The vSAN status is accessible from the main dashboard by clicking the **vSAN Tiers** count box, or via **Infrastructure → vSAN Tiers**.

Key indicators include:

- **Tier Health** -- Per-tier status shown via the `status` field (`online`, `noredundant`, `repairing`, `outofspace`, `offline`, ...) and the `redundant` boolean. The `working` flag indicates whether a Journal Walk is currently in progress, not overall tier health (a healthy idle tier shows `working=false`)
- **Capacity per Tier** -- Total, used, and available storage for each tier
- **Redundancy Status** -- Whether data redundancy requirements are met (critical after a drive or node failure)
- **Repair Status** -- Active repair operations and progress (should be all zeros during normal operation)
- **Device Count** -- Number of drives participating in each tier

{% hint style="warning" %}
**Storage Throttling Thresholds**

VergeOS applies automatic I/O throttling as storage fills up:

- **Below 91%** -- Normal operation, no throttling
- **91–95%** -- Low space throttling begins (10ms latency added)
- **96%+** -- Critical throttling (50ms latency added) with severe performance degradation

Monitor tier capacity proactively and configure alerts before reaching these thresholds.
{% endhint %}

## Network Status

Network health is monitored from **Networks** in the main navigation. For each network (external, internal, DMZ, tenant networks), you can view:

- **Connectivity status** -- Whether the network is running and reachable
- **Traffic statistics** -- RX/TX volume and rates per network
- **Connected machines** -- Which VMs and services are attached
- **Firewall rule hit counts** -- Activity on configured firewall rules
- **Network-specific logs** -- Events scoped to that particular network

## Running Machines View

Each node dashboard includes a **Running Machines** section showing all active workloads:

| Column           | Description                                        |
| ---------------- | -------------------------------------------------- |
| **Status**       | Running state indicator                            |
| **Type**         | Virtual Machine, vNet Container, or system service |
| **Name**         | Machine identifier                                 |
| **CPU Cores**    | Number of assigned cores                           |
| **CPU Usage**    | Current processor utilization percentage           |
| **RAM**          | Allocated memory with utilization percentage       |
| **Last Started** | Timestamp of when the workload was started         |

Common machine types include VMs, vNet containers (network services), and system services (NAS, DMZ, External network, etc.).

{% hint style="info" %}
**Coming from VMware or Nutanix?**

In VergeOS, node hardware, cluster resources, storage health, network status, and workload metrics all live in the same built-in UI -- no separate management server, monitoring suite, or CLI to install for day-to-day visibility.
{% endhint %}

## Best Practices

### Daily Health Checks

Review node temperatures, drive error counters, and fabric status across all
nodes. Address any fabric NICs showing **No Path** or **Degraded**, or
increasing drive errors, immediately.
### Use Maintenance Mode

Always enable maintenance mode before hardware changes, firmware updates, or
system updates. Eligible workloads are live-migrated away before you touch
the node; VMs that cannot live-migrate (GPU passthrough, host-passthrough
CPU type, USB passthrough, SR-IOV) must be powered off.
### Monitor vSAN Capacity

Keep tier utilization below 85% to maintain performance headroom. Configure
subscription alerts (covered in the next section) to notify you before
reaching throttling thresholds.
### Review Logs Regularly

Periodically check event logs for temperature warnings, drive errors, and
unexpected state changes. Catching issues early prevents cascading failures.
