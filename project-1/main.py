import tkinter as tk
import cv2
import subprocess
# Create the main window
root = tk.Tk()

# Make the window full-screen
root.attributes('-fullscreen', True)

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the proportions (e.g., 45% white and 55% black)
white_width = int(screen_width * 0.45)
black_width = screen_width - white_width

# Create a frame for the left (white) part
left_frame = tk.Frame(root, bg="white", width=white_width, height=screen_height)
left_frame.pack(side="left", fill="y")

# Create a frame for the right (black) part
right_frame = tk.Frame(root, bg="black", width=black_width, height=screen_height)
right_frame.pack(side="right", fill="y")

# Add a container frame to position the buttons
button_frame = tk.Frame(left_frame, bg="white")
button_frame.place(relx=0.15, rely=0.5, anchor='center')  # Adjust relx to move further left

# Global variable for video capture
video = None

# Function to quit the GUI
def quit_gui():
    global video
    if video is not None:
        video.release()
    root.destroy()

# Function to change button text color to blue on hover
def on_enter(event):
    event.widget.config(fg="blue")

# Function to revert button text color when not hovering
def on_leave(event):
    event.widget.config(fg="black")

# Function to change button text color to blue when cursor is near
def on_motion(event):
    widget = event.widget
    x, y = event.x, event.y
    if 0 <= x <= widget.winfo_width() and 0 <= y <= widget.winfo_height():
        widget.config(fg="blue")
    else:
        widget.config(fg="black")

# Function to select a random element from the lists


# Function to be called when the Play button is pressed
def play_button_clicked():
    global video
    global stop_video

    # Set stop flag to False
    stop_video = False
    

    # Load the video
    video = cv2.VideoCapture('vid1.mp4')

    # Create a named window with full-screen flag
    cv2.namedWindow('Video Playback', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Video Playback', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Play the video
    while True:
        # Read each frame of the video
        ret, f = video.read()

        # If no more frames, break the loop
        if not ret:
            break

        # Display the frame in full screen
        cv2.imshow('Video Playback', f)

        # Stop video if space bar or 'q' is pressed
        k = cv2.waitKey(25) & 0xFF
        if k == ord('q') or k == ord(' '):
            stop_video = True
        
        # Check if stop flag is set
        if stop_video:
            break
    
    # Release the video object and close windows
    video.release()
    cv2.destroyAllWindows()
    quit_gui()
    subprocess.run(['python', 'test.py'])

# Function to stop video playback
def stop_video_playback(event=None):
    global stop_video
    stop_video = True

# Add buttons to the button_frame with increased size and no border
play_button = tk.Button(button_frame, text="Play", bg="white", fg="black", width=20, height=3, bd=0, highlightthickness=0, command=play_button_clicked)
play_button.pack(padx=10, pady=5)

how_to_play_button = tk.Button(button_frame, text="How to Play", bg="white", fg="black", width=20, height=3, bd=0, highlightthickness=0, command=lambda: start_transition(True))
how_to_play_button.pack(padx=10, pady=5)

quit_button = tk.Button(button_frame, text="Quit", bg="white", fg="black", width=20, height=3, bd=0, highlightthickness=0, command=quit_gui)
quit_button.pack(padx=10, pady=5)

# Bind events for color changes on hover and motion
for button in [play_button, how_to_play_button, quit_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<Motion>", on_motion)

# Add a label to the right_frame with "Welcome back"
welcome_label = tk.Label(right_frame, text="Welcome back", bg="black", fg="white", font=("Helvetica", 24))
welcome_label.place(relx=0.5, rely=0.5, anchor='center')

# Function to exit full-screen mode when 'Escape' key is pressed
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

# Bind the 'Escape' key to exit full-screen mode
root.bind("<Escape>", exit_fullscreen)

# Bind the space key to stop video playback
root.bind("<space>", stop_video_playback)

# Function to immediately show the new message and button (no transition)
def start_transition(half_screen=False):
    # Hide the old button_frame
    button_frame.place_forget()

    def show_new_message():
        # Remove any existing labels from right_frame
        for widget in right_frame.winfo_children():
            widget.destroy()
        # Add the new message
        message_label = tk.Label(right_frame, text="Click the play button to start the game. You will be given a word, and you need to guess all the letters.", bg="black", fg="white", font=("Helvetica", 18), wraplength=black_width * 0.8)
        message_label.place(relx=0.5, rely=0.4, anchor='center')
        # Add the new button on the white screen
        understood_button = tk.Button(left_frame, text="I understood", bg="white", fg="black", width=20, height=3, bd=0, highlightthickness=0, command=go_to_home)
        understood_button.place(relx=0.15, rely=0.5, anchor='center')
        
        # Bind events for color changes on hover and motion
        understood_button.bind("<Enter>", on_enter)
        understood_button.bind("<Leave>", on_leave)
        understood_button.bind("<Motion>", on_motion)

    show_new_message()

# Function to handle navigation to the home page
def go_to_home():
    # Clear the existing widgets from both frames
    for widget in left_frame.winfo_children():
        widget.destroy()
    for widget in right_frame.winfo_children():
        widget.destroy()
    
    # Recreate the original screen layout
    button_frame = tk.Frame(left_frame, bg="white")
    button_frame.place(relx=0.15, rely=0.5, anchor='center')  # Adjust relx to move further left

    # Add buttons to the button_frame
    play_button = tk.Button(button_frame, text="Play", bg="white", fg="black", width=20, height=3, bd=0, highlightthickness=0, command=play_button_clicked)
    play_button.pack(padx=10, pady=5)

    how_to_play_button = tk.Button(button_frame, text="How to Play", bg="white", fg="black", width=20, height=3, bd=0, highlightthickness=0, command=lambda: start_transition(True))
    how_to_play_button.pack(padx=10, pady=5)

    quit_button = tk.Button(button_frame, text="Quit", bg="white", fg="black", width=20, height=3, bd=0, highlightthickness=0, command=quit_gui)
    quit_button.pack(padx=10, pady=5)

    # Add the "Welcome back" label to the right_frame
    welcome_label = tk.Label(right_frame, text="Welcome back", bg="black", fg="white", font=("Helvetica", 24))
    welcome_label.place(relx=0.5, rely=0.5, anchor='center')

    # Bind events for color changes on hover and motion
    for button in [play_button, how_to_play_button, quit_button]:
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Motion>", on_motion)

# Start the GUI event loop
cap = cv2.VideoCapture('vid.mp4')

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    # Read frame-by-frame
    ret, frame = cap.read()
    
    # If the frame was read correctly
    if not ret:
        break
    
    # Display the frame
    cv2.imshow('Video', frame)
    
    # Press 'q' to exit the video window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
root.mainloop()