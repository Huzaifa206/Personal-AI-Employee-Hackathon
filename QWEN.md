# Personal AI Employee Hackathon - Project Context

## Project Overview

This repository contains the blueprint and resources for building a **"Digital FTE" (Full-Time Equivalent)** — an autonomous AI agent that proactively manages personal and business affairs 24/7. The project is structured as a hackathon guide for creating a local-first, agent-driven automation system.

### Core Concept

The "Personal AI Employee" uses:
- **Qwen Code** as the reasoning engine and executor
- **Obsidian** (local Markdown) as the knowledge base and management dashboard
- **Python Watcher scripts** to monitor Gmail, WhatsApp, filesystems, and banking APIs
- **MCP (Model Context Protocol) servers** to handle external actions (sending emails, payments, social media posts)

### Key Architecture Layers

| Layer | Components | Purpose |
|-------|------------|---------|
| **Perception** | Gmail Watcher, WhatsApp Watcher, Finance Watcher | Monitor external inputs and create action files |
| **Reasoning** | Qwen Code | Read tasks, think, plan, and write reports |
| **Action** | MCP Servers (Email, Browser, Calendar, Slack) | Execute external actions |
| **Orchestration** | Orchestrator.py, Watchdog.py | Schedule tasks, manage processes, health monitoring |
| **Memory/GUI** | Obsidian Vault | Dashboard, Company Handbook, Business Goals, Logs |

### Human-in-the-Loop (HITL)

For sensitive actions (payments, new recipients, large amounts), the AI writes an approval request file to `/Pending_Approval/`. The human reviews and moves it to `/Approved/` to proceed, or `/Rejected/` to cancel.

### Ralph Wiggum Loop

A Stop hook pattern that keeps Qwen iterating until multi-step tasks are complete. The hook intercepts Qwen's exit and re-injects the prompt if the task file hasn't moved to `/Done/`.

## Directory Structure

```
Personal-AI-Employee-Hackathon/
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Main blueprint document
├── README.md                    # Project readme (minimal)
├── skills-lock.json             # Qwen skills configuration
├── .gitattributes               # Git text normalization
├── .qwen/
│   └── skills/
│       └── browsing-with-playwright/  # Playwright automation skill
└── QWEN.md                      # This file
```

### Expected Vault Structure (Created During Hackathon)

```
Vault/
├── Dashboard.md                 # Real-time summary
├── Company_Handbook.md          # Rules of engagement
├── Business_Goals.md            # Q1/Q2 objectives and metrics
├── Inbox/                       # Raw incoming items
├── Needs_Action/                # Items requiring processing
├── Plans/                       # Qwen-generated plans
├── Pending_Approval/            # Awaiting human approval
├── Approved/                    # Approved actions ready to execute
├── Rejected/                    # Rejected actions
├── Done/                        # Completed tasks
├── Logs/                        # Audit logs (YYYY-MM-DD.json)
├── Account ing/                 # Bank transactions, invoices
└── Briefings/                   # CEO briefing reports
```

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Qwen Code | Installed in your environment | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts & orchestration |
| Node.js | v24+ LTS | MCP servers & automation |
| GitHub Desktop | Latest | Version control |

### Hardware Requirements

- **Minimum:** 8GB RAM, 4-core CPU, 20GB free disk space
- **Recommended:** 16GB RAM, 8-core CPU, SSD storage
- **For always-on:** Dedicated mini-PC or cloud VM (Oracle Cloud Free Tier, AWS)

### Setup Checklist

1. Install all required software
2. Create Obsidian vault named `AI_Employee_Vault`
3. Verify Qwen Code is properly installed in your environment
4. Set up Python virtual environment (UV recommended)
5. Configure MCP servers if using external actions
6. Set up environment variables for credentials (never commit `.env`)

### Running Components

**Watcher Scripts** (run as daemons):
```bash
# Using PM2 for process management
npm install -g pm2
pm2 start gmail_watcher.py --interpreter python3
pm2 start whatsapp_watcher.py --interpreter python3
pm2 start filesystem_watcher.py --interpreter python3
pm2 save
pm2 startup
```

**Orchestrator** (master process):
```bash
python orchestrator.py
```

**Ralph Wiggum Loop** (for autonomous task completion):
```bash
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

**Scheduled Tasks** (cron/Task Scheduler):
```bash
# Daily CEO Briefing at 8:00 AM
0 8 * * * qwen "Generate Monday Morning CEO Briefing"
```

## Development Conventions

### Security Practices

1. **Never store credentials in plain text** — use environment variables or secrets manager
2. **Implement dry-run mode** for all action scripts during development
3. **Use separate sandbox accounts** for Gmail, banking during development
4. **Implement rate limiting** (e.g., max 10 emails/hour, max 3 payments/hour)
5. **Audit logging required** for every action (see `/Vault/Logs/`)

### Approval Thresholds

| Action | Auto-Approve | Require Approval |
|--------|--------------|------------------|
| Email replies | Known contacts | New contacts, bulk sends |
| Payments | < $50 recurring | All new payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move outside vault |

### Error Handling

- **Transient errors:** Exponential backoff retry (max 3 attempts)
- **Authentication errors:** Alert human, pause operations
- **Logic errors:** Route to human review queue
- **Data errors:** Quarantine file + alert
- **System errors:** Watchdog auto-restarts failed processes

### File Naming Conventions

- Action files: `{TYPE}_{source}_{timestamp}.md` (e.g., `EMAIL_client_a_2026-01-07.md`)
- Plan files: `PLAN_{task}_{timestamp}.md`
- Approval files: `APPROVAL_{action}_{description}.md`
- Logs: `YYYY-MM-DD.json`
- Briefings: `YYYY-MM-DD_Day_Briefing.md`

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12 hours | Obsidian dashboard, one Watcher, basic folder structure |
| **Silver** | 20-30 hours | Multiple Watchers, MCP server, HITL workflow, scheduling |
| **Gold** | 40+ hours | Full integration, Odoo MCP, weekly audit, Ralph Wiggum loop |
| **Platinum** | 60+ hours | Cloud deployment, domain specialization, A2A upgrades |

## Key Resources

- **Main Blueprint:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Qwen Code Documentation:** https://qwen.ai/
- **MCP Documentation:** https://modelcontextprotocol.io
- **Obsidian Help:** https://help.obsidian.md
- **Playwright Docs:** https://playwright.dev
- **Odoo 19 API:** https://www.odoo.com/documentation/19.0/developer/reference/external_api.html

## Learning Path

### Prerequisites (2-3 hours)
1. Qwen Code Fundamentals
2. Obsidian Basics
3. Python File I/O
4. MCP Introduction
5. Agent Skills Overview

### Core Skills (During Hackathon)
1. Qwen + Obsidian Integration
2. Building MCP Servers
3. Gmail/WhatsApp API Setup
4. Playwright Automation
5. Process Management (PM2/supervisord)

### Advanced Topics (Post-Hackathon)
1. Production MCP Server Development
2. OWASP API Security
3. Agent Architecture Patterns
4. Cloud Deployment & Monitoring

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Qwen Code not found | Check your IDE/plugin settings for Qwen Code integration |
| Watcher scripts stop overnight | Use PM2 or supervisord for process management |
| Gmail API 403 Forbidden | Enable Gmail API in Google Cloud Console |
| MCP server won't connect | Check server is running, verify absolute paths in `mcp.json` |
| Qwen making incorrect decisions | Review Company_Handbook.md, add more specific rules |

## Ethics & Responsibility

- **Disclose AI involvement** when sending emails on your behalf
- **Maintain audit trails** for all actions
- **Regular reviews:** Daily (2 min), Weekly (15 min), Monthly (1 hour)
- **Never automate:** Emotional contexts, legal matters, medical decisions, irreversible actions
- **You remain accountable** for all AI Employee actions
