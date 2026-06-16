---
description: Connect VergeOS Docs to Claude, Cursor, VS Code, and other AI tools through the hosted GitBook MCP server.
icon: plug
---

# Connect via MCP

VergeOS Docs publishes a hosted **MCP (Model Context Protocol) server**. Connect it to an AI assistant — Claude, Cursor, VS Code Copilot, Codex, and others — and that assistant can search and read this documentation directly while it helps you, instead of guessing or relying on stale training data.

{% hint style="info" %}
You need a client that supports **remote MCP servers over HTTP**. The server is public, so no API key or sign-in is required.
{% endhint %}

## The server

| | |
| --- | --- |
| **URL** | `https://docs.verge.io/~gitbook/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | None (public) |

## Add the server

{% tabs %}
{% tab title="Claude Code" %}
Run the CLI command to add it for your user account:

```bash
claude mcp add vergeos-docs --scope user --transport http https://docs.verge.io/~gitbook/mcp
```

Then confirm it connected:

```bash
claude mcp list
```
{% endtab %}

{% tab title="Claude Desktop" %}
1. Open **Settings → Connectors**.
2. Choose **Add custom connector**.
3. Name it `VergeOS Docs` and set the URL to:

   ```
   https://docs.verge.io/~gitbook/mcp
   ```
4. Save, then enable the connector in a new chat.
{% endtab %}

{% tab title="Cursor" %}
Add the server to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (per project):

```json
{
  "mcpServers": {
    "vergeos-docs": {
      "url": "https://docs.verge.io/~gitbook/mcp"
    }
  }
}
```
{% endtab %}

{% tab title="VS Code" %}
Use the one-click install link:

```
vscode:mcp/install?%7B%22name%22%3A%22VergeOS%20Docs%22%2C%22url%22%3A%22https%3A%2F%2Fdocs.verge.io%2F~gitbook%2Fmcp%22%7D
```

Or add it manually to `.vscode/mcp.json`:

```json
{
  "servers": {
    "VergeOS Docs": {
      "url": "https://docs.verge.io/~gitbook/mcp"
    }
  }
}
```
{% endtab %}

{% tab title="Codex" %}
Run the CLI command:

```bash
codex mcp add vergeos-docs --url https://docs.verge.io/~gitbook/mcp
```
{% endtab %}
{% endtabs %}

## What you get

Once connected, the assistant gains two tools:

- **`searchDocumentation`** — search across all VergeOS Docs and return matching content with direct page links.
- **`getPage`** — fetch the full Markdown of a specific documentation page.

## Try it

Ask your assistant something that should pull from the docs, for example:

{% hint style="success" %}
- "Search the VergeOS docs for how to configure a site sync."
- "Using the VergeOS docs, summarize the steps to migrate a VM from VMware."
- "What does the VergeOS documentation say about node sizing for an edge deployment?"
{% endhint %}

If the tools are available and answers cite VergeOS Docs pages, the connection is working.
