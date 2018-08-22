from gamegrid import *


class Dino(Actor):
    def __init__(self):
        Actor.__init__(self, "sprites/frog.gif")
		print(1)
		
		print(self.getDirection())
		self.inAir = False
		self.speed = 10

    def act(self):
        self.move()

    def onKeyRepeated(self, e):
        if not self.inAir:
			self.inAir = True