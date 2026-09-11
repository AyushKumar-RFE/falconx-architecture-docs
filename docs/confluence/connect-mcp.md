# Connect Confluence (Atlassian Rovo MCP)

## In this repo (Cursor)

`.cursor/mcp.json` already contains:

```json
{
  "mcpServers": {
    "Atlassian-MCP-Server": {
      "url": "https://mcp.atlassian.com/v1/mcp/authv2"
    }
  }
}
```

### Steps

1. Open this folder as a Cursor workspace (or merge the MCP entry into your user `~/.cursor/mcp.json`).
2. **Cursor Settings → MCP** — ensure `Atlassian-MCP-Server` is enabled.
3. Restart Cursor / reload MCP.
4. Complete **browser OAuth** when prompted (Atlassian Cloud site with Confluence).
5. In Agent chat, ask to list Confluence spaces or fetch a page to verify.

### Older Cursor builds

If URL MCP fails, use the `mcp-remote` bridge:

```json
{
  "mcpServers": {
    "Atlassian-Rovo-MCP": {
      "command": "npx",
      "args": ["mcp-remote@latest", "https://mcp.atlassian.com/v1/mcp/authv2"]
    }
  }
}
```

### Troubleshooting

- Tools visible in Settings but agent cannot call them: try a new Agent chat; set **Network → HTTP Compatibility Mode → http/1.1**; restart.
- Org admin may require API-token auth instead of OAuth — see Atlassian Rovo MCP docs.
- Rovo MCP usage may consume **Rovo credits** on your Atlassian plan.

Official guide: [Setting up IDEs (Atlassian Support)](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-ides/)
