from gamegrid import *

class Wolke(Actor):
    def __init__(self, "bilder/wolke.jpg"):
        Actor.__init__(self,)
    
    def act(self):
        self.move()
        if self.getX() < -100:
            self.setX(1650)
        if self.getX() > 1650:
            self.setX(-100)

wolke = Wolke("bilder/wolke.jpg")
def initWolke():
    for i in range(20):
        if i < 5:
            addActor(wolke, Location(350 * i, 100), 0)