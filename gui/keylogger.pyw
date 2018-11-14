import tkinter
from utils import set_output, Keylog

root = tkinter.Tk()
root.title('Timer')
output = set_output()
logging = Keylog(output)


sec = 0
min = 0
hour = 0
doTick = True


def tick():
    global sec, min, hour
    if not doTick:
        return
    sec += 1
    if sec == 60:
        min += 1
        sec = 0
    if min == 60:
        hour += 1
        min = 0

    sec = round(sec, 1)
    min = round(min, 1)
    hour = round(hour, 1)
    timeLabel.configure(text="%02d:%02d:%02d" % (hour, min, sec))
    root.after(1000, tick)


def start():
    reset()
    global doTick
    doTick = True
    tick()
    logging.setDaemon(True)
    logging.start()
    startButton.configure(text="Stop", bg="red", command=stop)


def stop():
    global doTick
    doTick = False
    logging.stop()
    pathLabel.configure(text="Saved to: \"" + set_output() + "\"")
    startButton.configure(text="Start", bg="green", command=start)


def reset():
    global sec, min, hour, doTick
    sec = 0
    min = 0
    hour = 0
    doTick = True
    pathLabel.configure(text=None)


timeLabel = tkinter.Label(root, fg='black',
                          text="%02d:%02d:%02d" % (hour, min, sec),
                          font=('Helvetica', 80))
timeLabel.pack(padx=100, pady=30)

startButton = tkinter.Button(
    root, bg='green', fg='white', text='Start', width=12, command=start)
startButton.pack(padx=100, pady=30)

pathLabel = tkinter.Label(root, anchor='center',
                          text=None, font=("Consolas", 10))
pathLabel.pack()

root.mainloop()
