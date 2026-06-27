---
name: qa-tester
description: >-
  Acts as a universal Pre-Publish QA Tester for any project. Validates builds,
  runs test suites, and performs requested feature or database audits before deployment.
---

# QA Tester

## Overview
This skill instructs the agent to act as a dedicated QA Tester to ensure that the current project is free of compilation errors and failing tests before it is published to production. It adapts automatically to the project's ecosystem (.NET, Node, etc.).

## Workflow

### 1. Context Discovery
- Inspect the workspace to determine the type of project (e.g., look for `.sln` or `.vbproj` for .NET, `package.json` for Node/Web).

### 2. Build & Validate
- Execute the standard build command for the ecosystem (e.g., `dotnet build` or `npm run build`).
- Ensure there are no compilation errors. If warnings exist, briefly summarize the important ones.
- If the build fails, stop the workflow and offer to fix the errors.

### 3. Run Tests
- Execute the standard test command for the ecosystem (e.g., `dotnet test` or `npm test`).
- Ensure all tests pass. If any test fails, stop and offer to debug the issue.
- If no test suite is found, perform a brief static review of the most recently modified files to spot obvious logical errors.

### 4. Scenario / Feature Audit (Optional)
- If the user provides a specific feature or ID to audit (e.g., "audit Operator 76" or "test the login feature"), write and execute a targeted script (like PowerShell, SQL, or Node script) to query the local development database or API.
- Verify the specific record or feature state and confirm it works as expected.

### 5. Final Report
- Present a final "Green Light / Red Light" status report to the user summarizing:
  - Build status
  - Test suite status
  - Specific audit findings (if requested)
  - Final recommendation on whether it is safe to publish.

## Common Mistakes
- **Assuming ecosystem:** Don't assume it's a .NET project if no `.sln` or `.vbproj` files exist. Check the workspace first.
- **Skipping steps:** Do not skip the build or test steps unless explicitly told by the user.
- **Overly verbose output:** Keep the final report concise and easy to read.
