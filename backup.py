import tkinter as tk
import random

# Path to your images
impath = 'C:\\Users\\kperp\\OneDrive\\Desktop\\2024-Code\\pokemon\\'

# Create Tkinter window
window = tk.Tk()

# Load images
try:
    idle = [tk.PhotoImage(file=impath + 'idle.gif', format='gif -index %i' % i) for i in range(5)]
    idle_to_sleep = [tk.PhotoImage(file=impath + 'idle_to_sleep.gif', format='gif -index %i' % i) for i in range(8)]
    sleep = [tk.PhotoImage(file=impath + 'sleep.gif', format='gif -index %i' % i) for i in range(3)]
    sleep_to_idle = [tk.PhotoImage(file=impath + 'sleep_to_idle.gif', format='gif -index %i' % i) for i in range(8)]
    walk_positive = [tk.PhotoImage(file=impath + 'walk_positive.gif', format='gif -index %i' % i) for i in range(8)]
    walk_negative = [tk.PhotoImage(file=impath + 'walk_negative.gif', format='gif -index %i' % i) for i in range(8)]
    print("Images loaded successfully!")
except Exception as e:
    print(f"Error loading images: {e}")

# Create a label to display images
label = tk.Label(window, bd=0, bg='black')
label.pack()

# Variables
x = 1400  # Initial x position
cycle = 0  # Initial frame cycle
check = 0  # Initial event (0 = idle)
event_number = random.randrange(1, 3, 1)  # Random event number

# Function to handle events and decide what to do
def event(cycle, check, event_number, x):
    if event_number == 1:  # Idle event
        check = 0
        print("Idle")
        window.after(400, update, cycle, check, event_number, x)  # Idle
    elif event_number == 2:  # Idle to sleep event
        check = 1
        print("From idle to sleep")
        window.after(100, update, cycle, check, event_number, x)  # Idle to sleep
    elif event_number == 3:  # Walking left event
        check = 4
        print("Walking towards left")
        window.after(100, update, cycle, check, event_number, x)  # Walk left
    elif event_number == 4:  # Walking right event
        check = 5
        print("Walking towards right")
        window.after(100, update, cycle, check, event_number, x)  # Walk right
    elif event_number == 5:  # Sleep event
        check = 2
        print("Sleeping")
        window.after(1000, update, cycle, check, event_number, x)  # Sleep
    elif event_number == 6:  # Sleep to idle event
        check = 3
        print("From sleep to idle")
        window.after(100, update, cycle, check, event_number, x)  # Sleep to idle

# Function to cycle through GIF frames
def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1)
    return cycle, event_number

# Function to update the label with the correct image
def update(cycle, check, event_number, x):
    if check == 0:  # Idle
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 1)
    elif check == 1:  # Idle to sleep
        frame = idle_to_sleep[cycle]
        cycle, event_number = gif_work(cycle, idle_to_sleep, event_number, 10, 10)
    elif check == 2:  # Sleeping
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)
    elif check == 3:  # Sleep to idle
        frame = sleep_to_idle[cycle]
        cycle, event_number = gif_work(cycle, sleep_to_idle, event_number, 1, 1)
    elif check == 4:  # Walking left
        frame = walk_positive[cycle]
        cycle, event_number = gif_work(cycle, walk_positive, event_number, 1, 8)
        x -= 3  # Move left
    elif check == 5:  # Walking right
        frame = walk_negative[cycle]
        cycle, event_number = gif_work(cycle, walk_negative, event_number, 1, 8)
        x += 3  # Move right

    # Update window and image
    window.geometry(f'100x100+{x}+1050')  # Move window with x position
    label.configure(image=frame)  # Update the label with the new image
    window.after(50, event, cycle, check, event_number, x)  # Continue the animation loop

# Start the animation loop
window.after(1, update, cycle, check, event_number, x)

# Start Tkinter main loop
window.mainloop()
