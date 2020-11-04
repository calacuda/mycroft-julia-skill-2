"""
term.py

prints the output of julia code

by: Calacuda | MIT Licence
"""


import pty
import os


pass_file = "/tmp/julia-voice-programming.txt"
shell = "julia"

def read(fd):
    data = os.read(fd, 1024)
    #script.write(data)
    if "julia>" not in data:
        with open(pass_file, 'w') as pf:
            pf.write(data.decode("utf-8"))
    return data


pty.spawn(shell, read)
