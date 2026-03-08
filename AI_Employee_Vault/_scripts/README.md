# AI Employee Watchers

Lightweight Python scripts that monitor external sources (Gmail, filesystems) and create action files for Qwen Code to process.

## Quick Start

### 1. Install Dependencies

```bash
cd watchers
pip install -r requirements.txt
```

### 2. Choose Your Watcher

**Option A: Filesystem Watcher** (Easiest - No API setup)
- Drag files into a folder
- Watcher creates action files automatically
- No credentials needed

**Option B: Gmail Watcher** (Requires Gmail API setup)
- Monitors Gmail for new unread messages
- Creates action files for each email
- Requires Google Cloud Console setup

### 3. Run the Watcher

**Filesystem Watcher:**
```bash
python filesystem_watcher.py --vault ../AI_Employee_Vault
```

**Gmail Watcher:**
```bash
python gmail_watcher.py --vault ../AI_Employee_Vault --credentials ./credentials.json
```

## Filesystem Watcher Setup

### Basic Usage

```bash
# Start watching (runs continuously)
python filesystem_watcher.py --vault ../AI_Employee_Vault

# Run in test mode (check once and exit)
python filesystem_watcher.py --vault ../AI_Employee_Vault --once
```

### How It Works

1. Create the `Drop_Folder` in your vault (created automatically)
2. Drag any file into the folder
3. Watcher detects the new file
4. Creates an action file in `Needs_Action/` folder
5. Qwen Code can process the action file

### Custom Drop Folder

```bash
python filesystem_watcher.py \
  --vault ../AI_Employee_Vault \
  --drop-folder /path/to/your/drop/folder
```

## Gmail Watcher Setup

### Step 1: Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### Step 2: Create Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Application type: **Desktop app**
4. Download the credentials JSON file
5. Save as `credentials.json` in the `watchers/` folder

### Step 3: First-Time Authorization

```bash
# This will open a browser window for OAuth authorization
python gmail_watcher.py \
  --vault ../AI_Employee_Vault \
  --credentials ./credentials.json \
  --once
```

Follow the browser prompts to authorize. A `token.json` file will be created for future use.

### Step 4: Run Continuously

```bash
python gmail_watcher.py \
  --vault ../AI_Employee_Vault \
  --credentials ./credentials.json \
  --interval 120
```

### Customization

Edit `gmail_watcher.py` to customize:

- `PRIORITY_KEYWORDS`: Words that flag high-priority emails
- `KNOWN_CONTACTS`: Email addresses of important contacts
- `check_interval`: How often to check for new mail (default: 120s)

## Configuration

### Using Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
VAULT_PATH=./AI_Employee_Vault
GMAIL_CREDENTIALS_PATH=./credentials.json
GMAIL_CHECK_INTERVAL=120
DRY_RUN=true
```

### Command Line Arguments

All watchers support these arguments:

| Argument | Description | Default |
|----------|-------------|---------|
| `--vault` | Path to Obsidian vault | `../AI_Employee_Vault` |
| `--interval` | Check interval (seconds) | Varies by watcher |
| `--once` | Run once and exit (testing) | False |

## Output Structure

Watchers create action files in `Vault/Needs_Action/`:

```
Needs_Action/
├── EMAIL_msgId123_20260107_103000.md    # From Gmail
├── FILE_invoice_20260107_104500.md      # From filesystem
└── WHATSAPP_chatId_20260107_110000.md   # From WhatsApp (Silver tier)
```

Each action file contains:
- Frontmatter with metadata (type, priority, status)
- Original content
- Suggested action checkboxes
- Notes section

## Integration with Qwen Code

Once action files are created, use Qwen Code to process them:

```bash
cd AI_Employee_Vault

# Process all items in Needs_Action
qwen "Check the Needs_Action folder and process each item. Create plans for multi-step tasks."

# Process specific item
qwen "Read and respond to the email in Needs_Action/EMAIL_*.md"
```

## Running as a Daemon (Production)

### Using PM2 (Recommended)

```bash
# Install PM2
npm install -g pm2

# Start filesystem watcher
pm2 start filesystem_watcher.py --interpreter python3 --name "fs-watcher"

# Start gmail watcher
pm2 start gmail_watcher.py --interpreter python3 --name "gmail-watcher" -- --vault ./AI_Employee_Vault

# Save configuration
pm2 save

# Setup startup (run the generated command)
pm2 startup
```

### Using systemd (Linux)

Create `/etc/systemd/system/ai-employee-watcher.service`:

```ini
[Unit]
Description=AI Employee Watcher
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/watchers
ExecStart=/usr/bin/python3 /path/to/watchers/filesystem_watcher.py --vault /path/to/vault
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable ai-employee-watcher
sudo systemctl start ai-employee-watcher
sudo systemctl status ai-employee-watcher
```

## Troubleshooting

### Gmail Watcher Issues

**"Credentials file not found"**
- Ensure `credentials.json` is in the correct location
- Use `--credentials` flag to specify path

**"Token expired"**
- Delete `token.json` and re-authorize

**"Gmail API error 403"**
- Check Gmail API is enabled in Google Cloud Console
- Verify OAuth consent screen is configured

### Filesystem Watcher Issues

**"Folder not found"**
- The drop folder is created automatically
- Check permissions on the vault directory

**"File not being detected"**
- Ensure file creation is complete (not partial write)
- Check watcher is running: `ps aux | grep filesystem_watcher`

### General Issues

**"Module not found"**
- Run `pip install -r requirements.txt`
- Ensure you're in the `watchers/` directory

**"Permission denied"**
- Check file permissions on vault directory
- Run watcher with appropriate user

## Security Notes

1. **Never commit credentials**: Add `credentials.json` and `token.json` to `.gitignore`
2. **Use environment variables**: Store sensitive paths in `.env`
3. **Enable dry run**: During development, set `DRY_RUN=true`
4. **Review action files**: Always review before Qwen processes

## Next Steps (Silver Tier)

Once you have the Bronze tier working:

1. Add WhatsApp Watcher using Playwright
2. Create MCP server for sending emails
3. Implement human-in-the-loop approval workflow
4. Set up scheduled tasks with cron/Task Scheduler

## License

MIT License - See main repository for details.
