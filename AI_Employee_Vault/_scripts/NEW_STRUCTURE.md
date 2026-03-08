# AI Employee - New Unified Structure

## What Changed?

**Before:** Scripts were scattered outside the vault (`watchers/` folder, `orchestrator.py` in root).

**Now:** Everything is inside `AI_Employee_Vault/_scripts/` for centralized management!

---

## New Folder Structure

```
Personal-AI-Employee-Hackathon/
└── AI_Employee_Vault/          # Everything inside!
    ├── _scripts/               # ← NEW! All Python scripts here
    │   ├── orchestrator.py     # Auto-processing (runs every 30s)
    │   ├── filesystem_watcher.py
    │   ├── gmail_watcher.py
    │   ├── base_watcher.py
    │   ├── auto_processor.py
    │   ├── requirements.txt
    │   ├── README.md
    │   └── QUICK_START.md
    ├── Drop_Folder/            # Drop files here
    ├── Needs_Action/           # Pending tasks
    ├── Done/                   # Completed tasks
    ├── Dashboard.md            # Status overview
    └── ...                     # Other vault folders
```

---

## Benefits

1. **Single Location** - All scripts managed from one folder
2. **Portable Vault** - Copy the entire vault and everything works
3. **Simpler Paths** - Scripts auto-detect vault location
4. **Better Organization** - Code separate from content
5. **Easy Backup** - One folder contains everything

---

## Updated Commands

### Setup (First Time)

```bash
cd AI_Employee_Vault/_scripts
pip install -r requirements.txt
```

### Start Filesystem Watcher

```bash
cd AI_Employee_Vault/_scripts
python filesystem_watcher.py
```

### Start Orchestrator (Auto-Processing)

```bash
cd AI_Employee_Vault/_scripts
python orchestrator.py
```

### Test Run

```bash
cd AI_Employee_Vault/_scripts
python orchestrator.py --once
```

---

## No More Path Arguments!

**Old way (outside vault):**
```bash
python filesystem_watcher.py --vault ../AI_Employee_Vault
python orchestrator.py --vault ./AI_Employee_Vault
```

**New way (inside vault):**
```bash
python filesystem_watcher.py    # Auto-detects parent folder
python orchestrator.py          # Auto-detects parent folder
```

Scripts now default to `..` (parent directory) since they're inside `_scripts/`.

---

## Migration (If You Had Old Setup)

1. Move all files from `watchers/` to `AI_Employee_Vault/_scripts/`
2. Move `orchestrator.py` to `AI_Employee_Vault/_scripts/`
3. Run `pip install -r requirements.txt` from new location
4. Update your shortcuts/PM2 configs to point to new location

---

## Running 24/7 with PM2

```bash
cd AI_Employee_Vault/_scripts

# Start filesystem watcher
pm2 start filesystem_watcher.py --interpreter python --name "fs-watcher"

# Start orchestrator
pm2 start orchestrator.py --interpreter python --name "orchestrator" -- --interval 30

# Save configuration
pm2 save

# Setup startup
pm2 startup
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `cd AI_Employee_Vault/_scripts && pip install -r requirements.txt` |
| Start watcher | `cd AI_Employee_Vault/_scripts && python filesystem_watcher.py` |
| Start orchestrator | `cd AI_Employee_Vault/_scripts && python orchestrator.py` |
| Test once | `cd AI_Employee_Vault/_scripts && python orchestrator.py --once` |
| Disable auto-process | `python orchestrator.py --no-auto-process` |

---

## Troubleshooting

**Scripts can't find the vault?**
- Make sure you're running from `_scripts/` folder
- Or explicitly specify: `python orchestrator.py --vault ..`

**Files not being processed?**
- Check orchestrator is running: Should see log output every 30 seconds
- Check `Needs_Action/` folder has `.md` files
- Check logs in `Logs/` folder

**Dashboard not updating?**
- Orchestrator updates every 30 seconds
- Run `python orchestrator.py --once` to force update

---

## Files Inside `_scripts/`

| File | Purpose |
|------|---------|
| `orchestrator.py` | Main auto-processing script |
| `filesystem_watcher.py` | Watches Drop_Folder for new files |
| `gmail_watcher.py` | Watches Gmail for new emails |
| `base_watcher.py` | Base class for all watchers |
| `auto_processor.py` | Standalone auto-processor (alternative) |
| `requirements.txt` | Python dependencies |
| `README.md` | Detailed documentation |
| `QUICK_START.md` | Quick reference guide |

---

*Last Updated: 2026-03-09*
