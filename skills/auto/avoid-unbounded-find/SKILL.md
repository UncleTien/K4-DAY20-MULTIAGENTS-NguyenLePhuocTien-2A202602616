---
name: avoid-unbounded-find
description: Use this skill when searching for files to prevent overly broad or long-running commands.
---
- Limit search scope to relevant directories (e.g., current directory or known subdirectories)
- Use `-maxdepth` to restrict search depth
- Add timeout (e.g., `timeout 30s find ...`) to prevent hanging
- Target specific file patterns instead of scanning entire filesystem
