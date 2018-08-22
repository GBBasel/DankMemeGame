from gamegrid import *


class Dino(Actor):
    def __init__(self, path):
        super().__init__(self, path)

    def act(self):
        self.move()
