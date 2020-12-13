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


def verbalize_old():
    """
    depricated, does not work as intended
    """
    #print("verbalized called")
    with open(pass_file, 'r') as df:
        #print("pass_file opened")
        lines = df.readlines()
        i = -1
        #try:
        if len(lines) > 0:
            line = lines[i].strip().replace('("', " ").replace('")', " ")
        else:
            print("death")
            return
        #except IndexError:
        #    return
        if line[0:6] != "julia>":
            print("trying to speak")
            try:
                # print(line)
                json_str = "{\"utterance\": \"" + line + "\"}"
                send("speak", json.loads(json_str))
                #with open(err_file, 'a') as ef:
                #    ef.write(f"line :  <{line}>")
            except json.decoder.JSONDecodeError as error:
                with open(err_file, 'a') as ef:
                    ef.write(json_str + "\n\n")
                    ef.write(str(error) + "\n\n")


def verbalize_new():
    with open(pass_file, 'r') as df:
        #print("pass_file opened")
        lines = [l for l in df.readlines() if l != "\n"]
        if len(lines) > 0:
            line = lines[-1].strip().replace('("', " ").replace('")', " ")
        else:
            #print("lines variable non exsistant")
            return
        if line[0:6] != "julia>" and len(line) > 1:
            #print("trying to speak")
            json_str = "{\"utterance\": \"" + line + "\"}"
            try:
                send("speak", json.loads(json_str))
            except json.decoder.JSONDecodeError:
                #print("json error : ", line)
                pass


def read(fd):
    data = os.read(fd, 1024)
    readable = ansi_escape.sub('', data.decode("utf-8"))
    bare = readable.replace("\r", "")
    if bare[0:6] != "julia>":
        with open(pass_file, 'a') as pf:
            pf.write(bare + "\n" if bare else "")
        with open(hist_file, 'a') as hf:
            hf.write(readable)
    else:
        with open(pass_file, 'w') as pf:
            pass
    #print("before verbalize")
    verbalize_new()
    #print("after verbalize")
    return data


pty.spawn(shell, read)
print("\n\n<ended>\n\n")
