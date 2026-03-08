"""
Gmail Watcher

Monitors Gmail for new unread messages and creates action files
in the Needs_Action folder for Qwen Code to process.

Setup Requirements:
1. Enable Gmail API in Google Cloud Console
2. Download credentials.json
3. Run once interactively to authorize
4. Store token.json securely (never commit)
"""

import os
import base64
from pathlib import Path
from datetime import datetime
from email import message_from_bytes

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from base_watcher import BaseWatcher

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Keywords that indicate high priority
PRIORITY_KEYWORDS = [
    'urgent', 'asap', 'invoice', 'payment', 'help', 'emergency',
    'deadline', 'important', 'action required', 'review needed'
]

# Known contacts (add your important contacts here)
KNOWN_CONTACTS = [
    # Add email addresses like: 'client@example.com',
]


class GmailWatcher(BaseWatcher):
    """
    Watches Gmail for new unread messages and creates action files.
    """
    
    def __init__(self, vault_path: str, credentials_path: str = None, check_interval: int = 120):
        """
        Initialize the Gmail watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            credentials_path: Path to Gmail credentials.json (default: ./credentials.json)
            check_interval: Seconds between checks (default: 120)
        """
        super().__init__(vault_path, check_interval)
        self.credentials_path = credentials_path or Path(__file__).parent / 'credentials.json'
        self.token_path = Path(__file__).parent / 'token.json'
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """
        Authenticate with Gmail API using OAuth2.
        """
        creds = None
        
        # Load existing token
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(
                self.token_path, SCOPES
            )
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not Path(self.credentials_path).exists():
                    self.logger.error(
                        f'Credentials file not found: {self.credentials_path}\n'
                        'Please download credentials.json from Google Cloud Console'
                    )
                    raise FileNotFoundError(f'Credentials not found: {self.credentials_path}')
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save token for future use
            self.token_path.write_text(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info('Successfully authenticated with Gmail API')
    
    def check_for_updates(self) -> list:
        """
        Check Gmail for new unread messages.
        
        Returns:
            List of message dictionaries
        """
        try:
            # Search for unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            new_messages = []
            
            for msg in messages:
                if msg['id'] not in self.processed_ids:
                    new_messages.append(msg['id'])
                    self.processed_ids.add(msg['id'])
            
            return new_messages
            
        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            return []
    
    def _get_message_details(self, message_id: str) -> dict:
        """
        Get full message details.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dictionary with message details
        """
        message = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        
        # Extract headers
        headers = message['payload'].get('headers', [])
        header_dict = {}
        for h in headers:
            header_dict[h['name']] = h['value']
        
        # Get body
        body = ''
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        break
        elif 'body' in message['payload']:
            if 'data' in message['payload']['body']:
                body = base64.urlsafe_b64decode(
                    message['payload']['body']['data']
                ).decode('utf-8')
        
        return {
            'id': message_id,
            'from': header_dict.get('From', 'Unknown'),
            'to': header_dict.get('To', ''),
            'subject': header_dict.get('Subject', 'No Subject'),
            'date': header_dict.get('Date', ''),
            'body': body,
            'snippet': message.get('snippet', '')
        }
    
    def _is_priority(self, message: dict) -> bool:
        """
        Check if message should be flagged as priority.
        
        Args:
            message: Message dictionary
            
        Returns:
            True if priority
        """
        # Check subject and body for priority keywords
        text = f"{message['subject']} {message['body']}".lower()
        if any(keyword in text for keyword in PRIORITY_KEYWORDS):
            return True
        
        # Check if from known contact
        if any(contact in message['from'] for contact in KNOWN_CONTACTS):
            return True
        
        return False
    
    def create_action_file(self, message_id: str) -> Path:
        """
        Create an action file for a Gmail message.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Path to the created action file
        """
        # Get message details
        message = self._get_message_details(message_id)
        
        # Determine priority
        priority = 'high' if self._is_priority(message) else 'normal'
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'EMAIL_{message_id}_{timestamp}.md'
        filepath = self.needs_action / filename
        
        # Create action file content
        content = f'''---
type: email
message_id: {message_id}
from: {message['from']}
to: {message['to']}
subject: {message['subject']}
received: {datetime.now().isoformat()}
priority: {priority}
status: unread
---

# Email: {message['subject']}

## Sender
{message['from']}

## Received
{message['date']}

## Content

{message['body'] if message['body'] else message['snippet']}

## Suggested Actions

- [ ] Read and triage
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing

## Notes

*Add any notes or context here*

---
*Created by Gmail Watcher v0.1 (Bronze Tier)*
'''
        
        filepath.write_text(content)
        self.logger.info(f'Created action file: {filepath.name}')
        
        # Log the action
        self.log_action('email_received', {
            'message_id': message_id,
            'from': message['from'],
            'subject': message['subject'],
            'priority': priority
        })
        
        return filepath


def main():
    """
    Main entry point for running the Gmail Watcher.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Gmail Watcher for AI Employee')
    parser.add_argument(
        '--vault',
        type=str,
        default='..',  # Default to parent directory (we're inside _scripts/)
        help='Path to Obsidian vault (default: parent directory)'
    )
    parser.add_argument(
        '--credentials',
        type=str,
        default='credentials.json',
        help='Path to Gmail credentials.json'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=120,
        help='Check interval in seconds'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (for testing)'
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    vault_path = Path(args.vault).resolve()
    credentials_path = Path(args.credentials).resolve()
    
    # Create watcher
    watcher = GmailWatcher(
        vault_path=str(vault_path),
        credentials_path=str(credentials_path),
        check_interval=args.interval
    )
    
    if args.once:
        # Test run
        print('Running test check...')
        items = watcher.check_for_updates()
        print(f'Found {len(items)} new messages')
        for item in items:
            filepath = watcher.create_action_file(item)
            print(f'  Created: {filepath}')
    else:
        # Run continuously
        try:
            watcher.run()
        except KeyboardInterrupt:
            print('\nStopping Gmail Watcher...')
            watcher.stop()


if __name__ == '__main__':
    main()
