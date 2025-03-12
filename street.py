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

def porte():
    a=randint(0,3)
    fd(15)
    for i in range(3):
        if i==a:
            beginfill("blue")
            fd()




for i in range(nbbats):
    fd(10)

    etage("red")
    lt(90)
    fd(50)
    rt(90)

done()