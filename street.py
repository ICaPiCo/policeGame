from turtle import*
from random import*
from math import*
#Fillcolor()          begin.fill()            end.fill()
#10 15 30 10 30 10 30 15 10
nbmagic=0
for i in range(18):
    nbmagic+=sin(i*10*pi/180)
up()
bk(700)
speed(10)
nbbats=8
def rectangle(lenght,width,color):
    fillcolor(color)
    begin_fill()
    down()
    for i in range(2):
        fd(lenght)
        lt(90)
        fd(width)
        lt(90)
    end_fill()
    up()
def etage(color):
    down()
    rectangle(140,50,color)

def fenetre(proba):
    if proba!=0:
        rectangle(30,30,'white')
        if proba>=6:
            lt(90)
            fd(10)
            lt(90)
            fd(5)
            lt(90)
            rectangle(15,40,'brown')
            lt(90)
            fd(5)
            rt(90)
            fd(10)
            lt(90)


def porte(proba):
    doorcolors=["gold1","burlywood4","DarkOrange4","DarkGray","LightCyan4","HotPink3"]
    e=randint(0,len(doorcolors)-1)
    if proba==0:
        rectangle(30,45,doorcolors[e])
    else:
        fillcolor(doorcolors[e])
        down()
        begin_fill()
        fd(30)
        lt(90)
        fd(30)
        circle(15,180)
        fd(30)
        lt(90)
        end_fill()
        up()

def deco_etage(etage):
    a=randint(0,2)
    fd(15)
    up()
    for i in range(3):
        if i==a and etage==0:
            d=randint(0,4)
            porte(d)
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
    if proba>=4:
        fillcolor('black')
        down()
        begin_fill()
        fd(150)
        lt(150)
        fd(80/(cos(30*pi/180)))
        lt(60)
        fd(80/(cos(30*pi/180)))
        lt(150)
        fd(10)
        up()
        end_fill()
    elif proba>=2:
        fillcolor('black')
        down()
        begin_fill()
        fd(150)
        lt(110)
        fd(80/(cos(70*pi/180)))
        lt(140)
        fd(80/(cos(70*pi/180)))
        lt(110)
        fd(10)
        up()
        end_fill()
    else:
        bk(5)
        rectangle(150,20,'black')
        fd(5)
        
    




housecolors=["firebrick","firebrick1","beige","bisque","bisque2","DarkKhaki","DarkSalmon","LightPink","papayawhip","PeachPuff","seagreen1","indianred1"]
print(nbmagic)
for i in range(nbbats):
    fd(25)
    nbEtages=randint(1,5)
    randcolors=randint(0,len(housecolors)-1)
    for i in range(nbEtages):
        etage(housecolors[randcolors])
        deco_etage(i)
        lt(90)
        fd(50)
        rt(90)
    c=randint(0,6)
    toit(c)
    rt(90)#descendre tt les etages
    fd(nbEtages*50)
    lt(90)
    fd(150)

done()