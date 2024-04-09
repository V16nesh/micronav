import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'data_topic',
            self.listener_callback,
            10)
        self.subscription  
        self.serial_port = serial.Serial('/dev/ttyS0', 9600, timeout=1) 

    def listener_callback(self, msg):
        received_data = msg.data
        self.get_logger().info('Received: "%s"' % received_data)
        self.send_serial_data(received_data)

    def send_serial_data(self, data):
        data_to_send = data.encode()
        self.serial_port.write(data_to_send)

def main(args=None):
    rclpy.init(args=args)
    subscriber_node = SubscriberNode()
    rclpy.spin(subscriber_node)
    subscriber_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()