cmake_minimum_required(VERSION 3.0.2)
project(rosbag-utils)


find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  rosbag
  rospy
  sensor_msgs
  std_msgs
  tf
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES rbop
#  CATKIN_DEPENDS cv_bridge rosbag rospy sensor_msgs std_msgs tf
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)