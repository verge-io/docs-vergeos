---
description: Install the VergeOS agent skills to give Claude Code and Codex task-focused workflows for troubleshooting, training, and managing VergeOS.
icon: wand-magic-sparkles
---

# VergeOS agent skills

[Connecting the docs via MCP](connect-via-mcp.md) lets an AI assistant *search and read* VergeOS Docs. The **VergeOS agent skills** go a step further: they package that same documentation access together with ready-made, task-focused workflows your assistant can run — resolving issues, explaining concepts, analyzing diagnostic bundles, managing infrastructure, and walking you through training.

Everything lives in one open-source repository, deployable as a **Claude Code plugin** or as **OpenAI Codex CLI** artifacts:

{% hint style="info" %}
**Repository:** [github.com/verge-io/agent-skills-vergeos](https://github.com/verge-io/agent-skills-vergeos)
{% endhint %}

## MCP vs. agent skills

| | [Connect via MCP](connect-via-mcp.md) | VergeOS agent skills |
| --- | --- | --- |
| What it adds | Two tools: search and fetch docs pages | Guided, multi-step workflows on top of the docs |
| Best for | Any MCP-capable assistant that just needs the docs | Claude Code and Codex users who want hands-on help |
| Setup | Add one remote server | Install the plugin (the docs MCP comes bundled) |

You don't have to choose first. The skills package **includes the docs MCP server**, so installing the skills wires up documentation access automatically.

## What's included

| Skill | Command | What it does |
| --- | --- | --- |
| Resolve | `/vergeos:resolve` | Pattern-matches common issues to known solutions |
| Explain | `/vergeos:explain` | Explains VergeOS concepts using the live docs |
| Diagnostics | `/vergeos:diag` | Analyzes diagnostic bundles with parallel subagents and PII scrubbing (Claude Code only) |
| Infrastructure | `/vergeos:vrg` | Manages VergeOS infrastructure through the `vrg` CLI |
| Training | `/vergeos:teach-me` | Delivers structured, hands-on training modules |
| Quizzes | `/vergeos:quiz-me` | Runs interactive knowledge-check quizzes |

{% hint style="info" %}
Guidance and troubleshooting in these skills target **VergeOS 26.0 and later**.
{% endhint %}

## Install

{% tabs %}
{% tab title="Claude Code" %}
Add the marketplace and install the plugin:

```bash
claude plugin marketplace add verge-io/agent-skills-vergeos
claude plugin install vergeos@verge-io
```

Or do the same interactively from inside Claude Code:

```
/plugin marketplace add verge-io/agent-skills-vergeos
/plugin install vergeos@verge-io
```

The bundled docs MCP server is wired up automatically — no API token required. Invoke a skill with its namespaced command, e.g. `/vergeos:resolve` or `/vergeos:diag /path/to/bundle`.
{% endtab %}

{% tab title="Codex CLI" %}
Clone the repository, then symlink the skills and add the docs MCP server:

```bash
ln -s "$(pwd)/.codex/skills"/* ~/.codex/skills/
codex mcp add vergeos-docs --url https://docs.verge.io/~gitbook/mcp
```

Invoke skills by name or in natural language. (The `diag` skill is Claude Code only.)
{% endtab %}
{% endtabs %}

## The `vrg` skill and the VergeOS CLI

The **Infrastructure** skill (`/vergeos:vrg`) drives the official [VergeOS CLI (`vrg`)](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/integrations-and-apis/vrg-cli) — 200+ commands across compute, networking, tenants, NAS, identity, and automation. Your assistant uses it to inspect and manage real infrastructure on your behalf, so it helps to have the CLI installed and authenticated first.

See [VergeOS CLI (vrg)](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/integrations-and-apis/vrg-cli) for installation, authentication, and the full command reference.

## Next steps

- Just want docs search in any assistant? Start with [Connect via MCP](connect-via-mcp.md).
- Want the full toolkit? Install the [agent skills](https://github.com/verge-io/agent-skills-vergeos) above.
- Going hands-on with infrastructure? Set up the [VergeOS CLI (vrg)](https://app.gitbook.com/s/sppYQkyIET58BuAo0kqm/integrations-and-apis/vrg-cli).
