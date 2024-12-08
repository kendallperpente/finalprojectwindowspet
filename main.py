import os
import random
import tkinter as tk
from flask import Flask, request, jsonify
import threading
import webbrowser
from pyvirtualdisplay import Display  # For virtual display in headless environments

# Start virtual display (use only if required in headless environments)
try:
    display = Display(visible=0, size=(800, 600))
    display.start()
    print("Virtual display started.")
except Exception as e:
    print(f"Error starting virtual display: {e}")

# Flask App Initialization
app = Flask(__name__)

# GLOBAL VARIABLES
x = 920  # window x position
y = 650  # window y position
cycle = 0
check = 0
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]
event_number = random.randrange(1, 3, 1)
impath = './images/'  # Path to where your GIFs are

window = None
tk_thread = None

# Tkinter Animation Function
def start_tkinter():
    global window, cycle, check, x, y

    try:
        window = tk.Tk()

        def event(cycle, check, event_number, x, y):
            if event_number in idle_num:
                check = 0
                window.after(400, update, cycle, check, event_number, x, y)
            elif event_number == 5:
                check = 1
                window.after(100, update, cycle, check, event_number, x, y)
            elif event_number in walk_left:
                check = 4
                window.after(100, update, cycle, check, event_number, x, y)
            elif event_number in walk_right:
                check = 5
                window.after(100, update, cycle, check, event_number, x, y)
            elif event_number in sleep_num:
                check = 2
                window.after(1000, update, cycle, check, event_number, x, y)
            elif event_number == 14:
                check = 3
                window.after(100, update, cycle, check, event_number, x, y)

        def gif_work(cycle, frames, event_number, first_num, last_num):
            if cycle < len(frames) - 1:
                cycle += 1
            else:
                cycle = 0
                event_number = random.randrange(first_num, last_num + 1, 1)
            return cycle, event_number

        def update(cycle, check, event_number, x, y):
            if check == 0:
                frame = idle[cycle]
                cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)
            elif check == 1:
                frame = idle_to_sleep[cycle]
                cycle, event_number = gif_work(cycle, idle_to_sleep, event_number, 10, 10)
            elif check == 2:
                frame = sleep[cycle]
                cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)
            elif check == 3:
                frame = sleep_to_idle[cycle]
                cycle, event_number = gif_work(cycle, sleep_to_idle, event_number, 1, 1)
            elif check == 4:
                frame = walk_positive[cycle]
                cycle, event_number = gif_work(cycle, walk_positive, event_number, 1, 9)
                x -= 3
            elif check == 5:
                frame = walk_negative[cycle]
                cycle, event_number = gif_work(cycle, walk_negative, event_number, 1, 9)
                x += 3

            window.geometry(f'100x100+{x}+{y}')
            label.configure(image=frame)
            window.after(1, event, cycle, check, event_number, x, y)

        label = tk.Label(window, bd=0)
        label.pack()

        # Load GIF frames and validate paths
        try:
            idle = [tk.PhotoImage(file=impath + 'idle.gif', format='gif -index %i' % i) for i in range(5)]
            idle_to_sleep = [tk.PhotoImage(file=impath + 'idle_to_sleep.gif', format='gif -index %i' % i) for i in range(8)]
            sleep = [tk.PhotoImage(file=impath + 'sleep.gif', format='gif -index %i' % i) for i in range(3)]
            sleep_to_idle = [tk.PhotoImage(file=impath + 'sleep_to_idle.gif', format='gif -index %i' % i) for i in range(8)]
            walk_positive = [tk.PhotoImage(file=impath + 'walk_positive.gif', format='gif -index %i' % i) for i in range(8)]
            walk_negative = [tk.PhotoImage(file=impath + 'walk_negative.gif', format='gif -index %i' % i) for i in range(8)]
        except Exception as e:
            print(f"Error loading GIFs: {e}")
            return

        window.after(1, update, cycle, check, event_number, x, y)
        window.overrideredirect(True)
        window.wm_attributes('-topmost', 1)
        window.mainloop()
    except Exception as e:
        print(f"Error in start_tkinter: {e}")

# Flask Routes
@app.route('/')
def home():
    return "<h1>Flask Server Running</h1><p>Access <a href='/pet'>/pet</a></p>"

@app.route('/pet')
def launch_pet():
    global tk_thread

    if tk_thread is None or not tk_thread.is_alive():
        try:
            tk_thread = threading.Thread(target=start_tkinter)
            tk_thread.daemon = True  # Allow Flask to exit even if Tkinter is running
            tk_thread.start()
            return jsonify({"message": "Pet animation running!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"message": "Pet animation already running."})

# Flask Server Initialization
if __name__ == "__main__":
    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True, host="0.0.0.0")
