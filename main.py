import sys
sys.path.append('H:\Desktop\DankMemeGame')
from gamegrid import *

from actors import Dino

makeGameGrid(800, 600, 1, None, "sprites/lane.gif", False)
setSimulationPeriod(50)
show()
doRun()
