# Intro
This document explains the TOYA_START terminal and startup setup. Its goal is to start the robot, NLP pipeline, and RoboKudo reliably with one command, while keeping everything understandable and maintainable.

# Big Picture
```
.bashrc inserts
 ├─ User-facing commands (aliases)
 ├─ Robot start orchestration (beep_bopp)
 ├─ NLP pipeline (Rasa + Whisper)
 ├─ RoboKudo helpers
 └─ Utility functions (waiting, cleanup, help)

help_text.txt
 └─ edit this for maintaining toya_help command

help_text_with_image.txt
 └─ generated with help_text.txt and toya.txt via toya_help_text_creator.py

toya.txt
 └─ ASCII art of Toya

toya_help_text_creator.py
 └─ execute this after changing help_text.txt to update the formatted help text (help_text_with_image.txt)

toya_start.sh
 └─ Opens Terminator with a predefined layout

toya_start_terminator_config.conf
 └─ Defines windows, splits, colors, and commands

```

# Setup
For the setup copy following code into the *.bashrc* file **and replace PATH with your path to the suturo_resources repository**. Also add your path to your local venvs in the `toya_help()` function and replace XXXXXXXXXX with the password and the other X's with the IP address for ssh.
## Code for bashrc
Copy this into your *.bashrc* file.
```bash
###################### Toya Start ###################### 
# starting the robot

alias beep_bopp_receptionist='beep_bopp nlp_rasa_receptionist_start receptionist'
alias beep_bopp_restaurant='beep_bopp nlp_rasa_restaurant_start restaurant'
alias beep_bopp_gpsr='beep_bopp nlp_rasa_gpsr_start gpsr'

# start robot with specific challenge like: beep_bopp nlp_rasa_gpsr_start gpsr
beep_bopp() {

    if [[ -n "$1" ]]; then
		RASA_CMD="$1"
	fi

	if [[ -n "$2" ]]; then
		RBKD_CMD="$2"
	fi

	export nlp_clean_start
	export RASA_CMD
	export RBKD_CMD
	
    source PATH1/suturo_resources/src/TOYA_START/toya_start.sh \
        "sshpass -p 'XXXXXXXXXX'  ssh -o PubkeyAuthentication=no -tt administrator@XXX.XXX.X.XXX 'sleep 2 ; source /opt/ros/humble/setup.bash ; export ROS_DOMAIN_ID=5 ; export ROS_IP=XXX.XXX.X.XXX ; export ROS_DOMAIN_ID=5 ; export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp ; export CYCLONEDDS_URI=/etc/opt/tmc/robot/cyclonedds_profile.xml ;   source ~/host_ws/install/setup.bash;  source ~/custom_controller_ws/install/setup.bash ; ros2 launch hsr_velocity_controller switch_to_velocity_controllers.launch.py ; exec bash'" \
        'sleep 5; source ~/cram-env/bin/activate; ros2 launch giskardpy_ros giskardpy_hsr_velocity.launch.py' \
        'rviz2' \
        'sleep 3; ros2 launch toya_slam map_server.launch.py' \
        "$RASA_CMD" \
        "$RBKD_CMD"
}

# show toya start help text
toya_help() {
    cat PATH1/suturo_resources/src/TOYA_START/help_text_with_image.txt
    ls -d PATH2/*/    # keep this updated with all venvs
}

# change and update helpfile
update_help_text() {
    cd PATH1/suturo_resources/src/TOYA_START
    nano help_text.txt
    python3 toya_help_text_creator.py
}

###################### robokudo  ######################
# default robokudo command
RBKD_CMD="receptionist"
rksetup() {
    source /opt/ros/jazzy/setup.bash
    source ~/robokudo_ws/install/setup.bash
    workon robokudo
}

# start with start_robokudo <challenge_name>, for example: 'start_robokudo gpsr'
start_robokudo() {
    local challenge=$1
    ros2 run robokudo main _ae="$challenge" _ros_pkg="robokudo_robocup_$challenge"
}

###################### NLP Start ######################
# Rasa execution
nlp_rasa_gpsr_start() {
	workon rasa_venv
	source ~/ros/nlp_ws/install/setup.bash
	cd ~/ros/nlp_ws/src/suturo_rasa/gpsr
	rasa run --enable-api
}

nlp_rasa_receptionist_start() {
	workon rasa_venv
	source ~/ros/nlp_ws/install/setup.bash
	cd ~/ros/nlp_ws/src/suturo_rasa/receptionist
	rasa run --enable-api
}

nlp_rasa_restaurant_start() {
	workon rasa_venv
	source ~/ros/nlp_ws/install/setup.bash
	cd ~/ros/nlp_ws/src/suturo_rasa/restaurant
	rasa run --enable-api
}

nlp_rasa_start() {
	workon rasa_venv
	source ~/ros/nlp_ws/install/setup.bash
	cd ~/ros/nlp_ws/src/suturo_rasa/demo_start_model
	rasa run --enable-api
}

# whisper execution
alias nlp_whisper_start="workon whisper_venv
source ~/ros/nlp_ws/install/setup.bash
source ~/ros/nlp_msg/install/setup.bash
python ~/ros/nlp_ws/src/suturo_nlp/activate_language_processing/scripts/nlp_mcrs.py"

# ros2 result output of spoken input
nlp_result() {
	wait_for_topic /nlp_out
	ros2 topic echo nlp_out -f
}

# ros2 nlp empty string sent in order to initialize input recognision
nlp_input_init() {
	ros2 topic pub /startListener std_msgs/msg/String "{data: ''}" --once
}


# nlp commands help
alias nlp_help="echo for boot you need: nlp_rasa_demo_start/nlp_rasa_gpsr_start/... , nlp_whisper_start, nlp_result, nlp_input_init"

# ---------- Config ----------
RASA_STATUS_URL="http://localhost:5005/status"
RASA_TIMEOUT=120
CHECK_INTERVAL=1

# ---------- Globals ----------
RASA_PID=""
WHISPER_PID=""
# default rasa command
RASA_CMD="nlp_rasa_start"

nlp_clean_start() {
    trap nlp_cleanup SIGINT

    if [[ -n "$1" ]]; then
	    RASA_CMD="$1"
    fi

    start_nlp "$RASA_CMD"
}


alias nlp_info="echo 'type nlp_clean_start to safely start the nlp pipeline'"

start_nlp() {
	trap nlp_cleanup SIGINT
	nlp_cleanup
	
	# if rasa model is given, replace default
	if [[ -n "$1" ]]; then
		RASA_CMD="$1"
	fi

	echo "▶ start_nlp using command: $RASA_CMD"

	if ! DO_NOT_CALL_start_nlp_nodes "$RASA_CMD"; then
		echo "Start failed / programm was interrupted"
	fi

	echo "NLP running"
	wait
}

DO_NOT_CALL_start_nlp_nodes() {
	
	trap nlp_cleanup SIGINT
	local cmd="$1"
	
	echo "Starting Rasa..."
	$cmd &
	RASA_PID=$!

	echo "Rasa PID: $RASA_PID"

	# ---------- Wait for Rasa ----------
	echo "Waiting for Rasa to become ready..."
	START_TIME=$(date +%s)

	while true; do
	  if curl -sf "$RASA_STATUS_URL" > /dev/null; then
	    echo "Rasa is ready"
	    break
	  fi

	  NOW=$(date +%s)
	  if (( NOW - START_TIME > RASA_TIMEOUT )); then
	    echo "Timeout waiting for Rasa"
	    cleanup
	  fi

	  sleep "$CHECK_INTERVAL"
	done

	# ---------- Start Whisper ----------
	echo "Starting Whisper..."
	nlp_whisper_start &
	WHISPER_PID=$!

	echo "Whisper PID: $WHISPER_PID"

	# ---------- Keep script alive ----------
	sleep 5
	echo "All services running. Press Ctrl+C to stop."
	wait
}


nlp_cleanup() {
	trap '' SIGINT
	echo

	echo "Running NLP cleanup"
	
	pkill -f "rasa"

	if [[ -n "${WHISPER_PID}" ]] && kill -0 "$WHISPER_PID" 2>/dev/null; then
	echo "Stopping Whisper ($WHISPER_PID)"
	kill "$WHISPER_PID"
	fi

	if [[ -n "${RASA_PID}" ]] && kill -0 "$RASA_PID" 2>/dev/null; then
	echo "Stopping Rasa ($RASA_PID)"
	kill -TERM -- "-$RASA_PID" 2>/dev/null || true
	fi

	sleep 3
	deactivate
	echo "Cleanup done"
	RASA_PID=""
	WHISPER_PID=""
}

# use like: wait_for_topic /your_topic
wait_for_topic() {
    local topic="$1"
    local timeout="${2:-0}"   # 0 = kein Timeout
    local start_time=$(date +%s)

    echo "waiting for topic: $topic"

    while true; do
        if ros2 topic list | grep -qx "$topic"; then
            echo "topic available: $topic"
            return 0
        fi

        if [[ "$timeout" -gt 0 ]]; then
            local now=$(date +%s)
            if (( now - start_time >= timeout )); then
                echo "timeout waiting for topic: $topic"
                return 1
            fi
        fi

        sleep 0.5
    done
}

```
## Replace Paths etc.
For the functions to work properly, you will have to change some paths, sorted by section.
### TOYA_START
- replace XXX.XXX.X.XXX with the robot ip adress
- replace XXXXXXXXXX with the ssh password for the robot
- install suturo_resources from github
- replace PATH1 with your path to the suturo_resources repository
- replace PATH2 with the path to your folder with all your venvs
- replace `source ~/cram-env/bin/activate` with your virtual environment for CRAM

### Robokudo
- for this you only need the robokudo_ws
- you need the workon command or have to replace it with sourcing your venv
- here the venv is named robokudo, replace if needed

### NLP
- install the nlp workspaces as written by NLP in the wiki 
- in suturo_rasa you should have following models as folder:
    - receptionist
    - restaurant
    - gpsr
    - demo\_start\_model
- you either need the workon command to start a venv or replace it with sourcing the path to activate the venv
- here the venvs are named rasa\_venv and whisper\_venv, replace if yours are named different


Now everything should be set up properly.

# Required tools
- terminator
- sshpass
- ROS 2 (Humble + Jazzy)
- Python virtualenvs (or workon)
- Rasa
- Whisper
- curl

# Explanation of the important commands
## beep_bopp
This is the command to start the robot. It will open two terminal windows and automatically execute the commands needed for starting the robot. There will be multiple labeled terminals in one window.

Color explanation: Dark green terminals are 'working terminals' means they can be used for working (window 2) or have a higher potential to need a restart (window 2 because of localization stuff).

**Warning:** This command loads a terminator config, therefore it can **only be started in the 'Terminal' app** while no Terminator windows are open, because if Terminator is started with one config, it can not load another one.

### beep_bopp <challenge_nlp> <challenge_robokudo>
To start beep\_bopp with a particular challenge, replace challenge\_nlp with `nlp_rasa_challenge_start` and insert your challenge name for `challenge` and replace challenge\_robokudo with the name of your challenge, for example: `beep_bopp nlp_rasa_gpsr_start gpsr`.
This also makes it possible to start the nlp model of one challenge and the robokudo model of another.

### beep_bopp <challenge>
with challenge being: `gpsr`, `receptionist`, `restaurant`

This way you can start beep\_bopp with the nlp model and robokudo model of the above-named challenges.

## toya_help
Shows the help text on how to use Toya and lists your Virtual Environments.

## update_help_text
- opens the help text in nano for editing
- after that automatically runs a script to format the help text in a column next to the image

**Warning:** 
The line length in the unformatted help text is the same as in the formatted version with the picture. Please orientate the line length on the existing lines to keep the formatting on the terminal clean.

**If you don't like nano:**
Just edit the file *help_text.txt* in the TOYA_START folder. After that run the command:
`python3 PATH/suturo_resources/src/TOYA_START/toya_help_text_creator.py`

Now the formatted help text is updated.

## nlp_clean_start <challenge>
This starts the NLP pipeline. When interrupted with ctrl+c, it executes a cleanup to properly close all nlp related processes.

## nlp_cleanup
If nlp processes are accidentally not terminated properly, use this function to close rasa and whisper, so the old rasa process won't block port 5005.

## wait_for_topic /topic
Use this function to wait until one topic gets published.

## nlp_help
Shows commands for manually starting the nlp pipeline.

## nlp_info
Shows commands to start and end the nlp pipeline via commands.

## nlp_input_init
Starts the recording of the nlp input.

## start_robokudo <challenge>
Starts robokudo for a specific challenge.



### window 1
**Terminal_Label: Toya**:
Commands:
- sshpass and ssh to connect with the robot
- source to find all packages etc.
- launch velocity controller
- show docker logs on robot for debugging

This terminal is responisble for the connection with the robot.

**Terminal_Label: Giskard**:
Commands:
- sleep 5 (gives enough time to establish connection with robot first)
- start giskard (only works if velocity controller is already launched on robot)

This terminal is responsible for giskard.

**Terminal_Label: RVIZ2**:
Commands:
- rviz2

This terminal starts and runs RVIZ2. It has to started before the map. 

**Terminal_Label: Toya_Map**:
Commands:
- sleep 3 (gives enough time to start RVIZ2 first
- launch map_server

Publishes the map, has to be started after RVIZ2.

### window 2
**Terminal_Label: Toya_Help**:
Shows a help text on how to use the robot with a beautiful picture of Toya with sunglasses and a bow on her head.



### window 3
**Terminal_Label: Rasa_and_Whisper**:
Starts Rasa and after successful launch Whisper.

**Terminal_Label: NLP Output**:
Shows all messages published on the topic nlp_out.

**Terminal_Label: Working terminal**:
Extra terminal, can be used for own things.

**Terminal_Label: NLP Init**:
Publishes the message to start recording for input via nlp.


### window 4
**Terminal_Label: rksetup**:
Starts robokudo with model for challenge.
**Terminal_Label: robokudo stuff**:
Terminal for sending queries.


```
............................................................
............................................................
............................................................
......................=-:..............:....................
.....................=======:......:=====..........=*.......
....................:--::..:==-::==-:::-:..---:..-*-+*-.....
..................-+=====--:.:::::::----..----:-****+.......
.................:+++-::---::... .--===-:.    -****.........
...................   ---::         :--- ..   .==:..........
.................     ..   ..................   -:..........
.................  .::::::::::::.............. .-...........
.................  :::::::::::::............   .............
................   ::::::::::::.............   :-...........
...............:  .:::::::::::..............   -:...........
...............   ::::::::::...............    -:...........
...............  .....::...................   .-............
...............  .........................#%+ --............
.....+::-..:---------------------.     --+@%%%%=............
.....*        .  :   ..           .. :    +++===- ..........
.....+.      - ::   :==-         -. -   .@@%%%%%*...........
.....*:::   .-----===-===-            .:+@%%%%%%=...........
.....@=.:=--+============--------....:-#@@%%%%%%:...........
.....@@@#+==============---====--==*#@@@@%%%%%%#............
.....@@@@@@@@%%%%%%%%%%%%%%%%%%@@@@@@@@@@%%%%%%-............
.....*@@@@@@@%#%###***********#@@@@@@@@@%%%%#=..............
.....:@@@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@%%%#................
......%%%%%%%#@@@@@@@@@@@@@@@@%@@@@@@@@%%%#.................
.......%%%%%%*%%%%%%%%%%%%%%%%%%%%%%%%%%%#..................
........*####%%%%%%%%%%%%%%%%%#%%%%%%%%%#...................
..............-%%%%%%%%%%%%%%%%*#######=....................
..........=@@%@@@@@@@@@@@@@@@@%@%###........................
.............#%%%%%%%%%%@@@%%@@@@@@@@@@%=...................
................-@@@@@@@@@@@%@@@@@@@@@@@+...................
.....................:=%@@@@@@@@@@*:........................
............................................................
............................................................
............................................................
```

