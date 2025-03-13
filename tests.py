from turtle import*
import random
import math
import time
'''
def div2(n):
    """test si divisible par 2"""
    if n % 2 == 0:
        return True
    else:
        return False
assert div2(2) == True
assert(div2(3) == False, "3 est divisible par 2")
assert div2(4) == True


def div3(n):
    """test si divisible par 3"""
    if n % 3 == 0:
        return True
    else:
        return False
assert div3(2) == False
assert div3(3) == True
assert div3(4) == False

def div5(n):
    """test si divisible par 5"""
    if n % 5 == 0:
        return True
    else:
        return False
assert div5(2) == False
assert div5(3) == False
assert div5(5) == True

def divN(N,nb):
    """test si divisible par n en (nb divisible par N) """
    if nb % N == 0:
        return True
    else:
        return False
assert divN(2,2) == True
assert divN(3,3) == True
assert divN(6,5) == False

'''


num = 0
posX = 0
posY = 0
speed(0)
goto(posX,posY)


def door():
    color = "black"
    x = xcor()
    y = ycor()
    #random.randint(0,255),random.randint(0,255),random.randint(0,255)
    fillcolor(color)
    fillcolor(color)
    begin_fill()
    pendown()
    circle(10)
    end_fill()
    left(90)
    forward(10)
    right(90)
    forward(10)
    right(90)
    forward(30)
    right(90)
    forward(20)
    right(90)
    forward(30)
    right(90)
    forward(10)
    end_fill()
    penup()
    goto(x,y)
def jump():
    global num
    posX = xcor()
    posY = ycor()
    goto(posX+30, posY)
    num+=1   
def window():
    x = xcor()
    y = ycor()
    for i in range(4):
        pendown()
        fillcolor("white")
        forward(20)
        right(90)
        
        end_fill()
        penup()
    goto(x,y)
def balcony():
    x = xcor()
    y = ycor()
    window()
    right(90)
    forward(20)

    fillcolor("red")
    
    pendown()
    forward(10)
    left(90)
    forward(20)
    left(90)
    forward(10)
    left(90)
    forward(20)
    setheading(0)
    penup()


    
    end_fill()
    goto(x,y) 
def level():
    global num
    posX = xcor()
    posY = ycor()
    posY+=70
    posX -= 30*num
    print(posX,posY)
    goto(posX,posY)
    pendown()
    forward(90)
    penup()
    goto(posX,posY)
    left(90)
    forward(20)
    right(90)

     ## 0
def building():
    func_list = [door(), jump(), window(), jump(), balcony(), level()]  # like hwat?

    for i in range(random.randint(1, 10)):
        random.choice(func_list) 

def road():
    goto(posX,posY)
    pass



