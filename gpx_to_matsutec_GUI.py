#!/usr/bin/env python3

import tkinter as tk
import gpx_to_matsutec as gm
from tkinter.filedialog import askopenfilename
import os
import datetime

window = tk.Tk()
window.title('GPX to Matsutec converter')
window.grid_columnconfigure(0, weight=1, uniform="fred")
window.grid_columnconfigure(1, weight=1, uniform="fred")
window.grid_columnconfigure(2, weight=1, uniform="fred")
window.grid_columnconfigure(3, weight=1, uniform="fred")
# window.grid_columnconfigure(4, weight=1, uniform="fred")
# window.grid_columnconfigure(5, weight=1, uniform="fred")

header = "GPX to Matsutec converter"

tk.Label(text=header).grid(row=0,column=0)

tk.Label(text="Source GPX file :").grid(row=1,column=0)
tk.Label(text="Output TXT file : ").grid(row=2,column=0)

result_msg = tk.Label(text="")
result_msg.grid(row=4,column=0, columnspan=3)

input_filevar = tk.StringVar()
output_filevar = tk.StringVar()

tk.Entry(window, textvariable=input_filevar, width=50).grid(row=1,column=1, columnspan=2)
tk.Entry(window, textvariable=output_filevar, width=50).grid(row=2,column=1, columnspan=2)

def process_waypoints():
    global input_filevar, output_filevar, result_msg
    ret = gm.process_waypoints(input_filevar.get(),output_filevar.get())
    if ret == "":
        msg = "GPX file successfully converted to TXT !"
    else:
        log_file_path = os.path.join(os.path.dirname(input_filevar.get()), "gpx_to_matsutec.log")
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        with open(log_file_path, "a") as f:
            f.write(timestamp + "\n")
            f.write(ret)
        msg = "Error during processing, error logs were written to gpx_to_matsutec.log"
    result_msg.config(text = msg)

def browse_file():
    global input_filevar, output_filevar, err_msg_format, result_msg
    input_file = askopenfilename()
    if input_file:
        result_msg.config(text = "")
        input_filevar.set(input_file)
        if input_file.rstrip(".gpx") == input_file:
            err_msg_format = tk.Label(text="Bad file format, use a .gpx file", fg="#f00")
            err_msg_format.grid(row=0, column=1)
            output_filevar.set("")
        else:
            if 'err_msg_format' in globals():
                err_msg_format.destroy()
            output_file = input_file.rstrip(".gpx") + ".txt"
            output_filevar.set(output_file)


# input_file.pack()

tk.Button(window, text="Browse", command=browse_file).grid(row=1,column=3)
tk.Button(window, text="Convert", command=process_waypoints).grid(row=3,column=0)
tk.Button(window, text="Quit", command=window.destroy).grid(row=3,column=3)

window.mainloop()
