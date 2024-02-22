from game.Player import Player as Player
from debug.logger import logger
class Level:
    def __init__(self):
        try:
            logger.debug(f"Class {Level=} initializing....")

            logger.debug(f"Class {Level=} intialized.")
        except Exception as e:
            logger.error(f"Failed {Level=} class initialization.\n Error: {e}")
        self.player = Player();

    def update(self):
        self.player.update();
