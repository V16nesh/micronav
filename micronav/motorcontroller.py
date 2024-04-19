import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial

class SerialPublisher(Node):
    def __init__(self):
        super().__init__('serial_publisher')
        self.serial_port = serial.Serial('/dev/ttyS0', 9600, timeout=0)  # Adjust the serial port and baud rate as needed
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )

    def cmd_vel_callback(self, msg):
        # Convert Twist message to serial command
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        if linear_x > 0:
            command = 'C frwd\n'
        elif linear_x < 0:
            command = 'C bwrd\n'
        elif angular_z > 0:
            command = 'C right\n'
        elif angular_z < 0:
            command = 'C left\n'
        else:
            command = 'C stop\n'

        if msg.angular.x == 85:  # 'U' key
            command = 'S up\n'
        elif msg.angular.x == 60:  # '<' key
            command = 'S mid\n'
        elif msg.angular.x == 79:  # 'O' key
            command = 'S down\n'

        # Send command over serial
        self.serial_port.write(command.encode())

def main(args=None):
    rclpy.init(args=args)
    serial_publisher = SerialPublisher()
    try:
        rclpy.spin(serial_publisher)
    finally:
        # Close serial port when shutting down
        serial_publisher.serial_port.close()
        serial_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
