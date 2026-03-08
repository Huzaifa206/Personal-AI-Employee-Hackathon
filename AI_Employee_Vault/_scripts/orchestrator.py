"""
Orchestrator for AI Employee

Master script that:
1. Monitors watcher processes
2. Automatically processes items in Needs_Action folder
3. Updates the Dashboard.md
4. Handles scheduling

Bronze Tier: Basic folder monitoring and dashboard updates
Silver Tier: Automatic processing with AutoProcessor
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Orchestrator')


class Orchestrator:
    """
    Orchestrates the AI Employee system.

    Features:
    - Monitor Needs_Action folder
    - Update Dashboard.md
    - Automatically process files with AutoProcessor
    - Log all activities
    """

    def __init__(self, vault_path: str, auto_process: bool = True):
        """
        Initialize the orchestrator.

        Args:
            vault_path: Path to the Obsidian vault
            auto_process: Whether to automatically process files (default: True)
        """
        self.vault_path = Path(vault_path).resolve()
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.logs_dir = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.auto_process = auto_process

        # Ensure directories exist
        for dir_path in [self.needs_action, self.done, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger('Orchestrator')
        self.processed_files = set()
        self.last_process_time = None
        self.process_cooldown = 60  # Seconds between processing runs
    
    def count_pending_items(self) -> int:
        """
        Count items in Needs_Action folder.
        
        Returns:
            Number of pending items
        """
        return len(list(self.needs_action.glob('*.md')))
    
    def count_completed_today(self) -> int:
        """
        Count items completed today.
        
        Returns:
            Number of completed items
        """
        today = datetime.now().strftime('%Y-%m-%d')
        return len(list(self.done.glob(f'*{today}*.md')))
    
    def get_recent_activity(self, limit: int = 5) -> list:
        """
        Get recent activity from logs.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of activity dictionaries
        """
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs_dir / f'{today}.json'
        
        if not log_file.exists():
            return []
        
        try:
            logs = json.loads(log_file.read_text())
            return logs[-limit:]
        except (json.JSONDecodeError, Exception) as e:
            self.logger.error(f'Error reading logs: {e}')
            return []
    
    def update_dashboard(self):
        """
        Update the Dashboard.md with current stats.
        """
        pending = self.count_pending_items()
        completed = self.count_completed_today()
        activity = self.get_recent_activity()
        
        # Build activity table
        activity_rows = []
        for entry in activity:
            timestamp = entry.get('timestamp', '')[:19].replace('T', ' ')
            action_type = entry.get('action_type', 'unknown')
            details = entry.get('details', {})
            summary = details.get('subject', details.get('file_name', action_type))
            activity_rows.append(f'| {timestamp} | {action_type} | {summary} |')
        
        activity_table = '\n'.join(activity_rows) if activity_rows else '| - | - | - |'
        
        # Build pending items list
        pending_items = []
        for item in self.needs_action.glob('*.md'):
            content = item.read_text()
            # Extract subject/title from frontmatter
            for line in content.split('\n')[:20]:
                if 'subject:' in line:
                    subject = line.replace('subject:', '').strip()
                    pending_items.append(f'- [ ] {subject} ({item.name})')
                    break
                elif 'original_name:' in line:
                    name = line.replace('original_name:', '').strip()
                    pending_items.append(f'- [ ] File: {name}')
                    break
        
        pending_list = '\n'.join(pending_items) if pending_items else '*No items requiring action*'
        
        # Update dashboard
        content = f'''---
last_updated: {datetime.now().isoformat()}
status: active
---

# AI Employee Dashboard

## Quick Stats

| Metric | Value |
|--------|-------|
| Pending Tasks | {pending} |
| Awaiting Approval | 0 |
| Completed Today | {completed} |
| Revenue MTD | $0 |

## Inbox Summary

*No new items*

## Needs Action

{pending_list}

## Pending Approvals

*No items awaiting approval*

## Recent Activity

| Timestamp | Action | Details |
|-----------|--------|--------|
{activity_table}

## Active Projects

| Project | Deadline | Status |
|---------|----------|--------|
| - | - | - |

## Quick Links

- [[Company_Handbook]] - Rules of engagement
- [[Business_Goals]] - Q1 2026 objectives
- /Inbox - Raw incoming items
- /Needs_Action - Items requiring processing
- /Plans - AI-generated plans
- /Pending_Approval - Awaiting human approval
- /Done - Completed tasks
- /Logs - Audit logs

---
*Generated by AI Employee v0.1 (Bronze Tier) - Powered by Qwen Code*
'''
        
        self.dashboard.write_text(content)
        self.logger.info('Dashboard updated')
    
    def log_event(self, event_type: str, details: dict):
        """
        Log an event to the daily log file.
        
        Args:
            event_type: Type of event
            details: Event details dictionary
        """
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs_dir / f'{today}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'actor': 'Orchestrator',
            'details': details
        }
        
        # Load existing logs
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except json.JSONDecodeError:
                logs = []
        else:
            logs = []
        
        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))
    
    def process_pending_files(self):
        """
        Automatically process files in Needs_Action folder.
        
        This uses simple rule-based processing to handle files automatically.
        For complex tasks, it creates summaries and flags for manual review.
        """
        if not self.auto_process:
            return
        
        # Check cooldown
        if self.last_process_time:
            time_since_last = time.time() - self.last_process_time
            if time_since_last < self.process_cooldown:
                self.logger.debug(f'Cooldown active: {time_since_last:.0f}s / {self.process_cooldown}s')
                return
        
        pending = self.count_pending_items()
        if pending == 0:
            return
        
        self.logger.info(f'Found {pending} item(s) to process automatically...')
        
        # Get all pending files (skip task queue files starting with _)
        files = [f for f in self.needs_action.glob('*.md') if not f.name.startswith('_')]
        
        processed_count = 0
        for filepath in files:
            try:
                self.logger.info(f'Processing: {filepath.name}')
                
                # Read the file
                content = filepath.read_text(encoding='utf-8')
                
                # Parse metadata
                metadata = self._parse_frontmatter(content)
                file_type = metadata.get('type', 'unknown')
                
                # Add processing summary
                summary = self._create_processing_summary(metadata, filepath.name)
                content = self._insert_summary(content, summary)
                
                # Move to Done
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                done_filename = f'{filepath.stem}_done_{timestamp}.md'
                done_path = self.done / done_filename
                done_path.write_text(content, encoding='utf-8')
                
                # Remove from Needs_Action
                filepath.unlink()
                
                self.logger.info(f'✓ Processed: {filepath.name} → {done_filename}')
                
                # Log the action
                self.log_event('auto_processed', {
                    'file': filepath.name,
                    'type': file_type,
                    'result': 'success'
                })
                
                processed_count += 1
                
            except Exception as e:
                self.logger.error(f'✗ Error processing {filepath.name}: {e}')
                self.log_event('auto_process_error', {
                    'file': filepath.name,
                    'error': str(e)
                })
        
        self.logger.info(f'Processed {processed_count} item(s)')
        self.last_process_time = time.time()
    
    def _parse_frontmatter(self, content: str) -> dict:
        """Parse YAML frontmatter from markdown."""
        metadata = {}
        lines = content.split('\n')
        in_frontmatter = False
        
        for line in lines:
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            
            if in_frontmatter and ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        return metadata
    
    def _create_processing_summary(self, metadata: dict, filename: str) -> str:
        """Create a processing summary based on file type."""
        file_type = metadata.get('type', 'unknown')
        
        if file_type == 'file_drop':
            original_name = metadata.get('original_name', 'unknown')
            return f'''
## ✓ Auto-Processed

**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Original File:** {original_name}

### Actions Taken
- [x] File received and logged
- [x] Categorized as: File Drop

### Next Steps
- [ ] Review original file content
- [ ] Extract key information if needed

> For detailed analysis, run: `qwen "Analyze {original_name} and extract key points"`
'''
        
        elif file_type == 'email':
            subject = metadata.get('subject', 'No Subject')
            from_addr = metadata.get('from', 'Unknown')
            priority = metadata.get('priority', 'normal')
            return f'''
## ✓ Auto-Processed

**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**From:** {from_addr}
**Subject:** {subject}
**Priority:** {priority}

### Actions Taken
- [x] Email logged and categorized
- [x] Priority: {priority}

### Next Steps
- [ ] Review email content
- [ ] Draft response if needed

> For response drafting, run: `qwen "Draft a professional response to this email"`
'''
        
        else:
            return f'''
## ✓ Auto-Processed

**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Type:** {file_type}

### Actions Taken
- [x] Item logged and categorized

### Next Steps
- [ ] Review and process manually

> For assistance, run: `qwen "Process this task according to the Company Handbook"`
'''
    
    def _insert_summary(self, content: str, summary: str) -> str:
        """Insert summary after frontmatter."""
        lines = content.split('\n')
        insert_pos = 0
        
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:
                insert_pos = i + 1
                break
        
        lines.insert(insert_pos, summary)
        return '\n'.join(lines)

    def check_for_qwen_processing(self):
        """
        Check if Qwen has processed any files (moved to Done).
        """
        self.logger.debug('Checking for processed files...')
    
    def run(self, check_interval: int = 30):
        """
        Run the orchestrator main loop.

        Args:
            check_interval: Seconds between checks
        """
        self.logger.info(f'Starting Orchestrator')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {check_interval}s')
        self.logger.info(f'Auto-processing: {self.auto_process}')

        # Initial dashboard update
        self.update_dashboard()

        while True:
            try:
                # Update dashboard
                self.update_dashboard()

                # Automatically process pending files
                self.process_pending_files()

                # Check for processed files
                self.check_for_qwen_processing()

                # Log heartbeat
                pending = self.count_pending_items()
                if pending > 0:
                    self.logger.info(f'{pending} item(s) awaiting processing')
                else:
                    self.logger.debug('No pending items')

            except Exception as e:
                self.logger.error(f'Error in orchestrator loop: {e}')

            time.sleep(check_interval)
    
    def stop(self):
        """
        Stop the orchestrator gracefully.
        """
        self.logger.info('Stopping Orchestrator')
        self.update_dashboard()  # Final update


def main():
    """
    Main entry point for the orchestrator.
    """
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument(
        '--vault',
        type=str,
        default='..',  # Default to parent directory (we're inside _scripts/)
        help='Path to Obsidian vault (default: parent directory)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Check interval in seconds'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (for testing)'
    )
    parser.add_argument(
        '--no-auto-process',
        action='store_true',
        help='Disable automatic processing (monitor only)'
    )

    args = parser.parse_args()

    vault_path = Path(args.vault).resolve()

    if not vault_path.exists():
        logger.error(f'Vault not found: {vault_path}')
        sys.exit(1)

    # Auto-process by default, unless --no-auto-process is specified
    auto_process = not args.no_auto_process
    
    orchestrator = Orchestrator(str(vault_path), auto_process=auto_process)

    if args.once:
        # Test run
        print('Running test check...')
        orchestrator.update_dashboard()
        pending = orchestrator.count_pending_items()
        print(f'Pending items: {pending}')
        completed = orchestrator.count_completed_today()
        print(f'Completed today: {completed}')
        
        if auto_process and pending > 0:
            print('\nProcessing pending items...')
            orchestrator.process_pending_files()
            print(f'Completed. Check Done/ folder for results.')
    else:
        # Run continuously
        try:
            orchestrator.run(check_interval=args.interval)
        except KeyboardInterrupt:
            print('\nStopping Orchestrator...')
            orchestrator.stop()


if __name__ == '__main__':
    main()
