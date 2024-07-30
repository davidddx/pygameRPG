import json
import os

'''
INVENTORY FORMAT
(if player has no occurences of an item it will be taken out of the dict then they wont be seen in the dict)
(each item is in one category only)
(ITEM_X_ID is a num in string format)

{
    "CATEGORY_1": {ITEM_1_ID: NUM_OCCURENCES, ... , ITEM_N_ID: NUM_OCCURENCES},
    "CATEGORY_2": {ITEM_2_ID: NUM_OCCURENCES, ... , ITEM_M_ID: NUM_OCCURENCES},
    ..... ,
    ..... ,
    ..... ,
    "CATEGORY_N": {ITEM_X_ID: NUM_OCCURENCES, ... , ITEM_L_ID: NUM_OCCURENCES}
}


'''


def getInventoryPath():
    return os.path.join(os.getcwd(), "gamedata", "playerdata", "Inventory.json")

def loadInventory() -> dict:
    print("loading saved inventory data...")
    fileObj = open(getInventoryPath(), "r")
    return json.load(fileObj)

def saveInventoryData(inventory: dict):
    print("saving inventory data...")
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
        print(val)
        if type(val) != dict and invalidValTypeErrorMsg not in errorMsgs:
            inventoryValid = False
            errorMsgs.append(invalidValTypeErrorMsg)

    for error in errorMsgs:
        print(error)


    if not inventoryValid: return None

    inventoryFile = open(path, "w")
    json.dump(inventory, inventoryFile) 

def checkItemInInventory(item_id: int, item_category: str, inventory: dict):
    categoryInventory = inventory[item_category]
    strItemId = f"{item_id}"
    if strItemId in categoryInventory.keys():
        return True
    return False

def addItemToInventory(item_id: int, item_category: str, inventory: dict, amount=1):
    #print(f"previous inventory before add: {inventory=}")
    categoryInventory = inventory[item_category]

    strItemId = f"{item_id}"
    if not checkItemInInventory(item_id, item_category, inventory):
        categoryInventory[strItemId] = 0
    categoryInventory[strItemId]+= amount
    inventory[item_category] = categoryInventory
    #print(f"inventory after add: \n{inventory=}")

def removeItemFromInventory(item_id: int, item_category: str, inventory):
    categoryInventory = inventory[item_category]
    print(f"inventory before item removal:\n{inventory}")
    strItemId = f"{item_id}"
    if not checkItemInInventory(item_id, item_category, inventory):
        print(f"error: {item_id=} not in {inventory.keys()=}")
        return None
    if categoryInventory[strItemId] == 1:
        del categoryInventory[strItemId]
    else:
        categoryInventory[strItemId] -= 1
    inventory[item_category] = categoryInventory
    print(f"inventory after item removal:\n{inventory}")

