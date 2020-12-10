"""
term.py

prints the output of julia code

by: Calacuda | MIT Licence
"""


import pty
import os
import re
import json
from mycroft.messagebus import send

pass_file = "/tmp/julia-voice-programming.txt"
hist_file = pass_file[:-4]+"_hist.txt"
err_file = pass_file[:-4]+"_err.txt"
succ_file = pass_file[:-4]+"_succ.txt"
shell = "julia"
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
# carage_retuirn = re.compile(r's/^M//')

# print(hist_file)


def verbalize():
    with open(pass_file, 'r') as df:
        lines = df.readlines()
        i = -1
        try:
            line = lines[i].strip().replace('("', " ").replace('")', " ")
        except IndexError:
            return
        if line[0:6] != "julia>":
            try:
                # print(line)
                json_str = "{\"utterance\": \"" + line + "\"}"
                send("speak", json.loads(json_str))
                with open(err_file, 'a') as ef:
                    ef.write(f"line :  <{line}>")
            except json.decoder.JSONDecodeError as error:
                with open(err_file, 'a') as ef:
                    ef.write(json_str + "\n\n")
                    ef.write(str(error) + "\n\n")
                    
        #try:
        #    # if "julia>" in hf.readlines()[-1]:
        #    
        #    with open(succ_file, 'a') as sf:
        #        sf.write(line)
        #    # os.system('notify-send "trying" "trying so hard" & ')
        #except json.decoder.JSONDecodeError:
        #    with open(err_file, 'a') as ef:
        #        ef.write(line)
        #    send("speak", json.loads('{"utterance": "no"}'))


def read(fd):
    data = os.read(fd, 1024)
    # readable = ansi_escape.sub('', data.decode("utf-8"))
    # script.write(data)
    readable = ansi_escape.sub('', data.decode("utf-8"))
    bare = readable.replace("\n", "").replace("\r", "")
    #if "julia" in ansi_escape.sub('', data.decode("utf-8")):
        #print("foobar")
        #verbalize()
    with open(pass_file, 'a') as pf:
        pf.write(bare + "\n" if bare else "")
    with open(hist_file, 'a') as hf:
        hf.write(readable)
    verbalize()
    return data


def read_test(fd):
    data = os.read(fd, 1024)
    readable = ansi_escape.sub('', data.decode("utf-8"))
    print(readable)
    return data


pty.spawn(shell, read)
