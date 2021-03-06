cmake_minimum_required(VERSION 2.8.3)
project(tracking_rviz_plugin)

find_package(catkin REQUIRED COMPONENTS rviz tracking_msgs human_attribute_msgs social_relation_msgs)
catkin_package()
include_directories(${catkin_INCLUDE_DIRS})
link_directories(${catkin_LIBRARY_DIRS})



## This plugin includes Qt widgets, so we must include Qt.
## We'll use the version that rviz used so they are compatible.
if(rviz_QT_VERSION VERSION_LESS "5")
  message(STATUS "Using Qt4 based on the rviz_QT_VERSION: ${rviz_QT_VERSION}")
  find_package(Qt4 ${rviz_QT_VERSION} EXACT REQUIRED QtCore QtGui)
  ## pull in all required include dirs, define QT_LIBRARIES, etc.
  include(${QT_USE_FILE})
  qt4_wrap_cpp(MOC_FILES
  src/detected_persons_display.h
  src/tracked_persons_display.h
  src/tracked_groups_display.h
  src/social_relations_display.h
  src/social_activities_display.h
  src/human_attributes_display.h
  src/person_display_common.h
  src/additional_topic_subscriber.h
)
else()
  message(STATUS "Using Qt5 based on the rviz_QT_VERSION: ${rviz_QT_VERSION}")
  find_package(Qt5 ${rviz_QT_VERSION} EXACT REQUIRED Core Widgets)
  ## make target_link_libraries(${QT_LIBRARIES}) pull in all required dependencies
  set(QT_LIBRARIES Qt5::Widgets)
  qt5_wrap_cpp(MOC_FILES
  src/detected_persons_display.h
  src/tracked_persons_display.h
  src/tracked_groups_display.h
  src/social_relations_display.h
  src/social_activities_display.h
  src/human_attributes_display.h
  src/person_display_common.h
  src/additional_topic_subscriber.h
)
endif()

add_definitions(-DQT_NO_KEYWORDS)



set(SOURCE_FILES
  src/detected_persons_display.cpp
  src/tracked_persons_display.cpp
  src/tracked_groups_display.cpp
  src/social_relations_display.cpp
  src/social_activities_display.cpp
  src/human_attributes_display.cpp
  src/person_display_common.cpp
  src/tracked_persons_cache.cpp
  src/visuals/person_visual.cpp
  ${MOC_FILES}
)


add_library(${PROJECT_NAME} ${SOURCE_FILES})
add_dependencies(${PROJECT_NAME} ${catkin_EXPORTED_TARGETS}) # for generation of message dependencies
target_link_libraries(${PROJECT_NAME} ${QT_LIBRARIES} ${catkin_LIBRARIES})


install(TARGETS
  ${PROJECT_NAME}
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(FILES 
  plugin_description.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

install(DIRECTORY media/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/media)

install(DIRECTORY icons/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/icons)

install(PROGRAMS scripts/send_test_msgs.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
