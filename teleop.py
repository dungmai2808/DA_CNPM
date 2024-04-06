import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(
            String,
            'teleop',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        data = json.loads(msg.data)  # Parse JSON string into a Python dictionary
        twist = Twist()

        # Extract the velocity components from the JSON data
        x = data.get('x', 0.0)
        y = data.get('y', 0.0)
        z = data.get('z', 0.0)
        th = data.get('th', 0.0)

        # Set the linear and angular velocity components
        twist.linear.x = x
        twist.linear.y = y
        twist.linear.z = z
        twist.angular.z = th

        # Publish the Twist message
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)

    teleop_node = TeleopNode()

    rclpy.spin(teleop_node)

    teleop_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
