---
name: "td"
description: "A compact skill for Todoist CLI, use this when you want to find out how to use the CLI with simple examples"
---

# `td`

Usage: td [options] [command]

Todoist CLI

td [--version,--no-spinner,--progress-jsonl,--verbose,-vvv,--accessible,--quiet,--user] # Todoist CLI
├── td add [--stdin,--json,--dry-run] # Quick add with natural language (human shorthand for "td task quickadd" / "td
├── td changelog [--count] # Show recent changelog entries
├── td doctor [--json,--offline] # Diagnose common CLI setup and environment issues
├── td hc # Search Todoist Help Center articles
│   ├── td hc locales [--json] # List supported Help Center locales
│   ├── td hc locale [--set-default] # Manage the default Help Center locale
│   ├── td hc search [--locale,--limit,--json,--ndjson] # Search Todoist Help Center articles
│   └── td hc view [--locale,--browser,--json,--html] # View a Help Center article by id:N, raw article ID, or URL
├── td today [--limit,--cursor,--all,--any-assignee,--workspace,--personal,--json,--ndjson,--full,--raw,--show-urls] # Show tasks due today and overdue
├── td upcoming [--limit,--cursor,--all,--any-assignee,--workspace,--personal,--json,--ndjson,--full,--show-urls] # Show tasks due in the next N days (default: 7)
├── td inbox [--priority,--due,--limit,--cursor,--all,--json,--ndjson,--full,--raw,--show-urls] # List tasks in Inbox
├── td completed # Show completed tasks
│   └── td completed list [--search,--since,--until,--project,--limit,--cursor,--all,--json,--ndjson,--full,--show-urls] # List completed tasks, or search by query
├── td task # Manage tasks
│   ├── td task list [--project,--parent,--label,--priority,--due,--filter,--assignee,--unassigned,--workspace,--personal,--limit,--cursor,--all,--json,--ndjson,--full,--raw,--show-urls] # List tasks
│   ├── td task view [--json,--full,--raw] # View task details
│   ├── td task complete [--forever,--dry-run] # Complete a task
│   ├── td task uncomplete [--dry-run] # Reopen a completed task (requires id:xxx)
│   ├── td task delete [--yes,--dry-run] # Delete a task
│   ├── td task add [--content,--due,--deadline,--priority,--project,--section,--labels,--parent,--description,--stdin,--assignee,--duration,--uncompletable,--order,--json,--dry-run] # Add a task
│   ├── td task quickadd [--stdin,--json,--dry-run] # Quick add a task using natural language (e.g. "Buy milk tomorrow p1 #Shopping")
│   ├── td task update [--content,--due,--no-due,--deadline,--no-deadline,--priority,--labels,--no-labels,--description,--stdin,--assignee,--unassign,--duration,--uncompletable,--completable,--order,--json,--dry-run] # Update a task
│   ├── td task move [--project,--section,--parent,--no-parent,--no-section,--dry-run] # Move task to project/section/parent
│   ├── td task reschedule [--json,--dry-run] # Reschedule a task (preserves recurrence)
│   └── td task browse # Open task in browser
├── td project # Manage projects
│   ├── td project list [--search,--limit,--cursor,--all,--personal,--json,--ndjson,--full,--show-urls] # List all projects, or search by name
│   ├── td project view [--json,--ndjson,--full,--detailed,--show-urls] # View project details
│   ├── td project collaborators [--json,--ndjson,--full] # List project collaborators
│   ├── td project delete [--yes,--dry-run] # Delete a project (must have no uncompleted tasks)
│   ├── td project create [--name,--color,--favorite,--parent,--view-style,--json,--dry-run] # Create a project
│   ├── td project update [--name,--color,--favorite,--no-favorite,--folder,--no-folder,--parent,--no-parent,--view-style,--json,--dry-run] # Update a project
│   ├── td project archive [--dry-run] # Archive a project
│   ├── td project unarchive [--dry-run] # Unarchive a project
│   ├── td project browse # Open project in browser
│   ├── td project move [--to-workspace,--to-personal,--folder,--visibility,--yes,--dry-run] # Move project between personal and workspace
│   ├── td project reorder [--before,--after,--position,--json,--dry-run] # Reorder a personal project among its siblings
│   ├── td project archived [--limit,--cursor,--all,--json,--ndjson,--full,--show-urls] # List archived projects
│   ├── td project archived-count [--workspace,--joined,--json] # Count archived projects
│   ├── td project permissions [--json] # Show project permission mappings by role
│   ├── td project join [--json,--dry-run] # Join a shared project
│   ├── td project progress [--json] # Show project completion progress
│   ├── td project health [--json] # Show project health status and recommendations
│   ├── td project health-context [--json] # Show detailed project metrics and task breakdown for health analysis
│   ├── td project activity-stats [--json,--weeks,--include-weekly] # Show project activity statistics
│   └── td project analyze-health [--json,--dry-run] # Trigger a new health analysis for a project
├── td label # Manage labels
│   ├── td label view [--limit,--all,--json,--ndjson,--full,--show-urls] # View label details and tasks
│   ├── td label list [--search,--limit,--all,--json,--ndjson,--full,--show-urls] # List or search labels
│   ├── td label create [--name,--color,--favorite,--json,--dry-run] # Create a label
│   ├── td label delete [--yes,--dry-run] # Delete a label
│   ├── td label update [--name,--color,--favorite,--no-favorite,--json,--dry-run] # Update a label
│   ├── td label browse # Open label in browser
│   ├── td label rename-shared [--name,--dry-run] # Rename a shared label
│   └── td label remove-shared [--yes,--dry-run] # Remove a shared label
├── td comment # Manage comments
│   ├── td comment list [--project,--limit,--all,--show-urls,--json,--ndjson,--full,--lines,--raw] # List comments on a task (or project with --project)
│   ├── td comment add [--project,--content,--stdin,--file,--file-name,--json,--dry-run] # Add a comment to a task (or project with --project)
│   ├── td comment delete [--yes,--dry-run] # Delete a comment
│   ├── td comment update [--content,--json,--dry-run] # Update a comment
│   ├── td comment view [--json,--full,--raw] # View a single comment with full details
│   └── td comment browse # Open comment in browser (requires id:xxx)
├── td attachment # Manage file attachments
│   └── td attachment view [--json] # View/download a file attachment by URL
├── td section # Manage project sections
│   ├── td section list [--project,--search,--limit,--all,--json,--ndjson,--full,--show-urls] # List sections in a project, or search by name
│   ├── td section create [--name,--project,--json,--dry-run] # Create a section
│   ├── td section delete [--yes,--dry-run] # Delete a section
│   ├── td section update [--name,--json,--dry-run] # Update a section
│   ├── td section archive [--dry-run] # Archive a section
│   ├── td section unarchive [--dry-run] # Unarchive a section
│   └── td section browse # Open section in browser (requires id:xxx)
├── td workspace # Manage workspaces
│   ├── td workspace list [--json,--ndjson,--full] # List all workspaces
│   ├── td workspace view [--json,--full] # View workspace details (uses the default workspace when [ref] is omitted)
│   ├── td workspace create [--name,--description,--link-sharing,--no-link-sharing,--guest-access,--no-guest-access,--domain,--domain-discovery,--no-domain-discovery,--restrict-email-domains,--no-restrict-email-domains,--json,--full,--dry-run] # Create a new workspace
│   ├── td workspace update [--name,--description,--link-sharing,--no-link-sharing,--guest-access,--no-guest-access,--domain,--domain-discovery,--no-domain-discovery,--restrict-email-domains,--no-restrict-email-domains,--collapsed,--no-collapsed,--json,--full,--dry-run] # Update a workspace (admin only)
│   ├── td workspace delete [--yes,--dry-run] # Delete a workspace (admin only)
│   ├── td workspace projects [--workspace,--limit,--cursor,--all,--json,--ndjson,--full] # List projects in a workspace
│   ├── td workspace users [--workspace,--role,--limit,--cursor,--all,--json,--ndjson,--full] # List users in a workspace
│   ├── td workspace user-tasks [--workspace,--user,--project-ids,--json,--ndjson,--full] # List tasks assigned to a user in a workspace
│   ├── td workspace activity [--workspace,--user-ids,--project-ids,--json,--ndjson,--full] # Show workspace members activity (tasks assigned/overdue)
│   ├── td workspace insights [--workspace,--json,--project-ids] # Show health and progress insights for workspace projects
│   └── td workspace use [--clear] # Set the default workspace used when [ref] is omitted from other commands
├── td activity [--since,--until,--type,--event,--project,--by,--limit,--cursor,--markdown,--json,--ndjson,--full] # View activity logs
├── td reminder # Manage task reminders
│   ├── td reminder location # Manage location-based reminders
│   │   ├── td reminder location add [--task,--name,--lat,--long,--trigger,--radius,--json,--dry-run] # Add a location reminder to a task
│   │   ├── td reminder location update [--name,--lat,--long,--trigger,--radius,--json,--dry-run] # Update a location reminder
│   │   ├── td reminder location delete [--yes,--dry-run] # Delete a location reminder
│   │   └── td reminder location get [--json,--full] # Get a single location reminder by ID
│   ├── td reminder list [--task,--type,--limit,--cursor,--all,--json,--ndjson,--full] # List reminders (optionally filtered by task, or reminder type)
│   ├── td reminder add [--task,--before,--at,--json,--dry-run] # Add a reminder to a task
│   ├── td reminder update [--before,--at,--dry-run] # Update a reminder
│   ├── td reminder delete [--yes,--dry-run] # Delete a reminder
│   └── td reminder get [--json,--full] # Get a single time-based reminder by ID
├── td settings # Manage user settings
│   ├── td settings themes # List available themes
│   ├── td settings view [--json] # View current settings
│   └── td settings update [--timezone,--time-format,--date-format,--start-day,--theme,--auto-reminder,--next-week,--start-page,--reminder-push,--reminder-desktop,--reminder-email,--completed-sound-desktop,--completed-sound-mobile] # Update settings
├── td auth # Manage authentication
│   ├── td auth login [--read-only,--callback-port,--json,--ndjson,--additional-scopes] # Authenticate with Todoist via OAuth
│   ├── td auth logout [--json,--ndjson,--user] # Remove the saved authentication token
│   ├── td auth status [--json,--ndjson,--user] # Show current authentication status
│   └── td auth token # Save API token for CLI authentication (or use a subcommand: `view`)
│       └── td auth token view # Print the stored API token for the active user (or --user <ref>) to stdout for
├── td user # Manage stored Todoist accounts (multi-user)
│   ├── td user list [--json,--ndjson] # List all stored Todoist accounts
│   ├── td user use # Set the default account used when --user is not provided
│   ├── td user default # Alias of `td user use <ref>`
│   ├── td user current [--json] # Show the active account (resolved from --user, default, or single login)
│   └── td user remove # Remove a stored account (deletes its token and config entry)
├── td apps # Manage your registered Todoist developer apps
│   ├── td apps list [--json,--ndjson] # List your registered Todoist apps
│   ├── td apps view [--json,--ndjson,--include-secrets] # View details for a single app (by name, id:N, or raw id)
│   └── td apps update [--add-oauth-redirect,--remove-oauth-redirect,--yes,--dry-run,--json] # Update a single app (by name, id:N, or raw id)
├── td backup # Manage backups
│   ├── td backup list [--json,--ndjson] # List available backups
│   └── td backup download [--output-file] # Download a backup file
├── td stats [--json,--full] # View productivity stats and karma
│   ├── td stats goals [--daily,--weekly] # Update daily/weekly goals
│   └── td stats vacation [--on,--off] # Toggle vacation mode
├── td filter # Manage filters
│   ├── td filter list [--json,--ndjson,--full,--show-urls] # List all filters
│   ├── td filter create [--name,--query,--color,--favorite,--json,--dry-run] # Create a filter
│   ├── td filter delete [--yes,--dry-run] # Delete a filter
│   ├── td filter update [--name,--query,--color,--favorite,--no-favorite,--dry-run] # Update a filter
│   ├── td filter view [--limit,--cursor,--all,--json,--ndjson,--full,--show-urls] # Show tasks matching a filter
│   └── td filter browse # Open filter in browser
├── td folder # Manage workspace folders
│   ├── td folder list [--workspace,--limit,--cursor,--all,--json,--ndjson] # List folders in a workspace
│   ├── td folder view [--workspace,--json,--full] # View folder details and contained projects
│   ├── td folder create [--workspace,--name,--default-order,--child-order,--json,--dry-run] # Create a folder
│   ├── td folder update [--workspace,--name,--default-order,--json,--dry-run] # Update a folder
│   └── td folder delete [--workspace,--yes,--dry-run] # Delete a folder
├── td notification # Manage notifications
│   ├── td notification list [--type,--unread,--read,--limit,--offset,--json,--ndjson,--full] # List notifications
│   ├── td notification view [--json] # View notification details
│   ├── td notification accept # Accept a share invitation
│   ├── td notification reject # Reject a share invitation
│   ├── td notification read [--all,--yes] # Mark notification(s) as read
│   └── td notification unread # Mark notification as unread
├── td skill # Manage coding agent skills/integrations
│   ├── td skill list # List supported agents and install status
│   ├── td skill install [--local,--force] # Install skill for a coding agent
│   ├── td skill update [--local] # Update installed skill to latest version
│   └── td skill uninstall [--local] # Uninstall skill for a coding agent
├── td template # Manage project templates (export, import, create)
│   ├── td template export-file [--project,--relative-dates,--output,--json] # Export a project as a CSV template file
│   ├── td template export-url [--project,--relative-dates,--json] # Export a project as a template URL
│   ├── td template create [--name,--file,--file-name,--workspace,--json,--dry-run] # Create a new project from a template file
│   ├── td template import-file [--project,--file,--file-name,--json,--dry-run] # Import a template file into an existing project
│   └── td template import-id [--project,--template-id,--locale,--json,--dry-run] # Import a template by ID into an existing project
├── td completion # Manage shell completions
│   ├── td completion uninstall # Remove shell completions
│   └── td completion install # Install shell completions (bash, zsh, fish)
├── td config # Manage CLI configuration
│   └── td config view [--json,--show-token] # Show the current CLI configuration file
├── td view # View a Todoist entity or page by URL
└── td update [--check,--channel,--json,--ndjson] # Update the CLI to the latest version for the configured channel
    └── td update switch [--stable,--pre-release,--json,--ndjson] # Switch update channel between stable and pre-release
