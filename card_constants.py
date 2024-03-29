from abilities_constants import *
from constants import *

deck_one = [
    {
        'card': {
            'name': 'Arha Initiate',
            'worth': 1,
            'card_type': 1,
            'faction': ENLIGHTENED,
            'buy': 1,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DRAW_1,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Arha Templar',
            'worth': 3,
            'card_type': 1,
            'faction': ENLIGHTENED,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DEFEAT_MONSTER_LT_4,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Ascetic of the Lidless Eye',
            'worth': 2,
            'card_type': 1,
            'faction': ENLIGHTENED,
            'buy': 5,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DRAW_2,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Master Dhartha',
            'worth': 3,
            'card_type': 1,
            'faction': ENLIGHTENED,
            'buy': 7,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DRAW_3,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Oziah the Peerless',
            'worth': 3,
            'card_type': 1,
            'faction': ENLIGHTENED,
            'buy': 6,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DEFEAT_MONSTER_LT_6,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Seer of the Forked Path',
            'worth': 1,
            'card_type': 1,
            'faction': ENLIGHTENED,
            'buy': 2,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DRAW_1_BANISH_CENTER,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Temple Librarian',
            'worth': 1,
            'card_type': 1,
            'faction': ENLIGHTENED,
            'buy': 2,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': IF_DISCARD_DRAW_TWO,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Twofold Askara',
            'worth': 2,
            'card_type': 1,
            'faction': ENLIGHTENED,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': COPY_EFFECT,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'The All-Seeing Eye',
            'worth': 2,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': ENLIGHTENED,
            'buy': 6,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_DRAW_1,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Tablet of Time\'s Dawn',
            'worth': 2,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': ENLIGHTENED,
            'buy': 5,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': BANISH_THIS_EXTRA_TURN,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Cetra, Weaver of Stars',
            'worth': 4,
            'card_type': CARD_TYPE_HERO,
            'faction': LIFEBOUND,
            'buy': 7,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': ACQUIRE_ANY_CENTER_HERO,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Druids of the Stone Circle',
            'worth': 3,
            'card_type': CARD_TYPE_HERO,
            'faction': LIFEBOUND,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': ACQUIRE_HERO_3_OR_LESS_TO_TOP_OF_DECK,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Flytrap Witch',
            'worth': 2,
            'card_type': CARD_TYPE_HERO,
            'faction': LIFEBOUND,
            'buy': 5,
            'kill': 0,
            'instant_worth': 2,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DRAW_1,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Landtalker',
            'worth': 3,
            'card_type': CARD_TYPE_HERO,
            'faction': LIFEBOUND,
            'buy': 6,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 3,
            'instant_kill': 0,
            'abilities': None,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Lifebound Initiate',
            'worth': 1,
            'card_type': CARD_TYPE_HERO,
            'faction': LIFEBOUND,
            'buy': 1,
            'kill': 0,
            'instant_worth': 1,
            'instant_buy': 1,
            'instant_kill': 0,
            'abilities': None,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Runic Lycanthrope',
            'worth': 1,
            'card_type': CARD_TYPE_HERO,
            'faction': LIFEBOUND,
            'buy': 3,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 2,
            'instant_kill': 0,
            'abilities': IF_LIFEBOUND_HERO_PLUS_2_KILL,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Wolf Shaman',
            'worth': 1,
            'card_type': CARD_TYPE_HERO,
            'faction': LIFEBOUND,
            'buy': 3,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 1,
            'instant_kill': 0,
            'abilities': DRAW_1,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Snapdragon',
            'worth': 2,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': LIFEBOUND,
            'buy': 5,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_PLUS_1_BUY_FIRST_LIFEBOUND_HERO_PLUS_1_POINT,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Yggdrasil Staff',
            'worth': 2,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': LIFEBOUND,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_PLUS_1_KILL_CAN_SPEND_4_TO_BUY_3_POINTS,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Avatar Golem',
            'worth': 2,
            'card_type': CARD_TYPE_HERO,
            'faction': MECHANA,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 2,
            'abilities': PLUS_1_POINT_PER_CONTROLLED_CONSTRUCT,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Kor, the Ferrormancer',
            'worth': 2,
            'card_type': CARD_TYPE_HERO,
            'faction': MECHANA,
            'buy': 3,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 2,
            'abilities': DRAW_1_IF_CONTROL_GT_2_CONSTRUCTS,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Mechana Insitute',
            'worth': 1,
            'card_type': CARD_TYPE_HERO,
            'faction': MECHANA,
            'buy': 1,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PLUS_1_BUY_OR_1_KILL,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Reactor Monk',
            'worth': 2,
            'card_type': CARD_TYPE_HERO,
            'faction': MECHANA,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 2,
            'instant_kill': 0,
            'abilities': NEXT_CONSTRUCT_1_LESS_BUY,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Burrower Mark II',
            'worth': 3,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': MECHANA,
            'buy': 3,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_WHEN_PLAY_MECHANA_CONSTRUCT_DRAW_1_INCLUDING_THIS_ONE,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Grand Design',
            'worth': 6,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': MECHANA,
            'buy': 6,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_PLUS_2_BUY_FOR_MECHANA_CONSTRUCT_ONLY,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Hedron Cannon',
            'worth': 8,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': MECHANA,
            'buy': 8,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_PLUS_1_KILL_PER_CONTROLLED_MECHANA_CONTRUCT,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Hedron Link Device',
            'worth': 7,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': MECHANA,
            'buy': 7,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': ALL_CONTRUCTS_ARE_MECHANA,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Rocker Courier x-99',
            'worth': 4,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': MECHANA,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_WHEN_ACQUIRE_MECHANA_CONSTRUCT_PUT_IN_PLAY,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Watchmaker Altar',
            'worth': 5,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': MECHANA,
            'buy': 5,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_PLUS_1_BUY_FOR_MECHANA_CONSTRUCT_ONLY,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Arbiter of the Precipice',
            'worth': 1,
            'card_type': CARD_TYPE_HERO,
            'faction': VOID,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DRAW_2_THEN_BANISH_1_HAND,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Demon Slyyer',
            'worth': 2,
            'card_type': CARD_TYPE_HERO,
            'faction': VOID,
            'buy': 4,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 3,
            'abilities': None,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Emri, One with the void',
            'worth': 3,
            'card_type': CARD_TYPE_HERO,
            'faction': VOID,
            'buy': 6,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 4,
            'abilities': None,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Shade of the Black Witch',
            'worth': 1,
            'card_type': CARD_TYPE_HERO,
            'faction': VOID,
            'buy': 3,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 2,
            'abilities': CAN_BANISH_1_HAND_OR_DISCARD,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Spike Vixen',
            'worth': 1,
            'card_type': CARD_TYPE_HERO,
            'faction': VOID,
            'buy': 2,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 1,
            'abilities': DRAW_1,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Void Initiate',
            'worth': 1,
            'card_type': CARD_TYPE_HERO,
            'faction': VOID,
            'buy': 1,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 1,
            'instant_kill': 0,
            'abilities': CAN_BANISH_1_HAND_OR_DISCARD,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Murasama',
            'worth': 4,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': VOID,
            'buy': 7,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_PLUS_3_KILL,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Shadow Star',
            'worth': 2,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': VOID,
            'buy': 3,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_PLUS_1_KILL,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Voidthirster',
            'worth': 3,
            'card_type': CARD_TYPE_PERSISTENT,
            'faction': VOID,
            'buy': 5,
            'kill': 0,
            'instant_worth': 0,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Avatar of the Fallen',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 7,
            'instant_worth': 4,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': CANNOT_BE_BANISHED_ACQUIRE_ANY_CENTER_CARD,
            'banishable': False,
        },
        'count': 1,
    },
    {
        'card': {
            'name': 'Corrosive Widow',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 4,
            'instant_worth': 3,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': OPPONENTS_DESTROY_1_CONSTRUCT,
        },
        'count': 4,
    },
    {
        'card': {
            'name': 'Earth Tyrant',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 6,
            'instant_worth': 5,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DRAW_2,
        },
        'count': 2,
    },
    {
        'card': {
            'name': 'Mephit',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 3,
            'instant_worth': 2,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': CAN_BANISH_1_CENTER,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Mistake of Creation',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 4,
            'instant_worth': 4,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': CAN_BANISH_1_HAND_OR_DISCARD_AND_CENTER,
        },
        'count': 4,
    },
    {
        'card': {
            'name': 'Samael Trickster',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 3,
            'instant_worth': 1,
            'instant_buy': 1,
            'instant_kill': 0,
            'abilities': None,
        },
        'count': 4,
    },
    {
        'card': {
            'name': 'Sea Tyrant',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 5,
            'instant_worth': 5,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': OPPONENTS_KEEP_1_CONSTRUCT,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Tormented Soul',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 3,
            'instant_worth': 1,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': DRAW_1,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Wind Tryant',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 5,
            'instant_worth': 3,
            'instant_buy': 3,
            'instant_kill': 0,
            'abilities': None,
        },
        'count': 3,
    },
    {
        'card': {
            'name': 'Xeron, Duke of Lies',
            'worth': 0,
            'card_type': CARD_TYPE_MONSTER,
            'faction': None,
            'buy': 0,
            'kill': 6,
            'instant_worth': 3,
            'instant_buy': 0,
            'instant_kill': 0,
            'abilities': ADD_RANDOM_CARD_TO_HAND_FROM_EACH_OPPONENT,
        },
        'count': 1,
    },

]
