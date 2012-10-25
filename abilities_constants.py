DRAW_1 = 'Draw a card'
DRAW_2 = 'Draw two cards'
DRAW_2_THEN_BANISH_1_HAND = 'Draw two cards. Then Banish any card in your hand'
DRAW_3 = 'Draw three cards'
DRAW_1_BANISH_CENTER = 'Draw a card. then you may banish a card in the center row'
DRAW_1_IF_CONTROL_GT_2_CONSTRUCTS = 'Draw a card if you control 2 or more Constructs'
IF_DISCARD_DRAW_TWO = 'If you discard a card, draw two cards'
BANISH_THIS_EXTRA_TURN = 'Banish this card to take an additional turn after this'
COPY_EFFECT = 'Copy the effect of a Hero played this turn'
DEFEAT_MONSTER_LT_6 = 'Defeat a Monster that has 6p or less'
DEFEAT_MONSTER_LT_4 = 'Defeat a Monster that has 4p or less'
ACQUIRE_ANY_CENTER_HERO = 'Acquire any Hero. Place it on top of your deck'
IF_LIFEBOUND_HERO_PLUS_2_KILL = 'If you played a Lifebound Hero this turn, gain 2 kill'
ACQUIRE_HERO_3_OR_LESS_TO_TOP_OF_DECK = 'Acquire a Hero that costs 3 buy or less. Place it on top of your deck'
PLUS_1_BUY_OR_1_KILL = 'Gain 1 buy or 1 kill'
PLUS_1_POINT_PER_CONTROLLED_CONSTRUCT = 'Gain 1 point for each type of Construct you control. {Types are Enlightened, Mechana, Lifebound, and Void}'
NEXT_CONSTRUCT_1_LESS_BUY = 'The next Construct you acquire this turn costs 1 buy less'
CAN_BANISH_1_HAND_OR_DISCARD_AND_CENTER = 'You may banish a card in the center row and/or a card in your discard pile'
OPPONENTS_KEEP_1_CONSTRUCT = 'Each opponent must choose a Construct they control and put the rest into their discard pile'
CAN_BANISH_1_CENTER = 'You may banish a card in the center row'
CANNOT_BE_BANISHED_ACQUIRE_ANY_CENTER_CARD= 'This monster cant be banished unless defeated. Rw: gain 4 points. Acquire or defeat any other card in the center row'
OPPONENTS_DESTROY_1_CONSTRUCT = 'Each opponent must put a Contruct he controls into his discard pile'
ADD_RANDOM_CARD_TO_HAND_FROM_EACH_OPPONENT = 'Take a card at random from each opponents hand and add that card to your hand'
PER_TURN_DRAW_1 = 'Once per turn, you may draw a card'
PER_TURN_PLUS_1_KILL_CAN_SPEND_4_TO_BUY_3_POINTS = 'Once per turn, gain 1 kill. Once per turn, you may spend 4 buy to gain 3 points'
PER_TURN_PLUS_1_BUY_FIRST_LIFEBOUND_HERO_PLUS_1_POINT = 'Once per turn, gain 1 buy. The first time you play a Lifebound Hero each turn, gain 1 point'
PER_TURN_WHEN_PLAY_MECHANA_CONSTRUCT_DRAW_1_INCLUDING_THIS_ONE = 'Draw a card the first time you put a Mechana construct into play each turn {Including this one} '
PER_TURN_PLUS_1_BUY_FOR_MECHANA_CONSTRUCT_ONLY = 'Once per turn, gain 1 buy. You may spent it only to acquire a Mechana Construct'
PER_TURN_WHEN_ACQUIRE_MECHANA_CONSTRUCT_PUT_IN_PLAY = 'Once per turn, when you acquire another Mechana Construct, you may put it directly into play'
PER_TURN_PLUS_2_BUY_FOR_MECHANA_CONSTRUCT_ONLY = 'Once per turn, gain 2 buy. You may spend it only to acquire Mechana Constructs'
PER_TURN_PLUS_1_KILL_PER_CONTROLLED_MECHANA_CONTRUCT = 'Once per turn, gain 1 kill for each Mechana Construct you control'
ALL_CONTRUCTS_ARE_MECHANA = 'You may treat all Constructs as Mechana Constructs'
PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT = 'Once per turn, gain 1 kill. The first time you defeat a Monster in the center row each turn, gain 1 point'
CAN_BANISH_1_HAND_OR_DISCARD = 'You may banish a card in your hand or discard pile'
PER_TURN_PLUS_3_KILL = 'Once per turn, gain 3 kill'
PER_TURN_PLUS_1_KILL = 'Once per turn, gain 1 kill'
ACQUIRE_OR_DEFEAT_ANY = 'Acquire or defeat any card without paying the cost'

# these are directly mapped to function names
ABILITY_MAP = {
    DRAW_1: 'draw_1',
    DRAW_2: 'draw_2',
    DRAW_2_THEN_BANISH_1_HAND: 'draw_2_then_banish_1_hand',
    DRAW_3: 'draw_3',
    DRAW_1_BANISH_CENTER: 'draw_1_banish_center',
    DRAW_1_IF_CONTROL_GT_2_CONSTRUCTS: 'draw_1_if_control_gt_2_constructs',
    IF_DISCARD_DRAW_TWO: 'if_discard_draw_two',
    BANISH_THIS_EXTRA_TURN: 'banish_this_extra_turn',
    COPY_EFFECT: 'copy_effect',
    DEFEAT_MONSTER_LT_6: 'defeat_monster_lt_6',
    DEFEAT_MONSTER_LT_4: 'defeat_monster_lt_4',
    ACQUIRE_ANY_CENTER_HERO: 'acquire_any_center_hero',
    IF_LIFEBOUND_HERO_PLUS_2_KILL: 'if_lifebound_hero_plus_2_kill',
    ACQUIRE_HERO_3_OR_LESS_TO_TOP_OF_DECK: 'acquire_hero_3_or_less_to_top_of_deck',
    PLUS_1_BUY_OR_1_KILL: 'plus_1_buy_or_1_kill',
    PLUS_1_POINT_PER_CONTROLLED_CONSTRUCT: 'plus_1_point_per_controlled_construct',
    NEXT_CONSTRUCT_1_LESS_BUY: 'next_construct_1_less_buy',
    CAN_BANISH_1_HAND_OR_DISCARD_AND_CENTER: 'can_banish_1_hand_or_discard_and_center',
    OPPONENTS_KEEP_1_CONSTRUCT: 'opponents_keep_1_construct',
    CAN_BANISH_1_CENTER: 'can_banish_1_center',
    CANNOT_BE_BANISHED_ACQUIRE_ANY_CENTER_CARD: 'cannot_be_banished_acquire_any_center_card',
    OPPONENTS_DESTROY_1_CONSTRUCT: 'opponents_destroy_1_construct',
    ADD_RANDOM_CARD_TO_HAND_FROM_EACH_OPPONENT: 'add_random_card_to_hand_from_each_opponent',
    PER_TURN_DRAW_1: 'per_turn_draw_1',
    PER_TURN_PLUS_1_KILL_CAN_SPEND_4_TO_BUY_3_POINTS: 'per_turn_plus_1_kill_can_spend_4_to_buy_3_points',
    PER_TURN_PLUS_1_BUY_FIRST_LIFEBOUND_HERO_PLUS_1_POINT: 'per_turn_plus_1_buy_first_lifebound_hero_plus_1_point',
    PER_TURN_WHEN_PLAY_MECHANA_CONSTRUCT_DRAW_1_INCLUDING_THIS_ONE: 'per_turn_when_play_mechana_construct_draw_1_including_this_one',
    PER_TURN_PLUS_1_BUY_FOR_MECHANA_CONSTRUCT_ONLY: 'per_turn_plus_1_buy_for_mechana_construct_only',
    PER_TURN_WHEN_ACQUIRE_MECHANA_CONSTRUCT_PUT_IN_PLAY: 'per_turn_when_acquire_mechana_construct_put_in_play',
    PER_TURN_PLUS_2_BUY_FOR_MECHANA_CONSTRUCT_ONLY: 'per_turn_plus_2_buy_for_mechana_construct_only',
    PER_TURN_PLUS_1_KILL_PER_CONTROLLED_MECHANA_CONTRUCT: 'per_turn_plus_1_kill_per_controlled_mechana_contruct',
    ALL_CONTRUCTS_ARE_MECHANA: 'all_contructs_are_mechana',
    PER_TURN_PLUS_1_KILL_FIRST_MONSTER_DEFEAT_PLUS_1_POINT: 'per_turn_plus_1_kill_first_monster_defeat_plus_1_point',
    CAN_BANISH_1_HAND_OR_DISCARD: 'can_banish_1_hand_or_discard',
    PER_TURN_PLUS_3_KILL: 'per_turn_plus_3_kill',
    PER_TURN_PLUS_1_KILL: 'per_turn_plus_1_kill',
    ACQUIRE_OR_DEFEAT_ANY: 'acquire_or_defeat_any',
}

# players must explicitly use these card for their effect to take place
PERSISTENT_USE_LIST = [
    PER_TURN_PLUS_1_KILL_CAN_SPEND_4_TO_BUY_3_POINTS,
    PER_TURN_DRAW_1,
    BANISH_THIS_EXTRA_TURN,
]
