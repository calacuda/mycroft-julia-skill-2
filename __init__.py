from mycroft import MycroftSkill, intent_handler
from os import system as cmd
import sys
#cmd("notify-send 'Mycroft' 'Julia Voice Programer installed'")
from julia import Main
#cmd("notify-send 'Mycroft' 'Julia Voice Programer installed'")


class JuliaVoiceProgramer: #(MycroftSkill):
    def __init__(self):
        super().__init__()
        
    def initialize(self):
        pass
        
    @intent_handler("program.intent")
    def handle_julia_intent(self):
        self.acknowledge()
        #self.make_repl()
        #self.repl = Main
        #self.acknowledge()
        self.speak("your julia console is ready sir")
        pass
        
    @intent_handler("type.intent")
    def handle_type_intent(self, code):
        cmd(f'notify-send "testing" "type code :  {code.data.get("code")}"')
        self.acknowledge()
        code = self.parse(code.data.get("code"))
        cmd(f'notify-send "testing" "code :  {code}"')
        output = Main.eval(code)
        cmd(f'notify-send "testing" "output :  {output}"')
        self.speak(output)
        return True

    def send_out(self, payload):
        return self.repl.eval(payload)

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
        #cmd(f'notify-send "debug" "parse returning {code}"')
        return code
    
    def shutdown(self):
        pass
        
    def stop(self):
        pass


def create_skill():
    #cmd("notify-send 'Mycroft' 'Julia Voice Programer installed'")
    return JuliaVoiceProgramer()


skill = create_skill()
skill.handle_julia_intent()
skill.handle_type_intent("f(x)=x*3")
