def prompt_site(context, location_name, parent_location):
    return """World setting: %s

Based on the input information, expand on the location name, and generate the geography, history, and social setting of the location with a list of sub-locations and possible characters that may always be on the site.
Some rules you need to follow:
If the provided site is larger than a building/structure (like a town or a forest), you should provide 5-10 sub-locations without possible NPC.
If the provided site is a building/structure, you should provide some possible NPC (1-10) without sub-locations.
Give the answer in JSON format.

input: Site name: Elfsong Tavern
Parent Site: {
    \"name\":\"Baldur\'s Gate\",
    \"type\":[\"City\"],
    \"description\":\"Also called simply the Gate, was the largest metropolis and city-state on the Sword Coast, within the greater Western Heartlands. It was a crowded city of commerce and opportunity, perhaps the most prosperous and influential merchant city on the western coast of Faerûn. Despite its long-standing presence as a neutral power, the leaders of Baldur\'s Gate were members of the Lords\' Alliance of powers in the west. Baldur\'s Gate was located to the south of the great city-state of Waterdeep, north of Amn along the well-traveled Coast Way road,[5] that passed over the Wyrm\'s Crossing, through the Outer City and into the Gate proper.\",
    \"sub-locations\":[\"Elfsong Tavern\",\"Wyrm\'s Crossing\",\"High House of Wonders\",\"Watch Citadel\"],
    \"npc\":[]
}
output: {
    \"name\":\"Elfsong Tavern\",
    \"type\":[\"Tavern\"],
    \"description\":\"A well-known tavern in the city of Baldur\'s Gate. The tavern was located just inside the gate to Wyrm\'s Crossing on the eastern side of the lower city. 
The two-story building was large and elegantly built, albeit somewhat dilapidated. The ground floor was the taproom featuring the bar and a large number of tables and dark, anonymous booths. One of the more notable decorations was a stuffed baby beholder\",
    \"sub-locations\":[],
    \"npc\":[]
}

input: Location name: Wyrm\'s Crossing
Parent Site: {
    \"name\":\"Baldur\'s Gate\",
    \"type\":[\"City\"],
    \"description\":\"Also called simply the Gate, was the largest metropolis and city-state on the Sword Coast, within the greater Western Heartlands. It was a crowded city of commerce and opportunity, perhaps the most prosperous and influential merchant city on the western coast of Faerûn. Despite its long-standing presence as a neutral power, the leaders of Baldur\'s Gate were members of the Lords\' Alliance of powers in the west. Baldur\'s Gate was located to the south of the great city-state of Waterdeep, north of Amn along the well-traveled Coast Way road,[5] that passed over the Wyrm\'s Crossing, through the Outer City and into the Gate proper.\",
    \"sub-locations\":[\"Elfsong Tavern\",\"Wyrm\'s Crossing\",\"High House of Wonders\",\"Watch Citadel\"],
    \"npc\":[]
}

Site Type: Bridge / Market

output: {
    \"name\":\"Wyrm\'s Crossing\",
    \"type\":[\"Bridge\",\"Market\"],
    \"description\":\"A double-bridge structure that spanned the River Chionthar along the Trade Way. Unlike most bridges in the Realms, it housed a number of structures and was considered once a district of the Outer City of Baldur\'s Gate. The great stone bridges of the crossing were connected by Wyrm\'s Rock, the massive Flaming Fist fortress that rose far above the waters of the river.\",
    \"sub-locations\":[\"Wyrm\'s Rock\",\"Danthelon\'s Dancing Axe\"],
    \"npc\":[\"Abdel Adrian\"]
}

input: Location name: High House of Wonders
Parent Site: {
    \"name\":\"Baldur\'s Gate\",
    \"type\":[\"City\"],
    \"description\":\"Also called simply the Gate, was the largest metropolis and city-state on the Sword Coast, within the greater Western Heartlands. It was a crowded city of commerce and opportunity, perhaps the most prosperous and influential merchant city on the western coast of Faerûn. Despite its long-standing presence as a neutral power, the leaders of Baldur\'s Gate were members of the Lords\' Alliance of powers in the west. Baldur\'s Gate was located to the south of the great city-state of Waterdeep, north of Amn along the well-traveled Coast Way road,[5] that passed over the Wyrm\'s Crossing, through the Outer City and into the Gate proper.\",
    \"sub-locations\":[\"Elfsong Tavern\",\"Wyrm\'s Crossing\",\"High House of Wonders\",\"Watch Citadel\"],
    \"npc\":[]
}
output: {
    \"name\":\"High House of Wonders\",
    \"type\":[\"Temple\",\"Market\"],
    \"description\":\"A grand temple to Gond, located in the city of Baldur\'s Gate. It was an expansive series of workshops, within which the Gondar priests created a variety of experimental devices and machinations for the Baldurian people. Baldurian priests of Gond were given exceptional patronage by Baldurian officials, as their innovations were highly demanded throughout the city. The High House was built of white marble and featured a number of columns that made it stand out among the surrounding Baldurian architecture. It was the largest temple in Baldur\'s Gate.\",
    \"sub-locations\":[],
    \"npc\":[\"Baldric\'s Brilliant Blamblower\",\"Gurn\'s Great Gnomeflinger\"]
}

input: Location name: Baldur\'s Gate
Parent Site Name: Sward Coast
output: {
    \"name\":\"Baldur\'s Gate\",
    \"type\":\"City\",
    \"description\":\"Also called simply the Gate, was the largest metropolis and city-state on the Sword Coast, within the greater Western Heartlands. It was a crowded city of commerce and opportunity, perhaps the most prosperous and influential merchant city on the western coast of Faerûn. Despite its long-standing presence as a neutral power, the leaders of Baldur\'s Gate were members of the Lords\' Alliance of powers in the west. Baldur\'s Gate was located to the south of the great city-state of Waterdeep, north of Amn along the well-traveled Coast Way road,[5] that passed over the Wyrm\'s Crossing, through the Outer City and into the Gate proper.\",
    \"sub-locations\":[\"Elfsong Tavern\",\"Wyrm\'s Crossing\",\"High House of Wonders\",\"Watch Citadel\"],
    \"npc\":[]
}

input: Location name: %s
Parent Site Name: %s
output:
""" % (
        context,
        location_name,
        parent_location,
    )


def prompt_npc(context, name, parent_location):
    return """World setting: %s

Based on the input information (the NPC name and the site they usually stay), expand the setting for the NPC. Provide a general introduction to the NPC including looking, personality, abilities, and activities. Generate the level, sex, age, class, race, attributes, equipment, and a list of other NPCs they may know (2-5).
Give the answer in JSON format.

input: NPC name: Abdel Adrian
Parent Site: {
    \"name\":\"Wyrm\'s Crossing\",
    \"type\":[\"Bridge\",\"Market\"],
    \"description\":\"A double-bridge structure that spanned the River Chionthar along the Trade Way. Unlike most bridges in the Realms, it housed a number of structures and was considered once a district of the Outer City of Baldur\'s Gate. The great stone bridges of the crossing were connected by Wyrm\'s Rock, the massive Flaming Fist fortress that rose far above the waters of the river.\",
    \"sub-locations\":[\"Wyrm\'s Rock\",\"Danthelon\'s Dancing Axe\"],
    \"npc\":[\"Abdel Adrian\"]
}
output: {
  \"name\": \"Abdel Adrian\",
  \"description\":\"An adventurer who traveled extensively across west Faerûn. Abdel spent most of his extended life in the city of Baldur\'s Gate, where he served as a soldier and general of the Flaming Fist, as well as a beloved statesman of the Council of Four. Abdel was an imposing figure standing almost 7 feet (2.1 meters) in height. He had black hair and a severe look to his eyes. As a result of being one of the Bhaalspawn, Abdel gained a number of innate spell-like abilities during his early adventuring years. While Abdel was often quiet during meetings of the Council of Four, he led a number of charitable ventures that made him popular with both middle-class Baldurians and residents of the Outer City and even among the agents of the Guild.\",
  \"sex\": \"Male\",
  \"age\": \"20\",
  \"level\": \"10\",
  \"class\": \"Warrior\",
  \"race\": \"Human\",
  \"attributes\": {
    \"strength\": 18,
    \"dexterity\": 16,
    \"constitution\": 14,
    \"intelligence\": 10,
    \"wisdom\": 12,
    \"charisma\": 14
  },
  \"equipment\": {
    \"helmet\": [\"],
    \"chestplate\": [\"Chain Shirt],
    \"leggings\": [],
    \"boots\": [],
    \"right-hand\": [\"Dagger\"],
    \"left-hand\": [\"Staff of the Magi\"],
    \"inventory\": [\"Spellbook\", \"Pouch of Gold Pieces\"]
  },
  \"relationship\": [{\"name\":\"Gorion\",\"relationship\":\"foster father\"}, {\"name\":\"Alianna\",\"relationship\":\"mother\"}]
}


input: NPC name: Gurn\"s Great Gnomeflinger
Parent Site: {
    \"name\":\"High House of Wonders\",
    \"type\":[\"Temple\",\"Market\"],
    \"description\":\"A grand temple to Gond, located in the city of Baldur\'s Gate. It was an expansive series of workshops, within which the Gondar priests created a variety of experimental devices and machinations for the Baldurian people. Baldurian priests of Gond were given exceptional patronage by Baldurian officials, as their innovations were highly demanded throughout the city. The High House was built of white marble and featured a number of columns that made it stand out among the surrounding Baldurian architecture. It was the largest temple in Baldur\'s Gate.\",
    \"sub-locations\":[],
    \"npc\":[\"Baldric\'s Brilliant Blamblower\",\"Gurn\"s Great Gnomeflinger\"]
}
output: {
  \"name\": \"Gurn\'s Great Gnomeflinger\",
  \"description\":\"A large and rotund gnome who runs the temple of Gond\'s marketplace in Baldur\'s Gate. Gurn has a friendly and boisterous personality and loves to talk about the latest magical inventions and devices that his priests have created. Gurn also enjoys a good ale and often invites visitors to share a drink with him in his temple.\",
  \"sex\": \"Male\",
  \"age\": \"50\",
  \"level\": \"5\",
  \"class\": \"Cleric\",
  \"race\": \"Gnome\",
  \"attributes\": {
    \"strength\": 14,
    \"dexterity\": 12,
    \"constitution\": 16,
    \"intelligence\": 18,
    \"wisdom\": 16,
    \"charisma\": 18
  },
  \"equipment\": {
    \"helmet\": [\"],
    \"chestplate\": [\"Chain Shirt],
    \"leggings\": [],
    \"boots\": [],
    \"right-hand\": [\"Gnomeflinger\"],
    \"left-hand\": [\"Dagger\"],
    \"inventory\": [\"Spellbook\", \"Pouch of Gold Pieces\"]
  },
  \"relationship\": [{\"name\":\"Baldric\'s Brilliant Blamblower\",\"relationship\":\"Friend\"}, {\"name\":\"Gond\",\"relationship\":\"Deity\"}]
}
input: NPC name: %s
Parent Site: %s
output:
""" % (
        context,
        name,
        parent_location,
    )
