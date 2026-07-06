---
description: Show the project registry or one project's context
argument-hint: [project-name]
---

Read `~/Smith/projects/README.md` for the registry overview.

If `$ARGUMENTS` is empty: list all tracked projects with a one-line status each.

If `$ARGUMENTS` names a project: open `~/Smith/projects/<name>.md` and summarise — stack, current focus, key tables/files, last activity. Fuzzy-match the name (e.g. "circulating" → `circulatingbox.md`).

Address the user as "sir".
