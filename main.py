import sys
sys.path.append('H:\Desktop\DankMemeGame')
from gamegrid import *
import random

class Dino(Actor):
    def __init__(self):
        Actor.__init__(self, "sprites/frog.gif")
        self.setCollisionRectangle(Point(0, 0), 50, 25)
        self.inAir = False
        self.speed = 30
        self.gravitation = -3
        self.pressed = False

    def act(self):  
        if self.inAir:
            y = self.getY()
            y -= self.speed
            self.speed += self.gravitation
            if self.pressed and self.speed > 0:
                self.speed += 2
            if y > GROUND:
                self.reset()
            else:
                self.setY(y)
    

    def collide(self, actor1, actor2):
        print('ENDE')
        return 0
                
    def reset(self):
        self.setY(GROUND)
        self.inAir = False
        self.speed = 20

    def onkeyPressed(self, e):
        self.inAir = True
        self.pressed = True

    def onKeyReleased(self, e):
        self.pressed = False
            
class Gegner(Actor):
    def __init__(self, path='sprites/frog.gif'):
        Actor.__init__(self, path)
        self.speed = 5

    def act(self):
        self.move()
        self.destroy()
    
    def move(self):
         x = self.getX()
         x -= self.speed
         self.setX(x)
         
    def destroy(self):
        if self.getX() < -100:
            del self
            
class Kaktus(Gegner):
    def __init__(self, path='sprites/frog.gif'):
        Gegner.__init__(self, path)
        self.speed = 20
        
class Vogel(Gegner):
    def __init__(self, path='sprites/frog.gif'):
        Gegner.__init__(self, path)
        self.speed = 30
    

WIDTH = 800
HEIGHT = 600
GROUND = HEIGHT // 2


dino = Dino()
makeGameGrid(WIDTH, HEIGHT, 1, None, "sprites/lane.gif", False, keyPressed=dino.onkeyPressed, keyReleased=dino.onKeyReleased)
setSimulationPeriod(50)
addActor(dino, Location(GROUND, GROUND), 90)
show()
doRun()

gegner = 0

while not isDisposed():
    if gegner > 100 and 0.005 > random.random():
        if 0.5 > random.random():
            gegner = Kaktus()
            addActor(gegner, Location(WIDTH +100, GROUND), 90)
        else:
            gegner = Vogel()
            addActor(gegner, Location(WIDTH +100, random.randint(50, GROUND-50)), 90)
        dino.addCollisionActor(gegner)
        gegner = 0
    if 0.005 > random.random():
        addActor(Gegner(), Location(WIDTH +100, random.randint(50, GROUND-50)), 90)

    gegner += 1
    delay(10)
    
    
    
    

