WHERE_GAME_HAND = 0
WHERE_PERSISTENT = 1
WHERE_PLAYER_HAND = 2
WHERE_PLAYED = 3
WHERE_GAME_DISCARD = 4
WHERE_PLAYER_DISCARD = 5
WHERE_PLAYER_PERSISTENT = 6

CARD_TYPE_MONSTER = 0
CARD_TYPE_HERO = 1
CARD_TYPE_PERSISTENT = 2

# pause game play to select card in order to do something with it
ACTION_BANISH = 1
ACTION_COPY = 2
ACTION_DISCARD_FROM_PLAYER_HAND = 3
# defeat means that player can defeat a monster without paying it's cost
ACTION_DEFEAT = 4
ACTION_ACQUIRE_TO_TOP = 5
ACTION_KEEP = 6
ACTION_BANISH_PLAYER_PERSISTENT = 7
ACTION_USE = 8
# kill means that a player can spend kill to defeat card
ACTION_KILL = 9
# buy means that a player can spend buy to acquire card
ACTION_BUY = 10
ACTION_PLAY = 11
ACTION_ACQUIRE_TO_HAND = 12
ACTION_ACQUIRE_TO_DISCARD = 13
ACTION_BANISH_PLAYER_HAND = 14
ACTION_BANISH_PLAYER_DISCARD = 15
ACTION_ACQUIRE_TO_PHAND = 16
ACTION_THIS_OR_THAT = 17

# normal game play
ACTION_NORMAL = [ACTION_BUY, ACTION_KILL, ACTION_PLAY]


BUY_1 = 'plus 1 buy'
KILL_1 = 'plus 1 kill'


# signifies we're done with the action
END_OF_ACTION = 0
END_OF_TURN = 1

ENLIGHTENED = 0
VOID = 1
MECHANA = 2
LIFEBOUND = 3
STARTING = 4

CANNOT_KILL_THIS_CARD = 'You cannot kill this card, it is a %s'
CANNOT_BUY_THIS_CARD = 'You cannot buy this card, it is a monster'
NOT_ENOUGH_KILL = 'Not enough kill'
NOT_ENOUGH_BUY = 'Not enough buy'
INVALID_SELECTION = 'No idea what you are doing, but it is wrong.'
NO_CARDS = 'You have no cards left. You should end your turn'
INVALID_CARD = 'Invalid card. Try a number 0 - %s. EX: c3 for the [c]ard with the 3 in front of it'
