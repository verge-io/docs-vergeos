---
title: "Shares"
description: "How to create NFS and CIFS shares on NAS volumes in VergeOS, including host access controls, user permissions, and advanced sharing options."
semantic_keywords:
  - "create NFS and CIFS shares on NAS volumes"
  - "NAS share permissions access control configuration"
  - "SMB CIFS share setup with valid users and groups"
  - "NFS share squashing and host access settings"
use_cases:
  - create_nfs_shares
  - create_cifs_shares
  - configure_share_permissions
  - restrict_host_access
  - set_user_group_squashing
tags:
  - nas
  - shares
  - nfs
  - cifs
  - smb
  - permissions
  - access control
  - file sharing
categories:
  - NAS
---

# Shares

Shares can be created to provide NFS and/or CIFS access to a NAS volume.

{% hint style="success" %}
**Multiple shares can be created for a single volume to provide varying security or different access for separate sets of users.**


{% endhint %}

## Create an NFS Share

1. From the top menu, select **NAS** > **NFS Shares**.
2. Select **New** from the left menu.
3. Select the **Volume** to share.
4. Enter a **Name** for the new NFS share (required).
5. Enter a **Share Path** (or leave blank to share the entire volume).
6. Enter a **Description** for the share (optional).
7. The **Allow Everyone** checkbox can be selected to allow all hosts
8. Specify one or more **Allowed Hosts** to grant access only from particular machines. Hosts can be specified by IP address or FQDN; wildcards can be used to allow entire domains, example: *.companyabc.com.
9. Optionally, a **Filesystem ID** can be specified.
10. Select desired **Data Access** from the dropdown list (***Read Only*** or ***Read and Write***).
11. Select **User/Group Squashing** option
    - ***No Squashing (default)***
    - ***Squash Root***
    - ***Squash All***
    
{% hint style="info" %}
**User/Root Squashing is a security feature that denies special access rights based on UID of the user on the client machine; i.e. user ID on the client (connecting) computer does not dictate permissions on the share.**


{% endhint %}

12. Specify **Anonymous User ID** (optional). Anonymously-connected users are given permission level of ID assigned here.
13. Specify **Anonymous Group ID** (optional). Anonymously-connected users operate as if they were in group assigned here.
14. The **Asynchronous** option can be selected to improve performance. However, in the event of an unclean server restart, there is a risk of data corruption/loss when the asynchronous option is enabled.
15. Optionally, the **No ACLs** option can be selected to disable ACLs (access-control lists).
16. Click **Submit** to save the settings and create the new NFS share.

## Create a CIFS Share

1. From the top menu, select **NAS** > **CIFS Shares**.
2. Select **New** from the left menu.
3. Select the **Volume** to share.
4. Enter a **Name** for the new CIFS share (required).
5. Enter a **Share Path** to share a specific path within the volume, or leave blank to share the entire volume from the root.
6. Optionally, a **Description** can be entered for the share to record additional administrative information. 
7. Optionally, The **Comment** field can be used to record descriptive information for the share that is available to SMB clients during share enumeration and discovery.
8. Optionally, specify **Valid Users** and/or **Valid Groups** lists to limit which users and groups can connect to the share. List one user or group per line.
   {% hint style="warning" %}
   **Valid Users and Valid Groups restrict who can connect**

   If you enter a **Valid Users** or **Valid Groups** list, only the users and groups in those lists can connect to the share. Everyone else is denied, including users and groups listed in **Admin Users**. To give an admin access to a share that has a valid users or groups list, also add them to **Valid Users** or **Valid Groups**.

   Leave both lists empty to allow any authenticated user to connect, subject to file and folder permissions.
   {% endhint %}

9. Optionally, limit which client machines or networks can connect to the share. Use **one** of the following lists, not both. List one entry per line; valid entries are hostnames, IP addresses, domain names, netgroups, and subnets.
    - **Allowed Hosts** - Only the hosts in this list can connect. All others are blocked.
    - **Denied Hosts** - The hosts in this list are blocked. All others can connect.

    Host lists only control which machines can connect. Users connecting from an allowed host must still authenticate and have permission to the share.

    {% hint style="warning" %}
    **Don't combine Allowed Hosts and Denied Hosts**

    When both lists are set, a host on the Allowed Hosts list can connect even if it's also denied, and a host on neither list **can** connect. Adding a Denied Hosts list to an Allowed Hosts list therefore opens the share to every host that isn't listed. 

    {% endhint %}

10. The **Read Only** option can be selected to deny any write operations via this share.
11. The **Browseable** option can be selected to make the share visible in lists of available shares. This option is disabled by default.
12. Specify a list of **Admin Users** and/or **Admin Groups** (optional). Admin Users/Groups are treated as root/administrator when accessing files through the share.  If the share has a **Valid Users** or **Valid Groups** list, admin users must also be included in one of those lists to connect.
13. A **Force User Option / Force Group Option** can be specified to define a user or group that will be used for all file operations performed via this share (regardless of the user account used to connect).
14. Select **Enable shadow copy** to let Windows users restore earlier versions of files and folders from the **Previous Versions** tab, using the volume's mounted snapshots. This also requires **Automatically Mount Snapshots** on the volume. See [Enabling Windows Previous Versions (Shadow Copy) on NAS CIFS Shares](https://app.gitbook.com/s/QZBMFpokMv2vWTIRbFzA/storage-vsan/how-to-enable-win-previous-versions-cifs-share).
15. **Advanced Configuration Options (advanced samba share options)** can be specified to handle special-case scenarios. (Advanced use only; please consult with VergeOS Support for assistance.)
16. Click **Submit** to save the settings and create the new CIFS share.

