@echo off
REM Starts the Django backend and the Vite frontend together in one window.
REM Press Ctrl+C once to stop both.

cd /d "%~dp0"
npm run dev
