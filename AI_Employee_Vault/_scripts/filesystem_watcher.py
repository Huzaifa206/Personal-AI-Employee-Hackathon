"""
File System Watcher

Monitors a drop folder for new files and creates action files
in the Needs_Action folder for Qwen Code to process.

This is a simpler alternative to Gmail Watcher that requires no API setup.
Users can drag files into the drop folder to trigger AI processing.
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """
    Handles file system events in the drop folder.
    """
    
    def __init__(self, watcher):
        """
        Initialize the handler.
        
        Args:
            watcher: The FilesystemWatcher instance
        """
        super().__init__()
        self.watcher = watcher
    
    def on_created(self, event):
        """
        Handle file creation events.
        
        Args:
            event: File system event
        """
        if event.is_directory:
            return
        
        self.watcher.process_new_file(event.src_path)


class FilesystemWatcher(BaseWatcher):
    """
    Watches a folder for new files and creates action files.
    """
    
    def __init__(self, vault_path: str, drop_folder: str = None, check_interval: int = 5):
        """
        Initialize the Filesystem watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            drop_folder: Path to the drop folder (default: ./drop_folder)
            check_interval: Seconds between checks (default: 5)
        """
        super().__init__(vault_path, check_interval)
        
        self.drop_folder = Path(drop_folder) if drop_folder else self.vault_path / 'Drop_Folder'
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        self.processed_files = set()
        self.observer = None
    
    def _get_file_hash(self, filepath: str) -> str:
        """
        Get MD5 hash of a file for deduplication.
        
        Args:
            filepath: Path to the file
            
        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def check_for_updates(self) -> list:
        """
        This method is not used - we use event-driven approach instead.
        
        Returns:
            Empty list
        """
        return []
    
    def process_new_file(self, src_path: str):
        """
        Process a newly created file.
        
        Args:
            src_path: Path to the new file
        """
        try:
            src_path = Path(src_path)
            
            # Skip hidden files and temp files
            if src_path.name.startswith('.') or src_path.suffix.endswith('.tmp'):
                return
            
            # Get file hash for deduplication
            file_hash = self._get_file_hash(str(src_path))
            
            if file_hash in self.processed_files:
                return
            
            self.processed_files.add(file_hash)
            self.create_action_file({
                'path': str(src_path),
                'name': src_path.name,
                'size': src_path.stat().st_size,
                'hash': file_hash
            })
            
        except Exception as e:
            self.logger.error(f'Error processing file {src_path}: {e}')
    
    def create_action_file(self, item) -> Path:
        """
        Create an action file for a dropped file.
        
        Args:
            item: Dictionary with file information
            
        Returns:
            Path to the created action file
        """
        src_path = Path(item['path'])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate filename
        safe_name = src_path.stem.replace(' ', '_')[:50]
        filename = f'FILE_{safe_name}_{timestamp}.md'
        filepath = self.needs_action / filename
        
        # Copy file to vault
        dest_path = self.vault_path / 'Attachments' / f'{timestamp}_{src_path.name}'
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(src_path, dest_path)
        except Exception as e:
            self.logger.error(f'Error copying file: {e}')
            dest_path = src_path  # Fallback to original path
        
        # Determine file type and suggested actions
        file_type = src_path.suffix.lower()
        suggested_actions = self._get_suggested_actions(file_type)
        
        # Create action file content
        content = f'''---
type: file_drop
original_path: {src_path}
original_name: {src_path.name}
file_size: {item['size']}
file_hash: {item['hash']}
received: {datetime.now().isoformat()}
priority: normal
status: pending
file_type: {file_type}
---

# File Drop: {src_path.name}

## File Information

- **Original Path**: {src_path}
- **Size**: {self._format_size(item['size'])}
- **Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Copied To**: `{dest_path}`

## Content Preview

*Add content summary or key points from this file*

## Suggested Actions

{suggested_actions}

## Notes

*Add any notes or context here*

---
*Created by Filesystem Watcher v0.1 (Bronze Tier)*
'''
        
        filepath.write_text(content)
        self.logger.info(f'Created action file: {filepath.name}')
        
        # Log the action
        self.log_action('file_dropped', {
            'original_path': str(src_path),
            'file_name': src_path.name,
            'file_size': item['size']
        })
        
        return filepath
    
    def _get_suggested_actions(self, file_type: str) -> str:
        """
        Get suggested actions based on file type.
        
        Args:
            file_type: File extension
            
        Returns:
            Markdown list of suggested actions
        """
        actions = {
            '.pdf': [
                '- [ ] Read and extract key information',
                '- [ ] Summarize content',
                '- [ ] Add to relevant project folder',
                '- [ ] Archive after processing'
            ],
            '.doc': [
                '- [ ] Read document',
                '- [ ] Extract action items',
                '- [ ] Convert to Markdown if needed',
                '- [ ] Archive after processing'
            ],
            '.docx': [
                '- [ ] Read document',
                '- [ ] Extract action items',
                '- [ ] Convert to Markdown if needed',
                '- [ ] Archive after processing'
            ],
            '.txt': [
                '- [ ] Read content',
                '- [ ] Process any instructions',
                '- [ ] Archive after processing'
            ],
            '.csv': [
                '- [ ] Analyze data',
                '- [ ] Create summary report',
                '- [ ] Import to database if needed',
                '- [ ] Archive after processing'
            ],
            '.xlsx': [
                '- [ ] Analyze spreadsheet',
                '- [ ] Create summary report',
                '- [ ] Archive after processing'
            ],
            '.jpg': [
                '- [ ] Analyze image content',
                '- [ ] Extract text if applicable (OCR)',
                '- [ ] Add description',
                '- [ ] Archive after processing'
            ],
            '.jpeg': [
                '- [ ] Analyze image content',
                '- [ ] Extract text if applicable (OCR)',
                '- [ ] Add description',
                '- [ ] Archive after processing'
            ],
            '.png': [
                '- [ ] Analyze image content',
                '- [ ] Extract text if applicable (OCR)',
                '- [ ] Add description',
                '- [ ] Archive after processing'
            ],
        }
        
        return '\n'.join(actions.get(file_type, [
            '- [ ] Review file content',
            '- [ ] Determine appropriate action',
            '- [ ] Archive after processing'
        ]))
    
    def _format_size(self, size: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size: Size in bytes
            
        Returns:
            Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f'{size:.1f} {unit}'
            size /= 1024
        return f'{size:.1f} TB'
    
    def run(self):
        """
        Start the file system watcher using watchdog.
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Watching folder: {self.drop_folder}')
        
        event_handler = DropFolderHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        self.observer.start()
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.observer.stop()
        
        self.observer.join()
    
    def stop(self):
        """
        Stop the watcher gracefully.
        """
        self.logger.info(f'Stopping {self.__class__.__name__}')
        if self.observer:
            self.observer.stop()
            self.observer.join()


def main():
    """
    Main entry point for running the Filesystem Watcher.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Filesystem Watcher for AI Employee')
    parser.add_argument(
        '--vault',
        type=str,
        default='..',  # Default to parent directory (we're inside _scripts/)
        help='Path to Obsidian vault (default: parent directory)'
    )
    parser.add_argument(
        '--drop-folder',
        type=str,
        default=None,
        help='Path to drop folder (default: vault/Drop_Folder)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (for testing)'
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    vault_path = Path(args.vault).resolve()
    drop_folder = Path(args.drop_folder).resolve() if args.drop_folder else None
    
    # Create watcher
    watcher = FilesystemWatcher(
        vault_path=str(vault_path),
        drop_folder=str(drop_folder) if drop_folder else None
    )
    
    if args.once:
        # Test run - check existing files
        print(f'Watching folder: {watcher.drop_folder}')
        print('Press Ctrl+C to stop')
        print(f'Drop files into: {watcher.drop_folder}')
    
    try:
        watcher.run()
    except KeyboardInterrupt:
        print('\nStopping Filesystem Watcher...')
        watcher.stop()


if __name__ == '__main__':
    main()
