import cv2

def capture_image():
    # Open the webcam (change index if you have multiple cameras)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Couldn't open the webcam.")
        return

    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Display the captured frame
        cv2.imshow("Captured Image", frame)
        cv2.waitKey(0)  # Wait indefinitely until any key is pressed

        # Save the captured image
        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured and saved as 'captured_image.jpg'.")

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_image()
