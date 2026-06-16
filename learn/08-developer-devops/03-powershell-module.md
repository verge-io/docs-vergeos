---
description: "Manage VergeOS infrastructure with the PSVergeOS PowerShell module — over 200 cmdlets for VM lifecycle, networking, storage, multi-tenancy, VPN, and disaster recovery automation."
---

# PowerShell Module (PSVergeOS)

**PSVergeOS** is a cross-platform PowerShell module that provides **over 200 cmdlets** for managing VergeOS infrastructure through the REST API. If your team already uses PowerShell for Windows Server, Active Directory, or VMware management, PSVergeOS lets you extend those same workflows and scripting patterns to VergeOS — with full pipeline support, tab completion, and the familiar `Verb-Noun` cmdlet naming convention.

## Requirements & Installation

| Requirement    | Version               |
| -------------- | --------------------- |
| **PowerShell** | 7.4 or later          |
| **VergeOS**    | 26.0 or later         |
| **Platform**   | Windows, macOS, Linux |

### From PowerShell Gallery (Recommended)

```powershell
Install-Module -Name PSVergeOS -Scope CurrentUser
```

### Manual Installation (Development)

```powershell
git clone https://github.com/verge-io/PSVergeOS.git
Import-Module ./PSVergeOS/PSVergeOS.psd1
```

### Verify Installation

```powershell
Get-Module PSVergeOS -ListAvailable
Get-Command -Module PSVergeOS | Measure-Object  # Should show 200+ cmdlets
```

## Authentication

PSVergeOS supports multiple authentication methods to fit different environments — from interactive admin sessions to fully automated pipelines.

### Interactive Credentials

Prompt for username and password at connection time:

```powershell
Connect-VergeOS -Server "vergeos.example.com"
# Prompts for credentials interactively
```

### PSCredential Object

Store credentials securely for non-interactive scripts:

```powershell
$cred = Get-Credential
Connect-VergeOS -Server "vergeos.example.com" -Credential $cred
```

### API Token

Use a pre-generated API token for automation pipelines:

```powershell
Connect-VergeOS -Server "vergeos.example.com" -Token $env:VERGEOS_TOKEN
```

### Self-Signed Certificates

For lab and development environments with self-signed certificates:

```powershell
Connect-VergeOS -Server "192.168.1.100" -Token $token -SkipCertificateCheck
```

{% hint style="warning" %}
Only use `-SkipCertificateCheck` in test environments. For production systems, configure valid SSL certificates.
{% endhint %}

## Multi-Server Management

PSVergeOS can manage **multiple VergeOS systems** from a single PowerShell session. Use the `-PassThru` parameter to capture connection objects and the `-Server` parameter to target specific systems:

```powershell
# Connect to multiple systems
$prod = Connect-VergeOS -Server "prod.vergeos.local" -Token $env:PROD_TOKEN -PassThru
$dev  = Connect-VergeOS -Server "dev.vergeos.local"  -Token $env:DEV_TOKEN  -PassThru

# Query VMs on a specific server
Get-VergeVM -Server $prod
Get-VergeVM -Server $dev

# Switch the default connection
Set-VergeConnection -Server "prod.vergeos.local"
```

This is particularly valuable for **MSPs** managing multiple customer environments or organizations with separate production and development VergeOS clusters.

## Cmdlet Categories

The module organizes its 200+ cmdlets into functional categories. Each category covers the full CRUD lifecycle plus resource-specific actions.

| Category               | Description                                                |
| ---------------------- | ---------------------------------------------------------- |
| **Connection**         | Connect, disconnect, manage server connections             |
| **Virtual Machines**   | Lifecycle, power control, snapshots, drives, NICs, cloning |
| **Networking**         | Virtual networks, firewall rules, DNS, DHCP, diagnostics   |
| **VPN**                | IPSec connections/policies, WireGuard interfaces/peers     |
| **NAS & Storage**      | NAS services, volumes, CIFS/NFS shares, snapshots, sync    |
| **Tenants**            | Provisioning, snapshots, storage/network block allocation  |
| **Users & Groups**     | Account management, permissions, API keys                  |
| **System**             | Clusters, nodes, licenses, settings                        |
| **Certificates**       | SSL certificate management                                 |
| **Tags**               | Resource tagging and categorization                        |
| **Webhooks**           | Event-driven automation hooks                              |
| **Monitoring & Tasks** | Alarms, logs, async task tracking                          |
| **Backup & DR**        | Snapshot profiles, cloud snapshots, site management, sync  |
| **Files & Media**      | ISO management, file uploads                               |
| **Resource Groups**    | Logical resource grouping                                  |

### VPN Cmdlets (IPSec & WireGuard)

The VPN category deserves special attention — PSVergeOS provides full management for both IPSec and WireGuard VPN implementations:

**IPSec:**

- `New-VergeIPSecConnection` / `Get-VergeIPSecConnection` / `Remove-VergeIPSecConnection`
- `New-VergeIPSecPolicy` / `Get-VergeIPSecPolicy` / `Remove-VergeIPSecPolicy`

**WireGuard:**

- `New-VergeWireGuardInterface` / `Get-VergeWireGuardInterface` / `Remove-VergeWireGuardInterface`
- `New-VergeWireGuardPeer` / `Get-VergeWireGuardPeer` / `Remove-VergeWireGuardPeer`

## Pipeline Support

One of PSVergeOS's biggest strengths is **full PowerShell pipeline support**. Cmdlets accept pipeline input and produce pipeline output, enabling concise one-liners for bulk operations:

```powershell
# Stop all development VMs
Get-VergeVM -Name "Dev-*" | Stop-VergeVM -Confirm:$false

# Snapshot all production VMs
Get-VergeVM -Name "Prod-*" | ForEach-Object {
    New-VergeVMSnapshot -VMName $_.Name -Name "Daily-$(Get-Date -Format 'yyyyMMdd')"
}

# Power on all VMs in a specific network
Get-VergeVM | Where-Object { $_.Network -eq "app-network" } | Start-VergeVM
```

Pipeline support makes PSVergeOS particularly effective for **scheduled maintenance** tasks integrated with Windows Task Scheduler or Linux cron jobs.

## Practical Examples

### Bulk Snapshot with Retention

```powershell
# Connect to the VergeOS system
Connect-VergeOS -Server "vergeos.example.com" -Token $env:VERGEOS_TOKEN

# Snapshot all running production VMs with a 24-hour retention
$vms = Get-VergeVM -Name "Prod-*" | Where-Object { $_.PowerState -eq "Running" }

foreach ($vm in $vms) {
    $snapshot = New-VergeVMSnapshot -VMName $vm.Name `
        -Name "Nightly-$(Get-Date -Format 'yyyyMMdd-HHmm')" `
        -Retention 86400
    Write-Host "Snapshotted $($vm.Name): $($snapshot.Name)"
}

Write-Host "Completed $($vms.Count) snapshots"
```

### VM Inventory CSV Export

```powershell
# Export complete VM inventory to CSV for reporting
Get-VergeVM | Select-Object Name, PowerState, RAM, CPUCores, OS,
    @{N='DiskGB'; E={[math]::Round($_.DiskSize / 1GB, 2)}},
    Created, Description |
    Export-Csv -Path "vm-inventory-$(Get-Date -Format 'yyyyMMdd').csv" -NoTypeInformation

Write-Host "Inventory exported to vm-inventory-$(Get-Date -Format 'yyyyMMdd').csv"
```

### Network Creation with Firewall Rules

```powershell
# Create an internal network with DHCP and firewall rules
$network = New-VergeNetwork -Name "web-tier" `
    -NetworkAddress "10.20.1.0/24" `
    -IPAddress "10.20.1.1" `
    -DHCPEnabled $true

# Add firewall rules
New-VergeNetworkRule -Network $network.Name `
    -Name "Allow HTTPS" -Action Accept -Protocol TCP -DestPort 443

New-VergeNetworkRule -Network $network.Name `
    -Name "Allow SSH" -Action Accept -Protocol TCP -DestPort 22

# Apply the rules and power on
Invoke-VergeNetworkApplyRules -Network $network.Name
Start-VergeNetwork -Name $network.Name

Write-Host "Network '$($network.Name)' is online with firewall rules applied"
```

### Multi-Tenant Resource Report

```powershell
# Generate a resource summary across all tenants
$report = @()

foreach ($tenant in Get-VergeTenant) {
    $tenantVMs = Get-VergeVM -Tenant $tenant.Name
    $report += [PSCustomObject]@{
        Tenant    = $tenant.Name
        VMCount   = $tenantVMs.Count
        TotalRAM  = ($tenantVMs | Measure-Object -Property RAM -Sum).Sum
        TotalCPU  = ($tenantVMs | Measure-Object -Property CPUCores -Sum).Sum
        Running   = ($tenantVMs | Where-Object PowerState -eq "Running").Count
        Stopped   = ($tenantVMs | Where-Object PowerState -ne "Running").Count
    }
}

$report | Format-Table -AutoSize
$report | Export-Csv "tenant-report.csv" -NoTypeInformation
```

### WireGuard VPN Setup

```powershell
# Create a WireGuard interface on the external network
$wgInterface = New-VergeWireGuardInterface -Network "External" `
    -Name "Remote-Access" `
    -IPAddress "10.100.0.1/24" `
    -ListenPort 51820

# Add a peer for a remote user
New-VergeWireGuardPeer -Interface $wgInterface.Name `
    -Name "Engineer-1" `
    -AllowedIPs "10.100.0.2/32" `
    -AutoGenerateConfig $true

# Apply network rules
Invoke-VergeNetworkApplyRules -Network "External"
```

## Integration with Task Scheduler

PSVergeOS scripts integrate naturally with scheduled task systems for hands-off automation:

**Windows Task Scheduler:**

```powershell
# Save as C:\Scripts\nightly-snapshot.ps1
Import-Module PSVergeOS
Connect-VergeOS -Server "vergeos.local" -Token $env:VERGEOS_TOKEN -SkipCertificateCheck
Get-VergeVM -Name "Prod-*" | ForEach-Object {
    New-VergeVMSnapshot -VMName $_.Name -Name "Nightly-$(Get-Date -Format 'yyyyMMdd')" -Retention 86400
}
Disconnect-VergeOS
```

**Linux cron (PowerShell 7.4+):**

```bash
# Run nightly at 2:00 AM
0 2 * * * /usr/bin/pwsh -File /opt/scripts/nightly-snapshot.ps1
```

## Common Use Cases

### Bulk VM Operations

Stop, start, snapshot, or migrate multiple VMs with pipeline one-liners.
Ideal for maintenance windows.
### Infrastructure Reporting

Export VM inventory, resource usage, and configuration data to CSV for
auditing and capacity planning.
### Network Automation

Create networks, configure DHCP, manage firewall rules, and set up VPN
tunnels programmatically.
### Scheduled Maintenance

Integrate with Task Scheduler or cron for automated snapshots, cleanup, and
compliance checks.

{% hint style="info" %}
**Coming from VMware or Nutanix?**

PSVergeOS uses the standard PowerShell `Verb-Noun` convention so muscle memory transfers — `Get-VM | Stop-VM` becomes `Get-VergeVM | Stop-VergeVM`. Authentication supports interactive prompts, `PSCredential` objects, and API tokens, so the same scripting patterns you already use for non-interactive automation apply here. To manage more than one VergeOS system from a single session, pass `-Server` on each cmdlet to target a specific connection.
{% endhint %}

## Additional Resources

- [GitHub Repository](https://github.com/verge-io/PSVergeOS) — Source code, issues, and 16 example scripts
- [PowerShell Gallery](https://www.powershellgallery.com/packages/PSVergeOS) — Latest release and install info
- [PowerShell 7.4 Documentation](https://learn.microsoft.com/en-us/powershell/) — PowerShell runtime reference
