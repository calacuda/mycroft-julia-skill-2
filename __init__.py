from mycroft import MycroftSkill, intent_handler
from os import system as cmd
import time
#import sys
#import pty
import subprocess
from pynput.keyboard import Key, Controller
#cmd("notify-send 'Mycroft' 'Julia Voice Programer installed'")
#from julia import Main
#cmd("notify-send 'Mycroft' 'all imported'")


pass_file = "/tmp/julia-voice-programming.txt"


class JuliaVoiceProgramer(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.keyboard = Controller()
        
    def initialize(self):
        pass
        
    @intent_handler("program.intent")
    def handle_julia_intent(self):
        self.acknowledge()
        self.repl = subprocess.Popen("urxvt -e /usr/bin/python3 /opt/mycroft/skills/mycroft-julia-skill-2.calacuda/term.py ", shell=True)
        self.speak("your julia console is ready sir")
        pass
        
    @intent_handler("type.intent")
    def handle_type_intent(self, code):
        #cmd(f'notify-send "testing" "type code :  {code.data.get("code")}"')
        self.acknowledge()
        code = self.parse(code.data.get("code"))
        self.keyboard.type(code)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        #cmd(f'notify-send "testing" "code :  {code}"')
        #output = Main.eval(code)
        #cmd(f'notify-send "testing" "output :  {output}"')
        #time.sleep(2)
        with open(pass_file, 'r') as pf:
            cmd(f'notify-send "testing" "{pf.read()}"')
            self.speak(pf.read())
        with open(pass_file, 'w') as pf:
            pass
        #return True

    def parse(self, utterance):
        #cmd(f'notify-send "debug" "parse :  {utterance}"')
        code = utterance.lower()
        symboles = {" (": "(", "single quote": "'", "quote": '"', "double quote": '"', "quotations": '"'}
        operators = {"equals": "=", "plus": "+", "times": "*", "divided by": "/", "minus": "-"}
        switcharoo = (symboles, operators)
        for switcher in switcharoo:
            for replaceable in switcher.keys():
                #code = code.replace(replaceable, switcher.get(replaceable))
                code = code.replace(" "+replaceable, switcher.get(replaceable))
                code = code.replace(replaceable+" ", switcher.get(replaceable))
                code = code.replace(replaceable, switcher.get(replaceable))
        #cmd(f'notify-send "debug" "code :  {code}"')
        if len([i for i in code if i == "("]) > len([i for i in code if i == ")"]):
            code += ")"
        elif len([i for i in code if i in {"(", ")"}]) == 0:
            code += "()"
        #cmd(f'notify-send "debug" "parse returning {code}"')
        return code
    
    def shutdown(self):
        self.stop()
        
    def stop(self):
        self.repl.terminate()


def create_skill():
    #cmd("notify-send 'Mycroft' 'Julia Voice Programer installed'")
    return JuliaVoiceProgramer()


#skill = create_skill()
#skill.handle_julia_intent()
#skill.handle_type_intent("f(x)=x*3")
