# Inbox

Drop raw ideas, questions, and source links here.

## 2026-06-26: CirculatingBox - Windows Desktop Notifications & ClickOnce Deployment
- Fixed a crash in IssueOrderOpenControl by migrating business logic from a backup (C:\Users\Wuttipong.t\Desktop\IssueOrderOpenControl) and dropping flawed designer file components.
- Implemented native Windows 11 Toast Notifications (client-side) using Microsoft.Toolkit.Uwp.Notifications.ToastContentBuilder inside MockNotificationService.
- Added logic in Program.vb to activate the CirculatingBox window (bringing it to the front) when the user clicks a notification.
- Successfully published and deployed the updated app (version 3.1.0.32) to the production server via ClickOnce using the circulatingbox-publish skill.
