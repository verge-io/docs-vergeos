---
description: "Declarative infrastructure-as-code for VergeOS using the Terraform provider, OpenTofu, and the Packer plugin for automated golden image creation."
---

# Terraform & Packer

Infrastructure-as-Code (IaC) brings the same version control, peer review, and repeatability that software teams rely on to infrastructure provisioning. The **VergeOS Terraform provider** lets you declare VMs, networks, and users in HCL configuration files, while the **Packer plugin** automates golden image creation. Together, they form a declarative pipeline: Packer builds the images, Terraform deploys the infrastructure.

## Terraform Provider

The VergeOS Terraform provider is published on the Terraform Registry and is fully compatible with **OpenTofu** (the open-source Terraform fork). It enables you to manage VergeOS resources through standard `terraform plan` / `terraform apply` workflows.

### Provider Configuration

```hcl
terraform {
  required_providers {
    vergeio = {
      source  = "verge-io/vergeio"
      version = "~> 0.1.0"
    }
  }
}

provider "vergeio" {
  host     = "https://vergeos.example.com"
  username = "admin"
  password = var.vergeos_password
  insecure = true  # Set to true for self-signed SSL certificates
}
```

| Parameter    | Required | Description                                           |
| ------------ | -------- | ----------------------------------------------------- |
| **host**     | Yes      | URL or IP address of the VergeOS system or tenant     |
| **username** | Yes      | VergeOS username with appropriate permissions         |
| **password** | Yes      | Password for the specified user (mark as `sensitive`) |
| **insecure** | No       | Set `true` to accept self-signed SSL certificates     |

{% hint style="success" %}
**OpenTofu Compatible**

The provider configuration is identical for OpenTofu. Simply replace `terraform` commands with `tofu` — no code changes required.
{% endhint %}

### Resources

The provider currently supports four managed resource types for creating and updating VergeOS objects:

| Resource              | Purpose                            | Key Attributes                                                                                                                                                                                  |
| --------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`vergeio_vm`**      | Create and manage virtual machines | `cpu_cores`, `ram`, `os_family`, `machine_type`, `ha_group`, `cluster`, `guest_agent`, `uefi`, `secure_boot`, `snapshot_profile`, `powerstate`, inline `vergeio_drive` and `vergeio_nic` blocks |
| **`vergeio_network`** | Configure virtual networks         | `network_address` (CIDR), `dhcp_enabled`, `dhcp_start`, `dhcp_end`, `dns_server_list`, `gateway`, `powerstate`                                                                                  |
| **`vergeio_user`**    | Provision users                    | User account management within VergeOS                                                                                                                                                          |
| **`vergeio_member`**  | Manage group membership            | Associate users with groups for RBAC                                                                                                                                                            |

### Data Sources

Eight read-only data sources let you query existing VergeOS objects for use in your configurations:

| Data Source                  | Returns                                                |
| ---------------------------- | ------------------------------------------------------ |
| **`vergeio_version`**        | Current VergeOS version information                    |
| **`vergeio_clusters`**       | Available compute/storage clusters                     |
| **`vergeio_nodes`**          | Nodes in the environment                               |
| **`vergeio_networks`**       | Existing virtual networks                              |
| **`vergeio_vms`**            | Virtual machines (filterable by name, snapshot status) |
| **`vergeio_groups`**         | User groups for RBAC                                   |
| **`vergeio_mediasources`**   | Uploaded ISOs and media files                          |
| **`vergeio_cloudinitfiles`** | Available cloud-init configuration files               |

### HCL Examples

#### VM with Drive and NIC

This example creates a Linux web server with a 10 GB virtio-scsi drive and a NIC attached to an internal network:

```hcl
resource "vergeio_vm" "web_server" {
  name                 = "my-web-server"
  description          = "Web Server"
  enabled              = true
  os_family            = "linux"
  cpu_cores            = 2
  machine_type         = "q35"
  ram                  = 2048
  powerstate           = false
  guest_agent          = true
  cloudinit_datasource = "nocloud"
  ha_group             = "web"

  # Storage
  vergeio_drive {
    name           = "Web Server OS Disk"
    description    = "Operating System Disk"
    disksize       = 10
    interface      = "virtio-scsi"
    preferred_tier = 3
    orderid        = 0
  }

  # Networking
  vergeio_nic {
    name        = "Web Server Network"
    description = "NIC for Web Server"
    interface   = "virtio"
    enabled     = true
    vnet        = vergeio_network.web_network.id
  }
}
```

#### Internal Network with DHCP

```hcl
resource "vergeio_network" "web_network" {
  name            = "web-internal-network"
  network_address = "192.168.10.0/24"
  dns_server_list = ["8.8.8.8", "8.8.4.4"]
  dhcp_enabled    = true
  dhcp_start      = "192.168.10.100"
  dhcp_end        = "192.168.10.200"
}
```

#### Querying Existing VMs

Use data sources to reference existing infrastructure without managing it:

```hcl
data "vergeio_vms" "production" {
  filter_name = "prod-db"
  is_snapshot  = false
}

output "production_vms" {
  value = data.vergeio_vms.production.vms
}
```

#### Cloud-Init Integration

The `vergeio_vm` resource supports cloud-init for first-boot automation. The provider schema exposes a `cloudinit_datasource` attribute on the VM and a `vergeio_cloudinitfiles` data source for referencing cloud-init files that already exist in VergeOS:

```hcl
resource "vergeio_vm" "app_server" {
  name                 = "app-server-01"
  os_family            = "linux"
  cpu_cores            = 4
  machine_type         = "q35"
  ram                  = 8192
  guest_agent          = true
  cloudinit_datasource = "nocloud"

  vergeio_drive {
    name           = "OS Disk"
    disksize       = 20
    interface      = "virtio-scsi"
    preferred_tier = 2
  }

  vergeio_nic {
    interface = "virtio"
    vnet      = vergeio_network.web_network.id
  }
}
```

For the exact syntax used to attach cloud-init files inline on the VM resource (vs. referencing pre-uploaded files via the data source), consult the [provider repository](https://github.com/verge-io/terraform-provider-vergeio) — the field-level form may evolve between releases.

### Maturity & Roadmap

{% hint style="warning" %}
**Check Current Resource Coverage**

The VergeOS Terraform provider is under active development, and not every VergeOS object is exposed as a managed resource yet. Examples of areas that may not have full provider coverage at a given point in time include tenant provisioning, snapshot profile management, and external/WAN network configuration.

Always check the [GitHub repository](https://github.com/verge-io/terraform-provider-vergeio) and the Terraform Registry listing for the current resource coverage and release notes before designing a configuration around them.
{% endhint %}

## Packer Plugin

The **Packer plugin for VergeOS** (`github.com/verge-io/packer-plugin-vergeio`) automates the creation of VM images directly on the VergeOS platform. Where Terraform manages running infrastructure, Packer focuses on building the **golden images** that serve as the foundation for deployments.

### Why Packer?

```mermaid
flowchart LR
    A["Base ISO"] --> B["Packer Build"]
    B --> C["Install Packages<br/>Harden OS<br/>Configure Services"]
    C --> D["Golden Image"]
    D --> E["VM Recipe"]
    D --> F["Terraform Deploy"]
    D --> G["Manual Provisioning"]

    style B fill:#4a9eff,color:#fff
    style D fill:#2ecc71,color:#fff
```

Golden images ensure every deployed VM starts from a known, tested, and hardened baseline. Instead of provisioning a bare OS and running configuration scripts on every deployment, Packer pre-bakes the image once:

- **Consistency** — Every VM created from the image is identical
- **Speed** — No first-boot provisioning delay; VMs are ready immediately
- **Compliance** — Security baselines and patches are baked in at build time
- **Pipeline integration** — Trigger image rebuilds from CI/CD on OS patch days

### Plugin Configuration

The Packer plugin is declared in a `required_plugins` block alongside a `source` and `build` for the target image. The exact field names for the `source "vergeio"` block (endpoint, credentials, VM sizing, disk options, etc.) should be taken from the plugin repository, as they may evolve between releases:

- [`verge-io/packer-plugin-vergeio` on GitHub](https://github.com/verge-io/packer-plugin-vergeio)

A typical `required_plugins` declaration looks like:

```hcl
packer {
  required_plugins {
    vergeio = {
      source  = "github.com/verge-io/vergeio"
      version = ">= 0.1.1"
    }
  }
}
```

### Capabilities

At a high level, the plugin drives the full Packer build lifecycle against the VergeOS API — creating a temporary VM, running provisioners, and capturing the resulting image. For the exact configuration schema, supported guest types, and shutdown/cleanup behavior, refer to the plugin repository directly:

- [`verge-io/packer-plugin-vergeio` on GitHub](https://github.com/verge-io/packer-plugin-vergeio)

### Packer → Recipes Pipeline

Packer images integrate naturally with the VergeOS **Recipe** system. A typical workflow:

1. **Packer** builds and hardens the golden image on a schedule (e.g., monthly patch cycle)
2. The image is registered as a **VM Recipe** in the VergeOS Marketplace
3. Users deploy standardized VMs from the recipe — either through the UI or via Terraform
4. Updates flow automatically: rebuild the Packer image, update the recipe, and all new deployments get the latest version

## IaC Workflow Patterns

### Terraform-Only Workflow

For teams that want declarative infrastructure without image pipelines:

```mermaid
flowchart LR
    A["HCL Config"] --> B["terraform plan"]
    B --> C["terraform apply"]
    C --> D["VergeOS API"]
    D --> E["VMs + Networks<br/>Created"]

    style B fill:#7b42f5,color:#fff
    style C fill:#4a9eff,color:#fff
```

### Full Pipeline (Packer + Terraform)

For production environments with golden image management:

```mermaid
flowchart LR
    A["Base ISO"] --> B["Packer Build"]
    B --> C["Golden Image"]
    C --> D["Terraform Deploy"]
    D --> E["Production VMs"]
    F["CI/CD Trigger"] -.-> B

    style B fill:#2ecc71,color:#fff
    style D fill:#4a9eff,color:#fff
```

### Combined with Other Tools

Terraform handles provisioning; configuration management tools handle the rest:

| Phase              | Tool                        | Purpose                            |
| ------------------ | --------------------------- | ---------------------------------- |
| **Image creation** | Packer                      | Build hardened golden images       |
| **Provisioning**   | Terraform                   | Deploy VMs, networks, users        |
| **Configuration**  | Ansible / cloud-init        | Post-deploy software configuration |
| **Monitoring**     | Prometheus / VergeOS alerts | Observe deployed infrastructure    |

{% hint style="info" %}
**VMware Bridge**

On VMware, Terraform's vSphere provider manages ESXi/vCenter/vSAN as separate concerns and Packer uses the `vsphere-iso` builder via vCenter. The single VergeOS `vergeio` provider handles VMs, networks, drives, and users through one API endpoint, and the Packer plugin targets the same API.
{% endhint %}

{% hint style="info" %}
**Nutanix Bridge**

The Nutanix Terraform provider (`nutanix/nutanix`) and Packer plugin both target Prism Central's v3 API. The VergeOS provider talks to a single endpoint (the VergeOS system or tenant URL) with no separate management instance, and exposes cloud-init configuration directly on the `vergeio_vm` resource via the `cloudinit_datasource` attribute and the `vergeio_cloudinitfiles` data source.
{% endhint %}

## Best Practices

### State Management

- **Use remote state backends** (S3, Consul, Terraform Cloud) for team collaboration
- **Never commit** `terraform.tfstate` to version control — it may contain credentials
- **Lock state files** to prevent concurrent modifications in multi-user environments

### Security

- **Use variables** for sensitive values (`var.vergeos_password`) — never hardcode credentials
- **Mark sensitive outputs** with `sensitive = true` to prevent accidental exposure in logs
- **Restrict provider permissions** — create a dedicated VergeOS API user with minimum required access

### Module Organization

- **Separate environments** into workspaces or directories (`dev/`, `staging/`, `prod/`)
- **Create reusable modules** for common patterns (e.g., a "web-server" module with VM + network + firewall rules)
- **Pin provider versions** to avoid unexpected breaking changes during upgrades

## Further Reading

- [Terraform Provider — GitHub](https://github.com/verge-io/terraform-provider-vergeio)
- [Terraform Registry — VergeIO Provider](https://registry.terraform.io/providers/verge-io/vergeio/latest)
- [Packer Plugin — GitHub](https://github.com/verge-io/packer-plugin-vergeio)
- [OpenTofu Registry — VergeIO Provider](https://search.opentofu.org/provider/verge-io/vergeio/latest)
- [VergeOS Docs — Terraform Provider](https://docs.verge.io/product-guide/tools-integrations/terraform-provider/)
