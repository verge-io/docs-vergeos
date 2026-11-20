---
title: "Network Hardening"
description: "Hardening controls for VergeOS networks: management and replication access, firewall rule order, DNS, DHCP, VPN, proxy, dynamic routing, IPv6, and time sources."
semantic_keywords:
  - "VergeOS network firewall rule hardening"
  - "restrict management access source IP"
  - "DNS recursion zone transfer restriction"
  - "WireGuard IPsec VPN hardening"
  - "NTP PTP time source security"
use_cases:
  - restrict_management_access
  - enforce_trust_zone_firewall_policy
  - restrict_dns_recursion_and_transfers
  - harden_vpn_tunnels
  - disable_unused_network_services
tags:
  - security
  - hardening
  - networking
  - firewall
  - network-rules
  - dns
  - vpn
  - wireguard
  - ipsec
  - ntp
categories:
  - Security
---

# Network Hardening

This page covers hardening controls for VergeOS networks, network services, VPNs, and time synchronization. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

Rule changes take effect only after **Apply Rules** completes on the network dashboard. Test only after the apply completes.

## NET01: Restrict management network sources

Allow UI and SSH access only from approved administrative networks.

**Default:** Depends on the installation topology. A new rule is enabled and accepts any incoming protocol.

{% hint style="warning" %}
Keep a tested second management path before you change these rules. A wrong source address can lock all administrators out.
{% endhint %}

**Configure:** In the External network's **Rules**, edit the **System UI** and **SSH Access** rules. Set **Source** to the administrative CIDRs, for example `10.10.0.0/24`. Remove rules that bypass the restriction, including pinned rules. Click **Submit**, then **Apply Rules**.

**Verify:** Ports 22 and 443 accept connections from an approved source and refuse them from any other source. A narrow rule later in the list does not deny traffic that an earlier rule accepts, so check all overlapping Accept and Translate rules.

## NET02: Enforce traffic policy between trust zones

Block unapproved lateral movement and egress between tenant, workload, and management zones.

**Default:** A new rule accepts any incoming protocol. Generated rules differ by network type.

**Configure:** In the network's **Rules**, create narrow Accept rules for each required flow (source, destination, protocol, port). Click **Apply Rules**. Unmatched incoming traffic is already dropped, except forwarded traffic on BGP networks. Attach each VM to the correct network in its **NICs**. Router rules do not filter traffic on a shared layer 2 segment, so put the block where traffic actually crosses a router. See NET11 for rule order.

{% hint style="warning" %}
The rule that accepts reply traffic comes after your rules. A broad Drop or Reject rule also blocks the replies for allowed flows.
{% endhint %}

**Verify:** From real guest and tenant sources, test allowed and denied flows in both directions, including existing sessions.

## NET03: Restrict replication network sources

Allow connections to the site replication service only from approved peers.

**Default:** Site replication uses port 14201. Source restrictions depend on the installed rules.

**Configure:** In the External network's **Rules**, set the replication rule's **Source** to the approved peer CIDRs and its port to the configured replication port. The replication rule is disabled by default. Do not enable it unless you use replication. If you no longer use replication, clear **Enabled**. Click **Submit**, then **Apply Rules**.

**Verify:** An approved peer connects to the replication port and an excluded source cannot. Check for overlapping rules that permit the same connection. This control does not isolate or verify the core link.

## NET04: Track boundary traffic without persistent packet tracing

Count the traffic that matches boundary rules without collecting packet contents. Rule statistics are counters. They do not record the time, source, or destination of each connection. If you need that record, collect it at an upstream device.

**Default:** **Trace/Debug Rule**, network trace, and **Port Mirroring** are off.

{% hint style="warning" %}
The **Log this rule** option does not create log entries. Do not rely on it for boundary logging.
{% endhint %}

**Configure:** Turn on **Track Rule Statistics** for management and trust-boundary rules. Leave **Trace/Debug Rule** and **Port Mirroring** off. Use trace and port mirroring only during an approved investigation.

**Verify:** Send allowed and denied traffic across a boundary. The statistics counters for the matching rules increase. Trace and port mirroring are off after each investigation.

## NET05: Control IPv6 exposure

Keep IPv6 paths from bypassing the network policy.

**Default:** `ipv6_enabled` is false.

**Configure:** In **System > Settings > Advanced Settings**, keep `ipv6_enabled` false unless the platform must route IPv6. This setting is a kernel boot option, so a change takes effect only after each node restarts. If you turn it on, add equivalent IPv6 firewall, management, and DNS controls.

**Verify:** Test management access and traffic between zones over IPv6. This setting does not block IPv6 between guests on the same layer 2 segment, so test guest traffic separately.

## NET06: Restrict DNS recursion and zone transfers

Prevent open-resolver abuse and disclosure of zone contents.

**Default:** BIND views have **Recursion** off and zones have **Allow Transfer** set to `none;`. **Match Clients** has no approved client list.

**Configure:** In the network's **DNS** views, keep **Recursion** off for authoritative views. For internal views that need recursion, set **Match Clients** to trusted CIDRs and order those views before external views. In each zone, keep **Allow Transfer** at `none;` or list only approved secondaries. Send notifications only to approved secondaries. Apply DNS. For Simple DNS, restrict port 53 with network rules.

**Verify:** From an untrusted source, recursion and zone transfer both fail over UDP and TCP. Approved clients and secondaries succeed only where you configured them:

```bash
dig @DNS_SERVER_IP example.com
dig @DNS_SERVER_IP ZONE_NAME AXFR
```

## NET07: Constrain IPsec negotiation and tunnel selectors

Authenticate peers, keep strong encryption, and limit which networks a tunnel carries.

**Default:** Phase 1 uses **Key Exchange** auto (`ike`), `aes256-sha256-modp2048`, and a pre-shared key. Phase 2 uses ESP with AES-128.

**Configure:** In **Phase 1**, use IKEv2 if the peer supports it, a strong unique pre-shared key or a certificate, and only approved proposals. In **Phase 2**, select approved proposals, for example AES-256, and set the local and remote networks to the narrowest CIDRs. Review the generated firewall rules. Test on an isolated tunnel first.

**Verify:** The tunnel negotiates the expected algorithms. A peer with a wrong key fails, and traffic outside the selectors does not cross the tunnel.

## NET08: Constrain WireGuard peers and permitted routes

Limit the reach of an authenticated VPN peer.

**Default:** **Allowed IPs** is required. **Configure Firewall** defaults to site-to-site and can create routes and Accept rules.

**Configure:** Give each peer its own key and the narrowest **Allowed IPs**. Use a default route only for an intended full tunnel. Review the Accept and SNAT rules that **Configure Firewall** creates. Click **Submit**, then **Apply Rules**.

**Verify:** Approved traffic succeeds and traffic to other subnets fails. Disable a test peer and confirm new traffic stops.

## NET09: Restrict proxy listener and fallback exposure

Keep a network proxy from exposing the VergeOS UI or unintended hostnames.

**Default:** The proxy is off. A new proxy listens on `0.0.0.0` and falls back to the VergeOS UI (**Default Self** on).

**Configure:** Turn on the proxy only where needed. Set **Proxy Listen Address** to the intended address. If proxy clients must not reach the VergeOS UI, turn off **Default Self**. Apply the proxy and rules.

**Verify:** From the exposed zone, request an approved hostname, an unknown hostname, and the bare IP address. Only the intended applications respond.

## NET10: Authorize dynamic routing peers and route advertisements

Keep untrusted neighbors and unapproved routes out of the fabric.

**Default:** No peer or authentication policy exists. A new route map permits.

**Configure:** In the network's routing settings, create restrictive import and export route maps first. Add BGP routers with explicit, authenticated neighbors, and attach the maps. In the OSPF commands, set `passive-interface default`, then enable only interfaces that face approved peers. Restart the routing configuration when prompted. Keep neighbor passwords out of reports.

**Verify:** On an isolated peer, an unknown neighbor, a wrong password, and an unapproved prefix are all rejected. Approved routes stay stable.

## NET11: Apply an ordered firewall policy without blocking reply traffic

Make the default-deny policy explicit and test the real routed path.

**Default:** Depends on the network type and its rules.

Unmatched incoming traffic is already dropped, except forwarded traffic on BGP networks. The rule that accepts reply traffic comes after your rules.

{% hint style="danger" %}
Do not add a catch-all incoming Drop. It adds no protection and blocks reply traffic, which can cut off management access.
{% endhint %}

**Configure:** Order the rules:

1. Pinned **Top**: narrow management and VPN rules that prevent lockout.
2. Service and east-west Accept rules from approved sources, for example SSH 22, RDP 3389, monitoring 9100, PostgreSQL 5432, and HTTPS 443.
3. Required egress Accept rules.
4. Narrow Translate rules, only on the receiving external network.
5. On BGP networks only: an incoming Drop for forwarded traffic. Set its **Connection Tracking State** to `!= { established, related }` so that it does not drop reply traffic. Apply it while the second management path is available, then test return traffic with this exact rule set.

Add an outgoing Drop only after DNS (UDP and TCP 53), NTP (UDP 123), updates, SMTP, backups, monitoring, and application dependencies work. Edit **System Rules** only as NET01 and NET03 describe. Test a **Connection Tracking State** of `!= { established, related }` on an isolated network before you use it. Keep **Interface** at **Auto** unless you need Router, DMZ, or WireGuard.

**Verify:** Keep a second management path. Apply in small steps. Test new flows, return traffic, existing sessions, and denied sources in both directions, and check **Track Rule Statistics** counters. A network rule covers only traffic that crosses that network, so protect node management upstream.

## NET12: Disable unused DNS, DHCP, and PXE services

Remove resolver, address-assignment, and network-boot services that nothing needs.

**Default:** Depends on each network's configuration.

{% hint style="warning" %}
Do not change DNS, DHCP, or PXE on the Core or provisioning networks. The nodes depend on them.
{% endhint %}

**Configure:** In each network's settings:

- **DNS:** **Disabled** unless the network must serve Simple or BIND DNS. Use only approved resolvers. With upstream DHCP, review **Override DHCP DNS**, and turn on **DHCP Broadcast** only if required.
- **DHCP:** On only where the network must assign addresses. Use static leases for infrastructure and keep the dynamic range clear of router, VIP, and static addresses. Turn off **Dynamic DHCP** on infrastructure networks.
- **PXE:** None, with TFTP cleared, except on an isolated provisioning network.

Apply DNS after changes.

**Verify:** Only the intended networks answer DNS, DHCP, and PXE requests. Clients receive the approved DNS, gateway, and range, and no second DHCP server answers. Clients outside the provisioning network get no boot options.

## NET13: Use trusted NTP or an explicitly designed PTP domain

Keep authentication, certificate checks, and log timestamps accurate.

**Default:** **NTP Servers** is `0.pool.ntp.org` through `3.pool.ntp.org`. **NTP Max Clocks** is 11, **NTP Min Clocks** is 4, and **NTP Min Sane** is 1.

**Configure:** In **System > Time Settings**, set **NTP Servers** to reachable, approved sources. Do not set a quorum the sources cannot meet. For example, four independent sources can use **NTP Max Clocks** 4, **NTP Min Clocks** 3, and **NTP Min Sane** 2; [Time Settings](../system/time-settings.md) advises changing these only with VergeOS support. Use PTP only with a dedicated physical timing network and interface, an assigned domain, and hardware timestamp support. Review priority (for example, 128), two-step, and DSCP against that design. Restrict timing traffic to approved infrastructure.

**Verify:** Node 1 synchronizes with the intended sources, and the other nodes synchronize with node 1. Time alarms clear, and node timestamps agree. The quorum holds when one source is lost.

## Related pages

- [Network Rules](../networks/network-rules.md)
- [Aliases](../networks/aliases.md)
- [Tracking Network Statistics](../networks/tracking-net-statistics.md)
- [Port Mirroring](../networks/port-mirroring.md)
- [VergeOS Authoritative DNS](../networks/authoritative-dns.md)
- [Internal Networks (General Instructions)](../networks/internal-networks.md)
- [IPsec Configuration](../vpn/ipsec.md)
- [WireGuard](../vpn/wireguard-config.md)
- [Advanced System Settings](../system/advanced-system-settings.md)
- [Time Settings](../system/time-settings.md)
- [Site Sync Configuration](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/sync-configuration)
- [Configuring a Proxy](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/tenants/configuring-proxy)
