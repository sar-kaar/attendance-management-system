#!/bin/bash
set -e
# face-recognition's setup.py declares a hard dependency on plain "dlib", which
# has no prebuilt wheel and fails to build without cmake/a C++ toolchain. We
# already installed dlib-bin (prebuilt, same import name) via requirements.txt,
# so install face-recognition itself with --no-deps to avoid pip re-triggering
# a source build of plain dlib.
pip install --no-deps face-recognition==1.3.0

# Do NOT add migrate/collectstatic here. The App Service startup command
# (az webapp config show --query appCommandLine) already runs both before
# gunicorn on every container start. Duplicating them would just slow deploys.
