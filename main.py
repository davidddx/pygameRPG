from debug.logger import logger
import game.Game as game
import sys
if __name__ == '__main__':
    game.loop();
    logger.info(f"Game method {game.loop=} has finished running.")
    sys.exit()
