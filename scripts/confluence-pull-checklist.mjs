#!/usr/bin/env node
/**
 * Reminder checklist for Confluence → git imports.
 * Actual page fetch should use Atlassian Rovo MCP in Cursor (OAuth),
 * not a token baked into this repo.
 */
console.log(`
FalconX architecture — Confluence pull checklist
================================================
1. Open this repo in Cursor with Atlassian-MCP-Server enabled
   (.cursor/mcp.json → https://mcp.atlassian.com/v1/mcp/authv2)
2. Complete OAuth if prompted
3. Ask the agent:
   - Search Confluence for "FalconX" / "architecture"
   - Fetch page by ID
   - Draft Markdown into docs/adr|catalog|flows|infra
4. Open a PR — git remains SSOT (ADR 0002)
5. Update the Confluence hub page to link here

Do not commit ATLASSIAN_API_TOKEN or page HTML dumps with secrets.
`)
