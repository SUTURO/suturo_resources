#ifndef _S_R_W_
#define _S_R_W_

#include <gazebo/common/Plugin.hh>
#include <gazebo/gui/GuiPlugin.hh>
#include <ros/ros.h>
#include <gazebo/common/common.hh>
#include "ros/callback_queue.h"
#include "ros/subscribe_options.h"
#include "std_msgs/String.h"
#include "rosgraph_msgs/Clock.h"
#include <thread>
#include <list>
#include <tuple>
#include <string>

// moc parsing error of tbb headers
#ifndef Q_MOC_RUN
#include <gazebo/transport/transport.hh>
#endif

namespace gazebo
{
    //GAZEBO_VISIBLE
    class GAZEBO_VISIBLE StringRendererWidget : public GUIPlugin
    {
        Q_OBJECT
        /// \brief Constructor
        public: StringRendererWidget();
        /// \brief Deconstructor
        public: virtual ~StringRendererWidget();

        /// \brief A signal used to set the sim time line edit.
        /// \param[in] _string String representation of sim time.
        signals: void SetSentence(QString _string);

        /// Handle an incoming String message from ROS
        private: void OnTextMsg(const std_msgs::StringConstPtr &_msg);
        private: void onClock(const rosgraph_msgs::ClockConstPtr &_msg);
        /// \brief ROS helper function that processes messages
        private: void QueueThread();

        /// \brief A node use for ROS transport
        private: std::unique_ptr<ros::NodeHandle> rosNode;
        /// \brief A ROS subscriber
        private: ros::Subscriber rosSub1;
        private: ros::Subscriber rosSub2;
        /// \brief A ROS callbackqueue that helps process messages
        private: ros::CallbackQueue rosQueue;
        /// \brief A thread the keeps running the rosQueue
        private: std::thread rosQueueThread;
        private: std::list<std::tuple <std::string, unsigned int>> sentencesWithTime;
        private: unsigned int currentSimTime;
        private: static unsigned int displayTime;
    };
}

#endif

