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
tmux send-keys -t "$SESSION:0.0" 'hsr' C-m
tmux send-keys -t "$SESSION:0.1" 'hsr' C-m
tmux send-keys -t "$SESSION:0.2" 'hsr' C-m
tmux send-keys -t "$SESSION:0.3" 'hsr' C-m

# map bekannt bzw in der nähe der bekannten map cml
tmux send-keys -t "$SESSION:0.0" 'roslaunch suturo_bringup suturo_tab.launch' C-m

tmux send-keys -t "$SESSION:0.0" 'roslaunch suturo_bringup cml_test.launch' C-m
tmux send-keys -t "$SESSION:0.1" 'robokudo_venv && rosrun robokudo main.py _ae=query_human_tracking_hsr _ros_pkg=robokudo_robocup_cml' C-m

# Magic Number
sleep 2
tmux send-keys -t "$SESSION:0.2" 'roslaunch giskardpy_ros giskardpy_hsr_real_vel_with_kitchen.launch' C-m

tmux new-window
tmux split-window -h -t "$SESSION:1"
tmux split-window -v -t "$SESSION:1.0"
tmux split-window -v -t "$SESSION:1.2"
tmux send-keys -t "$SESSION:1.0" 'hsr && rosrun rqt_reconfigure rqt_reconfigure' C-m

# Attach to the session
tmux attach-session -t "$SESSION:0"
