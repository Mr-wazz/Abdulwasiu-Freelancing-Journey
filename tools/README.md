# Installed tools (business plugins)

| Tool | Where | How to use |
|---|---|---|
| Google Maps Scraper | `tools/google-maps-scraper-kit/` + skill and `/scrape` commands | Say "find dentists in Lagos with no website". First run: `/scrape-setup`. Run it from inside the kit folder (`cd tools/google-maps-scraper-kit`). Needs Python 3.9+ and Chrome on the machine. |
| Agency Agents (82 business agents) | `.claude/agents/` | Marketing, sales, paid media, design, product, project management, strategy, support. Say "use the Sales Proposal Strategist agent...". Engineering and specialized divisions NOT installed (keeps Claude fast). Add later from github.com/msitarzewski/agency-agents. |
| LinkedIn Skills (12 skills) | plugin `linkedin-skills@linkedin-skills` | Ask for LinkedIn posts, comment drafts, hooks, profile rewrite. |
| OpenSEO | plugin `openseo@openseo` | Keyword research, competitors, backlinks, site audits. Needs a DataForSEO API key or the OpenSEO hosted account ($10/month). Setup: https://openseo.so/docs/skills/setup |

Plugins load when Claude Code starts and trusts this folder. If they do not show up, run `/plugin` and install them from the Discover tab.
Source repos are in your message history. Never paste API keys into files.
