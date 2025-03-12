from turtle import*
from random import*
#Fillcolor()          begin.fill()            end.fill()
#10 15 30 10 30 10 30 15 10

up()
bk(700)
speed(10)
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

def fenetre(proba):
    if proba!=0:
        fillcolor("white")
        begin_fill()
        down()
        for i in range(4):
            fd(30)
            lt(90)
        end_fill()
        up()
        if proba>=6:
            fillcolor("brown")
            lt(90)
            fd(10)
            lt(90)
            fd(5)
            lt(90)
            begin_fill()
            down()
            fd(15)
            lt(90)
            fd(40)
            lt(90)
            fd(15)
            lt(90)
            fd(40)
            lt(90)
            end_fill()
            up()
            lt(90)
            fd(5)
            rt(90)
            fd(10)
            lt(90)


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

def deco_etage(etage):
    a=randint(0,2)
    fd(15)
    up()
    for i in range(3):
        if i==a and etage==0:
            porte()
        else:
            if etage != 0:
                b=randint(0,9)
            else:
                b=randint(0,5)
            lt(90)
            fd(10)
            rt(90)
            fenetre(b)
            rt(90)
            fd(10)
            lt(90)
        fd(40)
    bk(135)

def toit(proba):
    fd(150)
    





for i in range(nbbats):
    fd(10)
    nbEtages=randint(1,5)
    for i in range(nbEtages):
        etage("red")
        deco_etage(i)
        lt(90)
        fd(50)
        rt(90)
    c=randint(0,2)
    toit(c)
    rt(90)#descendre tt les etages
    fd(nbEtages*50)
    lt(90)
    fd(150)

done()