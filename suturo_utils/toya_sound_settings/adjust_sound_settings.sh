#!/bin/bash

# Desired output and input device names (can also be passed as arguments)
DESIRED_OUTPUT="${1:-Pebble_V3}"
DESIRED_INPUT="${2:-VideoMic_NTG}"
OUTPUT_VOLUME="80%"  # Set desired output volume (adjust if needed)

# Get the corresponding sink (output) index
OUTPUT_INDEX=$(pactl list short sinks | grep "$DESIRED_OUTPUT" | awk '{print $1}')

# Get the corresponding source (input) index, ensuring it starts with "alsa_input"
INPUT_INDEX=$(pactl list short sources | grep "alsa_input.*$DESIRED_INPUT" | awk '{print $1}')

# Check if output device was found
if [ -n "$OUTPUT_INDEX" ]; then
    echo "Setting default output to: $OUTPUT_INDEX"
    pactl set-default-sink "$OUTPUT_INDEX"
    
    # Set output volume to the fixed level
    echo "Setting output volume to $OUTPUT_VOLUME"
    pactl set-sink-volume "$OUTPUT_INDEX" "$OUTPUT_VOLUME"
else
    echo "Error: No output device matching '$DESIRED_OUTPUT' found."
fi

# Check if input device was found
if [ -n "$INPUT_INDEX" ]; then
    echo "Setting default input to: $INPUT_INDEX"
    pactl set-default-source "$INPUT_INDEX"
else
    echo "Error: No input device matching '$DESIRED_INPUT' found."
fi

# Show confirmation
echo "Current default sink (output):"
pactl get-default-sink
echo "Current default source (input):"
pactl get-default-source

