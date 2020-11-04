"""
term.py

prints the output of julia code

by: Calacuda | MIT Licence
"""


import pty


pass_file = "/tmp/julia-voice-programming.txt"
shell = "julia"

def read(fd):
    data = os.read(fd, 1024)
    #script.write(data)
    with open(pass_file, 'w') as pf:
        pf.write(data)
    return data


pty.spawn(shell, read)