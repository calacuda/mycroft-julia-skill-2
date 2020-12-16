import __init__ as jvp
import time


skill = jvp.create_skill()
try:
    skill.handle_julia_intent()
except:
    pass
#print()
#print(skill.func_parser("f of x = x times x + 5"))
time.sleep(3)
skill.handle_type_intent("f of x = x * x + 5")
time.sleep(1)
skill.handle_type_intent("f of 5")
