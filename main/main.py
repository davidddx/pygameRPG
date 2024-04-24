from debug.logger import logger
import game.GameHandler as gameHandler
import sys
if __name__ == '__main__':
    gameHandler.loop();
    logger.info(f"Game method {gameHandler.loop=} has finished running.")
    sys.exit()