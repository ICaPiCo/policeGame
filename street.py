from random import*

def create_text():
    info = {"nose":["green","red","blue"],"hair":["black","blond","brown"],"eyes":["blue","green","brown"],"skin":["white","black","brown"]}
    text = ""
    for key in info:
        text += f"{key} : {choice(info[key])}, "
    print(text)

create_text()