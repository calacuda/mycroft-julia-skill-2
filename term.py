"""
term.py

prints the output of julia code

by: Calacuda | MIT Licence
"""


import pty
import os
import re


pass_file = "/tmp/julia-voice-programming.txt"
shell = "julia"
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def read(fd):
    data = os.read(fd, 1024)
    #script.write(data)
    with open(pass_file, 'w') as pf:
        pf.write(ansi_escape.sub('',data.decode("utf-8")))
    return data


pty.spawn(shell, read)
