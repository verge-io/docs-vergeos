---
title: >-
  vSAN Writes Fail with "No space left on device" While the Tier Shows Free
  Space (Mixed Drive Sizes)
slug: vsan-mixed-drive-sizes-no-space-left
author: VergeOS Documentation Team
date: 2026-11-06T00:00:00.000Z
semantic_keywords:
  - vsan no space left on device tier not full
  - error writing block to tier no space left on device
  - out of user space on device vsan
  - vm stopped block io error nospace
  - mixed drive sizes vsan tier capacity smallest drive
  - vsan tier percentage low but writes fail
use_cases:
  - troubleshoot_vsan_out_of_space_with_free_tier_capacity
  - diagnose_mixed_drive_sizes_in_vsan_tier
  - plan_vsan_scale_up_drive_sizes
categories:
  - Troubleshooting
  - vSAN
editor: markdown
dateCreated: 2026-11-06T00:00:00.000Z
description: >-
  When a vSAN tier mixes drive sizes, the tier can only use each drive up to the size of the smallest one. Writes can fail with "No space left on device" while the tier percentage still looks healthy. Here is how to confirm it and what to do.
tags:
  - vsan
  - storage
  - tiers
  - capacity
  - drives
  - scale up
  - no space left on device
  - troubleshooting
---

# vSAN Writes Fail with "No space left on device" While the Tier Shows Free Space (Mixed Drive Sizes)

VMs stop and writes fail with "No space left on device", yet the vSAN tier reports well under 100% used. If that tier has drives of different sizes, the tier may have used up the space it can actually allocate, even though it doesn't look full.

## Overview

{% hint style="info" %}
**Key Points**

- All drives in a tier should be the same capacity. When sizes are mixed, the tier can only use each drive up to the size of the smallest drive.
- In this situation, the tier's usage figure can show much more free space than the drives can actually take.
- Check individual drive sizes and usage, not the tier percentage.
- Free space where you can (e.g., expiring old snapshots, removing unnecessary files or backups), then plan matching-size drives.
{% endhint %}

## Symptoms

Writes fail across the system and VMs stop. System logs show lines like these:

```
ybvsan: Error writing block to tier <T>: (28) No space left on device
ybvsan: OUT OF USER SPACE!! on device <N>: (28) No space left on device
ybvsan: [CACHE] writepage error ino <N>, buffering...: (28) No space left on device
appserver: {"event":"BLOCK_IO_ERROR","data":{"nospace":true,"node-name":"drive<N>","reason":"No space left on device","operation":"write","action":"stop"}}
appserver: (<node>) [Virtual Machine '<VM>'] VM drive drive<N> error during write
```

Outgoing site syncs can fail at the same time:

```
appserver: (<node>) [Site '<site>'] [Outgoing sync] (-28) An error has occurred while syncing '<snapshot>': No space left on device
```

That sync error may also reflect space pressure on the *receiving* system. If your local logs show no write errors, only sync failures, check the receiving system's capacity before you delete anything locally.

Meanwhile, everything else looks healthy. All nodes are online, the tier is redundant, **Unavailable Drives** is 0 when you check it, and the tier's usage percentage is well below 100%.

## Why It Happens

Every drive in a vSAN tier should be the same size, on every node; this is a design requirement. [Node sizing](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/sizing) calls for identical disk configurations across storage nodes, and [Scaling Up a vSAN](scaling-up-a-vsan.md) requires any drives added later to match. When sizes are mixed, whether at deployment or during a later scale-up, the tier can only use each drive up to the size of the smallest drive in the tier. A larger drive fills to the same point as the smaller drives and stops there. The rest of that drive is unreachable.

vSAN also spreads data evenly across the nodes in a tier (see [vSAN Architecture](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-architecture)). When the drives on one node reach their limit, writes to the tier start failing, even if other drives still have room.

This is also why the tier percentage looks healthy. The tier's capacity figure adds up the full physical size of every drive, including the part of the larger drives that the tier can never reach. That unreachable space counts as free, so the percentage stays low while the drives that can actually take data fill up. A tier can show well under 100% used while its smallest drives are full. To confirm, compare the **Used** values on one of the smallest drives and one of the largest, as described in [What to Check](#what-to-check), rather than relying on the tier percentage.

As a planning approximation, not a supported capacity calculation, the raw space a node can use in the tier is roughly:

```
number of drives in the tier on that node × size of the smallest drive anywhere in the tier
```

The node with the lowest result sets the practical limit for the tier. This is raw space; redundant copies of your data come out of it, so the space available for your data is lower.

{% hint style="info" %}
**Example**

A three-node tier has four 1.92 TB drives in node 1 and node 2, and four 3.84 TB drives in node 3.

- **Raw physical capacity:** (4 × 1.92) + (4 × 1.92) + (4 × 3.84) = 30.72 TB. This is the figure the tier's capacity is based on.
- **Usable raw capacity:** each node can use only 4 × 1.92 TB = 7.68 TB, so the tier can use 3 × 7.68 = 23.04 TB.

When the 1.92 TB drives are full, the tier holds about 23 TB of raw data but measures it against 30.72 TB, so it reports about 75% used. Writes are already failing, and the remaining 7.68 TB on node 3's larger drives can never be used.
{% endhint %}

## What to Check

1. **Rule out drive failures and repairs.** Go to **Infrastructure → vSAN Tiers** and double-click the tier named in the error (the `tier <T>` value). Confirm that **Repairs** is 0, **Unavailable Drives** (labeled **Bad Drives** in some versions) is 0, and **Redundant** is checked. If all three are clean, a drive failure or repair isn't what's causing the errors. Capacity is the likely cause, so keep going. These values can be briefly non-zero or unchecked while a journal walk is running. If they are, wait for the walk to finish and check again. [vSAN Tier Status (Journal Walks)](understanding-journal-walks-and-vsan-tier-status.md) explains each field.
2. **Check whether the tier has mixed drive sizes.** From the same tier dashboard, select **Drives** to list every drive in the tier across all nodes, and compare the values in the **Size** column. If every drive is the same size, this article doesn't apply; see [Understanding and Explaining Unexpected vSAN Growth](understanding-and-explaining-unexpected-vsan-growth.md) instead. If the sizes differ, note one of the smallest drives and one of the largest drives for the next two steps.
3. **Check usage on one of the smallest drives.** Open one of the smallest drives in the tier. In the **vSAN Status** card, the **Used** field shows how much space is in use on that drive, with a percentage bar. If this issue is the cause, the bar will be at or near 100%. A drive in that state can't accept new writes for the tier.
4. **Compare it with one of the largest drives.** Go back to the drive list, open one of the largest drives in the tier, and check its **Used** field. If the larger drive shows a noticeably lower percentage while the smaller drive is full, the diagnosis is confirmed. The tier can only use each drive up to the size of its smallest drive, so the remaining space on the larger drives can't be used.

## Resolution

### Free space now

1. **Review older, never-expiring, and heavily changed snapshots first.**

   {% hint style="warning" %}
   **Before you delete a snapshot**

   - Make sure it isn't queued for or actively syncing to a DR site. Deleting a snapshot mid-sync aborts the transfer, and the snapshot never arrives on the other side.
   - Make sure you don't need it as a restore point. Deleting a snapshot is permanent.
   {% endhint %}

   A snapshot starts out identical to its source and takes more space as the data diverges, so its cost depends on how much has changed, not on age alone (see [System Snapshots](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/system-snapshots)). Go to **System → System Snapshots**, look for snapshots set to never expire or kept longer than you need, and remove what you can. Immutable snapshots can't be deleted until they're unlocked and their waiting period has passed (see [Immutable Snapshots](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/immutable-snapshots)), so start with the ones you can remove now.
2. **Check other places space builds up.** [Understanding and Explaining Unexpected vSAN Growth](understanding-and-explaining-unexpected-vsan-growth.md) has a checklist of other common causes, such as files, incoming syncs, and tenants.
3. **Expect a delay.** vSAN frees deleted blocks in the background, so used space drops over time, not the moment you delete (see [vSAN Deletion Process](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-deletion-process)).
4. **Bring workloads back once there's room.** When the smallest drives in the tier have enough free space for your environment, restart the affected VMs. Depending on the application, a VM that stopped mid-write may need application-level checks, or a restore from snapshot, before it's back in service.

{% hint style="success" %}
**Reclaim additional space with Discard and TRIM**

Once you've freed enough space for VMs to run again, consider checking whether **Discard** is enabled on your VM drives. Without it, files deleted inside a guest don't return space to the vSAN, so the guest's usage on the tier only grows.

Enabling Discard doesn't reclaim space that's already free inside the guest. To recover that space, run a TRIM inside the running guest: `Optimize-Volume -DriveLetter <letter> -ReTrim` on Windows, or `sudo fstrim -av` on Linux. See [Virtual Drive TRIM](../virtual-machines/virtual-drive-trim.md) for details.
{% endhint %}

### Fix the capacity long term

- **To use the full size of the larger drives, replace the smaller ones.** Replace each smaller drive in the tier with one that matches the larger drives, one drive at a time. Follow [Scenario 2: Proactively Replace a Working Drive](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/operations/drive-replacement#scenario-2-proactively-replace-a-working-drive) in Replacing a Defective or End-of-life Drive, and wait until each replacement finishes repairing and shows **Online** before you start the next. The tier gains no usable capacity until every smaller drive in the tier, on every node, has been replaced.
- **Add capacity only in balanced, consistently sized sets.** [Scaling Up a vSAN](scaling-up-a-vsan.md) requires all drives in a tier to be alike, and a drive larger than the tier's smallest adds only as much space as that smallest drive. So adding larger drives while the small ones remain doesn't unlock the unused space on the large ones. Add drives in equal numbers across the nodes, as [vSAN Architecture](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-architecture) describes. Follow the [vSAN Scale Up SOP](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/operations/vsan-scale-up-sop) for the procedure itself.

## Prevention

- **Keep drive sizes consistent within each tier.** When you buy drives for a tier, whether at deployment or for a scale-up, match the size of the drives already in it.
- **Monitor the smallest drives in any mixed-size tier.** Until the smaller drives have been replaced, check the **Used** value on the tier's smallest drives, not the tier percentage, so you catch the problem before writes fail and VMs stop. Plan capacity from the usable figure, not the raw total (see the example in [Why It Happens](#why-it-happens)).

## When to Contact Support

Contact VergeOS support, and include a system diagnostics report ([Generating System Diagnostics](../troubleshooting/generating-system-diagnostics.md)), if:

- Writes are still failing after you've freed space and the background cleanup has had time to run.
- **Repairs** or **Unavailable Drives** stays above 0, or **Redundant** stays unchecked, after the current journal walk finishes.
- You need assistance replacing the smaller drives in a tier.

## Additional Resources

- [Scaling Up a vSAN](scaling-up-a-vsan.md)
- [vSAN Scale Up SOP](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/operations/vsan-scale-up-sop)
- [vSAN Diagnostics](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-diagnostics)
- [vSAN Tier Status (Journal Walks)](understanding-journal-walks-and-vsan-tier-status.md)
- [Understanding and Explaining Unexpected vSAN Growth](understanding-and-explaining-unexpected-vsan-growth.md)
- [Understanding vSAN Redundancy Levels](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-redundancy-levels)

---

{% hint style="info" %}
**Document Information**

- Last Updated: 2026-11-06
{% endhint %}
