cmake_minimum_required(VERSION 3.8)
project(ana_1_1)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

# Define the executable for the controller
add_executable(controller_node src/controller.cpp)
ament_target_dependencies(controller_node
  rclcpp
  std_msgs
  geometry_msgs
)

# Set the include directories
target_include_directories(controller_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/meshes>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/worlds>
  $<INSTALL_INTERFACE:include>)

# Set the required C++ standard
target_compile_features(controller_node PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17

# Install the executable
install(TARGETS
  controller_node
  DESTINATION lib/${PROJECT_NAME})

# Install all directories needed
install(DIRECTORY 
  ${CMAKE_CURRENT_SOURCE_DIR}/meshes
  ${CMAKE_CURRENT_SOURCE_DIR}/worlds
  ${CMAKE_CURRENT_SOURCE_DIR}/launch
  ${CMAKE_CURRENT_SOURCE_DIR}/description
  ${CMAKE_CURRENT_SOURCE_DIR}/config
  DESTINATION share/${PROJECT_NAME}/
  FILES_MATCHING PATTERN "*.stl" PATTERN "*.urdf" PATTERN "*.mesh" PATTERN "*.world" PATTERN "*.sdf" PATTERN "*.xacro" PATTERN "*.rviz" PATTERN "*.yaml")

install(DIRECTORY launch/
    DESTINATION share/${PROJECT_NAME}/launch
    FILES_MATCHING PATTERN "*.launch.py"
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
