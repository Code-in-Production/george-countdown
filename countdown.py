#!/usr/bin/env python3
import datetime
import time
import tkinter

root = tkinter.Tk()
root.title("Countdown")

display_var = tkinter.StringVar()
display_var.set("0:00:00.0")
display = tkinter.Label(root, textvariable=display_var, font=("Helvetiva", 32))

entry_var = tkinter.StringVar()
entry = tkinter.Entry(root, textvariable=entry_var, font=("Helvetiva", 32), width=10, justify="right")
set_ = tkinter.Button(root, text="Set", font=("Helvetiva", 24), width=5)
toggle = tkinter.Button(root, text="Start", font=("Helvetiva", 24), width=5)
reset = tkinter.Button(root, text="Reset", font=("Helvetiva", 24), width=5)

display.grid(row=0, column=0, columnspan=4, sticky="nsew")
entry.grid(row=1, column=0, sticky="nsew")
set_.grid(row=1, column=1, sticky="nsew")
toggle.grid(row=1, column=2, sticky="nsew")
reset.grid(row=1, column=3, sticky="nsew")

delta = datetime.timedelta(0)

def convert_delta(delta):
    string = str(delta)
    if "." not in string:
        string += ".000000"
    if delta.seconds >= 60:
        string = string[:-7]
    else:
        string = string[:-5]
    return string

def on_set():
    global delta
    if running:
        return
    string = entry_var.get().strip()
    if not string:
        return
    seconds = 0
    for part in string.split(":"):
        seconds *= 60
        if not part.strip():
            continue
        seconds += int(part)
    delta = datetime.timedelta(seconds=seconds)
    display_var.set(convert_delta(delta))
set_["command"] = on_set

running = False
def on_toggle():
    global running, after, last
    running = not running
    toggle["text"] = "Stop" if running else "Start"
    reset["state"] = "disabled" if running else "normal"
    set_["state"] = "disabled" if running else "normal"
    if running:
        last = time.monotonic()
        on_tick()
    else:
        if after is not None:
            root.after_cancel(after)
            after = None
toggle["command"] = on_toggle

after = None
last = None
def on_tick():
    global delta, last, after
    if after is not None:
        root.after_cancel(after)
        after = None
    now = time.monotonic()
    if last is None:
        last = now
    delta -= datetime.timedelta(seconds=now - last)
    if delta.days < 0:
        delta = datetime.timedelta(0)
        on_toggle()
    else:
        after = root.after(50, on_tick)
    display_var.set(convert_delta(delta))
    last = now

def on_reset():
    global delta
    delta = datetime.timedelta(0)
    display_var.set(convert_delta(delta))
reset["command"] = on_reset

root.rowconfigure(0, weight=5)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=5)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

root.mainloop()
