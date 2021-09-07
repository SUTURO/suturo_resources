#include <sstream>
#include <gazebo/msgs/msgs.hh>
#include <gazebo/transport/transport.hh>
#include <gazebo/common/Plugin.hh>
#include <gazebo/gui/GuiPlugin.hh>
#include <ros/ros.h>
#include <gazebo/common/common.hh>
#include <ros/callback_queue.h>
#include <ros/subscribe_options.h>
#include <std_msgs/String.h>
// #include <tmc_msgs/TalkRequestActionGoal.h>
#include <tmc_msgs/Voice.h>
#include <rosgraph_msgs/Clock.h>
#include <thread>
#include <list>
#include <tuple>
#include <string>

#include "SRW.hh"
using namespace gazebo;

// Register this plugin with the simulator
GZ_REGISTER_GUI_PLUGIN(StringRendererWidget)

// GZ_PLUGIN_VISIBLE
StringRendererWidget::StringRendererWidget() : GUIPlugin()
{
    // Make sure the ROS node for Gazebo has already been initialized
    // Initialize ros, if it has not already bee initialized.
    if (!ros::isInitialized()) {
         std::cerr << "\n Plugin failed to load\n";
        ROS_FATAL_STREAM("A ROS node for Gazebo has not been initialized, unable to load ShowText plugin.");
        return;
    }
    // Create our ROS node. This acts in a similar manner to
    // the Gazebo node
    this->rosNode.reset(new ros::NodeHandle("gazebo_client"));

    // Set the frame background and foreground colors
    this->setStyleSheet("QFrame { background-color : rgba(100, 100, 100, 255); color : white; }");

    // Create the main layout
    QHBoxLayout *mainLayout = new QHBoxLayout;
    // Create the frame to hold all the widgets
    QFrame *mainFrame = new QFrame();
    // Create the layout that sits inside the frame
    QHBoxLayout *frameLayout = new QHBoxLayout();
    QLabel *label = new QLabel(tr("Toya said:"));
    // Create a sentence label (where the senteces go
    QLabel *sentenceLabel = new QLabel(tr("Simulator not started."));
    // Add the label to the frame's layout
    frameLayout->addWidget(label);
    frameLayout->addWidget(sentenceLabel);

    connect(this, SIGNAL(SetSentence(QString)),
        sentenceLabel, SLOT(setText(QString)), Qt::QueuedConnection);
    // Add frameLayout to the frame
    mainFrame->setLayout(frameLayout);
    // Add the frame to the main layout
    mainLayout->addWidget(mainFrame);
    // Remove margins to reduce space
    frameLayout->setContentsMargins(4, 4, 4, 4);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    this->setLayout(mainLayout);
    // Position and resize this widget
    this->move(10, 10);
    this->adjustSize();

    // Subscribe to both /talk_request(get the sentence) and /clock (get the sim time)
    ros::SubscribeOptions so1 =
            ros::SubscribeOptions::create<tmc_msgs::Voice>(
                    "/talk_request",
                    1,
                    boost::bind(&StringRendererWidget::OnVoiceMsg, this, _1),
                    ros::VoidPtr(), &this->rosQueue);
    ros::SubscribeOptions so2 =
            ros::SubscribeOptions::create<rosgraph_msgs::Clock>(
                    "/clock",
                    1,
                    boost::bind(&StringRendererWidget::onClock, this, _1),
                    ros::VoidPtr(), &this->rosQueue);

    this->rosSub1 = this->rosNode->subscribe(so1);
    this->rosSub2 = this->rosNode->subscribe(so2);

    // Spin up the queue helper thread.
    this->rosQueueThread =
            std::thread(std::bind(&StringRendererWidget::QueueThread, this));
    this->currentSimTime = displayTime;
}


/////////////////////////////////////////////////
StringRendererWidget::~StringRendererWidget()
{
}


/// Handle an incoming String message from ROS
void StringRendererWidget::OnVoiceMsg(const tmc_msgs::VoiceConstPtr &_msg) {
    unsigned int time = currentSimTime;

    std::string sentence = _msg->sentence;

    auto tuple = std::make_tuple(sentence, time);

    sentencesWithTime.push_front(tuple);
}

/// handle an incoming Clock msg
void StringRendererWidget::onClock(const rosgraph_msgs::ClockConstPtr &_msg) {

    // every second
    if (this->currentSimTime < (_msg->clock.sec + displayTime)) {
        this->currentSimTime = _msg->clock.sec + displayTime;
        int i = 0;
        auto c = this->sentencesWithTime.begin();
        std::list<std::string> showedSentenceList;

        // determine wich sentences we  want to show
        // we show the senteces from the last displayTime seconds
        // but aleast one

        while ((this->currentSimTime - displayTime < std::get<1>(*c)) and (i < this->sentencesWithTime.size())) {
            showedSentenceList.push_back(std::get<0>(*c).c_str());
            i++;
            c = std::next(c, 1);
        }
        // for the case that we had no sentence in the last displayTime seconds
        if (showedSentenceList.size() == 0 and sentencesWithTime.size() > 0) {
            showedSentenceList.push_back(std::get<0>(*(this->sentencesWithTime.begin())).c_str());
        } 

        showedSentenceList.reverse(); //now we have the sentences we want from oldest to newest

        std::string showedSentence = ""; // The string we will be showing

        for(const auto& sentence : showedSentenceList){ //Fill the string
            showedSentence = showedSentence + "\n\n" + sentence;
        }
        if (showedSentence.size() > 0){
            showedSentence.erase(showedSentence.begin());
            showedSentence.erase(showedSentence.begin()); // Drop the first \n\n
        }

        this->setUpdatesEnabled(false); // Dont update while changing the content
        this->SetSentence(QString::fromStdString(showedSentence));
        this->adjustSize();
        this->setUpdatesEnabled(true);
        this->update();//force  update
    }
}

/// \brief ROS helper function that processes messages
void StringRendererWidget::QueueThread() {
    static const double timeout = 0.01;
    while (this->rosNode->ok()) {
        this->rosQueue.callAvailable(ros::WallDuration(timeout));
    }
}

unsigned int StringRendererWidget::displayTime = 30;
