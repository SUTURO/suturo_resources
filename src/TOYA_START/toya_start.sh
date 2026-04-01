#!/bin/bash

TERMINAL1_COMMAND="$1"
TERMINAL2_COMMAND="$2"
TERMINAL3_COMMAND="$3"
TERMINAL4_COMMAND="$4"
TERMINAL6_COMMAND="$5"
TERMINAL10_COMMAND="$6"

# Escapen, damit Semikolons etc. korrekt in bash -c laufen
export TERMINAL1_COMMAND
export TERMINAL2_COMMAND
export TERMINAL3_COMMAND
export TERMINAL4_COMMAND
export TERMINAL6_COMMAND
export TERMINAL10_COMMAND

terminator --config ~/TOYA_START/toya_start_terminator_config.conf -l quad



