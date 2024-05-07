#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/int32.hpp>
#include <geometry_msgs/msg/twist.hpp>

class RobotController : public rclcpp::Node
{
public:
  RobotController() : Node("robot_controller")
  {
    // Publisher for velocity commands
    vel_pub = this->create_publisher<geometry_msgs::msg::Twist>("/model/ana_robot/cmd_vel", 10);

    // Subscriber to keyboard key press
    key_sub = this->create_subscription<std_msgs::msg::Int32>(
      "/keyboard/keypress", 10, std::bind(&RobotController::keyCallback, this, std::placeholders::_1));
  }

  void keyCallback(const std_msgs::msg::Int32::SharedPtr msg)
  {
    geometry_msgs::msg::Twist twist;

    // Depending on the key pressed, set the velocities
    switch (msg->data) {
      case 16777235: // Forward
        if (last_command != "forward") {
          resetVelocities();
        }
        twist.linear.x = 0.5;
        last_command = "forward";
        break;
      case 16777237: // Backward
        if (last_command != "backward") {
          resetVelocities();
        }
        twist.linear.x = -0.5;
        last_command = "backward";
        break;
      case 16777234: // Left
        if (last_command != "left") {
          resetVelocities();
        }
        twist.angular.z = 1.0;
        last_command = "left";
        break;
      case 16777236: // Right
        if (last_command != "right") {
          resetVelocities();
        }
        twist.angular.z = -1.0;
        last_command = "right";
        break;
      default:
        // If an unexpected key is pressed, do nothing
        return;
    }

    // Publish the command
    vel_pub->publish(twist);
  }

  void resetVelocities()
  {
    // Publish zero velocities to stop the robot
    geometry_msgs::msg::Twist twist;
    vel_pub->publish(twist);
    rclcpp::sleep_for(std::chrono::milliseconds(100)); // short delay to ensure the zero command is applied
  }

private:
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub;
  rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr key_sub;
  std::string last_command;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto controller = std::make_shared<RobotController>();
  rclcpp::spin(controller);
  rclcpp::shutdown();
  return 0;
}
