import sys
sys.path.append('H:\Desktop\DankMemeGame')
from gamegrid import *

class Dino(Actor):
    def __init__(self):
        Actor.__init__(self, "sprites/frog.gif")
        self.inAir = False
        self.speed = 30
        self.gravitation = -3
        self.pressed = False

    def act(self):  
        if self.inAir:
            y = self.getY()
            y += -self.speed
            self.speed += self.gravitation
            if y > 300:
                self.reset()
            else:
                self.setY(y)
                
    def reset(self):
        self.setY(300)
        self.inAir = False
        self.speed = 20

    def onKeyRepeated(self, e):
        self.inAir = True
        if self.speed > 0:
            self.speed += 1
            
class Gegner(Actor):
    def __init__(self):
        Actor.__init__(self, "sprites/frog.gif")
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

WIDTH = 800
HEIGHT = 600
speed = 10
GROUND = HEIGHT // 2


dino = Dino()
makeGameGrid(WIDTH, HEIGHT, 1, None, "sprites/lane.gif", False, keyPressed=dino.onKeyRepeated)
setSimulationPeriod(50)
addActor(dino, Location(GROUND, GROUND), 90)
show()
doRun()

while not isDisposed():
    addActor(Gegner(), Location(WIDTH +100, GROUND), 90)
    delay(1000)
    
    
    
    

