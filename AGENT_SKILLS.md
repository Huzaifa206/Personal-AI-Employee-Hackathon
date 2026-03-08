# AI Employee Agent Skills

This document defines the Agent Skills for Qwen Code to use when working with the AI Employee system.

## Overview

Agent Skills are predefined capabilities that Qwen Code can use to interact with the AI Employee vault and process tasks efficiently.

## Skill 1: Read Needs Action

**Purpose:** Read and analyze items in the Needs_Action folder.

**Usage:**
```
/needs-action
  List all pending items
  Read specific item: EMAIL_*.md or FILE_*.md
  Summarize content and suggest next steps
```

**Expected Output:**
- Summary of each pending item
- Priority classification (high/normal/low)
- Suggested actions based on Company_Handbook rules

## Skill 2: Create Plan

**Purpose:** Create a structured plan for multi-step tasks.

**Usage:**
```
/plan
  Create Plan.md in /Plans folder
  Define objective
  List steps with checkboxes
  Identify approval requirements
```

**Template:**
```markdown
---
created: YYYY-MM-DDTHH:MM:SSZ
status: pending_approval
objective: Clear statement of what needs to be done
---

# Plan: [Task Name]

## Objective
[Clear statement of the goal]

## Steps
- [ ] Step 1: Description
- [ ] Step 2: Description
- [ ] Step 3: Description

## Approval Required
[List any actions requiring human approval]

## Notes
[Any additional context or considerations]
```

## Skill 3: Update Dashboard

**Purpose:** Update the Dashboard.md with current status.

**Usage:**
```
/dashboard update
  Count pending items
  Count completed today
  List recent activity
  Update stats table
```

**Fields to Update:**
- `last_updated`: Current timestamp
- `Pending Tasks`: Count of files in Needs_Action
- `Completed Today`: Count of files in Done with today's date
- `Recent Activity`: Last 5 log entries

## Skill 4: Move to Done

**Purpose:** Move completed items to the Done folder.

**Usage:**
```
/done [filename]
  Move file from Needs_Action to Done
  Add completion timestamp
  Update Dashboard
  Log completion
```

**Rules:**
- Only move items that are fully completed
- Add timestamp to filename: `ORIGINAL_YYYYMMDD_HHMMSS.md`
- Update Dashboard after moving

## Skill 5: Request Approval

**Purpose:** Create approval request for sensitive actions.

**Usage:**
```
/approve [action_type] [details]
  Create file in /Pending_Approval
  Wait for human to move to /Approved
  Execute action once approved
```

**Approval Thresholds (from Company_Handbook):**
- Payments: Always require approval
- Emails to new contacts: Require approval
- Bulk operations: Require approval
- File deletions: Require approval

**Template:**
```markdown
---
type: approval_request
action: [action_type]
created: YYYY-MM-DDTHH:MM:SSZ
status: pending
---

# Approval Request: [Action Description]

## Details
[Full description of the proposed action]

## Why This Requires Approval
[Explanation based on Company_Handbook rules]

## To Approve
Move this file to /Approved folder

## To Reject
Move this file to /Rejected folder
```

## Skill 6: Log Activity

**Purpose:** Record all actions in the daily log.

**Usage:**
```
/log [action_type] [details]
  Append to /Logs/YYYY-MM-DD.json
  Include timestamp, actor, action, result
```

**Log Entry Format:**
```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_processed",
  "actor": "qwen_code",
  "details": {
    "message_id": "abc123",
    "from": "client@example.com",
    "action_taken": "created_reply_draft"
  },
  "result": "success"
}
```

## Skill 7: Read Company Handbook

**Purpose:** Reference the rules and guidelines.

**Usage:**
```
/handbook [section]
  Read Company_Handbook.md
  Apply rules to current situation
  Flag any rule violations
```

**Key Sections:**
- Communication Rules
- Financial Rules
- Task Management Rules
- Security Rules
- Escalation Rules

## Skill 8: Read Business Goals

**Purpose:** Align actions with business objectives.

**Usage:**
```
/goals [metric]
  Read Business_Goals.md
  Check current progress
  Suggest actions to improve metrics
```

**Key Metrics:**
- Revenue targets
- Client response time
- Invoice payment rate
- Software costs

## Skill 9: Triage Email

**Purpose:** Process incoming emails according to rules.

**Usage:**
```
/triage-email [email_file]
  Read email content
  Check priority keywords
  Check if from known contact
  Categorize and suggest actions
```

**Categories:**
- **Critical**: Respond within 1 hour
- **High**: Respond within 4 hours
- **Medium**: Respond within 24 hours
- **Low**: Respond within 1 week

## Skill 10: Process File Drop

**Purpose:** Handle files dropped into the system.

**Usage:**
```
/process-file [file]
  Read file content (if text-based)
  Extract key information
  Suggest categorization
  Create action plan
```

**File Type Handling:**
- PDF: Extract text, summarize
- DOC/DOCX: Read content, extract action items
- CSV/XLSX: Analyze data, create summary
- Images: Describe content, OCR if needed
- TXT: Read and process instructions

## Complete Workflow Example

```
1. Watcher creates: Needs_Action/EMAIL_abc123.md
2. Qwen runs: /needs-action
3. Qwen reads email, identifies as high priority
4. Qwen runs: /plan (creates Plans/PLAN_reply_client.md)
5. Qwen executes plan steps
6. If approval needed: /approve (creates Pending_Approval/...)
7. Once approved, Qwen completes action
8. Qwen runs: /done EMAIL_abc123.md
9. Qwen runs: /dashboard update
10. Qwen runs: /log "email_processed" {...}
```

## Integration with Ralph Wiggum Loop

For autonomous multi-step task completion, use the Ralph Wiggum pattern:

1. Create state file with task description
2. Qwen processes until complete
3. Qwen moves task file to /Done
4. Ralph hook checks: Is file in /Done?
5. If yes: Allow exit. If no: Re-inject prompt

## Security Reminders

When using these skills:

1. **Never** log sensitive information (passwords, account numbers)
2. **Always** check approval thresholds before acting
3. **Always** log every action taken
4. **Always** reference Company_Handbook for edge cases
5. **Never** execute irreversible actions without approval

---
*Agent Skills v0.1 - Bronze Tier*
