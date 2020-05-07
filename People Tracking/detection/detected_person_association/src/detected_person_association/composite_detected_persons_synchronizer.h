#ifndef _COMPOSITE_DETECTED_PERSONS_SYNCHRONIZER_H
#define _COMPOSITE_DETECTED_PERSONS_SYNCHRONIZER_H

#include <boost/thread.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/ptr_container/ptr_vector.hpp>

#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>

#include <tracking_msgs/CompositeDetectedPersons.h>

namespace detected_person_association
{
/// Abstract base class that synchronizes multiple tracking_msgs/CompositeDetectedPersons input topics, and creates a publisher for outputting tracking_msgs/CombinedDetectedPersons.
/// The specialty of this class is that it automatically reconfigures its message filters (synchronizers) if any of the subscribed topics goes down, or a new one becomes available.
/// This means that if e.g. the rear laser detector goes down, the front laser detections will still be output. Normally, this would cause the output to stop completely.
class CompositeDetectedPersonsSynchronizer
{
public:
    /// Must be called by derived class in onInit().
    void initSynchronizer(const std::string &nodeletName, ros::NodeHandle nodeHandle, ros::NodeHandle privateNodeHandle, int minNumInputTopics = 1, int maxNumInputTopics = 9);

    virtual ~CompositeDetectedPersonsSynchronizer();

protected:
    /// Must be overriden by derived classes to process the input messages.
    virtual void onNewInputMessagesReceived(const std::vector<tracking_msgs::CompositeDetectedPersons::ConstPtr> &inputMsgs) = 0;

    // Publisher for output tracking_msgs::CompositeDetectedPersons
    boost::shared_ptr<ros::Publisher> m_publisher;

private:
    //
    // Synchronizers, subscribers and callbacks
    //

    // -- Variables used regardless of number of input topics -- //
    ros::NodeHandle m_nodeHandle, m_privateNodeHandle;

    typedef message_filters::Subscriber<tracking_msgs::CompositeDetectedPersons> SubscriberType;
    boost::ptr_vector<SubscriberType> m_subscribers;
    message_filters::Connection m_currentCallback;

    typedef std::vector<SubscriberType *> ActiveTopics;
    ActiveTopics m_previouslyActiveTopics;

    int m_agePenalty, m_queueSize;
    double m_topicMonitorInterval;
    boost::thread m_monitorThread;
    boost::mutex m_monitorMutex;

    std::string m_nodeletName;

    // --- Synchronizer management --- //

    // Executed in a separate thread, continuously monitors if the number of active topics has changed.
    void monitorActiveTopics();

    // Determines which of the subscribed topics are active (=have publishers)
    ActiveTopics determineActiveTopics();

    // Sets up new synchronizers if the count of active topics has changed
    void setupSynchronizers(ActiveTopics &activeTopics);

    // --- Callback handling --- //

    void handleNewInputMessages(const std::vector<tracking_msgs::CompositeDetectedPersons::ConstPtr> &inputMsgs);

    // --- For ONE input topic (=no synchronization!) -- //
    void onSingleInputMessageReceived(tracking_msgs::CompositeDetectedPersons::ConstPtr msg);

    // --- For TWO input topics -- //
    void onTwoInputMessagesReceived(tracking_msgs::CompositeDetectedPersons::ConstPtr msg1, tracking_msgs::CompositeDetectedPersons::ConstPtr msg2);

    typedef message_filters::sync_policies::ApproximateTime<tracking_msgs::CompositeDetectedPersons, tracking_msgs::CompositeDetectedPersons> SyncPolicyWithTwoInputs;
    typedef message_filters::Synchronizer<SyncPolicyWithTwoInputs> SynchronizerWithTwoInputs;
    boost::shared_ptr<SynchronizerWithTwoInputs> m_synchronizerWithTwoInputs;
};
} // namespace detected_person_association

#endif // _COMPOSITE_DETECTED_PERSONS_SYNCHRONIZER_H
