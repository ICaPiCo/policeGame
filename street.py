from random import*

def create_text():
    info = {"nose":["green","red","blue"],"hair":["black","blond","brown"],"eyes":["blue","green","brown"],"skin":["white","black","brown"]}
    text = ""
    for key in info:
        text += f"{key} : {choice(info[key])}, "
    print(text)

<<<<<<< HEAD
create_text()
=======
up() #entre chaque fonctions, le stylo est en position up, pour bouger librement
speed(0) #y'a pas plus vite?? :(

def rectangle(lenght,width,color): #crée un rectangle rempli de couleur, reutilisé beacoup de fois
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

def etage(color): #fait un etage, surtout pour clarifier dans le code qu'on ne fait pas qu'un rectangle lambda mais un etage
    rectangle(140,50,color)

def fenetre(proba): #fait une fenetre avec ou sans balcon
    if proba!=0:
        rectangle(30,30,'white')
        if proba>=6: #avec balcon
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


def porte(proba): #fait une porte avec un haut rond ou carre avec une couleur alea
    doorcolors=["gold1","burlywood4","DarkOrange4","gray0","LightCyan4","HotPink3"] #liste pour avoir couleur aleatoire 
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
        circle(15,180) #moitie de cercle
        fd(30)
        lt(90)
        end_fill()
        up()

def deco_etage(etage,ecart): #decore chaque etage avec ou sans fenetre ou porte ou pont
    global bridgeH
    global lastBuilding
    a=randint(0,2) #A determine la position de la porte au premier etage, entre 3 positions
    br=randint(0,9) #1/10 chances d'avoir un pont
    fd(15)
    up()
    for i in range(3):
        if i==a and etage==0: #A  si on est a l'emplacement de la porte et au premier etage
            d=randint(0,4)
            porte(d) #porte avec 1/4 chances d'etre rectangulaire
        else:
            if etage != 0:
                b=randint(0,9) #B 1/3 chance environ d'avoir une fenetre avec balcon 
            else:
                b=randint(0,5) #B 1/4 chance de ne pas avoir de fenetre si au premier etage
            lt(90)
            fd(10)
            rt(90)
            fenetre(b)
            rt(90)
            fd(10)
            lt(90)
        fd(40)
    fd(5)
    if br==0 and etage!=0 and not lastBuilding: #1/10 chance si on est pas au premier etage et que ce n'est pas le dernier building
        bridgeH=etage #                         #pour avoir un pont (ce serait tres drole si ca existait vraiment)
        fd(ecart)
        lt(90)
        fillcolor('cornsilk2') #j'aime bien les couleurs comme ca, dans le PoliceGame aussi je me suis amuse avec 'color theory'
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
    

def toit(proba): #fait un toit avec des variantes
    if proba>=4: #faire un petit toit
        fd(150)
        lt(150)
        fd(80/(cos(30*pi/180)))
        lt(60)
        fd(80/(cos(30*pi/180)))
        lt(150)
        fd(10)
    elif proba>=2: #faire un grand toit
        fd(150)
        lt(110)
        fd(80/(cos(70*pi/180)))
        lt(140)
        fd(80/(cos(70*pi/180)))
        lt(110)
        fd(10)
    else: #faire un toit rectangulaire
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
        
def background(): #dessine des semblants d'arbres avec de l'aleatoire
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
    goto(-800,250)
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

def backgroundHouses(total,i):#dessine les silouhettes de maisons en background
    setheading(180)
    yhouse=-150+(total-i-1)*100/total #AA formule compliquée pour les maisons, complémentaire au fd avec commentaire AA 
    goto(-850-40*i,yhouse)
    rt(90)
    grays='gray'+str(20+(55*(total-i)//total)) #fait des couleurs de maisons de plus en plus foncées en gris
    fillcolor(grays)
    color(grays)
    begin_fill()
    down()
    fd(20*(total-i+2)+60) #AA avoir une hauteur prédéfinie(60), + de plus en plus petit par rapport a i
    a=randint(0,2)
    fd(a*50)
    rt(90)
    for o in range(12):
        fd(150)
        b=randint(0,2) #différence de hauteur des tmaisosn de fond
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
        if i+1==total:#1- si on est sur la derniere ligne de maisons
            if randint(0,1)!=0:#une chance sur deux d'avoir:
                toit(4) #petit toit 
        elif c<=6: #1- si c<=6 (1/2chances), encore une chance sur deux d'avoir:
            toit(c) #petit toit ou grand toit
        elif c==11:#1- si on est pas sur la derniere ligne, et c a 1/9chances de faire:
            toit(2) #grand toit
    setheading(0)
    fd(150)
    goto(800,yhouse)
    goto(-850-40*i,yhouse)
    up()
    end_fill()
    color('black')
    goto(0,0)
            

def whiteStripesOnRoad():
    for i in range(20):
        fd(80)
        rectangle(60,-10,'seashell')

def road(): #dessine une route devant les maisons
    goto(-800,-200)
    setheading(270)
    rectangle(150,1600,'gray20')
    goto(-860,-260)
    lt(90)
    whiteStripesOnRoad()
    goto(0,0)

def neigborhood(nbbats): #assemble les autres fonctions pour faire un alignement de maisons
    global bridgeH
    global lastBuilding
    ecart=40
    housecolors=["firebrick","firebrick1","beige","bisque","bisque2","DarkKhaki","DarkSalmon","LightPink","papayawhip","PeachPuff","indianred1"]
    bridgeH=0
    lastBuilding=False
    goto(-760,-155)
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

def city():
    nbBgHouses=10 #A consommer avec moderation
    background()
    for i in range(nbBgHouses):
        backgroundHouses(nbBgHouses,i)
    neigborhood(8)
    road()

city()

done() #pas 256 lignes :( ca veut dire que j'ai peut etre utilise chat gpt car ma signature n'est pas presente
>>>>>>> 4981e672b377405f3c9f4f4f9d1dc9cce1016107
