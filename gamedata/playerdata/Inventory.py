import json
import os
from debug.logger import logger

'''
INVENTORY FORMAT
(if player has no occurences of an item it will be taken out of the dict then they wont be seen in the dict)
(each item is in one category only)


{
    "CATEGORY_1": {ITEM_1_ID: NUM_OCCURENCES, ... , ITEM_N_ID: NUM_OCCURENCES},
    "CATEGORY_2": {ITEM_2_ID: NUM_OCCURENCES, ... , ITEM_M_ID: NUM_OCCURENCES},
    ..... ,
    ..... ,
    ..... ,
    "CATEGORY_N": {ITEM_3_ID: NUM_OCCURENCES, ... , ITEM_L_ID: NUM_OCCURENCES}
}


'''

Inventory = {}

def getInventoryPath():
    return os.path.join(os.getcwd(), "gamedata", "playerdata", "Inventory.json")

def loadInventory() -> dict:
    logger.info("Loading saved inventory data...")
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

def checkItemInInventory(item_id: int, item_category: str):
    global Inventory
    inventory = Inventory[item_category]
    if item_id in inventory.keys():
        return True
    return False

def addItemToInventory(item_id: int, item_category: str):
    global Inventory
    logger.debug(f"previous inventory before add {Inventory=}")
    inventory = Inventory[item_category]
    if not checkItemInInventory(item_id, item_category):
        inventory[item_id] = 1
    else:
        inventory[item_id]+=1
    Inventory[item_category] = inventory
    logger.debug(f"inventory after add {Inventory=}")

def removeItemFromInventory(item_id: int, item_category: str):
    global Inventory
    logger.debug(f"previous inventory before removal {Inventory=}")
    inventory = Inventory[item_category]
    if not checkItemInInventory(item_id, item_category):
        logger.debug(f"error: {item_id=} not in {inventory.keys()=}")
        return None
    if inventory[item_id] == 1:
        del inventory[item_id]
    else:
        inventory[item_id] -= 1
    Inventory[item_category] = inventory
    logger.debug(f"inventory after item removal {Inventory=}")

