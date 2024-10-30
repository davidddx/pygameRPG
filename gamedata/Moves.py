'''
MOVE FORMAT:
MOVE_NAME = {
    NAME : "MOVE_NAME",
    TYPE : MoveTypes.MOVE_TYPE,
    DMG : DMG_VAL,
    LUCK : LUCK_VAL

    
}
'''
NAME = 'NAME'
DMG = 'DAMAGE'
LUCK = 'LUCK'
TYPE = 'TYPE'
NONE = "NONE"
class MoveTypes:
    STATUS_EFFECT = "STATUS_EFFECT"
    MELEE = "MELEE"
    RANGED = "RANGED"

PUNCH = {
        NAME: "PUNCH",
        TYPE: MoveTypes.MELEE,
        DMG: 5,
        LUCK: 10,
}
HEADBUTT = {
        NAME: "HEADBUTT",
        TYPE: MoveTypes.MELEE,
        DMG: 7,
        LUCK: 0,
}
KICK = {
        NAME: 'KICK',
        TYPE: MoveTypes.MELEE,
        DMG: 7,
        LUCK: 5,
}

MOVE_LIST = [PUNCH, HEADBUTT, KICK]
MOVE_NAMES = [move[NAME] for move in MOVE_LIST]
