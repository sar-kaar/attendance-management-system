#!/usr/bin/env bash
# Starts the Django backend and the Vite frontend together (Linux/macOS).
# Linux equivalent of run.bat.  Press Ctrl+C once to stop both.
set -euo pipefail

# Move to the directory containing this script.
cd "$(dirname "$(readlink -f "$0")")"

# Pick a Python interpreter: prefer the Linux virtualenv, fall back to system python.
if [ -x "backend/.venv/bin/python" ]; then
    PYTHON="$PWD/backend/.venv/bin/python"
else
    PYTHON="$(command -v python3 || command -v python)"
    echo "WARN: backend/.venv not found, using system Python: $PYTHON" >&2
fi

# Ensure frontend dependencies are installed for THIS platform.
# node_modules is platform-specific (Vite's rolldown ships a native binary), so a
# tree copied from Windows won't have the Linux binding. Reinstall when either the
# folder is missing or the native binding for this arch is absent.
ensure_frontend_deps() {
    local arch binding
    arch="$(uname -m)"; [ "$arch" = "x86_64" ] && arch="x64"
    binding="frontend/node_modules/@rolldown/binding-linux-${arch}-gnu"
    if [ ! -d "frontend/node_modules" ]; then
        echo ">> Installing frontend dependencies (node_modules missing)..."
        ( cd frontend && npm install )
    elif [ ! -d "$binding" ]; then
        echo ">> Reinstalling frontend dependencies (Linux native binding missing)..."
        rm -rf frontend/node_modules
        ( cd frontend && npm install )
    fi
}
ensure_frontend_deps

# Free the dev ports before starting, so a leftover server from a previous run
# (e.g. one closed without Ctrl+C) doesn't cause "That port is already in use".
BACKEND_PORT=8000
FRONTEND_PORT=5173
free_port() {
    local port="$1" pids
    if command -v lsof >/dev/null 2>&1; then
        pids="$(lsof -ti "tcp:${port}" -sTCP:LISTEN 2>/dev/null || true)"
    elif command -v fuser >/dev/null 2>&1; then
        pids="$(fuser "${port}/tcp" 2>/dev/null || true)"
    fi
    if [ -n "${pids:-}" ]; then
        echo ">> Freeing port ${port} (killing: ${pids})"
        # shellcheck disable=SC2086
        kill -9 ${pids} 2>/dev/null || true
    fi
}
free_port "$BACKEND_PORT"
free_port "$FRONTEND_PORT"

# Ensure both child processes are killed when this script exits or is interrupted.
pids=()
cleanup() {
    trap - INT TERM EXIT
    for pid in "${pids[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
    wait 2>/dev/null || true
}
trap cleanup INT TERM EXIT

# Backend: Django dev server
( cd backend && exec "$PYTHON" manage.py runserver "$BACKEND_PORT" ) &
pids+=("$!")

# Frontend: Vite dev server
( cd frontend && exec npm run dev ) &
pids+=("$!")

# Wait for either process to exit; cleanup() then stops the other.
wait -n
