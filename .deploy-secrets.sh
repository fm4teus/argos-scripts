#!/bin/bash
SCRIPT="$1"
SCRIPT_BASE=$(basename "$SCRIPT")
SCRIPT_NAME="${SCRIPT_BASE%.*}"
SCRIPT_NAME="${SCRIPT_NAME%.[0-9]*s}"

if [ -f "secrets/$SCRIPT_NAME.py" ]; then
    cp "secrets/$SCRIPT_NAME.py" ~/.config/argos/secrets/
fi

if [ -f "secrets/$SCRIPT_NAME.sh" ]; then
    cp "secrets/$SCRIPT_NAME.sh" ~/.config/argos/secrets/
fi

