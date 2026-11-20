---
title: "NAS Hardening"
description: "Harden VergeOS NAS services: volume encryption, SMB protocol and signing, guest and share access, NFS squashing, antivirus, volume syncs, and remote mounts."
semantic_keywords:
  - "VergeOS NAS SMB NFS hardening"
  - "NAS volume encryption antivirus quarantine"
  - "CIFS share guest access minimum protocol"
  - "NFS root squash allowed hosts"
  - "volume sync ACL preservation"
use_cases:
  - encrypt_nas_volumes
  - restrict_smb_share_access
  - restrict_nfs_exports
  - enable_nas_antivirus
  - secure_volume_syncs
  - review_remote_nas_mounts
tags:
  - security
  - hardening
  - nas
  - smb
  - cifs
  - nfs
  - encryption
  - antivirus
categories:
  - Security
---

# NAS Hardening

This page covers hardening controls for NAS volumes, CIFS (SMB) and NFS shares, volume syncs, and remote volumes. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

Do the access tests on this page against a disposable volume or share and a test account.

## NAS01: Encrypt NAS volumes at creation

Volume encryption protects NAS data with its own key, independent of vSAN.

**Default:** Volumes are not encrypted. You can select encryption only at creation.

{% hint style="danger" %}
You must enter the key each time the volume comes online, for example after a NAS service reboot. Without the key, the volume cannot come online.
{% endhint %}

**Configure:** In **NAS > Volumes > New**, select **Encrypt Volume** and enter an **Encryption Key**. Store the key apart from the system. To encrypt an existing volume, move its data to a new encrypted volume.

**Verify:** Disable the disposable encrypted volume, then enable it. The volume comes online only after you enter the key. Test recovery of the encrypted volume.

Do not restart a NAS service for this test unless it is a dedicated test service. A restart interrupts every volume on the service, and each encrypted volume stays offline until someone enters its key.

## NAS02: Set an explicit minimum SMB protocol

**Default:** **Minimum Protocol Version** is **- None -**, which uses the Samba default. This does not mean SMB1 is on.

**Configure:** In **NAS > NAS Services**, edit the service **CIFS Settings** and set **Minimum Protocol Version** to **SMB2** or higher. Use **SMB3** or **SMB3_11** if all clients support it or you require encryption.

**Verify:** First confirm that a connection at your minimum dialect succeeds with the test credentials and share. Then force an older dialect. Set both client limits, or the client can refuse the dialect before the server does:

```bash
smbclient --option='client min protocol=NT1' -m NT1 //<nas>/<share> -U <user>
```

The server rejects the negotiation. If your minimum is SMB3, also confirm that an SMB2 connection fails (`--option='client min protocol=SMB2' -m SMB2`). Check the negotiated dialect, not only the saved setting.

## NAS03: Prevent unintended anonymous SMB access

**Default:** **Guest User Mapping** is **Invalid Users treated as a guest**: an unknown user name becomes a guest session.

**Configure:**

1. In the service **CIFS Settings**, set **Guest User Mapping** to **Invalid passwords rejected**.
2. In each protected share, turn off guest access.
3. Do not use broad **Force User** or admin mappings.

**Verify:** An anonymous connection and an unknown user name both fail. An authorized user succeeds.

## NAS04: Restrict SMB users, clients, and write access

**Default:** Share access lists are empty. **Extended ACL Support** is on.

**Configure:** In **NAS > Volumes**, open the volume, select **CIFS Shares**, and edit the share. Set **Valid Users** and **Allowed Hosts** to authorized entries only, select **Read Only** unless users must write, and keep **Admin Users** empty. Keep **Extended ACL Support** on in the service. **Enable shadow copy** turns off NT ACL handling for the share. See also [NAS09](#nas09-limit-share-paths-identity-forcing-and-protocol-side-effects).

**Verify:** Test allowed and denied users from allowed and denied hosts. A write as a read-only user fails. Existing file ACLs still apply.

## NAS05: Require SMB integrity and confidentiality where exposed

Use signing to prevent tampering, and SMB3 encryption on untrusted networks.

**Default:** No signing or encryption directive is set.

{% hint style="warning" %}
**Advanced Configuration Options** holds all directives as one block. Add these lines to the existing content; do not replace it.
{% endhint %}

**Configure:** In the service **CIFS Settings**, add to **Advanced Configuration Options**:

```
server signing = mandatory
smb encrypt = required
```

Add `smb encrypt` only if all clients support SMB3 encryption. Use the service setting: the share-level **Advanced Configuration Options** field is ignored.

**Verify:** Test the policy you selected:

- **Signing required:** `smbclient --client-protection=off` fails, and `--client-protection=sign` succeeds.
- **Encryption required:** `smbclient --client-protection=sign` fails, and `--client-protection=encrypt` succeeds. Confirm that the session is encrypted, on the client or in the NAS session list.

## NAS06: Restrict NFS clients and root authority

**Default:** New shares use **Squash Root** and **Read Only**. The NFS service defaults to **Squash Root** and **Read and Write**.

**Configure:** In the volume's **NFS Shares**, edit the share. Enter specific **Allowed Hosts** (not **Allow Everyone**), set **User/Group Squashing** to **Squash Root** or **Squash All**, set **Data Access** to **Read Only** unless clients must write, and turn off **Insecure** and **No ACLs**. NFS host checks are not user authentication; protect the transport separately if needed.

If **Enable NFSv4** is on, the service also exports `/mnt`, which contains every volume. That export uses the service's **Allowed Hosts**, **Data Access**, and **Allow Everyone** settings, not the share settings. Harden the service settings too.

**Verify:** A mount from a host that is not allowed fails, including an NFSv4 mount of `/mnt`. Files that client root creates show the anonymous owner. A write to a read-only export fails.

## NAS07: Enable NAS antivirus and quarantine handling

**Default:** Antivirus and on-access scanning are off. **Infected File Action** is **Move file to quarantine**.

**Configure:** In the volume **Antivirus** settings, turn on antivirus, keep **Infected File Action** at **Move file to quarantine**, and schedule scans. Fix any failed on-access check before you rely on on-access scanning.

**Verify:** Put an EICAR test file and a clean file on a test share and run a manual scan. Signatures are current. The EICAR file moves to quarantine; the clean file is unchanged. Turning on antivirus does not restrict access to the quarantine folder. Test each enabled CIFS and NFS share, and confirm that none gives users access to it.

## NAS08: Preserve access controls during NAS synchronization

**Default:** Volume syncs preserve ACLs, permissions, owners, and groups.

**Configure:** In **NAS > Volume Syncs**, keep these preservation options on when the destination supports them. Restrict access to the destination separately. See also [NAS10](#nas10-preserve-copy-semantics-without-mirroring-destructive-changes).

**Verify:** Owners, groups, and ACLs match on sample files. An authorized and an unauthorized test user each have the same access at both ends. A successful copy does not prove equal access.

## NAS09: Limit share paths, identity forcing, and protocol side effects

**Default:** Set for each share.

**Configure:**

* **All shares:** Share a dedicated subdirectory. Keep writable intake shares apart from read-only recovery data.
* **NFS:** Use **Squash All** only for a deliberate unprivileged mapping, and review the anonymous UID/GID (for example, 65534). Use a stable, unique fsid. Keep async and insecure off, and keep ACLs on. NFS has no write-only mode. A client IP address or UID does not prove the identity of a user.
* **SMB:** Keep **Admin Users** and **Force User/Group** empty unless justified, and never force a privileged identity. **Browseable** off only hides a share. Turn on **Enable shadow copy** only on purpose. It exposes snapshot history and turns off NT ACL handling for the share. Keep **Advanced Configuration Options** empty unless reviewed.

Do not assume that an empty access list is safe. Do not assume that a host that matches neither the allow list nor the deny list is denied. Test both cases.

{% hint style="warning" %}
Before you change a mount, confirm a tested recovery path and no pending drive operations.
{% endhint %}

**Verify:** Allowed hosts and users can connect, and denied hosts and users cannot. Users cannot leave the shared subdirectory. Root and anonymous users map as intended. A read-only share rejects writes, and ACLs and ownership stay intact. The share is online with no warnings.

## NAS10: Preserve copy semantics without mirroring destructive changes

A volume sync is a copy, not a backup. It copies encrypted or damaged files too, so also keep immutable remote recovery points.

**Default:** Depends on the sync settings.

**Configure:** In **NAS > Volume Syncs**, edit the sync:

1. Use narrow start directories and a schedule that does not overlap.
2. For a recovery copy, keep **Destination Delete** at **Never delete**, the default.
3. Preserve ACLs, xattrs, permissions, owners, and timestamps. Do not preserve device files without a reason.
4. Set **Max Errors** low so a partial copy shows as a failure. The default is 1000. The sync stops when the error count exceeds this value, and with several workers it can exceed it before stopping.
5. Run the sync as a least-privileged identity.

**Verify:** Sync a test tree. ACLs, xattrs, owners, and symlinks copy correctly, source deletions stay at the destination, and errors show in the sync logs. An unprivileged account cannot widen the destination.

## NAS11: Review remote mount protocols and external storage trust

Treat a remote file server as a separate trust domain.

**Configure:** For remote CIFS, set **SMB Protocol Version** to **3.0**; the default is 2.0. Never use 1.0. Add the signing and encryption you require to **Mount Options**, for example `seal` for SMB3 encryption. For remote NFS, use NFSv4 where possible; it does not add encryption or strong user identity by itself. Use narrow remote exports, dedicated credentials, and limited network access. Protect the encryption and backup policy on the remote server. A read-only volume and a read-only share are separate settings.

**Verify:** On the remote server, confirm the negotiated protocol and security mode. Allowed credentials and clients connect, and denied ones fail. Restores work. No broad remote export or legacy protocol fallback is in use.

## Related pages

* [NAS Overview](../nas/overview.md)
* [Add a NAS Service](../nas/nas-service.md)
* [Local Volumes](../nas/nas-local-volumes.md)
* [Remote Volumes](../nas/nas-remote-volumes.md)
* [Shares](../nas/nas-shares.md)
* [Volume Syncs](../nas/volume-syncs.md)
* [NAS Volume Snapshots and Restores](../nas/volume-snapshots-restores.md)
