import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraPublisher(Node):
    def __init__(self, resolution=(320, 240), queue_size=10):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, 'image_raw', queue_size)
        self.bridge = CvBridge()
        self.camera_resolution = resolution

    def capture_and_publish(self):
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            print("Error: Unable to open camera.")
            return

        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_resolution[0])
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_resolution[1])

        while True:
            ret, frame = capture.read()
            if not ret:
                print("Error: Unable to capture frame.")
                continue

            # Resize frame to desired resolution
            frame_resized = cv2.resize(frame, self.camera_resolution)

            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

            # Convert OpenCV image to ROS Image message
            ros_image_msg = self.bridge.cv2_to_imgmsg(gray_frame, encoding="mono8")

            # Publish ROS Image message
            self.publisher_.publish(ros_image_msg)

def main(args=None):
    rclpy.init(args=args)
    camera_resolution = (160, 120)  # Adjust the desired resolution here
    camera_publisher = CameraPublisher(resolution=camera_resolution, queue_size=10)
    try:
        camera_publisher.capture_and_publish()
    except KeyboardInterrupt:
        pass

    camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
