#!/usr/bin/env python3

import tkinter
import os
from datetime import datetime
from pathlib import Path
from subprocess import Popen
from threading import Thread

root = tkinter.Tk()
root.title('Timer')
root.configure(background='#3E4149')


class Keylog(Thread):
    def __init__(self, output):
        Thread.__init__(self)
        self._output = output
        self.proc = None
        self.stop_requested = False
        self.cmd = ['keylogger', self._output]

    def run(self):
        if self.proc is None:
            self.start_logging()

    def start_logging(self):
        self.proc = Popen(self.cmd)

    def stop_logging(self):
        if self.proc is not None:
            self.proc.terminate()


def set_output():
    home = str(Path.home())

    return os.path.join(
        home, 'keylogger_' + datetime.now().strftime('%Y-%m-%d') + '.log')


output = set_output()
logging = Keylog(output)
logging.daemon = True


sec = 0
min = 0
hour = 0
doTick = True
isRunning = False


def tick():
    global sec, min, hour
    if not doTick:
        return
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
    sec += 1
    root.after(1000, tick)


def start():
    reset()
    global doTick
    global isRunning
    doTick = True
    tick()

    if isRunning:
        logging.start_logging()
    else:
        logging.start()
        isRunning = True

    pathLabel.configure(text="")
    startButton.configure(text="Stop", bg="red", command=stop)


def stop():
    global doTick
    doTick = False
    logging.stop_logging()
    pathLabel.configure(text="Saved to: \"" + set_output() + "\"")
    startButton.configure(text="Start", bg="green", command=start)


def reset():
    global sec, min, hour, doTick
    sec = 0
    min = 0
    hour = 0
    doTick = True
    pathLabel.configure(text="")


timeLabel = tkinter.Label(root, fg='white', background='#3E4149',
                          text="%02d:%02d:%02d" % (hour, min, sec),
                          font=('Helvetica', 80))
timeLabel.pack(padx=100, pady=30)

startButton = tkinter.Button(
    root, bg='green', fg='white', highlightbackground='#3E4149',
    text='Start', width=12, command=start)
startButton.pack(padx=100, pady=20)

pathLabel = tkinter.Label(root, background='#3E4149', fg='white',
                          anchor='center', text="", font=("Consolas", 10))
pathLabel.pack(pady=20)

root.mainloop()
