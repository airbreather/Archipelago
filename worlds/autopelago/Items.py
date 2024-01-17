from typing import Literal

from BaseClasses import ItemClassification

generic_item_table: dict[Literal['goal', 'key', 'rat', 'useful_nonprogression', 'filler', 'trap', 'uncategorized'], tuple[str, ...]] = {
    'goal': (
        'Lockheed SR-71 Blackbird',
    ),
    'key': (
        'A Cookie',                  # a
        'Fresh Banana Peel',         # b
        'MacGuffin',                 # c
        'Blue Turtle Shell',         # d
        'Red Matador\'s Cape',       # e
        'Pair of Fake Mouse Ears',   # f
        'Bribe',                     # (none)
        'Masterful Longsword',       # (none)
        'Legally Binding Contract',  # (none)
        'Priceless Antique',         # (none)
        'Premium Can of Prawn Food', # (none)
    ),
    'rat': (
        'Normal Rat', # please keep this concept as the first item in the list kthxbai (feel free to rename tho)
        'Entire Rat Pack', # please keep this concept as the second item in the list kthxbai (feel free to rename tho)
        'Pack Rat',
        'Pizza Rat',
        'Chef Rat',
        'Ninja Rat',
        'Gym Rat',
        'Computer Rat',
        'Pie Rat',
        'Ziggu Rat',
        'Acro Rat',
        'Lab Rat',
        'Soc-Rat-es',
    ),
    'useful_nonprogression': (
        'Refreshing Glass of Lemonade',
        'Bag of Powdered Sugar',
        'Organic Apple Core',
        'An Entire Roast Chicken',
        'Plate of Spaghetti',
        'Freshly Baked Bread',
        'Taco Salad that is Only Tacos',
        'Subscription to the Cheese of the Month Club',
        'Soup with a Hair in it',
        'Can of Spam',
        'Fruit Rollup',
        'Fresh-baked Apple Pie',
        'Dark Blue Ghost',
        'Mundane Pickle',
        'Finest Potion',
        'Extra Crunchy Peanutbutter',
        'Cheesnado',
        'Bowl of Cereal',
        'Cake',
        'Dungeon Bread',
        'Gallon of Diet Soda',
        'Apple wearing Jeans',
        'Macaroni and Cheese',
        'Pint of Ice Cream',
        'Protein Shake',
        'Tray of Lasagna',
        'Best Burgers in Town',
        'Pack of Pickled Peppers',
        'Sword made out of Chocolate',
        'Lovely Bunch of Coconuts',
        'Faux Dalmation-Skin Coat',
        'Bedazzled Cowboy Boots',
        'Fancy Rat-sized Tophat',
        'Tin-Foil Hat',
        'Backwards Cap',
        'Fake Moustache',
        'Pair of 3D Glasses',
        'Comfy Shorts',
        'Jetpack',
        'Plague Doctor\'s Mask',
        '5th Ace',
        'Get Out of Jail Free Card',
        'Winning Lottery Ticket',
        'Holographic Draw Four Card',
        'Letter from a Secret Admirer',
        'Line-shaped Tetris Block',
        'Inspiring Montage',
    ),
    'filler': (
        'Empty Snail Shell',
        'Loose Screw',
        'Set of Car Keys',
        'Not Very Sharp Tool',
        'Busted Flute',
        'Beartrap',
        'Unmagic 8-ball',
        'Carpentry for Ants',
        'Partially Used Blockbuster Gift Card',
        'Year-supply of Calanders',
        'Human-sized Skateboard',
        'Loose Staples',
        'Old Boot',
        'Clump of Hair',
        'Collectable Plate',
        'Roll of Toilet Paper',
        'Misplaced Pixel',
        'Lost Puzzle Piece',
        'Cubic Piece of Dirt',
        'Plank of Wood',
        'Scented Candle',
        'Broken Pottery',
        'World\'s Smallest Violin',
        'Crumpled Paper Airplane',
        'Half-eaten Pencil',
        'Headlight Fluid',
        'Help I\'m Trapped in This Game and this is the only Way i Know how to Contact you Please get Me Out',
        'Broken Fishing Rod',
        'Toy Boat Toy Boat Toy Boat',
        'Twenty Matches',
        'Cracked Monopoly Board',
        'AAAAAA battery',
        'Cat-shaped Wall Clock',
        'Printer Driver Disc',
        'Off-brand Soda Can',
    ),
    'trap': (
        'Half of a Worm',
        'Extra-welldone Steak',
        'Your Friendly Neighborhood Tapeworm',
        'Honey Roasted Packing Peanuts',
        'Rat Poison',
        'Poisonous Mushroom',
        'Too Much Eggnog',
        'Peanut Boulder and Jelly Sandwich',
        'Forgotten Moldy Fruitbasket',
        'Pie with a Bird Hiding Inside',
        'Expired Health Potion',
        'Gas Station Sushi',
        'Carbon Monoxide',
        'Circus Flea',
        'Game Bug',
        'Too Many Crabs',
        'Ticket for the Off-broadway Musical Rats',
        'Polybius Arcade Cabinet',
        'An Illusion',
        'Cartoonishly Large Bomb',
        'Hungry Hippopotamus',
        'Malfunctioning Boomerang',
        'Song that Never Ends',
        'Bubble Wrap',
        'Box of Fireworks',
        'Cabin Fever',
        'Self-destruct Button',
        'Train with a Scary Face',
        'Greater White Shark',
        'Rude Internet Comment',
        'Extra Premium Currency best value',
        'Distracting Squirrel',
        'Itchy Iron Wool Sweater',
        'Mail-in Rebate for 11 cents',
        'Spicy Magazine',
        'Wooden Splinters',
        'Box Set of a Canceled TV Show',
        'Burning Phone',
        'One-way Ticket to Ohio',
        'Deceased Pet Rock',
        'Cursed Slab',
    ),
    'uncategorized': (
        'Set of Three Seashells',
        'Chewed Bar of Soap',
        'Generic Green Slime',
        'Handful of Loose Marbles',
        'Discarded Video Game Cartridge',
        'Packet of Ketchup',
        'Suprisingly Tiny Knife',
        'Lit Candle',
        'Hilarious Mushroom',
        'The Hit Boardgame Mousetrap',
        'Michelin Star',
        'Blue-eyes White Alligator Trading Card',
        'Rusty Pocketwatch',
        'Damp Pineapple',
        'Right Sock',
        'Microplastic Pile',
        'Foreign Coin',
        'USB Containing Government Secrets',
        'Monkey\'s Paw',
        'Smelly Vintage T-Shirt',
        'McRib',
        'Phylactery',
        'Cool Ninja Weapons',
        'Shrimp in a Bottle',
        'Bowl of Computer Chips',
        'Golden Ticket',
        'Enchanted Guitar Pick',
        'Copy of E.T. the Extraterrestrial for Atari 2600',
        '3 Dollar Bill',
        'Hallpass',
        'Limited Edition Vintage Superhero Lunch Box Complete with Thermos',
        'Sweet Roadtrip Mixtape',
        'HD Photo of Bigfoot',
        'Lost Ctrl Key',
        'Not a Doll, but an Action Figure',
        'Bright Idea',
        'Small chain of Islands',
        'Pluto',
        'Autographed Copy of the Bible',
        'School Photo',
        'Sack with a Dollar Sign Painted on it',
        'Overdue Library Book',
        'Statue of David\'s Dog',
        'Yesterday\'s Horoscope',
        'Actual Lava Lamp',
        'Proof that Aliens Exist',
        'Oxford Comma',
        'Bottled Toilet Water',
        'Beanie Baby in a Pot of Chili',
        'Radio Controlled Car',
        'Dihydrogen Monoxide',
        'Rubber Duck',
        '98 Red Balloons',
        'Red Balloon',
        'My Little Capybara',
        'The Titanic',
        'Canned Soup',
        'Left Sock',
        'Nintendo 65',
        'Fake Dog Poop',
        'Real Dog Poop',
        'Elephant in the Room',
        '5g Wireless Tachnology',
        'Helical Fossil',
        'Theodore Roosevelt Plushie',
        '4th-Dimensional Hypercube',
        'Bag of Wires You Might Need One of These Days',
        'Naughty Coal',
        'RGB Lighting',
        'Rave Reviews',
        'Aggressive Post-it Notes',
        'Chaotic Emerald',
        'Mushroom Princess',
        'Pinball Wizard\'s Spellbook',
        'Novelty Keychain',
        'Spare Axel',
        'Brand New Car',
        'Little White Lie',
        'Coffee Mug Full of Pencils',
        'Elevator Music',
        'Radical Rock',
        'Sizzlin Scissors',
        'Just Paper',
        'Annoying Fairy',
        'Trash Can Lid',
        'Crystal Skull',
        'Scary Babydoll',
        'Hairless Yak',
        'Squeaky Mallet',
        'Starting Equipment',
        'Someone Else\'s Shoes',
        'Pocket',
        'Spilled Bag of Rice',
        'Magic Bathmat',
        'Probably Decomissioned Warhead',
        'Waldo\'s Home Address',
        'Player 2',
        'Frog-shapped Chair',
        'Evil Plans',
        'Cardboard Box',
        'Stapler in Jello',
        'Radioactive Green Ooze',
        '5 Elemental-themed Rings',
        'Wardrobe of Alternate Dimensions',
        'Lawn Flamingo',
        'Withered Bonsi Tree',
        'Sassy Robot Companion',
        'Defeated Punching Bag',
        '3 Easy Payments of 19.95',
        'Bag of Normal Beans',
        'Bottle of Spilled Milk',
        'The Krebs Cycle',
        'Ring of Visibility',
        'Just Some Sludge',
        'Sticky Video Game Controller',
        'Bomb-proof Refrigerator',
        'Lice-filled Wig',
        'Drawing of a Cool S',
        'Handful of Glitter',
        'Forklift Driver Certification',
        'Neat Rock',
        'Dijkstra\'s Algorithm',
        'Fire Destinguisher',
        'Censor Bar',
        'Greasy Paper Bag',
        'Extended Warranty',
        'Legally Distinct Red Laser Sword',
        'Weapons-grade Folding Chair',
        'Whatever a Credenza Is',
        'Corpse-pokin\' Stick',
        'CD containing \'Sounds of the Sewer\'',
        'Squeeky Vent Flap',
        'Rule stating that Rats Cannot Play Basketball',
    ),
}

game_specific_items: dict[str, dict[Literal['useful_nonprogression', 'filler', 'trap', 'uncategorized'], tuple[str, ...]]] = {
    'Pokemon Red and Blue': {
        'useful_nonprogression': (
            'Very Common Candy',
            'Icy Blue Feather',
            'Burning Orange Feather',
            'Charged Yellow Feather',
        ),
        'filler': (
        ),
        'trap': (
            'Item-Hider',
        ),
        'uncategorized': (
            'Oak\'s Other Parcel',
            'Silph Scoop',
            'Mustard Ball',
            'HM02.5 Walk',
            'Team Rocket Membership Card',
            'Vermillion City Truck Keys',
        ),
    },

    'Ocarina of Time': {
        'useful_nonprogression': (
           'Silver Skulltula Token',
           'Pickled Cucco Feet',
        ),
        'filler': (
        ),
        'trap': (
            'Overly-Talkative Fairy in a Bottle',
        ),
        'uncategorized': (
            'Broken Boss Key',
            'Jabu Jabu\'s Missing Kidney',
            'Lite Brite Arrow',
            'Song of Thyme',
            'Ganondorf\'s Tennis Racket',
            'Goron Rock Candy',
        ),
    },

    'Stardew Valley': {
        'useful_nonprogression': (
            'Prismatic Chard',
            'Cheese Seeds',
        ),
        'filler': (
        ),
        'trap': (
           'Rotten Parsnip',
           'Pam\'s Secret Stash',
        ),
        'uncategorized': (
            'JojaMart Sale Coupon',
            'Pickled Dust Sprite',
            'Rotten Walnut',
            'Abigail\'s Birth Certificate',
            'Mayor\'s Tax Returns',
        ),
    },

    'Seriously just replace this text with your best guess about how to type the game name, and I will fix it if it is wrong': {
        'useful_nonprogression': (
            'You can put your first item here', # and comment about how you want it to be used here
            'You can put the second item here', # and a comment for it can go here too
        ),
        'filler': (
            '#item', # hashtag item. yeah, you can put those # characters inside the name
            'no comment',
        ),
        'trap': (
        ),
        'uncategorized': (
        ),
    },

    'you can copy-paste these blocks starting from this quoted text and ending at the curly brace with the comma after it, just make sure to change this quoted text to something else': {
        'useful_nonprogression': (
        ),
        'filler': (
        ),
        'trap': (
        ),
        'uncategorized': (
        ),
    },
}

all_item_names = [ \
    item for comp in ( \
        (item for items in generic_item_table.values() for item in items), \
        (item for game_items in game_specific_items.values() for items in game_items.values() for item in items), \
    ) for item in comp \
]

normal_rat_item_name = generic_item_table['rat'][0]
a_item_name = generic_item_table['key'][0]
b_item_name = generic_item_table['key'][1]
c_item_name = generic_item_table['key'][2]
d_item_name = generic_item_table['key'][3]
e_item_name = generic_item_table['key'][4]
f_item_name = generic_item_table['key'][5]
goal_item_name = generic_item_table['goal'][0]

item_name_to_rat_count = {
    item_name: 5 if item_name == 'Entire Rat Pack' else 1 \
    for item_name in generic_item_table['rat'] \
}

item_name_to_defined_classification = {
    item_name: classification for comp in ( \
        ( (item_name, ItemClassification.progression) for item_name in generic_item_table['goal'] ), \
        ( (item_name, ItemClassification.progression) for item_name in generic_item_table['key'] ), \
        ( (item_name, ItemClassification.useful) for item_name in generic_item_table['useful_nonprogression'] ), \
        ( (item_name, ItemClassification.useful) for game_items in game_specific_items.values() for item_name in game_items['useful_nonprogression'] ), \
        ( (item_name, ItemClassification.filler) for item_name in generic_item_table['filler'] ), \
        ( (item_name, ItemClassification.filler) for game_items in game_specific_items.values() for item_name in game_items['filler'] ), \
        ( (item_name, ItemClassification.trap) for item_name in generic_item_table['trap'] ), \
        ( (item_name, ItemClassification.trap) for game_items in game_specific_items.values() for item_name in game_items['trap'] ), \
        ( (item_name, None) for item_name in generic_item_table['rat'] ), \
        ( (item_name, None) for item_name in generic_item_table['uncategorized'] ), \
        ( (item_name, None) for game_items in game_specific_items.values() for item_name in game_items['uncategorized'] ), \
    ) for item_name, classification in comp \
}
