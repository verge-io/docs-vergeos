---
title: "Immutable Snapshots"
description: "How to enable and manage immutable snapshots in VergeOS, which block early deletion of system snapshots for ransomware protection for their retention period, up to 7 days."
semantic_keywords:
  - "immutable snapshots ransomware protection VergeOS"
  - "prevent snapshot deletion lock unlock"
  - "seven day unlock delay immutable flag"
  - "storage capacity planning immutable snapshot retention"
use_cases:
  - "enable_immutable_snapshot_protection"
  - "automate_immutable_snapshots_via_profile"
  - "unlock_immutable_snapshot"
  - "ransomware_recovery_planning"
tags:
  - snapshots
  - immutable
  - ransomware-protection
  - security
  - data-protection
  - storage-planning
categories:
  - Backup and DR
---

# Immutable Snapshots

## Overview

{% hint style="info" %}
**Key Points: Immutable Snapshot Protection**

- A system snapshot with an active immutable flag cannot be deleted — not by administrators, not by automated processes, and not by VergeOS Support.
- Removing the immutable flag triggers a mandatory unlock delay (up to 7 days), creating a critical response window if a rogue actor attempts to unlock snapshots.
- Expiration always takes precedence — snapshots auto‑purge at their natural expiration; otherwise, they become manually deletable after the unlock delay.
- Adequate free space is essential  — capacity planning must account for immutable snapshots that cannot be deleted until expiration or unlock delay.
 
{% endhint %}

Immutable snapshots provide a safeguard against accidental or malicious deletion of system snapshots. When a snapshot is marked **immutable**, no user — including administrators or VergeOS Support — can delete it early. The snapshot remains protected until it naturally expires or until the immutable flag is removed and the mandatory unlock delay completes.

A key purpose of immutability is to provide a **response window during security incidents**. If a rogue actor attempts to remove immutable protection, VergeOS generates alerts and enforces a mandatory unlock delay of up to **7 days**. This delay ensures administrators have time to detect the activity, investigate the account involved, and take corrective action before any protected snapshots can be deleted.

This design protects against sophisticated ransomware attacks that attempt to delete all recovery points, including those accessible to compromised admin accounts.

**Immutable protection applies to system snapshots only.**

---

## How Immutable Snapshots Work

When immutability is enabled:

- Early deletion is fully blocked for all users  
- Retention is not extended — snapshots expire normally  
- Removing the immutable flag starts a mandatory unlock delay of up to 7 days  
- Snapshots remain undeletable during the unlock delay  
- Expiration always takes precedence over the unlock delay  
- The unlock delay provides a critical detection and response window  

---

## Expiration vs. Unlock Delay

The snapshot’s original expiration date determines when it can be deleted:

- **If expiration occurs first:** VergeOS automatically purges the snapshot at expiration.  
- **If the unlock delay occurs first:** The snapshot becomes eligible for *manual* deletion at the end of the unlock delay. VergeOS does not automatically delete it unless expiration also arrives.

### Examples

| Snapshot Expiration | Unlock Requested | When Snapshot Is Deletable | Why |
|---------------------|------------------|-----------------------------|-----|
| 12 hours | Now | 12 hours (auto‑purge) | Expiration arrives first → system deletes automatically |
| 3 days | Now | 3 days (auto‑purge) | Expiration arrives first → system deletes automatically |
| 10 days | Now | 7 days (manual deletion allowed) | Unlock delay arrives first → snapshot becomes deletable but is not auto‑purged |
| Never | Now | 7 days (manual deletion allowed) | No expiration → unlock delay determines earliest manual deletion time |

**Auto‑purge:** VergeOS deletes the snapshot automatically at expiration.  
**Manual deletion allowed:** Snapshot is no longer protected and can be deleted by an admin, but VergeOS does not delete it automatically.

The unlock delay is the critical protection window that allows administrators to respond to unauthorized unlock attempts.

---

## Why Immutable Snapshots Protect Against Ransomware

Ransomware actors frequently attempt to delete all snapshots to eliminate recovery options. VergeOS’s immutable snapshot model prevents this by:

- Blocking deletion even from compromised admin accounts  
- Enforcing a mandatory unlock delay  
- Preserving recovery points long enough for administrators to detect and respond  
- Ensuring attackers cannot immediately erase protected snapshots  
- Providing a time buffer for administrators to react to unauthorized unlock attempts  

This design specifically addresses modern attacks that target privileged credentials.

---

## Default Behavior

The default **System Snapshots** profile marks **Hourly for 3 hours** snapshots as immutable. This provides a rapid‑cycle baseline protection layer.

This baseline assumes:

- Administrators monitor alerts consistently  
- Immutable‑flag removal alerts are acted on immediately  
- The organization has a short detection‑and‑response window  

Organizations with slower response windows may need longer‑retention immutable snapshots to ensure they have adequate time to react if a rogue actor attempts to unlock snapshots.

---

## Best Practices and Recommendations

### Choosing an Immutable Strategy Based on Response Window

#### Baseline (Default) Protection

- Hourly snapshots  
- 3‑hour retention  
- Immutable enabled  

Best for environments with fast response times (active SOC, 24/7 monitoring). Short‑retention immutable snapshots involve a short unlock delay - hourly snapshots are not deletable during their natural 3-hour retention.

#### Extended Protection

If your team cannot guarantee immediate response:

- Mark a **daily snapshot (24‑hour retention)** as immutable  
- Provides a full‑day reaction window  
- Ensures protected rollback points even during off‑hours  
- Gives administrators more time to respond to unauthorized unlock attempts  

Important: Daily immutable snapshots provide a longer response window but require more storage runway — they cannot be manually deleted during their full 24‑hour retention. 

#### Long‑Retention Immutable Snapshots

Use only when:

- Change rate is low  
- Ample free space is available  
- Multi‑day protected rollback points are required  
- You understand the operational impact of the unlock delay  
- You want a longer response window  

Generally suitable only for systems operating below ~70% storage capacity and non‑production environments.

**Critical:** Long‑retention immutable snapshots can hold space significantly longer. If expiration is 7 days or more, the unlock delay must fully elapse before deletion is possible.

---

## Storage Capacity Planning

Immutable snapshots delay deletion, so capacity planning must consider:

- Change rate  
- Retention  
- Free space  

### Critical Considerations

- Ensure free space can accommodate natural expirations or at least **7 days** of expected data change  
- Long‑retention immutable snapshots require capacity runway  
- Integrate capacity alerts with centralized monitoring or SIEM systems to ensure rapid response to an unauthorized unlock.
  
{% hint style="warning" %}
**Need Help Planning Your Immutable Snapshot Strategy?**

Immutable snapshots introduce strict deletion controls, and choosing the right retention and protection strategy requires confirming adequate free space. Contact VergeOS Support for guidance.
{% endhint %}

---

## Alerting and Monitoring Expectations

When an immutable flag is removed, VergeOS generates an alert. Administrators must treat this as a **high‑severity security event**.

Recommended actions:

- Investigate the user account and context  
- Verify whether the change was authorized  
- Consider pausing snapshot creation  
- Ensure alerts integrate with SIEM or centralized monitoring  

This ensures immutable‑flag removal cannot go unnoticed during an attack.

---

## Managing Immutable Snapshots

### Enable Immutable Protection (“Lock” a Snapshot)

1. Navigate to **System → System Snapshots**  
2. Double‑click the desired snapshot  
3. Toggle **Immutable** to enabled  
4. Click **Submit**  
5. Snapshot displays a lock icon  

### Automate Immutable Protection

1. Navigate to **System → Snapshot Profiles**  
2. Open the desired profile  
3. Select **Profile Periods**  
4. Edit a period and enable **Immutable**  
5. Click **Submit**  

Snapshots created under these periods will automatically be immutable.

### Disable Immutable Protection (“Unlock” a Snapshot)

1. Navigate to **System → System Snapshots**  
2. Double‑click the snapshot  
3. Toggle **Immutable** to disabled  
4. Click **Submit**  

Snapshot displays **Unlocking** and the scheduled unlock date.  
It remains undeletable until the unlock delay completes or expiration arrives.

---

## Troubleshooting

### Storage Emergency with Immutable Snapshots

**Symptom:** Storage at 90%+, cannot delete immutable snapshots.

#### Immediate Actions

- Request unlock for all immutable snapshots  
- Temporarily stop snapshot creation  
- Add physical storage capacity (only immediate solution)  
- Delete non‑immutable snapshots or VMs  

#### Prevention

Avoid emergencies by ensuring free space can comfortably accommodate natural expirations or **7 days of expected data change** for long‑retention immutable snapshots.

**Contact [VergeOS support](https://app.gitbook.com/s/uJc5d3O7cwI7qD8muSyG/support-and-services)** if you need emergency capacity planning assistance.

---
