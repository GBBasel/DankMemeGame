from gamegrid import *
from soundsystem import *
import random
import cmath
import math

PATH_TO_FILE = 'H:\Desktop\\DankMemeGame\\'

class Dino(Actor):
    def __init__(self):
        Actor.__init__(self, PATH_TO_FILE + "bilder\\dino200.png")
        self.setCollisionRectangle(Point(0, 0), 50, 25)
        self.gameOver = False
        self.inAir = False
        self.doubleJump = False
        self.gameOverText = None
        self.speed = 20
        self.boost = 20
        self.gravitation = -3
        self.pressed = False
        self.score = 0

    def act(self):
        if self.inAir:
            y = self.getY()
            y -= self.speed
            self.speed += self.gravitation
            if self.pressed and self.speed > 0:
                self.speed += 2
            if y > GROUND:
                self.putToGround()
            else:
                self.setY(y)
        self.score += 1
    

    def collide(self, actor1, actor2):
        self.game_over()
        return 0
                
    def putToGround(self):
        self.setY(GROUND)
        self.inAir = False
        self.doubleJump = False
        self.speed = 20

    def onkeyPressed(self, e):
        if not self.doubleJump and self.inAir and not self.pressed:
            self.speed += self.boost
            self.doubleJump = True
        
        self.inAir = True
        self.pressed = True
        if self.gameOver:
            self.restart()
        
    def onKeyReleased(self, e):
        self.pressed = False
    
    def game_over(self):
        self.gameOver = True
        self.gameOverText = TextActor("NOOB Game Over NOOB", Color.BLACK, Color.WHITE, Font("Arial", Font.BOLD, 60))
        addActor(self.gameOverText, Location(WIDTH//2-self.gameOverText.getWidth(0)//4, GROUND))
        doPause()
    
    def restart(self):
        self.gameOver = False
        removeActor(self.gameOverText)
        self.putToGround()
        for gegner in gegners:
            removeActor(gegner)
        doRun()
        
            
class Gegner(Actor):
    def __init__(self, path='sprites/frog.gif'):
        Actor.__init__(self, path)
        self.speed = 5
        self.cdirection = 1+0j
        
    def act(self):
        self.move()
        self.destroy()
        
    def turn(self, winkel):
        self.cdirection *= cmath.rect(1, winkel)
    
    def move(self):
         x = self.getX()
         y = self.getY()
         x -= int(self.speed * self.cdirection.real * SPEEDMULTIPLIERT)
         y -= int(self.speed * self.cdirection.imag * SPEEDMULTIPLIERT)
         self.setX(x)
         self.setY(y)
         
    def destroy(self):
        if self.getX() < -100:
            removeActor(self)
            
class Kaktus(Gegner):
    def __init__(self, path=PATH_TO_FILE + 'bilder/obiwandank.png'):
        Gegner.__init__(self, path)
        self.speed = 20
        
class Vogel(Gegner):
    def __init__(self, path=PATH_TO_FILE + 'bilder/bird60.png'):
        Gegner.__init__(self, path)
        self.speed = random.randint(10, 20)
        self.turn(random.uniform(-0.2, 0.2))
    
        
    def act(self):
        if random.random() < 0.05:
            self.turn(random.uniform(-0.5, 0.5))
        self.move()
        self.destroy()
        
        
class Boss(Gegner):
    def __init__(self, path='sprites/car1.gif'):
        Gegner.__init__(self, path)
        self.alive = 0   
    
    def act(self):
        self.alive += 0.1
        print(math.sin(self.alive))
        y = int(300 + math.sin(self.alive)*100)
        self.setY(y)
        if 0.05 > random.random():
            bullet = Bullet()
            addActor(bullet, Location(self.getX(), self.getY()), 90)
            dino.addCollisionActor(bullet)
       
class Bullet(Gegner):
    def __init__(self, path='sprites/frog.gif'):
        Gegner.__init__(self, path)
        self.speed = 20
        
        
WIDTH = 800
HEIGHT = 600
GROUND = HEIGHT // 2

SPEEDMULTIPLIERT = 1


dino = Dino()
makeGameGrid(WIDTH, HEIGHT, 1, None, PATH_TO_FILE + 'bilder/backgroundneu800.png', False, keyPressed=dino.onkeyPressed, keyReleased=dino.onKeyReleased)
setSimulationPeriod(50)
addActor(dino, Location(GROUND, GROUND), 90)

boss = Boss()
addActor(boss, Location(GROUND+350, GROUND), 90)
show()
doRun()


gegnerLauf = 0
gegners = []



while not isDisposed():
    if gegnerLauf > 80 and 0.05 > random.random():
        if 0.5 > random.random():
            gegner = Kaktus()
            addActor(gegner, Location(WIDTH +100, GROUND), 90)
        else:
            gegner = Vogel()
            addActor(gegner, Location(WIDTH +100, random.randint(50, GROUND-50)), 90)
        dino.addCollisionActor(gegner)
        gegnerLauf = 0
        gegners.append(gegner)
    if 0.005 > random.random():
        addActor(Gegner(path=PATH_TO_FILE + 'bilder/cloud100.png'), Location(WIDTH +100, random.randint(50, GROUND-50)), 90)
        
    if dino.gameOver:
        SPEEDMULTIPLIERT = 1
    else:
        SPEEDMULTIPLIERT += 0.001
        

    gegnerLauf += 1
    delay(10)
<<<<<<< Updated upstream
        

=======
    
    
          
>>>>>>> Stashed changes
