# Git Workflow Guide — Attendance Management System

> **Team:** Prizma (PM, GitHub: Prizma515), Abhishek (Backend/Admin, GitHub: sar-kaar), Ekata (Frontend, GitHub: ekatarimal)
> **Course:** CSE 405
> **Repository:** `attendance-management-system`
> **GitHub URL:** https://github.com/sar-kaar/attendance-management-system
> **Clone:** `gh repo clone sar-kaar/attendance-management-system`

**Repo rules (checked Jul 9):**

- `main` is protected: every merge into it needs a Pull Request with **1 approval**. `enforce_admins` is **on** — even sar-kaar (the repo admin) cannot bypass this and push straight to `main`.
- Any of the three team members can approve a PR — it does not have to be Prizma. Whoever reviews it and clicks Approve unblocks the merge.
- `develop` currently has **no protection** — anyone can push directly to it, but the team is not doing that. Everyone still branches off `develop` and opens a PR back into it. Decide as a team if `develop` should get the same 1-approval rule; not decided yet.
- Branch naming follows the multi-prefix scheme in Section 3 (`feature/US-NN-name`, `docs/name`, `bugfix/name`, `chore/name`, `hotfix/name`). Every branch on GitHub has been renamed to match this — see Section 7 for the current list.
- PRs are created with `gh pr create --base develop --head <branch-name> --title "..." --body "..."`, not through the GitHub website.

---

## Table of Contents

1. [Why Git? Why This Workflow?](#1-why-git-why-this-workflow)
2. [DAY 1 — GitHub Repo Setup (July 8)](#2-day-1--github-repo-setup-july-8)
3. [Branch Strategy](#3-branch-strategy)
4. [Daily Git Workflow](#4-daily-git-workflow)
5. [Commit Message Format](#5-commit-message-format)
6. [Weekly Git Schedule](#6-weekly-git-schedule)
7. [Branch Creation Schedule (Who Creates What)](#7-branch-creation-schedule-who-creates-what)
8. [Merge & Pull Request Checklist](#8-merge--pull-request-checklist)
9. [Common Git Commands Cheat Sheet](#9-common-git-commands-cheat-sheet)
10. [Resolving Merge Conflicts](#10-resolving-merge-conflicts)
11. [GitHub Project Board Integration](#11-github-project-board-integration)
12. [Recovery / Fixing Mistakes](#12-recovery--fixing-mistakes)
13. [Tagging & Releases](#13-tagging--releases)
14. [FAQ for Beginners](#14-faq-for-beginners)

---

## 1. Why Git? Why This Workflow?

Three people working on the same codebase at the same time will step on each other's toes without a system. Git is a **version control system** — it tracks every change, lets you work in parallel, and merges work together. This workflow (GitHub Flow modified for a 3-person team) gives us:

- **Isolation** — Each person works on their own branch. Your half-finished code never breaks someone else's work.
- **Code review** — Every feature is peer-reviewed before it lands in `develop`.
- **History** — Every commit has a clear message. Three months later you can find exactly why a change was made.
- **Safety** — Mistakes can be undone. Nothing is permanently lost.

---

## 2. Repo Setup — What Actually Happened

The repo was set up and rebuilt once already (Abhishek deleted and recreated it to get the branch protection rules right). This is the real, current state — not a plan to follow, a record of what's already done:

- Repo created: `gh repo create sar-kaar/attendance-management-system --public`
- Collaborators added with write access:
  ```bash
  '{"permission":"write"}' | gh api "repos/sar-kaar/attendance-management-system/collaborators/Prizma515" --method PUT --input -
  '{"permission":"write"}' | gh api "repos/sar-kaar/attendance-management-system/collaborators/ekatarimal" --method PUT --input -
  ```
- Initial commit pushed to `main`: the full Django project (accounts, students, courses, attendance apps + DRF + JWT)
- Branch protection set on `main` (1 required approval, no admin bypass, no force push, no deletions, linear history, conversation resolution required):
  ```bash
  '{"required_status_checks":null,"required_pull_request_reviews":{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_last_push_approval":true},"restrictions":null,"enforce_admins":true,"required_linear_history":true,"allow_force_pushes":false,"allow_deletions":false,"required_conversation_resolution":true}' | gh api "repos/sar-kaar/attendance-management-system/branches/main/protection" --method PUT --input -
  ```
- `develop` created from `main` and pushed
- Four branches created off `develop`, renamed to match the naming scheme below: `docs/er-diagram`, `feature/US-07-face-registration-api`, `feature/US-09-report-api`, `feature/US-10-dashboard-ui` — these map to the real remaining work (docs, face recognition build, exports/reports, dashboard stats)

### Who does what now

| Person | Role |
|--------|------|
| **Abhishek** | Repo admin. Reviews and merges PRs into `develop`. Owns backend `feature/`+`bugfix/`+`chore/` branches. |
| **Prizma**   | Reviews PRs when free, owns `docs/` branches. |
| **Ekata**    | Owns frontend `feature/` branches. |

Nobody pushes directly to `main`. Everyone can push to their own branch and open a PR into `develop`.

---

### Abhishek — Create the repository

#### Step 1: Create repo on GitHub website

1. Go to [github.com](https://github.com) and sign in to your account.
2. Click the **+** icon in the top-right corner → **New repository**.
3. Fill in the following:

   | Field | Value |
   |-------|-------|
   | Repository name | `attendance-management-system` |
   | Description | `Attendance Management System with facial recognition - CSE 405` |
   | Visibility | **Private** |
   | Initialize with README | **Unchecked** (we will create README locally) |

4. Click **Create repository**.

---

#### Step 2: Create local project structure

Open **Git Bash** (Windows) or **Terminal** (macOS/Linux) and run these commands:

```bash
# Navigate to where you want the project folder
cd ~/Documents

# Create the project directory
mkdir attendance-management-system

# Enter it
cd attendance-management-system

# Initialise an empty Git repository
git init

# Rename the default branch from "master" to "main" (modern convention)
git checkout -b main
```

**What each command does:**

| Command | Explanation |
|---------|-------------|
| `mkdir` | Makes a new directory (folder) |
| `cd` | Changes into that directory |
| `git init` | Creates a hidden `.git` folder — this is what makes it a Git repository |
| `git checkout -b main` | Creates a new branch called `main` and switches to it |

---

#### Step 3: Create initial files

```bash
# Create README.md with a heading
echo "# Attendance Management System" > README.md

# Create .gitignore — tells Git which files to NEVER track
echo "node_modules/" > .gitignore
echo ".env" >> .gitignore        # Append (>> not >)
echo "venv/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".DS_Store" >> .gitignore
echo "*.log" >> .gitignore
echo "dist/" >> .gitignore
echo "build/" >> .gitignore
```

**Why a `.gitignore`?**
- `node_modules/` — If you install npm packages, this folder is huge. Everyone runs `npm install` locally. It never goes in the repo.
- `.env` — Contains secrets (database passwords, API keys). Never commit secrets.
- `venv/` — Python virtual environment. Each person creates their own.
- `*.pyc` — Compiled Python bytecode. Auto-generated, useless in version control.
- `__pycache__/` — Python cache directories.
- `.DS_Store` — macOS folder metadata file.
- `*.log` — Log files change constantly and are machine-specific.
- `dist/`, `build/` — Generated output files.

---

#### Step 4: First commit

```bash
# Stage everything (tell Git "I want to save these files")
git add .

# Commit with a message (take a snapshot of everything staged)
git commit -m "[init] Initial project setup with README and .gitignore"
```

**What happens here:**

| Command | Explanation |
|---------|-------------|
| `git add .` | The dot means "everything in this folder". Files are now **staged** (ready to be committed). |
| `git commit -m "..."` | Takes a permanent snapshot of the staged files. The `-m` flag lets you write the message inline. |

---

#### Step 5: Connect to GitHub and push

```bash
# Tell Git where the remote repository lives on GitHub
git remote add origin https://github.com/Abhishek/attendance-management-system.git

# Push the main branch to GitHub (-u sets upstream tracking, so next time just "git push")
git push -u origin main
```

**What each part means:**

| Part | Explanation |
|------|-------------|
| `remote add` | Adds a remote server. Conventionally the main remote is called `origin`. |
| `origin` | Nickname for the GitHub URL (you can name it anything, but `origin` is standard). |
| `git push` | Uploads your commits to the remote. |
| `-u` | Sets upstream tracking — after this you can just type `git push` instead of `git push origin main`. |
| `origin main` | "Push to the remote called `origin`, branch called `main`." |

---

#### Step 6: Add team members as collaborators

1. Go to your repo on GitHub: `https://github.com/Abhishek/attendance-management-system`
2. Click **Settings** tab (near the top-right).
3. In the left sidebar, click **Collaborators** (under "Access").
4. Click **Add people**.
5. Enter **Prizma's GitHub username** and **Ekata's GitHub username**.
6. Click **Add to repository**.
7. They will receive an email invitation. They must accept it before they can push.

---

### Everyone — Clone the repository

Once you've accepted the collaborator invite, set up your local copy:

```bash
gh repo clone sar-kaar/attendance-management-system
cd attendance-management-system
git checkout develop
git pull
```

`develop` and `main` already exist on GitHub — you don't create them. You just check out `develop` and start branching from there.

---

### One-time git identity setup (each person, once per machine)

```bash
git config user.email "your.email@example.com"
git config user.name "your-github-username"
```

**`develop` vs `main`:**
- `main` — Only contains fully tested, production-ready code. No one pushes directly to `main`.
- `develop` — Integration branch. All feature branches merge here first. When `develop` is stable, it gets merged into `main`.

---

## 3. Branch Strategy

### Visual hierarchy

```
main                      ← Production-ready code (protected, no direct push)
  │
  └── develop             ← Integration branch (all features merge here first)
       │
       ├── feature/US-01-add-students        ← Abhishek's feature branches
       ├── feature/US-02-login-page          ← Ekata's feature branches
       ├── docs/srs-document                 ← Prizma's doc branches
       ├── bugfix/fix-login-error            ← Bug fix branches
       └── hotfix/critical-bug               ← Emergency fixes (rare)
```

### Branch types explained

| Branch Type | Prefix | Created From | Merges Into | Lifetime |
|-------------|--------|-------------|-------------|----------|
| Feature | `feature/` | `develop` | `develop` | Days (while building the feature) |
| Bug Fix | `bugfix/` | `develop` | `develop` | Hours to days |
| Hotfix | `hotfix/` | `main` | `main` AND `develop` | Hours (urgent production bugs) |
| Documentation | `docs/` | `develop` | `develop` | Varies |
| Chore | `chore/` | `develop` | `develop` | Short (tooling, config) |

### Naming rule in use

Use the prefix that matches the type of work:

- **`feature/US-NN-short-description`** — new feature tied to a user story number
- **`docs/short-description`** — documentation-only branches
- **`bugfix/short-description`** — bug fixes
- **`chore/short-description`** — tooling/config
- **`hotfix/short-description`** — urgent production fixes, branched from `main`

Every branch created off `develop` should use one of these. Section 7 lists the current real branches under this scheme.

### Why this structure?

- **Separation of concerns** — No one works directly on `develop`. If your code breaks, it only breaks your branch.
- **Traceability** — Branch names include the user story number (`US-01`). You can cross-reference with Trello/Jira.
- **Clean history** — When you merge via pull request, all commits from your feature branch become a single logical unit in `develop`.

---

## 4. Daily Git Workflow

### 4.1 Start of day (everyone)

Every morning, regardless of what you worked on yesterday:

```bash
# Step 1: Go to the develop branch
git checkout develop

# Step 2: Get the latest changes from GitHub (your teammates may have merged things)
git pull origin develop

# Step 3: Create a new feature branch for today's task
git checkout -b feature/US-XX-my-task
```

**Why this order?**
- `git checkout develop` switches you to the integration branch.
- `git pull origin develop` downloads any new commits your teammates pushed overnight.
- `git checkout -b feature/...` creates a fresh branch FROM the latest `develop`. This minimises merge conflicts later.

**One-time setup shortcut:**

```bash
# Set upstream tracking so future pulls default to origin/develop
git branch --set-upstream-to=origin/develop develop
```

After this, `git pull` while on `develop` automatically pulls from `origin/develop`.

---

### 4.2 During the day (while working)

```bash
# === See what files you've changed ===
git status

# === Stage specific files for commit ===
git add src/api/auth.js
git add src/api/user.js

# === Stage all changed files ===
git add .

# === Commit with a proper message ===
git commit -m "[US-01] Add user registration endpoint with validation"
```

**`git status` output explained:**

```
On branch feature/US-01-register-api
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   src/api/auth.js
        modified:   src/api/user.js

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/utils/validator.js
```

- **Modified** — Files that existed before and you changed them.
- **Untracked** — Brand new files Git has never seen before.

---

### 4.3 Staging basics (important!)

Git has three states for files:

```
Working Directory  →  Staging Area (index)  →  Local Repository (.git)
   (your files)        (git add)                (git commit)
```

| State | What it means | Command to get here |
|-------|---------------|---------------------|
| **Modified** | You edited a file but haven't told Git about it yet | Just edit and save |
| **Staged** | You marked the file to be included in the next commit | `git add <file>` |
| **Committed** | The staged files have been saved as a snapshot in Git history | `git commit -m "message"` |

**Keep commits small and focused.** Each commit should be one logical change:

```
Good:  "[US-01] Add input validation for registration form"
Bad:   "[US-01] fixed stuff"
Bad:   "[US-01] Add validation, fix button color, update readme, remove debug logs"
```

---

### 4.4 End of day (if feature NOT complete)

If your feature is not finished but you want to save your work (always do this before leaving):

```bash
# Stage everything (including half-finished files)
git add .

# Commit with "WIP" (Work In Progress) marker
git commit -m "[US-01] WIP: Registration form UI, validation pending"

# Push to GitHub — your branch exists only locally until you push
git push origin feature/US-01-my-task
```

**Why push half-done work?**

- **Backup** — Your laptop could die. Code on GitHub is safe.
- **Visibility** — Your teammates can see what you are working on.
- **Collaboration** — If you get stuck, someone can look at your branch and help.

---

### 4.5 When feature is complete

This is the most critical sequence. Follow it exactly.

```bash
# Step 1: Switch to develop and get the latest
git checkout develop
git pull origin develop

# Step 2: Go back to your feature branch
git checkout feature/US-01-my-task

# Step 3: Merge develop INTO your feature branch
# This brings your branch up to date with any changes that happened
# while you were working
git merge develop
```

**If there are merge conflicts**, see Section 10.

```bash
# Step 4: Push the updated feature branch
git push origin feature/US-01-my-task
```

**Step 5: Create a Pull Request with `gh`, not the website**

This is how the team actually does it:

```bash
gh pr create --base develop --head feature/US-XX-your-branch --title "Short title" --body "What this does. CC @sar-kaar"
```

| Field | Value |
|-------|-------|
| Base branch | `develop` (NOT main) |
| Head branch | `feature/US-XX-your-branch` (or `docs/`, `bugfix/`, `chore/` — match the work type) |
| Title | Short, plain description |
| Body | What the branch does, tag whoever should review |

**Step 6: Get it reviewed**

- Any of the three team members can review and approve — it isn't locked to a fixed pair.
- Whoever is free and understands the change reviews it. Tag a specific person in the PR body if you want a specific reviewer.
- Once approved, the PR author or the reviewer merges it into `develop`.

---

### 4.6 Code review process (peer review)

```
┌─────────────────────────────────────────────────────────┐
│  1. Developer creates PR on GitHub                       │
│  2. Developer assigns reviewer (the other team member)   │
│  3. GitHub sends notification to reviewer                │
│  4. Reviewer opens PR, reads code, adds comments         │
│  5. If changes requested → Developer fixes, pushes again  │
│  6. When approved → Reviewer clicks "Merge pull request"  │
│  7. DELETE the feature branch on GitHub (button appears)  │
│  8. Developer deletes local branch                       │
└─────────────────────────────────────────────────────────┘
```

**What reviewers look for:**

- **Logic** — Does the code do what the user story says?
- **Error handling** — What happens if the database is down? If the user enters invalid data?
- **Security** — Are inputs sanitised? Is there SQL injection risk? XSS?
- **Code style** — Does it match the project conventions?
- **No debugging leftovers** — `console.log`, `print()`, commented-out code.

**Code review etiquette:**

- Be specific in comments. Instead of "this is wrong", say "this SQL query is vulnerable to injection — use parameterised queries instead".
- If you don't understand something, ask. It is not an insult.
- Don't take feedback personally. Code reviews make the project better.

---

## 5. Commit Message Format

### Structure

```
[US-NN] Short title (max 50 characters)
                              ← blank line (required)
Optional body explaining WHAT and WHY,
not HOW. Wrap lines at 72 characters.

- Bullet points for listing multiple changes
- Reference issues: Closes #1, Related to #2
```

### Rules

1. **First line is like an email subject.** It should complete the sentence: "This commit will ____."
2. **Capitalise the first letter.** No period at the end of the subject line.
3. **Use the imperative mood.** "Add" not "Added" or "Adds".
4. **Body explains WHY, not HOW.** The code itself shows how. The commit message explains why you made that choice.
5. **Reference issues** with `Closes #N` (auto-closes the GitHub issue) or `Related to #N`.

### Good examples

```
[US-01] Add user registration API endpoint
```
```
[US-02] Create login page with form validation

Implements email/password validation on the client side
before sending to the API. Shows inline error messages
below each field. Prevents form submission if validation
fails.

Closes #4
```
```
[US-03] Implement RBAC middleware

Adds role-based access control middleware that checks
user roles before granting access to protected routes.
Three roles: admin, faculty, student.

Related to #7
```
```
[docs] Update SRS section 3.1 - System Architecture

Added deployment diagram and clarified the interaction
between frontend React app and backend Django API.

Closes #12
```

### Bad examples (DO NOT write these)

| Bad message | Why it is bad |
|-------------|---------------|
| `fixed stuff` | Tells you nothing |
| `asdflkj` | Meaningless |
| `Updated files` | Does not say what or why |
| `[US-01] Added validation and changed colours and fixed the thing` | Multiple changes in one commit |
| `WIP` alone | Fine temporarily, but squash before merging |

### Standard commit prefixes

| Prefix | When to use |
|--------|-------------|
| `[US-NN]` | User story work — `[US-01] Add register API` |
| `[docs]` | Documentation changes |
| `[chore]` | Tooling, config, dependencies |
| `[bugfix]` | Bug fixes |
| `[init]` | Initial project setup |
| `[refactor]` | Code restructuring with no behaviour change |
| `[test]` | Adding or updating tests |
| `[hotfix]` | Emergency production fix |
| `[merge]` | Merge commits (usually auto-generated) |

---

## 6. Weekly Git Schedule

| Day | Git Activity | Details |
|-----|-------------|---------|
| **Monday** | `git pull origin develop` | Get everyone's latest work |
| | `git checkout -b feature/US-XX-task` | Start fresh branch for the week's task |
| **Tuesday** | Work on feature, commit | At least one commit before end of day |
| | `git push origin feature/US-XX-task` | Push even if not done |
| **Wednesday** | Work on feature, commit | Regular commits |
| | `git push` | Keep remote up to date |
| **Thursday** | Work on feature, commit | Finalise the feature |
| | `git push` | Make sure everything is pushed |
| **Friday** | Complete feature | Test, fix bugs |
| | `git merge develop` | Get latest changes and resolve conflicts |
| | Push and create PR | On GitHub |
| | **Code review** | Review your teammate's PR |
| **Saturday** | Merge approved PRs | Reviewer clicks "Merge" |
| | Delete feature branches | Both remote and local |
| **Sunday** | `git tag sprint-N` | Tag the sprint for history |
| | Prepare next sprint | Create new Trello cards |

### Why commit every day?

Even if your code doesn't compile, commit at end of day with a note:

```
[US-01] WIP: Database connection not working, stuck on SQLAlchemy config
```

This serves two purposes:
1. Your code is backed up.
2. If you are stuck, your teammate can look at your branch and help.

---

## 7. Branch Creation Schedule (Who Creates What)

All branches below use the multi-prefix scheme from Section 3 (`feature/US-NN-name`, `docs/name`, `bugfix/name`, `chore/name`, `hotfix/name`). Backend auth + CRUD were already built into the initial commit, so Weeks 3–4 are verify/secure/connect branches, not build-from-scratch ones — see `Guidelines/REALITY_CHECK.md`.

### Already created (Week 1–2) — renamed to match this scheme

| Creator | Branch Name | Content |
|---------|-------------|---------|
| **Abhishek** | `docs/er-diagram` | ER diagram + docs (already has a PR open) |
| **Abhishek** | `feature/US-07-face-registration-api` | Reserved for Week 5 face recognition work |
| **Abhishek** | `feature/US-09-report-api` | Reserved for Week 6 export/report work |
| **Abhishek/Ekata** | `feature/US-10-dashboard-ui` | Reserved for Week 6 dashboard work |

### Week 3 — Auth verify/secure/connect

| Creator | Branch Name |
|---------|-------------|
| **Abhishek** | `bugfix/auth-tests`, `chore/cors-restrict` |
| **Ekata** | `feature/US-02-login-page`, `feature/US-03-register-page`, `feature/US-04-dashboard-shell` |

### Week 4 — Core Attendance UI

| Creator | Branch Name |
|---------|-------------|
| **Abhishek** | `feature/US-05-enrollment-decision`, `chore/crud-hardening` |
| **Ekata** | `feature/US-05-student-ui`, `feature/US-06-course-ui`, `feature/US-06-attendance-ui` |

### Week 5 — Face Recognition

| Creator | Branch Name |
|---------|-------------|
| **Abhishek** | `feature/US-07-face-registration-api` (already exists — use it) |
| **Ekata** | `feature/US-07-camera-component`, `feature/US-07-face-registration-ui`, `feature/US-08-face-attendance-ui` |

### Week 6 — Reports & Dashboard

| Creator | Branch Name |
|---------|-------------|
| **Abhishek** | `feature/US-09-report-api` (already exists), `feature/US-10-dashboard-ui` (already exists) |
| **Ekata** | `feature/US-10-dashboard-ui-frontend`, `feature/US-09-report-page` |

### Week 7 — Final Polish

| Creator | Branch Name |
|---------|-------------|
| **Abhishek** | `chore/production-config`, `docs/api-documentation` |
| **Ekata** | `chore/production-build` |
| **Prizma** | `docs/final-report` |

---

## 8. Merge & Pull Request Checklist

### Before creating a PR (developer)

```
□ Code compiles/runs without errors
□ Tested the feature manually (at least 3 test cases)
□ No console.log, print(), or debug code left behind
□ No commented-out code blocks
□ Code follows project style guide (indentation, naming, etc.)
□ No sensitive data (passwords, API keys) in code
□ Branch is up to date with develop (ran git merge develop)
□ Commit messages are clean and descriptive
```

### During code review (reviewer)

```
□ Logic is correct — does it satisfy the user story?
□ Error handling is proper — no uncaught exceptions
□ Edge cases handled — empty inputs, invalid data, missing records
□ Security:
   □ No SQL injection risk (use parameterised queries)
   □ No XSS vulnerabilities (sanitise user input)
   □ No hardcoded secrets
   □ Authentication/authorisation checks in place
□ Code is readable and maintainable
□ No unnecessary duplication
□ Performance is reasonable (no N+1 queries, no massive loops)
```

### After merge (developer)

```
□ Feature branch deleted on GitHub (button in PR after merge)
□ Local branch deleted:
   git checkout develop
   git branch -d feature/US-XX-task
□ Remote tracking branch cleaned up:
   git remote prune origin
□ Trello card moved to "Done" column
```

### Checklist for merging into `main` (end of sprint)

```
□ All features for the sprint are merged into develop
□ All tests pass
□ Manual smoke test on a staging environment
□ Product Owner (Prizma) approves
□ git checkout main
□ git merge develop
□ git tag sprint-1
□ git push origin main --tags
```

---

## 9. Common Git Commands Cheat Sheet

### Repository setup

```bash
git init                                    # Create a new Git repository in current folder
git clone <url>                             # Download a remote repo to your machine
git remote add origin <url>                 # Link local repo to GitHub
git remote -v                               # See which remotes are configured
```

### Branch management

```bash
git branch                                  # List local branches (* marks current branch)
git branch -a                               # List ALL branches (local + remote)
git branch -r                               # List only remote branches
git checkout <branch-name>                  # Switch to an existing branch
git checkout -b <branch-name>               # Create a new branch and switch to it
git branch -d <branch-name>                 # Delete a local branch (safe — warns if unmerged)
git branch -D <branch-name>                 # Force delete (even if unmerged — be careful)
git branch -m <old-name> <new-name>         # Rename a branch
```

### Making changes

```bash
git status                                  # Show changed files
git diff                                    # Show exact line-by-line changes (unstaged)
git diff --staged                           # Show changes in staging area
git add <file>                              # Stage a specific file
git add .                                   # Stage all changes (new, modified, deleted)
git add -p                                  # Stage interactively (review each change block)
git restore <file>                          # Discard uncommitted changes to a file
git restore --staged <file>                 # Unstage a file (keep changes in working dir)
git clean -fd                               # Remove untracked files and directories
```

### Committing

```bash
git commit -m "message"                     # Commit staged changes with inline message
git commit                                  # Commit and open editor for multi-line message
git commit -a -m "message"                  # Stage ALL modified files AND commit (skips git add)
                                            # WARNING: does NOT stage new (untracked) files
git commit --amend -m "new message"         # Change the last commit's message
git commit --amend --no-edit                # Add staged changes to last commit (keep message)
```

### Sync with remote

```bash
git pull                                    # Fetch + merge remote changes (from upstream branch)
git pull origin develop                     # Pull from a specific remote branch
git push                                    # Push local commits to remote (upstream must be set)
git push origin <branch>                    # Push a branch to the remote
git push -u origin <branch>                 # Push AND set upstream (do this the first time)
git push origin --delete <branch>           # Delete a remote branch
git push --tags                             # Push tags to remote
git fetch                                   # Download remote changes WITHOUT merging
git remote prune origin                     # Clean up stale remote-tracking branches
```

### Merging

```bash
git merge <branch>                          # Merge <branch> into current branch
git merge --no-ff <branch>                  # Merge with no fast-forward (creates merge commit)
git merge --abort                           # Abort a merge that has conflicts
```

### Viewing history

```bash
git log                                     # Full commit history
git log --oneline                           # Compact one-line-per-commit view
git log --oneline -5                        # Last 5 commits only
git log --graph --oneline --all             # Visual branch structure
git log --author="Abhishek"                 # Filter by author
git log --since="2026-07-08"                # Commits since a date
git log -p                                  # Show commits with diffs
git show <commit-hash>                      # Show details of a specific commit
git show HEAD                               # Show details of the latest commit
```

### Undoing things

```bash
git restore <file>                          # Discard unstaged changes (risky — cannot undo)
git restore --staged <file>                 # Unstage (opposite of git add)
git reset HEAD~1                            # Undo last commit, keep changes staged
git reset --soft HEAD~1                     # Undo last commit, keep changes staged (same as above)
git reset --mixed HEAD~1                    # Undo last commit, keep changes unstaged
git reset --hard HEAD~1                     # Undo last commit AND discard changes (DANGER!)
git reset --hard origin/develop             # Reset local branch to match remote exactly
git revert <commit-hash>                    # Create a NEW commit that undoes the specified commit
                                            # (safer than reset if others already have the commit)
```

### Stashing (temporary save)

```bash
git stash                                   # Save uncommitted changes temporarily
git stash list                              # List all stashes
git stash pop                               # Restore most recent stash and delete it
git stash apply                             # Restore stash but keep it in the list
git stash drop stash@{2}                    # Delete a specific stash
git stash push -m "half-done feature X"     # Stash with a descriptive message
```

### Tagging

```bash
git tag                                     # List all tags
git tag sprint-1                            # Create a lightweight tag
git tag -a v1.0.0 -m "Sprint 1 release"    # Create an annotated tag
git show v1.0.0                             # Show tag details
git push origin sprint-1                    # Push a specific tag
git push --tags                             # Push all tags
git tag -d sprint-1                         # Delete a local tag
```

---

## 10. Resolving Merge Conflicts

### What is a merge conflict?

A merge conflict happens when two people change the **same lines** of the **same file** in different ways. Git doesn't know which version to keep, so it asks you to decide.

### Real-world example

Abhishek and Ekata both edit `src/api/auth.js`:

- **Abhishek** (on `feature/US-01-register-api`) changes line 15-20 to add validation.
- **Ekata** (on `feature/US-02-login-api`) changes line 15-20 to add logging.

When Abhishek runs `git merge develop` (or vice versa), Git will stop and say:

```
Auto-merging src/api/auth.js
CONFLICT (content): Merge conflict in src/api/auth.js
Automatic merge failed; fix conflicts and then commit the result.
```

### Step-by-step resolution

#### Step 1: Identify conflicting files

```bash
# See which files have conflicts
git status
```

Output will show "both modified" files under "Unmerged paths".

#### Step 2: Open the conflicted file

In your code editor, the conflict looks like this:

```javascript
<<<<<<< HEAD
// Your code (the branch you are merging INTO)
function validateUser(input) {
    const errors = [];
    if (!input.email) errors.push('Email is required');
    return errors;
}
=======
// Their code (the branch you are merging FROM)
function validateUser(input) {
    console.log('Validating user:', input);
    return input.email !== '';
}
>>>>>>> develop
```

#### Step 3: Decide what to keep

**Markers explained:**

| Marker | Meaning |
|--------|---------|
| `<<<<<<< HEAD` | Start of YOUR version (current branch) |
| `=======` | Separator between versions |
| `>>>>>>> develop` | End of THEIR version (the branch being merged) |

**Options:**
- Keep only your code (delete `<<<<<<<` through `>>>>>>>`)
- Keep only their code
- Combine both (most common)

For this example, the correct resolution keeps both (validation + logging):

```javascript
function validateUser(input) {
    console.log('Validating user:', input);
    const errors = [];
    if (!input.email) errors.push('Email is required');
    return errors;
}
```

**After editing, delete the conflict markers** (`<<<<<<<`, `=======`, `>>>>>>>`).

#### Step 4: Mark as resolved and continue

```bash
# Stage the resolved file(s)
git add src/api/auth.js

# Continue the merge
git commit

# Git will open an editor with a pre-written merge message.
# Save and close (or use -m flag)
git commit -m "[merge] Resolve conflict in auth.js"
```

#### Step 5: Verify

```bash
# Ensure everything compiles and tests pass
npm test
# or
python -m pytest
```

### Tips for minimising conflicts

1. **Pull `develop` into your branch frequently** (at least once a day). Small, frequent merges have fewer conflicts.
2. **Communicate** — Tell your team if you are working on a file someone else might touch.
3. **Divide work by feature, not file** — If Abhishek owns backend (`src/api/`) and Ekata owns frontend (`src/components/`), you will rarely conflict.
4. **Use `git merge --no-commit --no-ff`** to inspect a merge before committing.

### Resolving conflicts in binary files (images, PDFs)

Git cannot merge binary files. If both people change the same image:

```bash
# Keep one version explicitly
git checkout --ours -- path/to/image.png    # Keep your version
git checkout --theirs -- path/to/image.png  # Keep their version

# Then continue the merge
git add path/to/image.png
git commit
```

### Aborting a merge (if things go wrong)

```bash
# If you are overwhelmed, you can abort and start over
git merge --abort
```

This resets everything to before the merge command.

---

## 11. GitHub Project Board Integration

### Linking commits to Trello

Every commit message should reference the Trello card number:

```
git commit -m "[US-01] Add registration API — Closes Trello card US-01"
```

### Pull Request template

GitHub allows you to create a PR template. Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description
<!-- Briefly describe what this PR does -->

## Related User Story
<!-- US-01, US-02, etc. -->

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactor

## Testing
<!-- Describe how you tested this -->

## Screenshots (if applicable)

## Checklist
- [ ] Code compiles
- [ ] Tested manually
- [ ] No debug code left
- [ ] Branch up to date with develop
```

---

## 12. Recovery / Fixing Mistakes

### Scenario 1: You committed to the wrong branch

```bash
# Save the commit hash
git log --oneline -1

# Switch to the correct branch
git checkout correct-branch

# Cherry-pick the commit (apply it here)
git cherry-pick <commit-hash>

# Go back and remove it from the wrong branch
git checkout wrong-branch
git reset --hard HEAD~1
```

### Scenario 2: You need to undo a pushed commit

```bash
# Revert creates a NEW commit that undoes the old one
# Safe because it doesn't rewrite history
git revert <commit-hash>
git push origin <branch>
```

### Scenario 3: You accidentally deleted a branch

```bash
# Find the commit hash from the reflog (Git's safety net)
git reflog

# Look for the commit that was the tip of your deleted branch
# Then recreate the branch at that commit
git checkout -b recovered-branch <commit-hash>
```

### Scenario 4: You need to squash multiple commits into one

```bash
# Squash the last 3 commits into 1
git rebase -i HEAD~3

# In the editor, change "pick" to "squash" (or "s") for all except the first
# Save and close, then write a new commit message
```

### Scenario 5: You committed sensitive data (password, API key)

```bash
# IMMEDIATELY rotate the exposed credential (change password, revoke key)
# Then remove the file from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive-file" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (needs --force because we rewrote history)
git push origin --force --all
git push origin --force --tags
```

**⚠️ WARNING:** Force pushing rewrites history. Only do this if you understand the consequences. It can break your teammates' local repos.

### Scenario 6: "Oh no, I ran git reset --hard and lost my changes"

```bash
# Check the reflog — it records every HEAD movement for ~30 days
git reflog

# Find the state before the reset
# Restore HEAD to that state
git reset --hard HEAD@{2}
```

---

## 13. Tagging & Releases

### When to tag

At the end of each sprint, after merging everything into `main`:

```bash
git checkout main
git pull origin main
git merge develop
git tag -a sprint-1 -m "Sprint 1 - Auth & Registration"
git push origin main --tags
```

### Semantic versioning (if needed)

```
v1.0.0  ← Major.Minor.Patch
```

| Part | When to increment | Example |
|------|-------------------|---------|
| **Major** | Breaking changes (rewritten API) | v1.0.0 → v2.0.0 |
| **Minor** | New features (backward compatible) | v1.0.0 → v1.1.0 |
| **Patch** | Bug fixes | v1.0.0 → v1.0.1 |

### Viewing a specific version

```bash
# Checkout code as it was at a tag
git checkout sprint-1

# Create a branch from a tag (e.g., to patch an old release)
git checkout -b hotfix/patch-for-sprint-1 sprint-1
```

---

## 14. FAQ for Beginners

### Q1: What is the difference between `git pull` and `git fetch`?

- `git fetch` downloads changes from GitHub but does NOT apply them. You can inspect what changed before merging.
- `git pull` does `git fetch` + `git merge` in one step. It downloads AND applies changes.

Use `git fetch` when you want to see what your teammates did before integrating it. Use `git pull` for daily workflow.

### Q2: What does "detached HEAD" mean?

You see this message:
```
You are in 'detached HEAD' state.
```

This means you checked out a specific commit (or tag) instead of a branch. Your changes will not belong to any branch. To fix:

```bash
git checkout -b new-branch-name
```

This creates a branch at your current position.

### Q3: Why did Git say "Please tell me who you are"?

When you first use Git, it needs your name and email (used in commit history):

```bash
git config --global user.name "Prizma Chaudhary"
git config --global user.email "prizma@example.com"
```

Set these once and forget about it. The `--global` flag applies to all repositories on your machine.

### Q4: What should I NOT commit?

- `.env` files (secrets)
- `node_modules/` (run `npm install` locally)
- `venv/` (run `python -m venv venv` locally)
- Compiled files (`.pyc`, `.exe`, `.dll`)
- Large binary files (>50MB) — GitHub will reject them
- IDE settings (`.vscode/`, `.idea/`)
- Operating system files (`.DS_Store`, `Thumbs.db`)

### Q5: What is the difference between `git merge` and `git rebase`?

Both integrate changes, but they do it differently:

- **Merge** creates a new commit that joins two histories. The branch structure is preserved. Safe and straightforward.
- **Rebase** rewrites history by moving your commits to the tip of another branch. Creates a linear history but changes commit hashes.

**Rule for this project:** Always use `git merge`. Never use rebase on branches that others are working on.

### Q6: How do I fix a typo in my last commit message?

```bash
git commit --amend -m "[US-01] Fix typo in validation function"
```

**Warning:** If you already pushed the commit, you will need to force push:

```bash
git push --force-with-lease
```

Ask your team before force-pushing.

### Q7: I see "Your branch is ahead of 'origin/develop' by 3 commits" — what does this mean?

Your local branch has 3 commits that are not yet on GitHub. Push them:

```bash
git push origin <your-branch-name>
```

### Q8: How do I contribute to a PR review as a beginner?

1. Read the diff on GitHub (switch to the "Files changed" tab).
2. Look for anything that looks suspicious or different from what you would do.
3. Click the **+** icon next to any line to leave a comment.
4. Use the "Finish your review" button to submit.
5. Even "Looks good to me!" is a valid review.

### Q9: What does "fast-forward" mean during a merge?

If your branch is directly ahead of the branch you are merging into (no divergent changes), Git can simply move the branch pointer forward — no new merge commit needed. This is called a fast-forward.

When merging feature branches into `develop`, we sometimes use `--no-ff` to force a merge commit for traceability:

```bash
git merge --no-ff feature/US-01
```

### Q10: My teammate merged something that broke my code. What do I do?

1. Don't panic.
2. Run `git log --oneline develop` to find the breaking commit.
3. Communicate with your teammate.
4. Either:
   - They revert their commit: `git revert <commit-hash>`
   - Or you fix it in your branch and carry on.

---

## Appendix A: Full .gitignore template

```gitignore
# Dependencies
node_modules/
venv/
.virtualenvs/
.env
.env.local

# Python
*.pyc
__pycache__/
*.pyo
*.egg-info/
dist/
build/
*.egg

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
Desktop.ini

# Logs
*.log
npm-debug.log*

# Testing
.coverage
htmlcov/
.pytest_cache/

# Uploads (local development)
uploads/
media/

# Database (local)
*.sqlite3
*.db
```

---

## Appendix B: Quick reference card

```bash
╔══════════════════════════════════════════════════════════╗
║              QUICK REFERENCE — ONE-LINERS                ║
╠══════════════════════════════════════════════════════════╣
║                                                        ║
║  START OF SPRINT                                        ║
║  git checkout develop                                   ║
║  git pull origin develop                                ║
║  git checkout -b feature/US-XX-my-task                  ║
║                                                        ║
║  DAILY WORK                                             ║
║  git status                                             ║
║  git add <file>                                         ║
║  git commit -m "[US-XX] description"                    ║
║  git push origin feature/US-XX-my-task                  ║
║                                                        ║
║  FINISH FEATURE                                          ║
║  git checkout develop                                   ║
║  git pull origin develop                                ║
║  git checkout feature/US-XX-my-task                     ║
║  git merge develop                                      ║
║  # Fix conflicts if any                                 ║
║  git push origin feature/US-XX-my-task                  ║
║  # Create PR on GitHub                                  ║
║                                                        ║
║  AFTER PR MERGED                                        ║
║  git checkout develop                                   ║
║  git pull origin develop                                ║
║  git branch -d feature/US-XX-my-task                    ║
║                                                        ║
║  EMERGENCY FIX                                           ║
║  git checkout main                                      ║
║  git checkout -b hotfix/critical-fix                    ║
║  # Fix → commit → push                                  ║
║  # PR to main → merge → tag                             ║
║  # Also merge main into develop                         ║
║                                                        ║
║  TAG RELEASE                                            ║
║  git checkout main                                      ║
║  git pull origin main                                   ║
║  git tag -a sprint-1 -m "Sprint 1 release"              ║
║  git push origin main --tags                            ║
║                                                        ║
╚══════════════════════════════════════════════════════════╝
```

---

## Appendix C: Git configuration (one-time setup)

Each team member should run this once after installing Git:

```bash
# Your identity (shows in commit history)
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"

# Default branch name (new repos use "main" instead of "master")
git config --global init.defaultBranch main

# Use VSCode as default editor (optional)
git config --global core.editor "code --wait"

# Line endings (Windows)
git config --global core.autocrlf true

# Line endings (macOS/Linux)
git config --global core.autocrlf input

# Coloured output (easier to read)
git config --global color.ui auto
```

---

> **Remember:** Git is a tool, not a religion. This workflow is designed for three students working on a semester project. If something isn't working, talk to your teammates. The most important rule is not "follow the workflow perfectly" — it's **don't lose each other's work**.
>
> When in doubt: `git status`, `git log --oneline`, and ask your team.
