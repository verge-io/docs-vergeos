---
title: "Identity and Access Hardening"
description: "Harden VergeOS sign-in and access: MFA, password and lockout policy, session limits, least-privilege permissions, API key controls, OIDC applications, and host access."
semantic_keywords:
  - "VergeOS identity access hardening MFA password lockout"
  - "least privilege permissions API users API keys"
  - "session timeout physical access SSH break-glass"
  - "OIDC application access restriction redirect URI"
use_cases:
  - enforce_multifactor_authentication
  - set_password_and_lockout_policy
  - limit_session_lifetime
  - scope_user_and_api_permissions
  - restrict_api_keys
  - control_host_ssh_access
tags:
  - security
  - hardening
  - mfa
  - passwords
  - permissions
  - api-keys
  - oidc
  - ssh
  - users
categories:
  - Security
---

# Identity and Access Hardening

This page covers the controls for sign-in, sessions, permissions, API keys, OIDC applications, and host access. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

Use a disposable test account for the verification steps on this page.

## IAM01: Require multifactor authentication

MFA limits what an attacker can do with a stolen password.

**Default:** The global MFA policy is off. MFA is off for each user, and the default factor is email.

{% hint style="warning" %}
Make sure a second administrator with working MFA exists before you enforce MFA. A failed enrollment without a recovery path can lock you out.
{% endhint %}

**Configure:**

1. In **System > Users**, edit each interactive administrator account.
2. Select **Two Factor Authentication**, set the type to **Authenticator**, and require setup at next login.
3. In **System > Settings > Advanced Settings**, set `two_factor_authentication` to **Required**.

The global setting applies only to new accounts. It does not turn on MFA for existing accounts. For API keys, apply IAM08 to IAM10.

Email is the default factor. Make sure each local user with MFA has a valid email address, or the user cannot sign in.

**Verify:** Sign in as a normal user from a new browser session. A login with only a password fails. Test HTTP Basic authentication and each external authentication source separately. If a Basic credential still works with only a password, turn MFA off and on again for that account and test again. Test this sequence on a disposable account first. A TOTP code that was already used must fail.

## IAM02: Limit MFA device trust

Limit how long a trusted device skips the MFA challenge.

**Default:** Trusted devices expire after 7884000 seconds (about 91 days). Email codes expire after 300 seconds. A device expiry of 0 means the device never expires.

**Configure:** In **System > Settings > Advanced Settings**, set `two_factor_authentication_uuid_expire` to a nonzero lifetime, for example 86400 seconds. Keep `two_factor_authentication_code_expire` at 300 seconds.

**Verify:** A new browser gets the challenge. A trusted browser skips the challenge before expiry and gets the challenge after it. An expired email code fails.

## IAM03: Enforce local password strength

**Default:** `password_complexity` is `length:8`.

**Configure:** In **System > Settings > Advanced Settings**, set `password_complexity` to the approved policy. For example, require 12 characters with lowercase, uppercase, a number, and a symbol.

{% hint style="warning" %}
Do not force a password reset on the only working administrator account. Keep a tested second administrator.
{% endhint %}

The policy applies only when a password is set. External authentication sources need their own policy.

**Verify:** A password that is too short or missing a required character class is rejected. A compliant password is accepted. The policy does not check existing passwords, so assess them separately.

## IAM04: Lock out repeated failed logins

**Default:** `failed_login_lockout_attempts` is 0, so lockout is off. `failed_login_lockout_minutes` is 15.

**Configure:** In **System > Settings > Advanced Settings**, set `failed_login_lockout_attempts` to a nonzero value, for example 5. Keep `failed_login_lockout_minutes` at 15 or set your recovery interval. A very low threshold lets an attacker lock out real users.

**Verify:** Reach the threshold with wrong passwords. The correct password fails during the lockout and works after the interval. Test a manual unlock separately.

## IAM05: Bound interactive session lifetime

**Default:** `token_inactivity_timeout` is 86400 seconds. `token_expiration` is 259200 seconds.

**Configure:** In **System > Settings > Advanced Settings**, set `token_inactivity_timeout` (for example, 900 seconds) and `token_expiration` (for example, 28800 seconds). Use restricted API identities for automation instead of long human sessions.

Review active sessions and their source addresses, and end suspicious sessions.

**Verify:** An idle session with no auto-refreshing pages expires after the idle limit. An active session expires at the absolute limit. An expired or ended session cannot make an authenticated request. Closing a browser tab does not end a session.

## IAM06: Remove default broad read grants and scope roles

Permissions add up across direct grants and groups.

**Default:** New Normal and API users get broad list and read grants, plus access to their own account.

**Configure:**

1. In **System > Users** or **System > Groups**, open the identity and select **Permissions**.
2. Remove cloud-wide read and other broad permissions from restricted identities.
3. Add permissions only for the object types or objects the identity needs.
4. In **Groups**, remove members who do not need administrator membership.

Use one group per role (for example, network, storage, auditors, automation). Avoid direct user grants and broad delete rights. Review Super Users separately. Scope VergeIQ access with [AI01](vergeiq.md).

**Verify:** As the restricted identity, first confirm that a permitted read succeeds. A denial proves nothing until a permitted operation works. Then confirm that lists show only permitted objects, and other reads and unauthorized changes fail. Check grants inherited from groups as well as direct grants.

## IAM07: Restrict physical and SSH administration

**Default:** **Physical Access** is off. When on, it gives full node administration, including passwordless sudo.

**Configure:** In **System > Users**, select **Physical Access** only for designated administrators. Remove unused **SSH Keys**. Restrict SSH network access with [NET01](networking.md). See also IAM13.

**Verify:** A designated administrator can connect over SSH. An ordinary user cannot. Do not replace the generated SSH configuration.

## IAM08: Use restricted API identities

Limit what a stolen automation credential can do.

**Default:** The user type is Normal. An API key has the permissions of its owner and the owner's groups.

**Configure:**

1. In **System > Users**, create a user with type **API**.
2. Grant only the permissions the integration needs. Remove the default broad reads (IAM06, [AI01](vergeiq.md)).
3. Create the API key under this user and store it in a secret manager.
4. Move integrations to the new key, then delete old administrator-owned keys.

Use one API user per integration and one key per caller. Rotate keys on a schedule, for example every 90 days.

**Verify:** With the key, required operations succeed and one forbidden operation fails. Review **Last Logged In IP** for each key.

## IAM09: Expire and revoke API keys

**Default:** **Expiration Type** is **Set Date**.

**Configure:** In **System > Users > *user* > API Keys**, set **Expiration Type** to **Set Date** and set **Expires** for each key. To revoke a key, delete it.

Expiry runs in the background, so a key can work briefly after its expiry date.

If you need immediate containment, also disable the account that owns the key. Then confirm that the access path is denied.

**Verify:** Use a previously used test key before expiry, after expiry, and after deletion. Record how long it still worked. A successful delete does not prove that its sessions have ended. Treat any access that continues after deletion as an open issue.

## IAM10: Restrict API keys by source address

**Default:** The **IP Allow List** and **IP Deny List** are empty.

**Configure:** When you create a key, add the approved CIDR range to the **IP Allow List**. Use the source address after NAT.

{% hint style="warning" %}
Do not edit the list of a key already in use. A previously used key kept working for minutes after the edit. Create a new restricted key, then delete the old key.
{% endhint %}

**Verify:** A request from an approved address succeeds and one from another address fails. A replaced key no longer authenticates.

## IAM11: Disable retired accounts

**Default:** New users are enabled.

**Configure:** In **System > Users**, edit each identity that no longer needs access and clear **Enabled**.

Before you delete an identity, remove its VergeIQ permissions and confirm that none remain. A new identity with the same identifier can inherit them.

**Verify:** Password and API key sign-in both fail for the user.

## IAM12: Restrict OIDC application access and claims

**Default:** **Restrict Access** is off. The profile, email, and groups scopes are on.

**Configure:**

1. In **System > OIDC Applications**, edit the application.
2. Set **Redirect URI** to the exact HTTPS callback URI.
3. Add the allowed users or groups.
4. Select **Restrict Access**.
5. Clear the scopes the application does not need.

Assign users and groups before you select **Restrict Access**. Leave **Map User** empty unless you want all users mapped to one shared identity. MFA, conditional access, and offboarding in an external identity provider need their own checks. Keep authorization source settings and client secrets private.

**Verify:** An assigned user signs in. An unassigned user and an unregistered redirect URI fail. Tokens contain only the approved claims and the intended audience, and their signatures validate.

## IAM13: Preserve break-glass access and bound host sessions

**Default:** Depends on node configuration.

{% hint style="danger" %}
Test a second host or console access path before you remove host access. Without it, you can lose administrative access to the nodes.
{% endhint %}

**Configure:**

1. Give each host administrator an individual account with **Physical Access** and approved **SSH Keys**.
2. In **System > Settings > Advanced Settings**, set **Shell/SSH Idle Timeout**, for example 900 to 1800 seconds.
3. Review whether SSH allows password-only sign-in. Portal MFA does not apply to SSH.

The `/vsan/.ssh_no_password` marker is not a UI setting. Confirm release support and test console recovery before you use it.

**Verify:** In a maintenance window, an approved key connects, an ordinary user is denied, an idle shell disconnects, and break-glass recovery works. `sudo sshd -T` shows the effective SSH configuration.

## Related pages

* [Two-Factor Authentication (MFA)](../auth/multifactor-auth.md)
* [Authorization Sources - Overview](../auth/auth-sources-general.md)
* [VergeOS OIDC Applications Overview](../auth/oidc-apps-overview.md)
* [Users and Groups](../system/users-groups.md)
* [Permissions](../system/permissions.md)
* [API Keys](../system/api-keys.md)
* [Advanced System Settings](../system/advanced-system-settings.md)
