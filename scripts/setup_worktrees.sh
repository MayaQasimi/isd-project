#!/bin/bash
# Run from the repository root after: git init && git add . && git commit -m "init"
git worktree add ../lms-auth    feature/auth
git worktree add ../lms-catalog feature/catalog
git worktree add ../lms-members feature/members
git worktree add ../lms-loans   feature/loans
echo "Worktrees created:"
git worktree list
