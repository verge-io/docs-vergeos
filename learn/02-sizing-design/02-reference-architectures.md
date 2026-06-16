---
description: "Three VergeOS deployment models -- HCI, HCI + Dedicated Compute, and UCI -- with a decision framework, topology diagrams, and guidance for edge and CSP scenarios."
---

# Reference Architectures

VergeOS supports three deployment architectures from the same software installation. Choosing the right one depends on node count, growth pattern, and workload specialization requirements. This page walks through each model, provides a decision framework, and covers two common real-world scenarios: edge deployments and cloud service provider (CSP) multi-tenant environments.

## Architecture Decision Tree

Use the following framework to guide your recommendation. The node-count bands below are course rules-of-thumb (Marvin documents only the general guidance that HCI fits "smaller deployments, 2--12 nodes typically," and that UCI applies when growth diverges or specialized hardware is needed).

```mermaid
flowchart TD
    A["How many nodes will<br/>the deployment have?"] --> B{"2 -- 6 nodes"}
    A --> C{"6 -- 10 nodes"}
    A --> D{"10+ nodes"}

    B --> E{"Will compute and storage<br/>grow proportionally?"}
    E -->|"Yes"| F["HCI"]
    E -->|"No -- compute growing faster"| G["HCI + Dedicated Compute<br/>(Hybrid 2-Cluster UCI)"]
    E -->|"Uncertain"| H{"Specialized hardware<br/>needed? (GPU, high-mem)"}

    C --> H
    D --> I["UCI (Canonical 3-Cluster)"]

    H -->|"Yes"| I
    H -->|"No"| G
    H -->|"Maybe in the future"| G

    style F fill:#e8f5e9,stroke:#2e7d32
    style G fill:#fff3e0,stroke:#e65100
    style I fill:#f0f4ff,stroke:#336
```

**Quick rules of thumb:**

1. **Start with HCI** unless you have a specific reason not to.
2. **Consider HCI + Compute** when compute demand outpaces storage growth (6--10 nodes).
3. **Choose UCI** for 10+ node environments, specialized hardware, or maximum performance isolation.
4. You can **evolve** from HCI to HCI + Compute to UCI as the environment grows -- the same VergeOS installation supports all three.

---

## Model 1: HCI (Hyperconverged Infrastructure)

**Node range:** 2--6 nodes | **Clusters:** 1

In an HCI deployment every node contributes **both** compute and storage. The two controller nodes carry Tier 0 (vSAN metadata) plus Tier 1 (workload) storage and run VMs. Scale-out nodes add Tier 1 storage and compute capacity to the same cluster.

```mermaid
graph TB
    subgraph cluster1["Cluster 1 -- HCI"]
        N1["Node 1 -- Controller<br/>Tier 0 + Tier 1<br/>Storage + Compute"]
        N2["Node 2 -- Controller<br/>Tier 0 + Tier 1<br/>Storage + Compute"]
        S1["Node 3 -- Scale-out<br/>Tier 1<br/>Storage + Compute"]
        S2["Node 4 -- Scale-out<br/>Tier 1<br/>Storage + Compute"]
    end
    subgraph fabric["Core Fabric"]
        CF["Core 1 + Core 2"]
    end
    N1 --- CF
    N2 --- CF
    S1 --- CF
    S2 --- CF

    style cluster1 fill:#e8f5e9,stroke:#2e7d32
    style fabric fill:#f0f4ff,stroke:#336
```

### Advantages

- **Operational simplicity** -- single cluster, single hardware spec, unified management.
- **Predictable scaling** -- every node adds both storage and compute proportionally.
- **Lowest entry point** -- a 2-node cluster is the smallest VergeOS deployment possible.
- **Single hardware specification** simplifies procurement and spare-parts inventory.

### Limitations

- Cannot scale compute independently of storage (or vice versa).
- Limited hardware specialization -- all nodes share the same role.
- Recommended maximum of approximately 6 nodes before considering a second cluster.
- Potential resource contention on controller nodes running both metadata operations and VM workloads.

### Ideal Use Cases

| Scenario                              | Why HCI Works                                     |
| ------------------------------------- | ------------------------------------------------- |
| Small/medium deployments (2--6 nodes) | Minimal complexity, every node pulls double duty  |
| Balanced workloads                    | Storage and compute grow at roughly the same rate |
| Edge / remote sites                   | 2-node clusters with full HA and small footprint  |
| Evaluation and testing                | Fastest path to a working VergeOS system          |

---

## Model 2: HCI + Dedicated Compute (Hybrid 2-Cluster UCI)

**Node range:** 6--10 nodes | **Clusters:** 2

This is the hybrid 2-cluster variant of UCI: controller and storage roles stay collapsed on one HCI cluster, while compute is split out into its own cluster. The HCI cluster (Cluster 1) provides all storage via its controller and optional scale-out nodes. The compute cluster (Cluster 2) runs VM workloads without contributing any disks.

```mermaid
graph TB
    subgraph cluster1["Cluster 1 -- HCI (Storage + Compute)"]
        N1["Node 1 -- Controller<br/>Tier 0 + Tier 1"]
        N2["Node 2 -- Controller<br/>Tier 0 + Tier 1"]
        S1["Node 3 -- HCI<br/>Tier 1 (optional)"]
    end
    subgraph cluster2["Cluster 2 -- Compute Only"]
        C1["Node 4 -- Compute"]
        C2["Node 5 -- Compute"]
        C3["Node 6 -- Compute"]
        C4["Node 7+ -- Scale"]
    end
    subgraph fabric["Core Fabric"]
        CF["Core 1 + Core 2"]
    end
    N1 --- CF
    N2 --- CF
    S1 --- CF
    C1 --- CF
    C2 --- CF
    C3 --- CF
    C4 --- CF

    style cluster1 fill:#fff3e0,stroke:#e65100
    style cluster2 fill:#e3f2fd,stroke:#1565c0
    style fabric fill:#f0f4ff,stroke:#336
```

### Key Design Principles

### Cluster 1 -- HCI (Combined)

- Always includes Nodes 1 & 2 with Tier 0 storage (controllers). - Can
include additional HCI scale-out nodes for more storage and compute. - A
cluster-level toggle controls whether this cluster also runs VM workloads. -
All storage tiers exist in this cluster.
### Cluster 2 -- Compute Only

- Pure compute -- maximum CPU and RAM available for VMs. - Scales
independently based on compute demand. - Supports flexible,
workload-optimized hardware (GPU nodes, high-memory nodes). - Storage I/O
from compute nodes traverses the core fabric to Cluster 1.

### Advantages

- Independent compute scaling without buying unwanted storage.
- Maintains HCI operational simplicity for the storage layer.
- Cost-effective -- scale only the resource tier that is growing.
- Clear growth path to the canonical 3-cluster UCI if needs evolve further.

### Limitations

- Storage I/O from compute nodes crosses the network (adequate core fabric bandwidth is essential).
- More complex than pure HCI (two clusters to manage instead of one).
- Requires a decision on whether the HCI cluster should also run workloads.

### Ideal Use Cases

| Scenario                         | Why HCI + Compute Works                             |
| -------------------------------- | --------------------------------------------------- |
| 6--10 node deployments           | Sweet spot for the two-cluster model                |
| Compute growth outpacing storage | Add CPU/RAM without expanding disks                 |
| GPU or specialized compute       | Dedicated compute cluster with passthrough hardware |
| Cost optimization                | Scale only what you need                            |

---

## Model 3: UCI (Ultra Converged Infrastructure) -- Canonical 3-Cluster

**Node range:** 10+ nodes | **Clusters:** 3+

The canonical 3-cluster UCI completely separates controllers, storage, and compute into dedicated clusters. Each resource tier is independently scalable and uses hardware optimized for its role. (UCI is an umbrella term for any independent-scaling deployment; Model 2 above is its hybrid 2-cluster variant.)

```mermaid
graph TB
    subgraph cluster1["Cluster 1 -- Dedicated Controllers"]
        N1["Node 1 -- Controller<br/>Tier 0 Only | High Memory"]
        N2["Node 2 -- Controller<br/>Tier 0 Only | High Memory"]
    end
    subgraph cluster2["Cluster 2 -- Dedicated Storage"]
        ST1["Node 3 -- Storage<br/>NVMe Dense | Tier 1"]
        ST2["Node 4 -- Storage<br/>NVMe Dense | Tier 1"]
        ST3["Node 5 -- Storage<br/>NVMe Dense | Tier 1"]
    end
    subgraph cluster3["Clusters 3+ -- Specialized Compute"]
        C1["Standard Compute"]
        C2["GPU Compute"]
        C3["High-Memory"]
    end
    subgraph fabric["Core Fabric"]
        CF["Core 1 + Core 2"]
    end
    N1 --- CF
    N2 --- CF
    ST1 --- CF
    ST2 --- CF
    ST3 --- CF
    C1 --- CF
    C2 --- CF
    C3 --- CF

    style cluster1 fill:#f3e5f5,stroke:#6a1b9a
    style cluster2 fill:#e8f5e9,stroke:#2e7d32
    style cluster3 fill:#e3f2fd,stroke:#1565c0
    style fabric fill:#f0f4ff,stroke:#336
```

### Cluster Specialization

| Cluster                      | Role                                | Optimized For                                                                    |
| ---------------------------- | ----------------------------------- | -------------------------------------------------------------------------------- |
| **Cluster 1 -- Controllers** | Tier 0 metadata, cluster management | High memory (e.g. 768 GB in the Data-Science RA), high-endurance NVMe for Tier 0 |
| **Cluster 2 -- Storage**     | All workload storage (Tier 1+)      | Maximum drive density, NVMe or SAS/SATA SSD                                      |
| **Clusters 3+ -- Compute**   | VM workloads, specialized hardware  | Standard, GPU, high-memory, or custom node types                                 |

### Advantages

- **Maximum performance** -- no resource contention between storage and compute.
- **Complete independent scaling** -- add storage without compute (or vice versa).
- **Hardware specialization** -- right-size hardware per role (NVMe-dense for storage, GPU-equipped for compute).
- **Workload isolation** -- different compute clusters for different workload types.
- **Optimal for large-scale and multi-tenant environments.**

### Limitations

- Highest operational complexity of all three architectures.
- Minimum 6 nodes (derived from the 2-node-per-cluster minimum × 3 clusters: 2 controllers + 2 storage + 2 compute).
- More complex capacity planning across three cluster types.
- Higher core fabric bandwidth requirements between clusters.
- Professional services recommended for initial deployment.

### Ideal Use Cases

| Scenario                              | Why UCI Works                                            |
| ------------------------------------- | -------------------------------------------------------- |
| 10+ node enterprise deployments       | Independent scaling avoids over-provisioning             |
| AI / HPC / GPU workloads              | Dedicated GPU compute clusters, separate from storage    |
| Cloud service providers               | Optimize hardware spend per resource tier across tenants |
| Storage-heavy or compute-heavy growth | Scale only what is growing                               |

---

## Architecture Comparison

| Aspect                   | HCI             | HCI + Compute (Hybrid 2-Cluster UCI) | UCI (Canonical 3-Cluster)           |
| ------------------------ | --------------- | ------------------------------------ | ----------------------------------- |
| **Minimum nodes**        | 2               | 4 (2 HCI + 2 compute)                | 6 (2+2+2)                           |
| **Cluster count**        | 1               | 2                                    | 3+                                  |
| **Performance**          | Good            | Better                               | Optimal                             |
| **Hardware flexibility** | Low             | Medium                               | Maximum                             |
| **Independent scaling**  | No              | Partial (compute only)               | Complete                            |
| **Specialization**       | None            | Compute only                         | Full (controller, storage, compute) |
| **Complexity**           | Low             | Medium                               | High                                |
| **Resource efficiency**  | Variable        | Good                                 | Maximum                             |
| **Best fit**             | Small, balanced | Mid-size, compute-heavy              | Large, specialized                  |

---

## Edge Deployment Scenarios

Edge clusters are compact, 2-node VergeOS deployments designed for remote or branch office locations. They use low-power, small form factor hardware and are directly connected (no switches required for the core fabric).

### Typical Edge Configuration

- **2 nodes** directly connected via dual NICs (core fabric).
- Small form factor hardware (Intel NUC, SFF 1L PCs, or similar).
- 2 TB NVMe for workloads + 4 TB SSD for bulk storage per node.
- Full HA and redundancy despite the minimal footprint.

```mermaid
graph LR
    N1["Node 1<br/>Controller + Storage + Compute"] <-->|"Core Fabric<br/>(Direct Connect)"| N2["Node 2<br/>Controller + Storage + Compute"]
    N1 --- EXT["External Network<br/>(Uplink)"]
    N2 --- EXT

    style N1 fill:#e8f5e9,stroke:#2e7d32
    style N2 fill:#e8f5e9,stroke:#2e7d32
```

### Edge Management Models

VergeOS supports three edge management scenarios of increasing sophistication:

1. **Standalone with central management** -- 2-node clusters at each site, managed centrally via the **Sites** dashboard. Catalog Repositories distribute VM recipes from the management cluster to all edge sites.

2. **Centralized backup and DR** -- Same as above, plus a central cluster at the primary data center provides **Site Sync** replication, **ioGuardian** repair servers, and centralized snapshot storage for all branch offices.

3. **Multi-tier with archive** -- Adds a secondary archive cluster at a DR site for long-term retention using high-capacity HDDs, providing a complete 3-2-1 backup strategy.

### When to Recommend Edge

- Space or power constraints at remote sites.
- Applications that store data centrally but need local compute.
- Organizations managing 5--100+ distributed locations.
- Cost-sensitive branch office deployments.

---

## CSP / Multi-Tenant Scenarios

Cloud Service Providers leverage VergeOS multi-tenancy to deliver IaaS from shared infrastructure. Each tenant operates as an isolated Virtual Data Center (VDC) with its own UI, networks, storage, and access controls.

### Typical CSP Configuration

- **6-node HCI clusters** at primary data centers (high-density servers, 768 GB+ RAM per node).
- **Site Sync** between data centers for DR.
- **ioGuardian** repair servers for automatic block retrieval from remote sites.
- **Global inline deduplication** reduces storage consumption across replicated snapshots.
- **Tenant Recipes** automate provisioning of complete customer environments (tenant, networks, firewall rules, VMs, storage).

### CSP Growth Path

| Phase       | Deployment                                                 | Nodes                     |
| ----------- | ---------------------------------------------------------- | ------------------------- |
| **Phase 1** | 2 primary sites with DR via Site Sync                      | 6 per site                |
| **Phase 2** | Add 2-node edge clusters in new regions                    | 2 per region              |
| **Phase 3** | Scale out edge sites by adding clusters (illustrative)     | varies per site           |
| **Phase 4** | Add dedicated storage clusters for S3-compatible offerings | 2+ storage nodes per site |

### Key VergeOS Features for CSPs

- **Multi-tenancy** with complete isolation between customer environments.
- **Self-service management** via web UI and API for tenant administrators.
- **Catalog Repositories** for centralized VM recipe management.
- **OpenID Authentication** integration with existing identity providers.
- **Tenant Recipes** for automated, repeatable customer onboarding.
- **S3-compatible storage** offerings via dedicated storage clusters and tenant recipes.

---

## Network Design Models Overview

The deployment architecture you choose influences your network design. VergeOS supports several network topologies, covered in detail in [Module 4: Networking](../04-networking/README.md). Here is a brief overview to inform your architecture decision:

| Model                           | NICs per Node | Core Fabric            | External Network               | Best For                                   |
| ------------------------------- | ------------- | ---------------------- | ------------------------------ | ------------------------------------------ |
| **L2 Static + Dedicated Core**  | 4             | 2 dedicated L2         | Bonded L2 (LACP)               | Production environments, VMware migrations |
| **L3 Dynamic + Dedicated Core** | 4             | 2 dedicated L2         | BGP / OSPF / EIGRP advertised  | Large-scale, advanced segmentation         |
| **L3 Static + Dedicated Core**  | 4             | 2 dedicated L2         | Bonded L3 (static routes)      | Large-scale, Layer 3 switching             |
| **L2 Static (2 NICs)**          | 2             | 2 shared (VLAN tagged) | Shared with core (VLAN tagged) | Edge, PoC, small deployments               |

**Key requirements across all models:**

- Core fabric networks must be on **dedicated Layer 2 segments** (isolated from each other).
- Jumbo frames (**MTU 9216+**) on all core fabric switch ports.
- **Zero switch hops** between nodes on core fabric -- all nodes must connect to the same switching fabric.
- STP disabled on core fabric ports.

---

{% hint style="info" %}
**VMware Bridge**

Coming from VMware? VergeOS lets you scale storage and compute independently inside one system — compute-only clusters consume the shared vSAN over the core fabric, with no external SAN/NAS and no separate storage product to license.
{% endhint %}

{% hint style="info" %}
**Nutanix Bridge**

Coming from Nutanix? VergeOS builds pure storage clusters and pure compute clusters in one system — storage runs as an integrated OS service, so there is no CVM consuming RAM/CPU on any node type.
{% endhint %}

## Summary

| Concept           | Key Takeaway                                                                           |
| ----------------- | -------------------------------------------------------------------------------------- |
| **HCI**           | Every node does everything. Simple, cost-effective at small scale. Start here.         |
| **HCI + Compute** | Hybrid 2-cluster UCI: collapsed controller+storage, independent compute scaling.       |
| **UCI**           | Canonical 3-cluster: dedicated controller, storage, and compute. Maximum flexibility.  |
| **Edge**          | 2-node direct-connect clusters for remote sites, centrally managed.                    |
| **CSP**           | Multi-tenant HCI deployments with Site Sync DR and tenant recipe automation.           |
| **Evolution**     | Same VergeOS installation supports all three models -- grow from HCI to UCI over time. |

## Next Steps

- **[Customer Scoping](03-customer-scoping.md)** -- Learn the requirements gathering methodology to translate customer needs into a specific architecture recommendation.
- **[Networking](../04-networking/README.md)** -- Deep dive into network design models referenced above.
