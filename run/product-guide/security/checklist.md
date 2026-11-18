---
title: "Hardening Checklist"
description: "Track the configuration and verification of each VergeOS security baseline control. Download the checklist as a CSV file to record values, exceptions, and owners."
semantic_keywords:
  - "VergeOS hardening checklist"
  - "security baseline control tracking"
  - "security review configuration verification record"
use_cases:
  - track_hardening_progress
  - prepare_security_audit
  - record_security_exceptions
tags:
  - security
  - hardening
  - checklist
  - compliance
  - audit
categories:
  - Security
---

# Hardening Checklist

Use this checklist to track each control in the [Security Baseline](overview.md). Use a separate copy for each environment.

{% file src="../../.gitbook/assets/vergeos-hardening-checklist.csv" %}
Hardening checklist (CSV)
{% endfile %}

For each control, record these items:

- **Configured**: You applied the selected settings.
- **Verified**: You completed the **Verify** steps for the control.
- **N/A**: The control does not apply. Record the reason.
- **Values and exceptions**: The values you selected and any exceptions to the baseline.
- **Owner** and **Review date**: The person who owns the control and the date of the next review.

## Identity and access

| Control | Title |
| --- | --- |
| [IAM01](identity-access.md#iam01-require-multifactor-authentication) | Require multifactor authentication |
| [IAM02](identity-access.md#iam02-limit-mfa-device-trust) | Limit MFA device trust |
| [IAM03](identity-access.md#iam03-enforce-local-password-strength) | Enforce local password strength |
| [IAM04](identity-access.md#iam04-lock-out-repeated-failed-logins) | Lock out repeated failed logins |
| [IAM05](identity-access.md#iam05-bound-interactive-session-lifetime) | Bound interactive session lifetime |
| [IAM06](identity-access.md#iam06-remove-default-broad-read-grants-and-scope-roles) | Remove default broad read grants and scope roles |
| [IAM07](identity-access.md#iam07-restrict-physical-and-ssh-administration) | Restrict physical and SSH administration |
| [IAM08](identity-access.md#iam08-use-restricted-api-identities) | Use restricted API identities |
| [IAM09](identity-access.md#iam09-expire-and-revoke-api-keys) | Expire and revoke API keys |
| [IAM10](identity-access.md#iam10-restrict-api-keys-by-source-address) | Restrict API keys by source address |
| [IAM11](identity-access.md#iam11-disable-retired-accounts) | Disable retired accounts |
| [IAM12](identity-access.md#iam12-restrict-oidc-application-access-and-claims) | Restrict OIDC application access and claims |
| [IAM13](identity-access.md#iam13-preserve-break-glass-access-and-bound-host-sessions) | Preserve break-glass access and bound host sessions |

## Management access and TLS

| Control | Title |
| --- | --- |
| [TLS01](management-tls.md#tls01-configure-management-tls-certificates) | Configure management TLS certificates |
| [TLS02](management-tls.md#tls02-limit-management-tls-cipher-suites) | Limit management TLS cipher suites |
| [TLS03](management-tls.md#tls03-remove-unnecessary-http-entry-points) | Remove unnecessary HTTP entry points |
| [TLS04](management-tls.md#tls04-limit-trusted-ca-roots-and-certificate-renewal-exposure) | Limit trusted CA roots and certificate renewal exposure |

## Networking

| Control | Title |
| --- | --- |
| [NET01](networking.md#net01-restrict-management-network-sources) | Restrict management network sources |
| [NET02](networking.md#net02-enforce-traffic-policy-between-trust-zones) | Enforce traffic policy between trust zones |
| [NET03](networking.md#net03-restrict-replication-network-sources) | Restrict replication network sources |
| [NET04](networking.md#net04-log-boundary-decisions-without-persistent-packet-tracing) | Log boundary decisions without persistent packet tracing |
| [NET05](networking.md#net05-control-ipv6-exposure) | Control IPv6 exposure |
| [NET06](networking.md#net06-restrict-dns-recursion-and-zone-transfers) | Restrict DNS recursion and zone transfers |
| [NET07](networking.md#net07-constrain-ipsec-negotiation-and-tunnel-selectors) | Constrain IPsec negotiation and tunnel selectors |
| [NET08](networking.md#net08-constrain-wireguard-peers-and-permitted-routes) | Constrain WireGuard peers and permitted routes |
| [NET09](networking.md#net09-restrict-proxy-listener-and-fallback-exposure) | Restrict proxy listener and fallback exposure |
| [NET10](networking.md#net10-authorize-dynamic-routing-peers-and-route-advertisements) | Authorize dynamic routing peers and route advertisements |
| [NET11](networking.md#net11-apply-an-ordered-firewall-policy-without-blocking-reply-traffic) | Apply an ordered firewall policy without blocking reply traffic |
| [NET12](networking.md#net12-disable-unused-dns-dhcp-and-pxe-services) | Disable unused DNS, DHCP and PXE services |
| [NET13](networking.md#net13-use-trusted-ntp-or-an-explicitly-designed-ptp-domain) | Use trusted NTP or an explicitly designed PTP domain |

## Compute and VMs

| Control | Title |
| --- | --- |
| [HV01](compute-vms.md#hv01-keep-cpu-security-mitigations-enabled) | Keep CPU security mitigations enabled |
| [HV02](compute-vms.md#hv02-limit-nested-virtualization-and-device-passthrough) | Limit nested virtualization and device passthrough |
| [HV03](compute-vms.md#hv03-verify-guest-boot-integrity-and-protect-guest-encryption-keys) | Verify guest boot integrity and protect guest encryption keys |
| [HV04](compute-vms.md#hv04-restrict-vm-consoles-and-snapshot-exports) | Restrict VM consoles and snapshot exports |
| [HV05](compute-vms.md#hv05-constrain-sr-iov-vgpu-and-direct-device-privileges) | Constrain SR-IOV, vGPU and direct-device privileges |

## Tenant isolation

| Control | Title |
| --- | --- |
| [TEN01](tenants.md#ten01-authorize-tenant-layer-2-attachments) | Authorize tenant layer 2 attachments |
| [TEN02](tenants.md#ten02-control-tenant-access-to-historical-snapshots) | Control tenant access to historical snapshots |
| [TEN03](tenants.md#ten03-prepare-tenant-network-containment) | Prepare tenant network containment |

## Storage and recovery

| Control | Title |
| --- | --- |
| [STO01](storage-recovery.md#sto01-encrypt-vsan-during-initial-installation) | Encrypt vSAN during initial installation |
| [STO03](storage-recovery.md#sto03-protect-recovery-points-with-immutability) | Protect recovery points with immutability |
| [STO04](storage-recovery.md#sto04-encrypt-replication-and-restrict-intersite-authority) | Encrypt replication and restrict intersite authority |
| [STO05](storage-recovery.md#sto05-define-immutable-snapshot-schedules-and-consistency-boundaries) | Define immutable snapshot schedules and consistency boundaries |
| [STO06](storage-recovery.md#sto06-protect-site-sync-queues-and-the-separate-recovery-domain) | Protect Site Sync queues and the separate recovery domain |
| [STO07](storage-recovery.md#sto07-validate-recovery-without-treating-a-system-restore-as-a-harmless-test) | Validate recovery without treating a system restore as a harmless test |

## NAS

| Control | Title |
| --- | --- |
| [NAS01](nas.md#nas01-encrypt-nas-volumes-at-creation) | Encrypt NAS volumes at creation |
| [NAS02](nas.md#nas02-set-an-explicit-minimum-smb-protocol) | Set an explicit minimum SMB protocol |
| [NAS03](nas.md#nas03-prevent-unintended-anonymous-smb-access) | Prevent unintended anonymous SMB access |
| [NAS04](nas.md#nas04-restrict-smb-users-clients-and-write-access) | Restrict SMB users, clients and write access |
| [NAS05](nas.md#nas05-require-smb-integrity-and-confidentiality-where-exposed) | Require SMB integrity and confidentiality where exposed |
| [NAS06](nas.md#nas06-restrict-nfs-clients-and-root-authority) | Restrict NFS clients and root authority |
| [NAS07](nas.md#nas07-enable-nas-antivirus-and-quarantine-handling) | Enable NAS antivirus and quarantine handling |
| [NAS08](nas.md#nas08-preserve-access-controls-during-nas-synchronization) | Preserve access controls during NAS synchronization |
| [NAS09](nas.md#nas09-limit-share-paths-identity-forcing-and-protocol-side-effects) | Limit share paths, identity forcing and protocol side effects |
| [NAS10](nas.md#nas10-preserve-copy-semantics-without-mirroring-destructive-changes) | Preserve copy semantics without mirroring destructive changes |
| [NAS11](nas.md#nas11-review-remote-mount-protocols-and-external-storage-trust) | Review remote mount protocols and external storage trust |

## Logging and monitoring

| Control | Title |
| --- | --- |
| [AUD01](logging-monitoring.md#aud01-export-security-logs-outside-the-cluster) | Export security logs outside the cluster |
| [AUD02](logging-monitoring.md#aud02-capture-node-logs-and-preserve-trustworthy-timestamps) | Capture node logs and preserve trustworthy timestamps |
| [AUD03](logging-monitoring.md#aud03-retain-finite-api-abuse-limits) | Retain finite API abuse limits |
| [AUD04](logging-monitoring.md#aud04-export-application-audit-tables-separately-from-node-syslog) | Export application audit tables separately from node syslog |
| [AUD05](logging-monitoring.md#aud05-route-alarms-and-exact-owner-sync-events-through-tested-tasks) | Route alarms and exact-owner sync events through tested tasks |
| [AUD06](logging-monitoring.md#aud06-monitor-protection-freshness-and-ransomware-indicators-externally) | Monitor protection freshness and ransomware indicators externally |

## VergeIQ

| Control | Title |
| --- | --- |
| [AI01](vergeiq.md#ai01-scope-ai-permissions-separately-from-platform-permissions) | Scope AI permissions separately from platform permissions |
| [AI02](vergeiq.md#ai02-set-chat-history-retention) | Set chat history retention |

## Integrations

| Control | Title |
| --- | --- |
| [INT01](integrations.md#int01-validate-external-repository-and-migration-endpoints) | Validate external repository and migration endpoints |
| [INT02](integrations.md#int02-restrict-catalog-publication) | Restrict catalog publication |
| [INT03](integrations.md#int03-protect-outbound-webhooks) | Protect outbound webhooks |
| [INT04](integrations.md#int04-protect-smtp-when-used-for-security-notifications-or-mfa) | Protect SMTP when used for security notifications or MFA |
| [INT05](integrations.md#int05-disable-authentication-source-debug-logging) | Disable authentication source debug logging |

## Platform operations

| Control | Title |
| --- | --- |
| [OPS01](platform-operations.md#ops01-use-supported-signed-updates-with-bounded-rollback-exposure) | Use supported signed updates with bounded rollback exposure |
| [OPS02](platform-operations.md#ops02-isolate-bmc-access-and-manage-bmc-credentials-at-their-source) | Isolate BMC access and manage BMC credentials at their source |
| [OPS03](platform-operations.md#ops03-maintain-owner-inventory-and-recurring-boundary-reviews) | Maintain owner inventory and recurring boundary reviews |
