# Team Sync Protocol (use every week, every day)

One page. Read this before you touch any task.

## Before you start work (any day)

1. Open Trello. Check your cards are still "To Do" and no one else moved them.
2. Run `git checkout develop && git pull origin develop`. See what teammates pushed since yesterday.
3. Post in Discord: "Starting on [task] now, branch `[branch-name]`." One line, before you start, not after.
4. If your task depends on someone else's file (schema, API contract, component), open that file first and confirm it exists and matches what you expected. Don't assume — check.
5. If you're behind schedule, say so now in Discord. Don't wait for standup.

## What to say at standup (10 min, every day, 9 AM)

Each person, in order: Prizma → Abhishek → Ekata

- Yesterday: what you finished (1 line)
- Today: what you're doing (1 line)
- Blockers: yes/no, what you need

PM writes down blockers and chases them same day.

## If something is off track (behind, broken, unclear)

1. Say it in standup or Discord immediately — don't hide it.
2. PM decides: cut scope, shift task to tomorrow, or ask teammate for help.
3. Never silently skip a task. Mark it "blocked" on Trello with a one-line reason.

## End of day (every day, everyone)

1. Log hours: Progress Tracker Sheet → **Personal Log** tab.
2. Log hours: Project Tracker Sheet → **Sprint Backlog** tab (Day column for today).
3. Move your Trello cards to the right list (To Do / In Progress / Review / Done).
4. Push all code: `git add . && git commit -m "[type] short description" && git push`.

Skip this and we lose burndown data — don't skip it.

## Links

- Personal Log: https://docs.google.com/spreadsheets/d/1eXQK5cUmhQcFO2-vORI2bhKRxO1QXZ_PUo57qQxKqUY
- Sprint Backlog: https://docs.google.com/spreadsheets/d/1B2m9trSqt1Vl2SHmgeCLXnJxx1nJuS3GUKxXHmV-cKM
- Trello: https://trello.com/b/tf3ceNmA
- GitHub: https://github.com/sar-kaar/attendance-management-system
