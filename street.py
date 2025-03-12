from turtle import*
from random import*
#Fillcolor()          begin.fill()            end.fill()
#10 15 30 10 30 10 30 15 10

up()
bk(700)
nbbats=5
def etage(color):
    down()
    fillcolor(color)
    begin_fill()
    fd(140)
    lt(90)
    fd(50)
    lt(90)
    fd(140)
    lt(90)
    fd(50)
    lt(90)
    end_fill()
    up()

def fenetre():
    fillcolor("white")
    begin_fill()
    down()
    for i in range(4):
        fd(30)
        lt(90)
    end_fill()
    up()

def porte():
    fillcolor("blue")
    begin_fill()
    down()
    fd(30)
    lt(90)
    fd(45)
    lt(90)
    fd(30)
    lt(90)
    fd(45)
    lt(90)
    end_fill()
    up()

def deco_etage(porte):
    a=randint(0,2)
    fd(15)
    up()
    for i in range(3):
        if i==a and porte=='porte':
            porte()
        else:
            lt(90)
            fd(10)
            rt(90)
            fenetre()
            rt(90)
            fd(10)
            lt(90)
        fd(40)
    bk(135)
    




for i in range(nbbats):
    fd(10)
    nbEtages=randint(1,5)
    for i in range(nbEtages):
        etage("red")
        deco_etage(porte)
        lt(90)
        fd(50)
        rt(90)
    rt(90)
    fd(nbEtages*50)
    lt(90)
    fd(150)

done()