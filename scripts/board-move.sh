#!/usr/bin/env bash
# Move GitHub Project (v2) items through the board: set Status (and optionally Sprint).
#
# PREREQUISITE: the gh token needs the `project` write scope. Grant it once with:
#     gh auth refresh -s project
# (the local token as of 2026-08-06 has only read:project, so writes fail without this.)
#
# Usage:
#     scripts/board-move.sh <issue-number> <todo|in-progress|done> [--sprint]
#
# Examples:
#     scripts/board-move.sh 36 in-progress          # Backend Readiness -> In Progress
#     scripts/board-move.sh 42 todo --sprint        # Push Notifications -> Todo, add to current Sprint
#     scripts/board-move.sh 23 done                 # ECA -> Done
set -euo pipefail

OWNER="sar-kaar"
PROJECT_NUMBER=5
PROJECT_ID="PVT_kwHOAwqSsc4Bc6Sj"
STATUS_FIELD_ID="PVTSSF_lAHOAwqSsc4Bc6SjzhXfqKc"
SPRINT_FIELD_ID="PVTIF_lAHOAwqSsc4Bc6SjzhY5KJc"

# Status single-select option IDs (from `gh project field-list 5 --owner sar-kaar --format json`).
declare -A STATUS_OPT=(
    [todo]="f75ad846"
    [in-progress]="47fc9ee4"
    [done]="98236657"
)

issue="${1:?issue number required}"
status="${2:?status required: todo|in-progress|done}"
want_sprint="${3:-}"

opt="${STATUS_OPT[$status]:-}"
if [ -z "$opt" ]; then
    echo "ERROR: status must be one of: todo | in-progress | done" >&2
    exit 1
fi

# Resolve the project item id for this issue number.
item_id="$(gh project item-list "$PROJECT_NUMBER" --owner "$OWNER" --format json \
    | python3 -c "import sys,json;d=json.load(sys.stdin);print(next(i['id'] for i in d['items'] if i.get('content',{}).get('number')==$issue))")"

echo ">> Issue #$issue -> Status=$status (item $item_id)"
gh project item-edit --id "$item_id" --project-id "$PROJECT_ID" \
    --field-id "$STATUS_FIELD_ID" --single-select-option-id "$opt"

if [ "$want_sprint" = "--sprint" ]; then
    # Current iteration id: first entry in the Sprint field's active iterations.
    iter_id="$(gh project field-list "$PROJECT_NUMBER" --owner "$OWNER" --format json \
        | python3 -c "import sys,json;d=json.load(sys.stdin);f=next(x for x in d['fields'] if x['id']=='$SPRINT_FIELD_ID');its=f.get('configuration',{}).get('iterations') or f.get('iterations') or [];print(its[0]['id'] if its else '')")"
    if [ -n "$iter_id" ]; then
        echo ">> Issue #$issue -> Sprint (iteration $iter_id)"
        gh project item-edit --id "$item_id" --project-id "$PROJECT_ID" \
            --field-id "$SPRINT_FIELD_ID" --iteration-id "$iter_id"
    else
        echo "WARN: no active Sprint iteration found; skipping sprint assignment" >&2
    fi
fi
echo ">> Done."
