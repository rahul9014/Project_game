import cv2

# Open the video file
cap = cv2.VideoCapture('vid3.mp4')

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Create a named window
cv2.namedWindow('Video Playback', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Video Playback', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Break the loop if the video has ended
    if not ret:
        break

    # Display the frame in a window
    cv2.imshow('Video Playback', frame)

    # Exit the video playback window when the space bar is pressed
    if cv2.waitKey(30) & 0xFF == 32:  # 32 is the ASCII code for space bar
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
