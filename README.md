# Personal AI Employee Hackathon 0: Building Autonomous FTEs in 2026

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

---

## 🎯 Project Overview

This repository contains the complete blueprint and implementation for building a **"Digital FTE" (Full-Time Equivalent)** — an autonomous AI agent that proactively manages personal and business affairs 24/7. 

The **Personal AI Employee** uses:
- **Qwen Code** as the reasoning engine and executor
- **Obsidian** (local Markdown) as the knowledge base and management dashboard
- **Python Watcher scripts** to monitor Gmail, WhatsApp, filesystems, and banking APIs
- **MCP (Model Context Protocol) servers** to handle external actions

This is a **local-first, privacy-centric** architecture that keeps your data on your machine while enabling powerful automation.

---

## 💡 The Big Idea

**A Digital FTE works nearly 9,000 hours a year vs a human's 2,000.**

| Feature | Human FTE | Digital FTE |
|---------|-----------|-------------|
| Availability | 40 hours/week | 168 hours/week (24/7) |
| Monthly Cost | $4,000 – $8,000+ | $500 – $2,000 |
| Ramp-up Time | 3 – 6 Months | Instant |
| Consistency | 85–95% accuracy | 99%+ consistency |
| Scaling | Linear (hire 10 for 10x) | Exponential (instant duplication) |
| Cost per Task | ~$3.00 – $6.00 | ~$0.25 – $0.50 |

**The "Aha!" Moment:** 85–90% cost reduction—usually the threshold where a CEO approves a project without further debate.

---

## 🏗️ Architecture: Perception → Reasoning → Action

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERSONAL AI EMPLOYEE                         │
│                      SYSTEM ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SOURCES                           │
├─────────────────┬─────────────────┬─────────────────────────────┤
│     Gmail       │    WhatsApp     │     Bank APIs    │  Files   │
└────────┬────────┴────────┬────────┴─────────┬────────┴────┬─────┘
         │                 │                  │             │
         ▼                 ▼                  ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PERCEPTION LAYER (Watchers)                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │ Gmail Watcher│ │WhatsApp Watch│ │Finance Watcher│            │
│  │  (Python)    │ │ (Playwright) │ │   (Python)   │            │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘            │
└─────────┼────────────────┼────────────────┼────────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT (Local)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /Needs_Action/  │ /Plans/  │ /Done/  │ /Logs/            │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Dashboard.md    │ Company_Handbook.md │ Business_Goals.md│  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ /Pending_Approval/  │  /Approved/  │  /Rejected/         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REASONING LAYER                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                      QWEN CODE                            │ │
│  │   Read → Think → Plan → Write → Request Approval          │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────┘
                                 │
              ┌──────────────────┴───────────────────┐
              ▼                                      ▼
┌────────────────────────────┐    ┌────────────────────────────────┐
│    HUMAN-IN-THE-LOOP       │    │         ACTION LAYER           │
│  ┌──────────────────────┐  │    │  ┌─────────────────────────┐   │
│  │ Review Approval Files│  │    │  │    MCP SERVERS          │   │
│  │ Move to /Approved    │──┼───▶│  │  ┌──────┐ ┌──────────┐  │   │
│  └──────────────────────┘  │    │  │  │Email │ │ Browser  │  │   │
│                            │    │  │  │ MCP  │ │   MCP    │  │   │
└────────────────────────────┘    │  │  └──┬───┘ └────┬─────┘  │   │
                                  │  └─────┼──────────┼────────┘   │
                                  └────────┼──────────┼────────────┘
                                           │          │
                                           ▼          ▼
                                  ┌────────────────────────────────┐
                                  │     EXTERNAL ACTIONS           │
                                  │  Send Email │ Make Payment     │
                                  │  Post Social│ Update Calendar  │
                                  └────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Orchestrator.py (Master Process)             │ │
│  │   Scheduling │ Folder Watching │ Process Management       │ │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Watchdog.py (Health Monitor)                 │ │
│  │   Restart Failed Processes │ Alert on Errors              │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Personal-AI-Employee-Hackathon/
├── README.md                                   # This file
├── BRONZE_README.md                            # Bronze Tier quick start
├── AGENT_SKILLS.md                             # Qwen Code agent skills
├── QWEN.md                                     # Project context
├── Personal AI Employee Hackathon 0_...md      # Full blueprint
│
└── AI_Employee_Vault/                          # Obsidian Vault
    ├── _scripts/                               # All Python scripts
    │   ├── orchestrator.py                     # Auto-processing engine
    │   ├── filesystem_watcher.py               # Watches Drop_Folder
    │   ├── gmail_watcher.py                    # Watches Gmail
    │   ├── base_watcher.py                     # Base class
    │   ├── auto_processor.py                   # Standalone processor
    │   ├── requirements.txt                    # Dependencies
    │   ├── README.md                           # Scripts docs
    │   ├── QUICK_START.md                      # Quick reference
    │   └── NEW_STRUCTURE.md                    # Migration guide
    │
    ├── Dashboard.md                            # Real-time status
    ├── Company_Handbook.md                     # Rules of engagement
    ├── Business_Goals.md                       # Q1 2026 objectives
    ├── Drop_Folder/                            # Drop files here
    ├── Needs_Action/                           # Pending tasks
    ├── Done/                                   # Completed tasks
    ├── Pending_Approval/                       # Awaiting approval
    ├── Approved/                               # Approved actions
    ├── Rejected/                               # Rejected items
    ├── Plans/                                  # AI-generated plans
    ├── Logs/                                   # Audit logs
    ├── Accounting/                             # Financial records
    ├── Briefings/                              # CEO briefings
    ├── Inbox/                                  # Raw incoming
    └── In_Progress/                            # Currently working
```

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

| Component | Requirement | Purpose |
|-----------|-------------|---------|
| **Python** | 3.13+ | Watcher scripts & orchestration |
| **Obsidian** | v1.10.6+ | Knowledge base & dashboard |
| **Qwen Code** | Latest | Primary reasoning engine |
| **Node.js** | v24+ LTS | MCP servers & automation |
| **Git** | Latest | Version control |

### Hardware Requirements

- **Minimum:** 8GB RAM, 4-core CPU, 20GB free disk
- **Recommended:** 16GB RAM, 8-core CPU, SSD storage
- **For always-on:** Dedicated mini-PC or cloud VM (Oracle Cloud Free Tier)

### Step 1: Install Dependencies

```bash
cd AI_Employee_Vault/_scripts
pip install -r requirements.txt
```

### Step 2: Start the System

**Terminal 1 - Filesystem Watcher:**
```bash
cd AI_Employee_Vault/_scripts
python filesystem_watcher.py
```

**Terminal 2 - Orchestrator (Auto-Processing):**
```bash
cd AI_Employee_Vault/_scripts
python orchestrator.py
```

### Step 3: Test It

Drop a file:
```bash
echo "Test document" > AI_Employee_Vault/Drop_Folder/test.txt
```

Within 30-60 seconds, the system will:
1. Detect the file
2. Create an action file in `Needs_Action/`
3. Auto-process it
4. Move to `Done/` with summary
5. Update `Dashboard.md`

---

## 🎓 Hackathon Tiers

### **Bronze Tier: Foundation** (8-12 hours) ✅ COMPLETE

- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] One working Watcher script (Filesystem + Gmail)
- [x] Qwen Code integration for reading/writing to vault
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] Agent Skills documentation
- [x] Auto-processing Orchestrator

### **Silver Tier: Functional Assistant** (20-30 hours)

- [ ] Two or more Watcher scripts (Gmail + WhatsApp + LinkedIn)
- [ ] Automatically post on LinkedIn about business
- [ ] Qwen reasoning loop that creates Plan.md files
- [ ] One working MCP server for external action (sending emails)
- [ ] Human-in-the-loop approval workflow
- [ ] Basic scheduling via cron or Task Scheduler

### **Gold Tier: Autonomous Employee** (40+ hours)

- [ ] Full cross-domain integration (Personal + Business)
- [ ] Odoo Community accounting integration via MCP
- [ ] Facebook, Instagram, Twitter integration
- [ ] Multiple MCP servers
- [ ] Weekly Business Audit with CEO Briefing
- [ ] Error recovery and graceful degradation
- [ ] Ralph Wiggum loop for autonomous multi-step tasks

### **Platinum Tier: Production** (60+ hours)

- [ ] Cloud deployment (24/7 always-on)
- [ ] Work-Zone Specialization (Cloud vs Local)
- [ ] Vault sync via Git or Syncthing
- [ ] Odoo on Cloud VM with HTTPS
- [ ] A2A (Agent-to-Agent) upgrades

---

## 📖 How It Works

### The Watcher Pattern

Watchers are lightweight Python scripts that run continuously, monitoring external sources:

```python
# All Watchers follow this pattern
class BaseWatcher:
    def __init__(self, vault_path, check_interval=60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        
    def run(self):
        while True:
            items = self.check_for_updates()
            for item in items:
                self.create_action_file(item)
            time.sleep(self.check_interval)
```

### Available Watchers

| Watcher | Purpose | Complexity |
|---------|---------|------------|
| **Filesystem** | Drop folder monitoring | Easy (no API) |
| **Gmail** | Email monitoring | Medium (OAuth setup) |
| **WhatsApp** | Message monitoring | Advanced (Playwright) |
| **Finance** | Bank transaction monitoring | Advanced (API integration) |

### The Orchestrator

The Orchestrator is the master process that:
- Checks `Needs_Action/` every 30 seconds
- Auto-processes files with rule-based logic
- Moves completed items to `Done/`
- Updates `Dashboard.md`
- Logs all activities

### Human-in-the-Loop (HITL)

For sensitive actions (payments, new recipients, large amounts):

1. AI creates approval request in `/Pending_Approval/`
2. Human reviews and moves to `/Approved/` or `/Rejected/`
3. Orchestrator executes approved actions
4. Everything is logged for audit

**Approval Thresholds:**

| Action | Auto-Process | Require Approval |
|--------|--------------|------------------|
| Email replies | Known contacts | New contacts, bulk |
| Payments | Never | Always |
| Subscriptions | < $50/month | > $50/month |
| File operations | Create, read | Delete, move |

---

## 🔧 Configuration

### Environment Variables

```bash
cd AI_Employee_Vault/_scripts
cp .env.example .env
```

Edit `.env`:
```env
# Gmail Watcher
GMAIL_CREDENTIALS_PATH=./credentials.json
GMAIL_CHECK_INTERVAL=120

# Filesystem Watcher
DROP_FOLDER_PATH=./Drop_Folder

# Security
DRY_RUN=true
MAX_ACTIONS_PER_HOUR=10

# Logging
LOG_LEVEL=INFO
```

### Gmail Setup (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project, enable Gmail API
3. Create OAuth credentials (Desktop app)
4. Download `credentials.json` to `_scripts/`
5. Authorize once:
   ```bash
   python gmail_watcher.py --once
   ```
6. Run continuously:
   ```bash
   python gmail_watcher.py
   ```

---

## 📊 Example: End-to-End Invoice Flow

### Scenario
Client sends WhatsApp: "Hey, can you send me the invoice for January?"

### Step 1: Detection (WhatsApp Watcher)
```
Watcher creates: Needs_Action/WHATSAPP_client_a_2026-01-07.md
```

### Step 2: Processing (Orchestrator)
```
Auto-processes and creates: Plans/PLAN_invoice_client_a.md
```

### Step 3: Approval (Human)
```
Creates: Pending_Approval/EMAIL_invoice_client_a.md
You review and move to Approved/
```

### Step 4: Action (MCP)
```
Orchestrator executes email send via MCP
Logs to: Logs/2026-01-07.json
```

### Step 5: Completion
```
Files moved to: Done/
Dashboard.md updated
```

---

## 🔒 Security & Privacy

### Credential Management

- **NEVER** store credentials in vault or code
- Use environment variables
- Create `.env` file (in `.gitignore`)
- Rotate credentials monthly

### Audit Logging

Every action logged to `Logs/YYYY-MM-DD.json`:
```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_send",
  "actor": "orchestrator",
  "target": "client@example.com",
  "result": "success"
}
```

### Permission Boundaries

| Category | Auto | Approval Required |
|----------|------|-------------------|
| Email replies | Known contacts | New, bulk |
| Payments | < $50 recurring | All new, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move |

---

## 🛠️ Running as a Service (24/7)

### Using PM2 (Recommended)

```bash
# Install PM2
npm install -g pm2

# Start services
cd AI_Employee_Vault/_scripts
pm2 start filesystem_watcher.py --interpreter python --name "fs-watcher"
pm2 start orchestrator.py --interpreter python --name "orchestrator" -- --interval 30

# Save configuration
pm2 save
pm2 startup
```

### Check Status

```bash
pm2 status          # Running processes
pm2 logs            # View logs
pm2 stop all        # Stop services
pm2 delete all      # Remove from PM2
```

---

## 🐛 Troubleshooting

### Setup Issues

**Q: Python says "module not found"**
```bash
cd AI_Employee_Vault/_scripts
pip install -r requirements.txt --force-reinstall
```

**Q: Gmail API returns 403 Forbidden**
- Enable Gmail API in Google Cloud Console
- Check OAuth consent screen is configured

### Runtime Issues

**Q: Watcher scripts stop running overnight**
- Use PM2 for process management (see above)

**Q: Orchestrator not processing files**
- Ensure orchestrator is running in separate terminal
- Check `Needs_Action/` has `.md` files
- Run `python orchestrator.py --once` to test

**Q: Dashboard not updating**
- Orchestrator updates every 30 seconds
- Force update: `python orchestrator.py --once`

### Security Concerns

**Q: How do I know credentials are safe?**
- Never commit `.env` files
- Use environment variables
- Implement audit logging
- Rotate credentials monthly

---

## 📚 Learning Resources

### Prerequisites (2-3 hours)

| Topic | Resource | Time |
|-------|----------|------|
| Qwen Code Fundamentals | [Qwen Documentation](https://qwen.ai/) | 3 hours |
| Obsidian Basics | [Obsidian Help](https://help.obsidian.md) | 30 min |
| Python File I/O | [Real Python](https://realpython.com/read-write-files-python) | 1 hour |
| MCP Introduction | [MCP Docs](https://modelcontextprotocol.io) | 1 hour |

### Core Skills (During Hackathon)

| Topic | Resource |
|-------|----------|
| Qwen + Obsidian Integration | See AGENT_SKILLS.md |
| Building MCP Servers | [MCP Quickstart](https://modelcontextprotocol.io/quickstart) |
| Gmail API Setup | [Gmail API Docs](https://developers.google.com/gmail/api) |
| Playwright Automation | [Playwright Docs](https://playwright.dev) |

### Deep Dives (Post-Hackathon)

- MCP Server Development: [github.com/anthropics/mcp-servers](https://github.com/anthropics/mcp-servers)
- Production Automation: "Automate the Boring Stuff with Python"
- Security: OWASP API Security Top 10
- Agent Architecture: "Building LLM-Powered Applications"

---

## 📋 Submission Requirements

For hackathon submission:

- [ ] GitHub repository with all code
- [ ] README.md with setup instructions
- [ ] Demo video (5-10 minutes)
- [ ] Security disclosure
- [ ] Tier declaration (Bronze/Silver/Gold)
- [ ] Submit form: [Hackathon Submission](https://forms.gle/JR9T1SJq5rmQyGkGA)

### Judging Criteria

| Criterion | Weight |
|-----------|--------|
| Functionality | 30% |
| Innovation | 25% |
| Practicality | 20% |
| Security | 15% |
| Documentation | 10% |

---

## ⚖️ Ethics & Responsible Automation

### When AI Should NOT Act Autonomously

- **Emotional contexts:** Condolence messages, conflict resolution
- **Legal matters:** Contract signing, legal advice
- **Medical decisions:** Health-related actions
- **Financial edge cases:** Unusual transactions, new recipients
- **Irreversible actions:** Anything that cannot be undone

### Transparency Principles

1. **Disclose AI involvement** when sending emails
2. **Maintain audit trails** for all actions
3. **Allow opt-out** for contacts preferring human-only communication
4. **Regular reviews** of AI decisions

### Oversight Schedule

| Frequency | Time | Activity |
|-----------|------|----------|
| Daily | 2 min | Dashboard check |
| Weekly | 15 min | Action log review |
| Monthly | 1 hour | Comprehensive audit |
| Quarterly | 4 hours | Security review |

**Remember:** You remain accountable for all AI Employee actions.

---

## 🤝 Community & Support

### Research Meetings

- **When:** Every Wednesday at 10:00 PM PKT
- **Where:** [Zoom Meeting](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- **Recording:** [YouTube @panaversity](https://www.youtube.com/@panaversity)

### Getting Help

1. Check [Troubleshooting](#-troubleshooting) section
2. Review `BRONZE_README.md` for detailed instructions
3. Check logs in `AI_Employee_Vault/Logs/`
4. Attend Wednesday research meetings

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🙏 Acknowledgments

- **Qwen Code** - AI reasoning engine
- **Obsidian** - Knowledge base platform
- **Panaversity** - Hackathon organizers

---

## 📞 Quick Command Reference

```bash
# Setup
cd AI_Employee_Vault/_scripts
pip install -r requirements.txt

# Start Filesystem Watcher
python filesystem_watcher.py

# Start Orchestrator (Auto-Processing)
python orchestrator.py

# Test Run
python orchestrator.py --once

# Disable Auto-Process
python orchestrator.py --no-auto-process

# Gmail Watcher (with API setup)
python gmail_watcher.py

# Running 24/7 with PM2
pm2 start filesystem_watcher.py --interpreter python --name "fs-watcher"
pm2 start orchestrator.py --interpreter python --name "orchestrator" -- --interval 30
pm2 save
pm2 startup
```

---

*AI Employee v0.1 - Bronze Tier Complete*  
*Last Updated: 2026-03-09*  
*Built with Qwen Code + Obsidian + Python*
