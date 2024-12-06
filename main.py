import random
import tkinter as tk
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# VARIABLES
x = 920  # window x position
y = 650  # window y position
cycle = 0
check = 0
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]
event_number = random.randrange(1, 3, 1)
impath = './images/'  # Change to where your gifs are

window = None
tk_thread = None


def start_tkinter():
    """Function to initialize and run the Tkinter window."""
    global window, cycle, check, event_number, x, y

    window = tk.Tk()

    def event(cycle, check, event_number, x, y):
        if event_number in idle_num:
            check = 0
            window.after(400, update, cycle, check, event_number, x, y)  # Idle
        elif event_number == 5:
            check = 1
            window.after(100, update, cycle, check, event_number, x, y)  # Idle to sleep
        elif event_number in walk_left:
            check = 4
            window.after(100, update, cycle, check, event_number, x, y)  # Walk left
        elif event_number in walk_right:
            check = 5
            window.after(100, update, cycle, check, event_number, x, y)  # Walk right
        elif event_number in sleep_num:
            check = 2
            window.after(1000, update, cycle, check, event_number, x, y)  # Sleep
        elif event_number == 14:
            check = 3
            window.after(100, update, cycle, check, event_number, x, y)  # Sleep to idle

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

    idle = [tk.PhotoImage(file=impath + 'idle.gif', format='gif -index %i' % i) for i in range(5)]
    idle_to_sleep = [tk.PhotoImage(file=impath + 'idle_to_sleep.gif', format='gif -index %i' % i) for i in range(8)]
    sleep = [tk.PhotoImage(file=impath + 'sleep.gif', format='gif -index %i' % i) for i in range(3)]
    sleep_to_idle = [tk.PhotoImage(file=impath + 'sleep_to_idle.gif', format='gif -index %i' % i) for i in range(8)]
    walk_positive = [tk.PhotoImage(file=impath + 'walk_positive.gif', format='gif -index %i' % i) for i in range(8)]
    walk_negative = [tk.PhotoImage(file=impath + 'walk_negative.gif', format='gif -index %i' % i) for i in range(8)]

    window.after(1, update, cycle, check, event_number, x, y)
    window.overrideredirect(True)
    window.wm_attributes('-topmost', 1)
    window.mainloop()


@app.route("/pet", methods=["GET"])
def launch_pet():
    """Endpoint to start the Tkinter pet animation."""
    global tk_thread

    if tk_thread is None or not tk_thread.is_alive():
        tk_thread = threading.Thread(target=start_tkinter)
        tk_thread.start()
        return jsonify({"message": "Pet animation started!"})
    else:
        return jsonify({"message": "Pet animation is already running."})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
