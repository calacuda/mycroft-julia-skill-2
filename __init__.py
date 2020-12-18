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
        self.repl = subprocess.Popen(call, shell=True)
        time.sleep(0.1)
        #print("repl : ", self.repl)
        connected = False
        #while not connected:
        for i in range(10):
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
                break
        if not connected:
            self.speak("there was an error connecting ot the tmux session")
            return False
        print("free willie")
        self.window = self.session.attached_window
        self.pane = self.window.attached_pane
        self.speak("your julia console is ready sir")
        return True
        #pass
        
    @intent_handler("enter_code.intent")
    def handle_type_intent(self, code):
        #cmd(f'notify-send "testing" "type code :  {code.data.get("code")}"')
        self.acknowledge()
        code = self.parse(code.data.get("code"))
        #code = self.parse(code)
        self.pane.send_keys(code)
        return True
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
        if " = " in code or code.split(" ")[1] == "of":
            return self.func_parser(code)
        else:
            return self.gen_parser(code)

    def func_parser(self, text):
        """
        parses one line function deffenitions.
        """
        try:
            deff, code = text.split(" = ")
            code = self.gen_parser(code)
        except ValueError:
            deff = text
            code = None
        name, params = deff.split(" of ")
        return f"{name}({params.replace(' ', ', ')}){' = ' + code if code else ''}"

    def gen_parser(self, code):
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
        if code.count("(") > code.count(")"):
            code += ")"
        #cmd(f'notify-send "debug" "parse returning {code}"')
        return code
    
    #def func_def_parse(self, parse_text, parse_key):
    #    """
    #    returns input text, parse_text, parsed as code.
    #    parse_text = the input to parse.
    #    parse_key  = a tuple of tuples in the same stucture that the text will be parsed.
    #                 if parse_key is (' first ', (' alpha_1 a ', ' alpha_1 b '))
    #                 this function will split parse_text, will call this alpha, into alpha.split(' first ').
    #                 then split alpha[0] on ' alpha_1 a ', and alpha[1] on ' alpha_1 b '.
    #    """
    #    #deff, func = code.split(" = ")
    #    #deff = deff
    #    print(parse_text, parse_key if parse_key else "none")
    #    #parsed = []
    #    if type(parse_key) == str:
    #        parsed = parse_text.split(parse_key)
    #    elif type(parse_key) in [list, tuple]:
    #        parsed = [self.func_def_parse(parse_text[i].split(parse_key[i]), parse_key[i]) for i in range(len(parse_key))]
    #    else:
    #        parsed = parse_text
    #    return parsed
            
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
