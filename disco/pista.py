from .sector import Sector

class Pista:
    def __init__(self, num_sectores):
        self.sectores = [Sector() for _ in range(num_sectores)]
