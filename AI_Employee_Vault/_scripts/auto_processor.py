"""
Auto-Processor for AI Employee

This script automatically processes items in Needs_Action folder
using simple rule-based logic. For complex tasks, it creates
a summary and moves items to Done.

This is a stopgap solution until Qwen Code CLI is available.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('AutoProcessor')


class AutoProcessor:
    """
    Simple rule-based processor for Needs_Action items.
    
    This provides basic automatic processing without requiring
    Qwen Code to be invoked. For complex tasks, it creates
    summaries and flags for manual review.
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path).resolve()
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.logs_dir = self.vault_path / 'Logs'
        self.plans = self.vault_path / 'Plans'
        
        for dir_path in [self.needs_action, self.done, self.logs_dir, self.plans]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger('AutoProcessor')
        self.processed_files = set()
    
    def process_file(self, filepath: Path) -> bool:
        """
        Process a single file from Needs_Action.
        
        Returns True if successfully processed.
        """
        try:
            content = filepath.read_text(encoding='utf-8')
            
            # Extract metadata from frontmatter
            metadata = self._parse_frontmatter(content)
            file_type = metadata.get('type', 'unknown')
            
            self.logger.info(f'Processing {filepath.name} (type: {file_type})')
            
            # Process based on type
            if file_type == 'file_drop':
                result = self._process_file_drop(content, filepath)
            elif file_type == 'email':
                result = self._process_email(content, filepath)
            else:
                result = self._process_generic(content, filepath, metadata)
            
            if result:
                # Move to Done
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                done_filename = f'{filepath.stem}_done_{timestamp}.md'
                done_path = self.done / done_filename
                
                # Add completion note
                updated_content = content + f'\n\n---\n*Processed automatically by AutoProcessor at {datetime.now().isoformat()}*\n'
                done_path.write_text(updated_content, encoding='utf-8')
                filepath.unlink()  # Remove from Needs_Action
                
                self.logger.info(f'Moved to Done: {done_filename}')
                self._log_action('auto_processed', {
                    'file': filepath.name,
                    'type': file_type,
                    'result': 'success'
                })
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f'Error processing {filepath.name}: {e}')
            self._log_action('auto_process_error', {
                'file': filepath.name,
                'error': str(e)
            })
            return False
    
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
    
    def _process_file_drop(self, content: str, filepath: Path) -> bool:
        """Process a file drop item."""
        metadata = self._parse_frontmatter(content)
        original_name = metadata.get('original_name', 'unknown')
        
        # Create a simple summary
        summary = f'''## Auto-Processing Summary

**Original File:** {original_name}
**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Type:** File Drop

## Actions Taken

- [x] File received and logged
- [x] Content analyzed
- [ ] **Requires Review:** Please check the original file for detailed content

## Notes

This file was automatically processed. For complex analysis, please run Qwen Code manually:
```bash
cd AI_Employee_Vault
qwen "Analyze the file drop for {original_name} and extract key information"
```
'''
        
        # Insert summary after frontmatter
        lines = content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:
                insert_pos = i + 1
                break
        
        lines.insert(insert_pos, summary)
        content = '\n'.join(lines)
        
        return True
    
    def _process_email(self, content: str, filepath: Path) -> bool:
        """Process an email item."""
        metadata = self._parse_frontmatter(content)
        subject = metadata.get('subject', 'No Subject')
        from_addr = metadata.get('from', 'Unknown')
        priority = metadata.get('priority', 'normal')
        
        # Create a simple summary
        summary = f'''## Auto-Processing Summary

**From:** {from_addr}
**Subject:** {subject}
**Priority:** {priority}
**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Actions Taken

- [x] Email logged and categorized
- [x] Priority flagged: {priority}
- [ ] **Requires Review:** Please craft a response if needed

## Suggested Response Template

Dear {from_addr.split("@")[0] if "@" in from_addr else "Sender"},

Thank you for your email regarding "{subject}".

[Add your response here]

Best regards,
[Your Name]

---

*For complex email responses, run Qwen Code manually:*
```bash
qwen "Draft a professional response to this email"
```
'''
        
        # Insert summary after frontmatter
        lines = content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:
                insert_pos = i + 1
                break
        
        lines.insert(insert_pos, summary)
        content = '\n'.join(lines)
        
        return True
    
    def _process_generic(self, content: str, filepath: Path, metadata: dict) -> bool:
        """Process a generic item."""
        item_type = metadata.get('type', 'unknown')
        
        summary = f'''## Auto-Processing Summary

**Type:** {item_type}
**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Actions Taken

- [x] Item logged and categorized
- [ ] **Requires Review:** Please process manually

## Notes

This item requires manual processing. Run Qwen Code:
```bash
qwen "Process this {item_type} task according to the Company Handbook"
```
'''
        
        lines = content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:
                insert_pos = i + 1
                break
        
        lines.insert(insert_pos, summary)
        content = '\n'.join(lines)
        
        return True
    
    def _log_action(self, action_type: str, details: dict):
        """Log an action to the daily log."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs_dir / f'{today}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'auto_processor',
            'details': details
        }
        
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []
        else:
            logs = []
        
        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))
    
    def run(self, check_interval: int = 30):
        """Run the auto-processor loop."""
        self.logger.info(f'Starting Auto-Processor')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {check_interval}s')
        
        while True:
            try:
                # Check for new files
                files = list(self.needs_action.glob('*.md'))
                
                # Skip task queue files (those are for Qwen)
                files = [f for f in files if not f.name.startswith('_')]
                
                if files:
                    self.logger.info(f'Found {len(files)} file(s) to process')
                    for f in files:
                        if f not in self.processed_files:
                            self.process_file(f)
                            self.processed_files.add(f)
                else:
                    self.logger.debug('No files to process')
                
            except Exception as e:
                self.logger.error(f'Error in auto-processor loop: {e}')
            
            time.sleep(check_interval)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Employee Auto-Processor')
    parser.add_argument(
        '--vault',
        type=str,
        default='../AI_Employee_Vault',
        help='Path to Obsidian vault'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Check interval in seconds'
    )
    
    args = parser.parse_args()
    
    vault_path = Path(args.vault).resolve()
    
    if not vault_path.exists():
        logger.error(f'Vault not found: {vault_path}')
        sys.exit(1)
    
    processor = AutoProcessor(str(vault_path))
    
    try:
        processor.run(check_interval=args.interval)
    except KeyboardInterrupt:
        print('\nStopping Auto-Processor...')


if __name__ == '__main__':
    main()
