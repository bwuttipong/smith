---
name: circulatingbox-publish
description: >-
  Automates the release process for the CirculatingBox application by bumping version numbers and executing the ClickOnce deployment script via Developer Command Prompt.
---

# CirculatingBox Publish

## Overview
Automates the exact build and deployment workflow for the CirculatingBox application:
1. Increments `AssemblyVersion` and `FileVersion` in `CirculatingBox.vbproj`
2. Increments `ApplicationRevision` in `ClickOnceProfile.pubxml`
3. Locates Visual Studio installation via `vswhere`
4. Executes `DEPLOY_TO_SERVER.cmd` using the Visual Studio Developer Command Prompt

## Dependencies
None. Uses Python standard library.

## Quick Start
To trigger a new release, just tell the agent: "Publish a new version of CirculatingBox" or "Bump the CirculatingBox version and deploy it".

## Utility Scripts
This skill uses a python CLI script located at `scripts/publisher.py`. The agent should invoke it using `uv run` to ensure dependencies are isolated (though it only uses the standard library).

### Bumping Versions
To bump the version in the project files:
```bash
uv run "c:\Users\Wuttipong.t\Smith\skills\circulatingbox_publish\scripts\publisher.py" bump --workspace "C:\Users\Wuttipong.t\Workspaces\Circulating_Box\CirculatingBox"
```

### Deploying
To execute the deployment script:
```bash
uv run "c:\Users\Wuttipong.t\Smith\skills\circulatingbox_publish\scripts\publisher.py" deploy --workspace "C:\Users\Wuttipong.t\Workspaces\Circulating_Box\CirculatingBox"
```

## Common Mistakes
- Not specifying the correct workspace path to the root of the solution.
- Forgetting to quote the path in the `--workspace` parameter.
