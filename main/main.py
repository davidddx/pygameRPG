from debug.logger import logger
import game.GameHandler as gameHandler
import sys
if __name__ == '__main__':
    try:
        gameHandler.loop();
        logger.info(f"Game method {gameHandler.loop=} has finished running.")
    except Exception as e:
        logger.error(f"Exception caught: {e}");
    finally:
        sys.exit()