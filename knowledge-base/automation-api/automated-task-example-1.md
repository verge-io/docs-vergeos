---
title: Automated Task Example - Power on/off VMs Automatically as Needed
slug: automated-task-example-1
author: VergeOS Documentation Team
date: 2025-12-10T19:25:40.109Z
semantic_keywords:
  - automated vm power on off user login logout
  - task engine schedule trigger event
  - resource conservation gpu workload automation
  - tag-based vm power management scheduling
use_cases:
  - automated_vm_power_management
  - user_login_event_trigger
  - scheduled_vm_shutdown
  - resource_conservation_automation
categories:
  - Automation
  - System Administration
editor: markdown
dateCreated: 2025-12-09-11T18:16:54.516Z
description: >-
  Configuration example of automated tasks that conserve resources by powering
  VMs on when a designated user logs in, and off on logout or at a scheduled
  time such as end of business hours.
tags:
  - automation
  - tasks
  - automated
  - schedule
---

# Automated Task Example - Power on/off VMs Automatically as Needed

## Automated Task Example

{% hint style="info" %}
**Key Points**

* The _**VergeOS Task Engine**_ allows you to automate operations, triggered by specific events or scheduled times. Using modular, reusable components (tasks, events, schedules, and webhooks) you can easily configure automation tailored to your environment.
* The following example displays the use of tags, tasks, events and schedules used together to seamlessly bring workloads online and offline as they are needed, improving resource efficiency.
{% endhint %}

#### Use Case

User JThompson relies on multiple GPU-powered virtual machines to perform 3D modeling and animation work. These VMs consume significant compute and memory resources, and leaving them running when idle is wasteful.

By configuring automation to power them on only when needed - when JThompson logs into the system, and to shut them down when the user logs out or at a scheduled time (for example, every Friday at 6pm), we can ensure that resources are available exactly when needed while avoiding unnecessary usage.

The automation consists of creating tags, defining tasks, and attaching event and schedule triggers. The steps below walk you through the full configuration:

{% hint style="info" %}
**1. Create a Tag Category and Tag**

**A tag category organizes related tags. We then create a specific tag within that category to designate the VMs to control with this automation.**

_**System > Tags > New**_

<img src="../.gitbook/assets/new-tag-category-vms-light.png" alt="Create tag category" data-size="original">

**Double-click category created above >** _**New**_

<img src="../.gitbook/assets/create-vm-tag-light.png" alt="New tag" data-size="original">

{% endhint %}

{% hint style="info" %}
**2. Assign the Tag to the VMs to Automatically Power On/Off**

**This will identify the VMs that should be controlled by the automation.**

_**Virtual Machines > List >**_ **select VMs >** _**Assign Tags**_ **> select the tag from above**

<img src="../.gitbook/assets/assign-tag-vms-light.png" alt="Assign tag to VMs" data-size="original">

The VMs will now show the assigned tag in the _**Tags**_ column.

<img src="../.gitbook/assets/vms-tags-column-light.png" alt="VMs with tag" data-size="original">

{% endhint %}

{% hint style="info" %}
**3. Create a Task to Power On VMs**

**This task defines the action of starting up the tagged virtual machines.**

_**System > Tasks Dashboard > New Task**_

<img src="../.gitbook/assets/task-poweron-jthompson-light.png" alt="Task to power on tagged VMs" data-size="original">

{% endhint %}

{% hint style="info" %}
**4. Configure an Event Trigger for User Login**

**Here we define the activity that will invoke the task (JThompson logs into the system).**

From the new task dashboard: _**Event Triggers > New**_

<img src="../.gitbook/assets/jthompson-event-login-light.png" alt="Event trigger user login" data-size="original">

{% endhint %}

{% hint style="info" %}
**5. Create a Task to Power Off the VMs**

**This defines the action of powering down the tagged virtual machines.**

_**System > Tasks Dashboard > New Task**_

<img src="../.gitbook/assets/task-poweroff-jthompson-light.png" alt="Task to power off tagged VMs" data-size="original">

{% endhint %}

{% hint style="info" %}
**6. Configure an Event Trigger for User Logout**

**This configures the task to launch when JThompson logs out.**

From the new task dashboard: 
_**Event Triggers > New**_

<img src="../.gitbook/assets/jthompson-event-logoff-light.png" alt="Event trigger user logout" data-size="original">

{% endhint %}

{% hint style="info" %}
**7. Create a Schedule for Fridays at 6:00pm**

**Creating a schedule allows us to define specific dates/times. After creating the schedule it can be applied to our task and other tasks.**

_**System > Tasks Dashboard > New Schedule**_

<img src="../.gitbook/assets/schedule-eob-friday-light.png" alt="Schedule COB" data-size="original">

{% endhint %}

{% hint style="info" %}
**8. Create a Schedule Trigger for the Power Off**

**We apply the schedule (Fridays at 6pm) to the task to automatically power off the VMs every Friday evening.**

From the dashboard of the new task:
_**Schedule Triggers > New**_

<img src="../.gitbook/assets/jthompson-schedule-poweroff-light.png" alt="Schedule trigger" data-size="original">

{% endhint %}

### Verification

* Log in as JThompson → tagged VMs should power on automatically
* Log out → VMs should power off
* At Friday 6:00pm → VMs should power off even if the user is still logged in

### Troubleshooting

* If VMs do not power on, verify the tag is assigned to each VM.
* If schedule triggers do not fire, confirm the system time zone is correct.
* If login/logout triggers fail, ensure the user account name matches exactly.

This automation ensures that the GPU‑powered VMs are only active when the designated user is logged in. When the user logs out, or at the scheduled cutoff time (Friday 6pm), the VMs are powered down to conserve resources. The pattern can be applied to other high‑resource workloads such as integration test environments, interactive machine learning, CAD rendering stations, or financial modeling clusters, or any system that benefits from running only when needed.
