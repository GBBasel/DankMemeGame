from gamegrid import *
from soundsystem import *
import random
import cmath
import math
import time

# Für jeden PC anders
PATH_TO_FILE = 'C:\\Jetbrains\\PyCharm\\DankMemeGame\\'


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
        self.startTime = time.time()

    def act(self):
        if self.inAir:
            # beschleunigung berechnung
            y = self.getY()
            y -= self.speed
            self.speed += self.gravitation
            # wenn man eine taste dr�ckt und der dino nicht f�llt, f�llt er langsamer
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
        # reset dino
        self.setY(GROUND)
        self.inAir = False
        self.doubleJump = False
        self.speed = 20

    def onkeyPressed(self, e):
        # wird ausgef�ht wenn eine taste gedr�ckt wird
        # double jump
        if not self.doubleJump and self.inAir and not self.pressed:
            self.speed += self.boost
            self.doubleJump = True

        self.inAir = True
        self.pressed = True
        # wenn das spiel vorbei ist wird es neu gestartet
        if self.gameOver:
            self.restart()

    def onKeyReleased(self, e):
        self.pressed = False

    def game_over(self):
        self.gameOver = True
        self.gameOverText = TextActor("Game Over Score: {}".format(self.score), Color.BLACK, Color.WHITE,
                                      Font("Arial", Font.BOLD, 60))
        addActor(self.gameOverText, Location(WIDTH // 2 - self.gameOverText.getWidth(0) // 4, GROUND))
        doPause()

    def restart(self):
        # global
        self.gameOver = False
        removeActor(self.gameOverText)
        # dino
        self.putToGround()
        self.score = 0
        # boss
        removeActor(boss)
        self.startTime = time.time()
        boss.aktive = False
        boss.onespawned = False
        # gegner
        for gegner in gegnersliste:
            removeActor(gegner)
        doRun()


class Gegner(Actor):
    def __init__(self, path='sprites/frog.gif'):
        Actor.__init__(self, path)
        self.speed = 5
        self.cdirection = 1 + 0j  # richtung mit einer komplexen zahl

    def act(self):
        self.move()
        self.destroy()

    def turn(self, winkel):
        # dreht sich um 'winkel' in radian
        self.cdirection *= cmath.rect(1, winkel)

    def move(self):
        # bewegung
        x = self.getX()
        y = self.getY()
        x -= int(self.speed * self.cdirection.real * SPEEDMULTIPLIERT)
        y -= int(self.speed * self.cdirection.imag * SPEEDMULTIPLIERT)
        self.setX(x)
        self.setY(y)

    def destroy(self):
        # l�scht objekt
        if self.getX() < -100:
            removeActor(self)
            del self


class Kaktus(Gegner):
    def __init__(self, path=PATH_TO_FILE + 'bilder\\obiwandank100.png'):
        Gegner.__init__(self, path)
        self.speed = 20


class Vogel(Gegner):
    def __init__(self, path=PATH_TO_FILE + 'bilder\\bird60.png'):
        Gegner.__init__(self, path)
        self.speed = random.randint(10, 20)  # zuf�llige geschwindigkeit
        self.turn(random.uniform(-0.2, 0.2))

    def act(self):
        # �ndert zuf�llig seine richtung
        if random.random() < 0.05:
            self.turn(random.uniform(-0.5, 0.5))
        self.move()
        self.destroy()


class Boss(Gegner):
    def __init__(self, path=PATH_TO_FILE + 'bilder\\boss200.png'):
        Gegner.__init__(self, path)
        self.alive = 0  # variable f�r die bewegung
        self.aktive = False  # True wenn er da ist
        self.onespawned = False  # spawned nur einmal pro game
        self.timeSpawned = None  # zeitpunkt des spawnens

    def act(self):
        # nach 10 sekunden wird er despawned
        if time.time() - self.timeSpawned > 10:
            self.aktive = False
            removeActor(self)
        # brechnet und setzt position
        self.alive += 0.1
        y = int(300 + math.sin(self.alive) * 100)
        self.setY(y)
        # spawned bullets
        if 0.025 > random.random():
            bullet = Bullet()
            addActor(bullet, Location(self.getX(), self.getY()), 90)
            dino.addCollisionActor(bullet)
            gegnersliste.append(bullet)


class Bullet(Gegner):
    def __init__(self, path=PATH_TO_FILE + 'bilder\\bullet.png'):
        Gegner.__init__(self, path)
        self.speed = 20


WIDTH = 800
HEIGHT = 600
GROUND = HEIGHT // 2

SPEEDMULTIPLIERT = 1  # geschwindigkeit der gegenr

dino = Dino()

makeGameGrid(WIDTH, HEIGHT, 1, None, PATH_TO_FILE + 'bilder/backgroundneu800.png', False, keyPressed=dino.onkeyPressed,
             keyReleased=dino.onKeyReleased)
setSimulationPeriod(50)

addActor(dino, Location(GROUND, GROUND), 90)

boss = Boss()

show()
doRun()

gegnerLauf = 0  # verhindert zu viele gegner spawns
gegnersliste = []  # speichert alle gegner um sie sp�ter zu l�schen

# Game Loop
while not isDisposed():
    # Boss Spawn
    if time.time() - dino.startTime > 10 and not boss.aktive and not boss.onespawned:
        # init boss
        boss.aktive = True
        boss.onespawned = True
        boss.timeSpawned = time.time()
        addActor(boss, Location(GROUND + 350, GROUND), 90)
    # Gegner Spawn
    if gegnerLauf > 80 and 0.05 > random.random() and not boss.aktive:
        if 0.5 > random.random():  # 50%
            gegner = Kaktus()
            addActor(gegner, Location(WIDTH + 100, GROUND), 90)
        else:
            gegner = Vogel()
            addActor(gegner, Location(WIDTH + 100, random.randint(50, GROUND - 50)), 90)
        dino.addCollisionActor(gegner)
        gegnerLauf = 0
        gegnersliste.append(gegner)
    # Wolken Spawn
    if 0.005 > random.random() and not dino.gameOver:
        addActor(Gegner(path=PATH_TO_FILE + 'bilder/cloud100.png'),
                 Location(WIDTH + 100, random.randint(50, GROUND - 50)), 90)

    if dino.gameOver:
        SPEEDMULTIPLIERT = 1
    elif not boss.aktive:
        SPEEDMULTIPLIERT += 0.001

    gegnerLauf += 1
    delay(10)
