"""
term.py

prints the output of julia code

by: Calacuda | MIT Licence
"""


import pty
import os
import re
import json
import asyncio
from mycroft.messagebus import send

pass_file = "/tmp/julia-voice-programming.txt"
hist_file = pass_file[:-4]+"_hist.txt"
shell = "julia"
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


#print(hist_file)


async def verbalize(sentence):
    """
    tells mycroft to speak sentence.
    """
    


def read(fd):
    data = os.read(fd, 1024)
    #script.write(data)
    with open(pass_file, 'a') as pf:
        pf.write(ansi_escape.sub('',data.decode("utf-8")))
    with open(hist_file, 'a') as hf:
        hf.write(ansi_escape.sub('',data.decode("utf-8")))
    send("speak", json.loads('{"utterance": "' + data.decode("utf-8") + '"}'))
    return data


pty.spawn(shell, read)
