# AI Employee - Quick Start

## Everything Is Inside This Folder!

All scripts are now in `AI_Employee_Vault/_scripts/` for easy management.

---

## Setup (One Time)

### 1. Install Python Dependencies

```bash
cd AI_Employee_Vault/_scripts
pip install -r requirements.txt
```

---

## Daily Use

### Terminal 1: Start Filesystem Watcher

```bash
cd AI_Employee_Vault/_scripts
python filesystem_watcher.py
```

**What it does:**
- Watches `Drop_Folder/` for new files
- Creates action files in `Needs_Action/`
- Runs continuously (keep terminal open)

---

### Terminal 2: Start Orchestrator (Auto-Processing)

```bash
cd AI_Employee_Vault/_scripts
python orchestrator.py
```

**What it does:**
- Checks `Needs_Action/` every 30 seconds
- **Automatically processes** pending files
- Moves completed to `Done/`
- Updates `Dashboard.md`
- Runs continuously (keep terminal open)

---

## Test It

### Drop a file:
```bash
echo "Test document" > AI_Employee_Vault/Drop_Folder/test.txt
```

### Watch the magic:
Within 30 seconds:
- File appears in `Needs_Action/` as `.md` file
- Orchestrator auto-processes it
- Moves to `Done/` with summary

---

## Commands Summary

| Task | Command |
|------|---------|
| Install | `pip install -r requirements.txt` |
| Watcher | `python filesystem_watcher.py` |
| Orchestrator | `python orchestrator.py` |
| Test once | `python orchestrator.py --once` |

---

## Folder Structure

```
AI_Employee_Vault/
├── _scripts/           ← You are here
│   ├── orchestrator.py
│   ├── filesystem_watcher.py
│   ├── gmail_watcher.py
│   └── requirements.txt
├── Drop_Folder/        ← Drop files here
├── Needs_Action/       ← Pending tasks
├── Done/               ← Completed tasks
├── Dashboard.md        ← Status overview
└── Logs/               ← Activity logs
```

---

## Stop Scripts

Press `Ctrl+C` in each terminal.

---

## Running 24/7

See `README.md` in this folder for PM2 setup instructions.
