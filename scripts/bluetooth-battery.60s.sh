#!/usr/bin/env bash

# Load configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../secrets/bluetooth-battery.sh"

# Try alternative locations
if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE="$HOME/.config/argos/secrets/bluetooth-battery.sh"
fi

if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    echo "🎧: ⚠️ Config not found"
    exit 1
fi

battery_info=$(bluetoothctl info "$BLUETOOTH_MAC" | grep 'Battery Percentage' | awk -F'[()]' '{print $2}')

if [[ -z $battery_info ]]; then
    echo "🎧: 🔴"
    exit 0
fi

color="#00bb00"
if (( battery_info <= 20 )); then
    color="#bb0000"
elif (( battery_info <= 50 )); then
    color="#ddbb00"
fi

output="🎧: "
for i in {1..10}; do
    if [[ $i -le $((battery_info / 10)) ]]; then
        output+="<span color='$color'>█</span>"
    else
        output+="<span color='#666666'>░</span>"
    fi
done

echo "{ $output $battery_info% }"

