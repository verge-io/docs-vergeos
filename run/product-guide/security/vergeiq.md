---
title: "VergeIQ Hardening"
description: "Harden VergeIQ: limit AI permissions separately from platform permissions, and set a finite chat history lifetime."
semantic_keywords:
  - "VergeIQ AI permissions hardening"
  - "AI chat history retention lifetime"
  - "private AI assistant access control"
use_cases:
  - scope_ai_permissions
  - set_chat_history_retention
  - remove_ai_grants_before_user_deletion
tags:
  - security
  - hardening
  - vergeiq
  - private-ai
  - permissions
  - data-retention
categories:
  - Security
---

# VergeIQ Hardening

This page covers VergeIQ permissions and chat history retention. Part of the [Security Baseline](overview.md). Track progress with the [Hardening Checklist](checklist.md).

{% hint style="info" %}
Defaults can change between releases. Confirm the current value before you change it.
{% endhint %}

## AI01: Scope AI permissions separately from platform permissions

VergeIQ permissions are separate from platform permissions. A restricted platform user can still have broad AI access.

**Default:** New users get list and read access to all AI resources.

{% hint style="warning" %}
AI grants stay after you delete a user or group. If the ID is reused, the new identity gets the old access. Remove an identity's AI grants before you delete it, then confirm that none remain.
{% endhint %}

**Configure:** Using the VergeOS API, remove broad AI grants from restricted users and groups, and grant only the assistants each needs. Platform permissions in the UI do not show AI access.

**Verify:** As a restricted user, you can open an allowed assistant but cannot open or change others. Test file, history, and inference access separately before you expose sensitive retrieval content.

## AI02: Set chat history retention

**Default:** **Chat History Lifetime** is 60 days.

**Configure:** In **AI > AI Settings**, set **Chat History Lifetime** to a finite value, for example 7 days. An assistant's **Always Off** chat history mode does not prove conversations are never stored or readable through the API.

**Verify:** A test conversation is available before the lifetime ends and gone after the lifetime and cleanup processing. Test older conversations and exported copies separately. This setting does not sanitize the storage media.

## Related pages

* [AI Configuration](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/private-ai/configuration)
* [Interactive Chat Sessions](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/private-ai/chat-sessions)
* [Private AI Overview](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/private-ai/overview)
