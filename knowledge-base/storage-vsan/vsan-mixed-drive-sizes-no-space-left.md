---
title: >-
  vSAN Writes Fail with "No space left on device" While the Tier Shows Free
  Space (Mixed Drive Sizes)
slug: vsan-mixed-drive-sizes-no-space-left
author: VergeOS Documentation Team
date: 2026-11-05T00:00:00.000Z
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
dateCreated: 2026-10-30T00:00:00.000Z
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

VMs stop and writes fail with "No space left on device", yet the vSAN tier reports something like 58% or 68% used. If that tier has drives of different sizes, the tier may have used up the space it can actually allocate, even though it doesn't look full. This article shows how to confirm it and how to get space back.

## Overview

{% hint style="info" %}
**Key Points**

- All drives in a tier should be the same capacity. When sizes are mixed, the tier can only use each drive up to the size of the smallest drive.
- In this situation the tier's usage figure can show much more free space than the drives can actually take.
- Check individual drive sizes and usage, not the tier percentage. Free space where you can (e.g.  expiring old snapshots, removing unnecessary files or backups, etc.), then plan matching-size drives.
{% endhint %}

## Symptoms

Writes fail across the system and VMs stop. Logs show lines like these:

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

Meanwhile, everything else looks healthy. All nodes are online, the tier is redundant, **Unavailable Drives** is zero when you check it, and the tier's usage percentage is well below 100%.

## Why It Happens

As a design rule, every drive in a vSAN tier should be the same size, on every node. This is a design requirement: [Node sizing](https://app.gitbook.com/s/Q2bN3ctQdjv01GivTI08/implementation-guide/sizing) calls for identical disk configurations across storage nodes, and [Scaling Up a vSAN](scaling-up-a-vsan.md) requires any drives added later to match. When sizes are mixed, whether at deployment or during a later scale-up, the tier can only use each drive up to the size of the smallest drive in the tier. A larger drive fills to the same point as the smaller drives and stops there. The rest of that drive is unreachable.

vSAN also spreads data evenly across the nodes in a tier (see [vSAN Architecture](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-architecture)). When the drives on one node reach their limit, writes to the tier start failing, even if other drives still have room.

In affected mixed-size tiers, the tier summary can show much more free space than the per-drive limit allows, so a tier can show 58% used while the smaller drives are close to full. Confirm it from each drive's vSAN used and max values rather than treating the tier percentage as the answer.

As a planning approximation, not a supported capacity calculation, the raw space a node can use in the tier is roughly:

```
number of drives in the tier on that node × size of the smallest drive anywhere in the tier
```

The node with the lowest result tends to set the practical limit for the tier. This is raw space. Redundant copies of your data come out of it, so the space available for your data is lower. Check the real limit against each drive's vSAN max and the tier status.

## What to Check

1. **Rule out drive failures and repairs.** Go to **Infrastructure → vSAN Tiers** and double-click the tier named in the error (the `tier <T>` value). Confirm that **Repairs** is 0, **Unavailable Drives** (labeled **Bad Drives** in some versions) is 0, and **Redundant** is checked. If all three are clean, a failed drive or an active repair isn't the cause, so keep going. These values can be briefly non-zero or unchecked while a journal walk is running. If they are, wait for the walk to finish and check again. [vSAN Tier Status (Journal Walks)](understanding-journal-walks-and-vsan-tier-status.md) explains each field.
2. **Check whether the tier has mixed drive sizes.** Go to **Nodes**, open a node, and select **Drives**. Filter the list to the affected tier using the tier column heading, and note the size of each drive. Repeat for each node in the tier. If every drive is the same size, this article doesn't apply; see [Understanding and Explaining Unexpected vSAN Growth](understanding-and-explaining-unexpected-vsan-growth.md) instead. If the sizes differ, note where one of the smallest drives and one of the largest drives are.
3. **Check usage on one of the smallest drives.** Open one of the smallest drives in the tier. In the **vSAN Status** card, the **Used** field shows how much space is in use on that drive, with a percentage bar. If this issue is the cause, the bar will be at or near 100%. A drive in that state can't accept new writes for the tier.
4. **Compare it with one of the largest drives.** Go back to the drive list, open one of the largest drives in the tier, and check its **Used** field. If the larger drive shows a noticeably lower percentage while the smaller drive is full, the diagnosis is confirmed. The tier can only use each drive up to the size of its smallest drive, so the remaining space on the larger drives can't be used.

## Resolution

### Free space now

1. **Review older, never-expiring, and heavily changed snapshots first.** A snapshot starts out identical to its source and costs more space as the data diverges, so the cost depends on how much has changed, not on age alone (see [System Snapshots](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/system-snapshots)). Review **System → System Snapshots** for snapshots set to never expire or kept longer than you need, and remove what you can. Before you delete one, make sure it isn't queued or actively syncing to a DR site. Deleting it mid-sync aborts that transfer, and the snapshot never arrives on the other side. Removing a snapshot is permanent, so confirm you don't need it as a restore point first. Immutable snapshots can't be deleted until they're unlocked and their waiting period has passed (see [Immutable Snapshots](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/backup-and-dr/immutable-snapshots)), so start with the ones you can remove now.
2. **Check other places space builds up.** [Understanding and Explaining Unexpected vSAN Growth](understanding-and-explaining-unexpected-vsan-growth.md) has a checklist of other common causes, such as files, incoming syncs, and tenants.
3. **Expect a delay.** vSAN frees deleted blocks in the background, so used space drops over time, not the moment you delete (see [vSAN Deletion Process](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-deletion-process)).

{% hint style="success" %}
**Reclaim additional space with Discard and TRIM**

Once you've freed enough space for VMs to run again, consider checking whether **Discard** is enabled on your VM drives. Without it, files deleted inside a guest don't return space to the vSAN, so the guest's usage on the tier only grows.

Enabling Discard doesn't reclaim space that's already free inside the guest. To recover that space, run a TRIM inside the running guest: `Optimize-Volume -DriveLetter <letter> -ReTrim` on Windows, or `sudo fstrim -av` on Linux. See [Virtual Drive TRIM](../virtual-machines/virtual-drive-trim.md) for details.
{% endhint %}

4. **Restart the stopped VMs once the smallest drives show headroom.** VMs that stopped on a write error don't resume on their own. Check that the smallest tier drives have dropped in usage and show adequate headroom, then power the VMs on. If you restart them before space has actually been freed, they'll stop again on their next write.

### Fix the capacity long term

- **Add capacity only in balanced, consistently sized sets.** [Scaling Up a vSAN](scaling-up-a-vsan.md) requires all drives in a tier to be alike, and a drive larger than the tier's smallest adds only as much space as that smallest drive. So adding larger drives while the small ones remain doesn't unlock the unused space on the large ones. Add drives in equal numbers across the nodes, as [vSAN Architecture](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-architecture) describes. Follow the [vSAN Scale Up SOP](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/operations/vsan-scale-up-sop) for the procedure itself.
- **To use the full size of the larger drives, replace the smaller ones.** Replace each smaller drive in the tier with one that matches the larger drives, one drive at a time. Follow [Scenario 2: Proactively Replace a Working Drive](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/operations/drive-replacement#scenario-2-proactively-replace-a-working-drive) in Replacing a Defective or End-of-life Drive, and wait until each replacement finishes repairing and shows **Online** before you start the next. The tier gains no usable capacity until every smaller drive in the tier, on every node, has been replaced.

## When to Contact Support

Contact VergeOS support, and include a system diagnostics report ([Generating System Diagnostics](../troubleshooting/generating-system-diagnostics.md)), if:

- Writes are still failing after you've freed space and the background cleanup has had time to run.
- **Repairs** or **Unavailable Drives** stays above 0, or **Redundant** stays unchecked, after the current journal walk finishes.
- You want to replace the smaller drives in a tier.

## Additional Resources

- [Scaling Up a vSAN](scaling-up-a-vsan.md)
- [vSAN Scale Up SOP](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/operations/vsan-scale-up-sop)
- [vSAN Diagnostics](https://app.gitbook.com/s/pODKGSQETqL1gSqyxIq3/storage/vsan-diagnostics)
- [vSAN Tier Status (Journal Walks)](understanding-journal-walks-and-vsan-tier-status.md)
- [Understanding and Explaining Unexpected vSAN Growth](understanding-and-explaining-unexpected-vsan-growth.md)
