class Camera:
    def __init__(self, pos : tuple[int, int]):
        self.pos = pos

    def changePos(self, x_factor : int, y_factor : int):
        self.pos = (self.pos[0] + x_factor, self.pos[1] + y_factor);