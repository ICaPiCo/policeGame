from turtle import*
from random import*
from math import*


up()
speed(10)
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
    doorcolors=["gold1","burlywood4","DarkOrange4","gray0","LightCyan4","HotPink3"]
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

def deco_etage(etage,ecart):
    global bridgeH
    global lastBuilding
    a=randint(0,2)
    br=randint(0,9)
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
    fd(5)
    if br==0 and etage!=0 and not lastBuilding:
        bridgeH=etage
        fd(ecart)
        lt(90)
        fillcolor('cornsilk2')
        begin_fill()
        down()
        circle(ecart/2,180)
        bk(15)
        circle(ecart/2,-180)
        bk(15)
        end_fill()
        up()
        rt(90)
        bk(ecart)
    bk(140)
    

def toit(proba):
    if proba>=4:
        fd(150)
        lt(150)
        fd(80/(cos(30*pi/180)))
        lt(60)
        fd(80/(cos(30*pi/180)))
        lt(150)
        fd(10)
    elif proba>=2:
        fd(150)
        lt(110)
        fd(80/(cos(70*pi/180)))
        lt(140)
        fd(80/(cos(70*pi/180)))
        lt(110)
        fd(10)
    else:
        bk(5)
        fd(150)
        lt(90)
        fd(20)
        lt(90)
        fd(150)
        lt(90)
        fd(20)
        lt(90)
        fd(5)
        
def background():
    goto(-800,500)
    rt(90)
    rectangle(1000,1600,'skyblue1')
    lt(180)
    goto(800,250)
    fillcolor('chartreuse2')
    begin_fill()
    down()
    for i in range(10):
        ranAngles=randint(125,150)
        ranRad=randint(100,200)
        ranDistance=50+(ranAngles/16)+randint(5,30)
        setheading(ranAngles)
        circle(ranRad,ranDistance)
    goto(-800,0)
    setheading(180)
    goto(800,0)
    goto(800,250)
    end_fill()
    up()
    goto(800,0)
    rectangle(1600,500,'azure4')
    rectangle(1600,200,'gray55')
    goto(0,0)

def backgroundHouses(total,i):#a fix, i et total un peu bizarre~~
    setheading(180)
    yhouse=-200+200*(total-i)/total
    print(yhouse)
    goto(-850-40*i,yhouse)
    rt(90)
    grays='gray'+str(20+(55*(total-i)//total))
    fillcolor(grays)
    color(grays)
    begin_fill()
    down()
    fd(150)
    a=randint(0,3)
    fd(a*50)
    rt(90)
    for i in range(12):
        fd(150)
        b=randint(0,3)
        while a!=b:
            if a<b:
                lt(90)
                fd(50)
                rt(90)
                a+=1
            elif b<a:
                rt(90)
                fd(50)
                lt(90)
                a+=-1
        fd(10)
        c=randint(2,11)
        if c<=6:
            toit(c)
    goto(800,yhouse)
    goto(-850-40*i,yhouse)
    up()
    end_fill()
    color('black')
    goto(0,0)
            



def road():
    goto(-800,-200)
    setheading(270)
    rectangle(150,1600,'gray20')
    goto(-860,-260)
    lt(90)
    cote=10/cos(50*pi/180)
    for i in range(20):
        fd(80)
        rectangle(60,-10,'seashell')
    goto(0,0)

def neigborhood():
    global bridgeH
    global lastBuilding
    ecart=40
    nbbats=8
    housecolors=["firebrick","firebrick1","beige","bisque","bisque2","DarkKhaki","DarkSalmon","LightPink","papayawhip","PeachPuff","indianred1"]
    bridgeH=0
    lastBuilding=False
    goto(-780,-155)
    setheading(0)
    for i in range(nbbats):
        fd(ecart)
        if i == nbbats-1:
            lastBuilding=True
        if bridgeH==0:
            nbEtages=randint(1,5)
        else:
            nbEtages=bridgeH+randint(1,5-bridgeH)
            bridgeH=0
        randcolors=randint(0,len(housecolors)-1)
        for i in range(nbEtages):
            etage(housecolors[randcolors])
            deco_etage(i,ecart)
            lt(90)
            fd(50)
            rt(90)
        c=randint(0,6)
        fillcolor('black')
        begin_fill()
        down()
        toit(c)
        end_fill()
        up()
        rt(90)#descendre tt les etages
        fd(nbEtages*50)
        lt(90)
        fd(140)
    bk((140+ecart)*nbbats-800)


nbBgHouses=3
background()
for i in range(nbBgHouses):
    backgroundHouses(nbBgHouses,i)
neigborhood()
road()


done()