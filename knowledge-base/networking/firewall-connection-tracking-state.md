---
title: Using Connection Tracking State in Firewall Rules
slug: firewall-connection-tracking-state
author: VergeOS Documentation Team
date: 2026-08-03T12:00:00.000Z
semantic_keywords:
  - firewall rule connection tracking state ct_state
  - stateful firewall drop rule blocks return traffic
  - block new inbound connections allow established related
  - nftables conntrack new established related untracked
use_cases:
  - block_unsolicited_inbound_traffic
  - fix_outbound_traffic_broken_by_drop_rule
  - scope_firewall_rules_by_connection_state
categories:
  - Networking
editor: markdown
dateCreated: 2026-08-03T12:00:00.000Z
description: >-
  How to use the Connection Tracking State field on VergeOS firewall rules to
  block new inbound connections without dropping return traffic for outbound
  connections.
tags:
  - networking
  - firewall
  - rules
  - conntrack
  - nat
  - snat
  - troubleshooting
---

# Using Connection Tracking State in Firewall Rules

## Overview

{% hint style="info" %}
**Key Points**

- VergeOS firewall rules are stateful; the **Connection Tracking State** field matches packets by conntrack state.
- Scope a **Drop** rule to state `new` to block unsolicited inbound connections without dropping return traffic.
- Do not add your own accept rule for return traffic — the generated chain already accepts `established`/`related` traffic.
{% endhint %}

VergeOS firewall rules are stateful. The **Connection Tracking State** field on a network rule matches only the selected conntrack states. Its most common use is to make a **Drop** rule block *new* inbound connections without also dropping the *return traffic* of connections that the protected host starts itself.

## Prerequisites

- Familiarity with [VergeOS network rules](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/network-rules).
- A user with permission to edit network rules.

## The Connection Tracking State Field

The field is in the **Advanced** section of a network rule's edit form. Leave it blank to match any state.

**Allowed values:** `new`, `established`, `related`, `untracked`.

| State | Meaning |
|-------|---------|
| `new` | The first packet of a connection — an unsolicited connection attempt. |
| `established` | Packets that belong to a connection already seen in both directions. |
| `related` | A new connection that conntrack ties to an existing one (for example, FTP data channels and ICMP errors). |
| `untracked` | Packets explicitly excluded from connection tracking. |

The field accepts multiple states separated by commas (`established,related`) and negation with a leading `!=` (`!= new`).

{% hint style="info" %}
There is no `invalid` option. VergeOS already drops invalid packets with a system baseline rule (`ct state invalid drop`) near the top of every generated chain, so you do not add one yourself.
{% endhint %}

## The Problem: A Drop Rule That Breaks Outbound Traffic

A single public IP is often used both for inbound services and as the outbound SNAT address for a tenant or VM behind it. A blanket **Drop** rule on that destination IP blocks unsolicited inbound traffic as intended — but it also drops the replies to the tenant's own outbound traffic, because those replies arrive at the same public IP in state `established`.

The symptom: the tenant cannot reach the internet, and removing the deny rule fixes it.

Removing the drop lets the established replies through, but it also re-opens unsolicited inbound access — exactly what the rule was created to block. Do not remove the rule; scope it.

## The Fix: Scope the Drop to New Connections

1. From the network's dashboard, click **Rules** on the left menu.
2. Select the **Drop** rule and click **Edit** on the left menu.
3. In the **Connection Tracking State** field, enter `new`.
4. Click **Submit**.
5. Click **Apply Rules** on the left menu to put the change into effect.

The drop now matches only new, unsolicited inbound connections. Return traffic for outbound connections is in state `established`, no longer matches the drop, and falls through to the chain's trailing `ct state established,related accept`.

## Why No Return-Path Accept Rule Is Needed

VergeOS generates each network's `input` and `forwarding` chains with a `drop` policy and a trailing `ct state established,related accept` as the last line. nftables evaluates rules top-down, and `drop` and `accept` are terminal: an un-scoped drop placed above that trailing accept catches return traffic before it reaches the accept. Scoping the drop to `new` lets established and related traffic pass down to the trailing accept — you do not add an accept rule of your own.

> **Mental model:** Block `new` to lock out unsolicited inbound. Let `established` and `related` flow so anything the protected host started can finish.

## Worth Knowing

- Rule order matters. The trailing `established,related accept` is the last line of the generated chain; a blanket drop above it with no state set swallows return traffic.
- The same scoping applies to any rule, not just drops. For example, scope an inbound **Accept** to `new` to control which side can start connections.
- The `related` state matters for protocols with helper-tracked secondary flows (FTP, some VoIP, ICMP errors); the trailing system accept covers these.

## Additional Resources

- [Network Rules](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/networking/network-rules)

{% hint style="info" %}
**Need Help?**

If you have questions or problems with this procedure, contact the VergeOS support team.
{% endhint %}
