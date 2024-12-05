import random
import tkinter as tk

from flask import Flask, request

app = Flask(__name__)


# VARIABLES
x = 920 # window x position
y = 650 # window y position
cycle = 0
check = 0
idle_num =[1,2,3,4]
sleep_num = [10,11,12,13,15]
walk_left = [6,7]
walk_right = [8,9]
event_number = random.randrange(1,3,1)
impath = './images/' # change to where your gifs are
window = tk.Tk()

@app.route("/pet")
def launch_pet():
    pet_num = request.args.get("pet")
    
    #window configuration

# FUNCTIONS
def event(cycle,check,event_number,x,y):
    if event_number in idle_num:
        check = 0
        #print('idle')
        window.after(400,update,cycle,check,event_number,x,y) #no. 1,2,3,4 = idle
    elif event_number == 5:
        check = 1
        #print('from idle to sleep')
        window.after(100,update,cycle,check,event_number,x,y) #no. 5 = idle to sleep
    elif event_number in walk_left:
        check = 4
        #print('walking towards left')
        window.after(100,update,cycle,check,event_number,x,y) #no. 6,7 = walk towards left
    elif event_number in walk_right:
        check = 5
        #print('walking towards right')
        window.after(100,update,cycle,check,event_number,x,y) #no 8,9 = walk towards right
    elif event_number in sleep_num:
        check  = 2
        #print('sleep')
        window.after(1000,update,cycle,check,event_number,x,y) #no. 10,11,12,13,15 = sleep
    elif event_number == 14:
        check = 3
        #print('from sleep to idle')
        window.after(100,update,cycle,check,event_number,x,y) #no. 15 = sleep to idle

def gif_work(cycle,frames,event_number,first_num,last_num):
    if cycle < len(frames) -1:
        cycle+=1
    else:
        cycle = 0
        event_number = random.randrange(first_num,last_num+1,1)
    return cycle,event_number

def update(cycle,check,event_number,x,y):
    #idle
    if check == 0:
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle,idle,event_number,1,9)
  
    #idle to sleep
    elif check == 1:
        frame = idle_to_sleep[cycle]
        cycle, event_number = gif_work(cycle,idle_to_sleep,event_number,10,10)

    #sleep
    elif check == 2:
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle,sleep,event_number,10,15)

    #sleep to idle
    elif check == 3:
        frame = sleep_to_idle[cycle]
        cycle, event_number = gif_work(cycle,sleep_to_idle,event_number,1,1)

    #walk toward left
    elif check == 4:
        frame = walk_positive[cycle]
        cycle, event_number = gif_work(cycle,walk_positive,event_number,1,9)
        x -= 3

    #walk towards right
    elif check == 5:
        frame = walk_negative[cycle]
        cycle , event_number = gif_work(cycle,walk_negative,event_number,1,9)
        x -= -3
    window.geometry(f'100x100+{x}+{y}') # +'+1050'
    label.configure(image=frame)
    window.after(1,event,cycle,check,event_number,x,y)

label = tk.Label(window,bd=0)
label.pack()

#call buddy's action .gif to an array
idle = [tk.PhotoImage(file=impath+'idle.gif',format = 'gif -index %i' %(i)) for i in range(5)]#idle gif , 5 frames
idle_to_sleep = [tk.PhotoImage(file=impath+'idle_to_sleep.gif',format = 'gif -index %i' %(i)) for i in range(8)]#idle to sleep gif, 8 frames
sleep = [tk.PhotoImage(file=impath+'sleep.gif',format = 'gif -index %i' %(i)) for i in range(3)]#sleep gif, 3 frames
sleep_to_idle = [tk.PhotoImage(file=impath+'sleep_to_idle.gif',format = 'gif -index %i' %(i)) for i in range(8)]#sleep to idle gif, 8 frames
walk_positive = [tk.PhotoImage(file=impath+'walk_positive.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to left gif, 8 frames
walk_negative = [tk.PhotoImage(file=impath+'walk_negative.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to right gif, 8 frames


#loop the program
window.after(1,update,cycle,check,event_number,x,y)
window.overrideredirect(True)
window.wm_attributes('-topmost', 1)
window.mainloop()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
