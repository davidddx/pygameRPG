import json
import os
from debug.logger import logger

def getInventoryPath():
    return os.path.join(os.getcwd(), "gamedata", "playerdata", "Inventory.json")

def loadInventory() -> dict:
    logger.info("loading inventory saved data...")
    fileObj = open(getInventoryPath(), "r")
    return json.load(fileObj)

def saveInventoryData(inventory: dict):

    logger.info("saving inventory data....")
    #### checking if valid formatted inventory ####
    path = getInventoryPath()
    previousInventoryFile = open(path, "r")
    previousInventory = json.load(previousInventoryFile)
    previousInventoryKeys = previousInventory.keys()
    errorMsgs = []
    inventoryValid = True
    if len(inventory.keys()) != len(previousInventoryKeys):
        inventoryValid = False
        errorMsgs.append("error, could not save data. Inventory has invalid number of keys")

    invalidKeyTypeErrorMsg = "error, the key type of inventory must be str"
    keyNotFoundErrorMsg = "error, a key was entered in the inventory that was not previously there"

    for key in inventory.keys():
        if type(key) != str and invalidKeyTypeErrorMsg not in errorMsgs:
            inventoryValid = False
            errorMsgs.append(invalidKeyTypeErrorMsg)
        if key not in previousInventoryKeys and keyNotFoundErrorMsg not in errorMsgs:
            inventoryValid = False
            errorMsgs.append(keyNotFoundErrorMsg)
   
    invalidValTypeErrorMsg = "error, value type of inventory is dict"
    for val in inventory.values():
        if type(val) != dict[str, int] and invalidValTypeErrorMsg not in errorMsgs:
            inventoryValid = False
            errorMsgs.append(invalidValTypeErrorMsg)

    for error in errorMsgs:
        logger.error(error)
        print(error)

    if not inventoryValid: return None

    inventoryFile = open(path, "w")
    json.dump(inventory, inventoryFile) 

