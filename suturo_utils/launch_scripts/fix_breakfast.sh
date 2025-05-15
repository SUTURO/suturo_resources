#!/bin/bash

# Session Name
SESSION="hsr-session"

# Kill existing session if it exists
tmux kill-session -t $SESSION 2>/dev/null

# Start new session in detached mode
tmux new-session -d -s $SESSION

tmux split-window -h -t "$SESSION"
tmux split-window -v -t "$SESSION:0.0"
tmux split-window -v -t "$SESSION:0.2"
tmux send-keys -t "$SESSION:0.0" 'hotfix' C-m
tmux send-keys -t "$SESSION:0.1" 'hotfix' C-m
tmux send-keys -t "$SESSION:0.2" 'hotfix' C-m
tmux send-keys -t "$SESSION:0.3" 'hotfix' C-m

tmux send-keys -t "$SESSION:0.0" 'roslaunch suturo_bringup GermanOpen_bringup.launch' C-m
tmux send-keys -t "$SESSION:0.1" 'robokudo_venv && rosrun robokudo main.py _ae=serve_breakfast _ros_pkg=milestone1' C-m
# Magic Number
sleep 2
tmux send-keys -t "$SESSION:0.2" 'roslaunch giskardpy_ros giskardpy_hsr_real_vel_with_kitchen.launch' C-m

# Attach to the session
tmux attach-session -t "$SESSION:0"
