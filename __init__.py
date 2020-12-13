from mycroft import MycroftSkill, intent_handler
import mycroft
from os import system as cmd
import time
import subprocess
import libtmux


pass_file = "/tmp/julia-voice-programming.txt"
mycroft_python_dir = "/".join(mycroft.__file__.split("/")[:-2]) + "/.venv/bin/python3"


class JuliaVoiceProgramer(MycroftSkill):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.repl = None
        self.server = None
        self.session = None
        self.window = None
        self.pane = None
        pass

    @intent_handler("program.intent")
    def handle_julia_intent(self):
        self.acknowledge()
        session_name = "Julia_Voice_Programer"
        skill_dir = "/opt/mycroft/skills/mycroft-julia-skill-2.calacuda/"
        call = f"{skill_dir + 'term.sh'} {session_name} {mycroft_python_dir}"
        #call = f"./term.sh {session_name} {mycroft_python_dir}"
        #call = f"$TERMINAL -e tmux new-session -s {session_name} -n {session_name}"
        self.repl = subprocess.Popen(call, shell=True)
        time.sleep(0.1)
        #print("repl : ", self.repl)
        connected = False
        while not connected:
            print("looking for the tmux server")
            try:
                self.tmux_server = libtmux.Server(session_name)
                self.session = self.tmux_server.find_where({"session_name": session_name})
                # connected = True
                print(self.tmux_server.list_sessions())
            except libtmux.exc.LibTmuxException:
                time.sleep(0.1)
            else:
                print("found tmux server")
                connected = True
        print("free willie")
        self.window = self.session.attached_window
        self.pane = self.window.attached_pane
        self.speak("your julia console is ready sir")
        #pass
        
    @intent_handler("enter_code.intent")
    def handle_type_intent(self, code):
        #cmd(f'notify-send "testing" "type code :  {code.data.get("code")}"')
        self.acknowledge()
        code = self.parse(code.data.get("code"))
        self.pane.send_keys(code)
        
        #self.keyboard.type(code)
        #self.keyboard.press(Key.enter)
        #self.keyboard.release(Key.enter)

        #cmd(f'notify-send "testing" "code :  {code}"')
        #output = Main.eval(code)
        #cmd(f'notify-send "testing" "output :  {output}"')
        #time.sleep(2)
        #with open(pass_file, 'r') as pf:
            #cmd(f'notify-send "testing" "{pf.read()}"')
        #    self.speak(pf.read().replace("julia>", "" ))
        #with open(pass_file, 'w') as pf:
        #    pass
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
        self.session.kill_session()


def create_skill():
    #cmd("notify-send 'Mycroft' 'Julia Voice Programer installed'")
    return JuliaVoiceProgramer()


#skill = create_skill()
#skill.handle_julia_intent()
#skill.handle_type_intent("f(x)=x*3")
