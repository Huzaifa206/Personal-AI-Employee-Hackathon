# Personal AI Employee - Bronze Tier

A local-first, agent-driven automation system that proactively manages personal and business affairs 24/7 using Qwen Code and Obsidian.

**Bronze Tier** includes:
- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script (Filesystem + Gmail)
- ✅ Qwen Code integration for reading/writing to vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ Agent Skills documentation

## Quick Start

### 1. Install Prerequisites

- **Python 3.13+**: [Download](https://www.python.org/downloads/)
- **Obsidian**: [Download](https://obsidian.md/download)
- **Qwen Code**: Follow installation instructions for your environment
- **Node.js v24+**: [Download](https://nodejs.org/)

### 2. Setup Scripts (Inside Vault)

```bash
cd AI_Employee_Vault/_scripts
pip install -r requirements.txt
```

### 3. Start the Filesystem Watcher

```bash
cd AI_Employee_Vault/_scripts
python filesystem_watcher.py
```

This creates a `Drop_Folder` in your vault. Drag any file into it to trigger AI processing.

### 4. Start the Orchestrator (Auto-Processing)

Open a **new terminal**:

```bash
cd AI_Employee_Vault/_scripts
python orchestrator.py
```

That's it! Both scripts automatically find the vault since they're inside it.

## Project Structure

```
Personal-AI-Employee-Hackathon/
└── AI_Employee_Vault/          # Obsidian vault - EVERYTHING INSIDE!
    ├── Dashboard.md            # Real-time status dashboard
    ├── Company_Handbook.md     # Rules of engagement
    ├── Business_Goals.md       # Q1 2026 objectives
    ├── _scripts/               # ALL PYTHON SCRIPTS HERE
    │   ├── orchestrator.py     # Auto-processing orchestrator
    │   ├── filesystem_watcher.py
    │   ├── gmail_watcher.py
    │   ├── base_watcher.py
    │   ├── auto_processor.py
    │   ├── requirements.txt
    │   └── README.md
    ├── Drop_Folder/            # Drop files here (auto-created)
    ├── Inbox/                  # Raw incoming items
    ├── Needs_Action/           # Items requiring processing
    ├── Plans/                  # AI-generated plans
    ├── Pending_Approval/       # Awaiting human approval
    ├── Approved/               # Approved actions
    ├── Rejected/               # Rejected actions
    ├── Done/                   # Completed tasks
    ├── Logs/                   # Audit logs
    ├── Accounting/             # Bank transactions
    └── Briefings/              # CEO briefing reports
```

## How It Works

### Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   External      │     │   Watchers       │     │   Obsidian      │
│   Sources       │────▶│   (Python)       │────▶│   Vault         │
│   (Gmail, Files)│     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   External      │     │   Qwen Code      │     │   Action Files  │
│   Actions       │◀────│   (Reasoning)    │◀────│   (Needs_Action)│
│   (Email, etc)  │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Workflow

1. **Watcher detects change** (new email, file drop, etc.)
2. **Creates action file** in `Needs_Action/` folder
3. **Qwen Code reads** the action file
4. **Qwen creates plan** in `Plans/` folder
5. **Qwen executes** tasks (requests approval if needed)
6. **Qwen moves** completed items to `Done/`
7. **Orchestrator updates** Dashboard.md

## Watcher Options

### Filesystem Watcher (Recommended for Bronze)

No API setup required. Just drag files into the drop folder.

```bash
python filesystem_watcher.py --vault ../AI_Employee_Vault
```

**Pros:**
- No credentials needed
- Works immediately
- Good for testing

**Cons:**
- Manual file creation

### Gmail Watcher

Automatically monitors Gmail for new unread messages.

```bash
# First-time setup
python gmail_watcher.py --vault ../AI_Employee_Vault --credentials ./credentials.json --once

# Run continuously
python gmail_watcher.py --vault ../AI_Employee_Vault --credentials ./credentials.json
```

**Setup Requirements:**
1. Enable Gmail API in Google Cloud Console
2. Download `credentials.json`
3. Run once to authorize (creates `token.json`)

See [watchers/README.md](watchers/README.md) for detailed setup.

## Configuration

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cd watchers
cp .env.example .env
```

Edit `.env` with your settings:

```env
VAULT_PATH=./AI_Employee_Vault
GMAIL_CREDENTIALS_PATH=./credentials.json
GMAIL_CHECK_INTERVAL=120
DRY_RUN=true
```

## Usage Examples

### Process a Dropped File

1. Drag `invoice.pdf` into `AI_Employee_Vault/Drop_Folder/`
2. Watcher creates `Needs_Action/FILE_invoice_*.md`
3. Run Qwen:
   ```bash
   qwen "Process the new file in Needs_Action. Extract key information and suggest next steps."
   ```

### Process Email

1. Gmail Watcher detects new email
2. Creates `Needs_Action/EMAIL_*.md`
3. Run Qwen:
   ```bash
   qwen "Triage the new emails in Needs_Action. Create reply drafts for high-priority items."
   ```

### Update Dashboard

```bash
qwen "Update Dashboard.md with current stats from Needs_Action, Done, and Logs folders"
```

### Generate Weekly Briefing

```bash
qwen "Read Business_Goals.md and Logs from this week. Create a Weekly Briefing in Briefings/ folder"
```

## Agent Skills

See [AGENT_SKILLS.md](AGENT_SKILLS.md) for the full list of Qwen Code agent skills.

Quick reference:
- `/needs-action` - List and read pending items
- `/plan` - Create structured task plans
- `/dashboard update` - Update status dashboard
- `/done [file]` - Move completed items
- `/approve [action]` - Request human approval
- `/log [event]` - Record activities

## Company Handbook

The [Company_Handbook.md](AI_Employee_Vault/Company_Handbook.md) defines:

- Communication rules (tone, response times)
- Financial rules (approval thresholds)
- Task priorities (critical/high/medium/low)
- Security rules (credential handling)
- Escalation rules (when to wake the human)

**Key Approval Thresholds:**

| Action | Auto-Process | Require Approval |
|--------|--------------|------------------|
| Payments | Never | Always |
| Email replies | Known contacts | New contacts |
| Subscriptions | < $50/month | > $50/month |
| File operations | Read, create | Delete, move |

## Running as a Service

### Using PM2 (Recommended)

```bash
npm install -g pm2

# Start filesystem watcher
pm2 start watchers/filesystem_watcher.py --interpreter python3 --name "fs-watcher"

# Start orchestrator
pm2 start orchestrator.py --name "orchestrator" -- --vault ./AI_Employee_Vault

# Save and setup startup
pm2 save
pm2 startup
```

### Using Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At logon
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `watchers/filesystem_watcher.py --vault AI_Employee_Vault`

## Troubleshooting

### Watcher Not Detecting Files

- Ensure watcher is running: Check terminal output
- Verify vault path is correct
- Check file permissions

### Qwen Code Not Found

- Ensure Qwen Code is properly installed in your environment
- Check your IDE/plugin settings for Qwen Code integration

### Gmail API Errors

- Check `credentials.json` exists
- Re-authorize: Delete `token.json` and run with `--once`
- Verify Gmail API is enabled in Google Cloud Console

## Next Steps (Silver Tier)

After mastering Bronze tier:

1. **Add WhatsApp Watcher** - Monitor WhatsApp messages
2. **Create MCP Server** - Enable Qwen to send emails
3. **Human-in-the-Loop** - Approval workflow for sensitive actions
4. **Scheduled Tasks** - Daily briefing at 8 AM via cron

## Security Notes

1. **Never commit credentials**: `credentials.json`, `token.json`, `.env`
2. **Use dry run mode** during development: `DRY_RUN=true`
3. **Review all actions** before approving
4. **Rotate credentials** monthly
5. **Enable audit logging** in `Logs/` folder

## Resources

- [Main Blueprint Document](Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Qwen Code Documentation](https://qwen.ai/)
- [Obsidian Help](https://help.obsidian.md)
- [Agent Skills Documentation](AGENT_SKILLS.md)

## License

MIT License - See main repository for details.

---
*AI Employee v0.1 - Bronze Tier*
