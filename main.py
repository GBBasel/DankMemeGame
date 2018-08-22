import sys
sys.path.append('H:\Desktop\DankMemeGame')
from gamegrid import *

class Dino(Actor):
    def __init__(self):
        Actor.__init__(self, "sprites/frog.gif")
        self.inAir = False
        self.speed = 20
        self.gravitation = -2
        self.pressed = False

    def act(self):  
        if self.inAir:
            y = self.getY()
            y += -self.speed
            if self.pressed:
                self.speed += 1
            self.speed += self.gravitation
            if y > 300:
                self.setY(300)
                self.inAir = False
                self.speed = 20
            else:
                self.setY(y)
        self.pressed = False

    def onKeyRepeated(self, e):
        self.inAir = True
        self.pressed = True

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

