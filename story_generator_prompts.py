import vertexai
from vertexai.preview.language_models import (
    ChatModel,
    InputOutputTextPair,
    TextGenerationModel,
)


def prompt_structure(context, location_name, parent_location):
    return """World setting: %s

You are a dungeon master for a D&D or COC-styled game.
Based on the input information, generate a setting for a structure (a building or a landmark).
Consider the following and combine them into a detailed description with at least 200 words:
Geography,
Related structures,
History,
Social background,
Give the answer in JSON format.
Also, generate a list of possible specific characters (at least 2) that may always be on the site.
Give a name for the characters.

input: Structure name: Elfsong Tavern
Parent Region: {
    \"name\":\"Baldur\'s Gate\",
    \"type\":[\"City\"],
    \"description\":\"Also called simply the Gate, was the largest metropolis and city-state on the Sword Coast, within the greater Western Heartlands. It was a crowded city of commerce and opportunity, perhaps the most prosperous and influential merchant city on the western coast of Faerûn. Despite its long-standing presence as a neutral power, the leaders of Baldur\'s Gate were members of the Lords\' Alliance of powers in the west. Baldur\'s Gate was located to the south of the great city-state of Waterdeep, north of Amn along the well-traveled Coast Way road,[5] that passed over the Wyrm\'s Crossing, through the Outer City and into the Gate proper.\",
    \"sub-regions\":[\"Wyrm\'s Crossing\"],
    \"structures\":[\"Elfsong Tavern\",\"High House of Wonders\",\"Watch Citadel\"],
    \"inhabitants\":[\"Human\", \"Half-elves\",\"Dwarves\"]
}
output: {
    \"name\":\"Elfsong Tavern\",
    \"type\":[\"Tavern\"],
    \"description\":\"A well-known tavern in the city of Baldur\'s Gate. The tavern was located just inside the gate to Wyrm\'s Crossing on the eastern side of the lower city. 
The two-story building was large and elegantly built, albeit somewhat dilapidated. The ground floor was the taproom featuring the bar and a large number of tables and dark, anonymous booths. One of the more notable decorations was a stuffed baby beholder.\",
    \"npc\":[]
}

input: Structure name: High House of Wonders
Parent Region: {
    \"name\":\"Baldur\'s Gate\",
    \"type\":[\"City\"],
    \"description\":\"Also called simply the Gate, was the largest metropolis and city-state on the Sword Coast, within the greater Western Heartlands. It was a crowded city of commerce and opportunity, perhaps the most prosperous and influential merchant city on the western coast of Faerûn. Despite its long-standing presence as a neutral power, the leaders of Baldur\'s Gate were members of the Lords\' Alliance of powers in the west. Baldur\'s Gate was located to the south of the great city-state of Waterdeep, north of Amn along the well-traveled Coast Way road,[5] that passed over the Wyrm\'s Crossing, through the Outer City and into the Gate proper.\",
    \"sub-regions\":[\"Wyrm\'s Crossing\"],
    \"structures\":[\"Elfsong Tavern\",\"High House of Wonders\",\"Watch Citadel\"],
    \"inhabitants\":[\"Human\", \"Half-elves\",\"Dwarves\"]
}
output: {
    \"name\":\"High House of Wonders\",
    \"type\":[\"Temple\",\"Market\"],
    \"description\":\"A grand temple to Gond, located in the city of Baldur\'s Gate. It was an expansive series of workshops, within which the Gondar priests created a variety of experimental devices and machinations for the Baldurian people. Baldurian priests of Gond were given exceptional patronage by Baldurian officials, as their innovations were highly demanded throughout the city. The High House was built of white marble and featured a number of columns that made it stand out among the surrounding Baldurian architecture. It was the largest temple in Baldur\'s Gate.\",
    \"npc\":[\"Baldric\'s Brilliant Blamblower\",\"Gurn\'s Great Gnomeflinger\"]
}

input: Structure name: Wyrm\'s Rock
Parent Region:{
    \"name\":\"Wyrm\'s Crossing\",
    \"type\":[\"Bridge\",\"Market\"],
    \"description\":\"A double-bridge structure that spanned the River Chionthar along the Trade Way. Unlike most bridges in the Realms, it housed a number of structures and was considered once a district of the Outer City of Baldur\'s Gate. The great stone bridges of the crossing were connected by Wyrm\'s Rock, the massive Flaming Fist fortress that rose far above the waters of the river.\",
    \"sub-regions\":[],
    \"structure\":[\"Wyrm\'s Rock\",\"Danthelon\'s Dancing Axe\"],
}
output: {
    \"name\":\"Wyrm\'s Rock\",
    \"type\":[\"Fortress\"],
    \"description\":\"A massive fortress of the Flaming Fist that was located on the western end of Wyrm\'s Crossing. It was the headquarters of the Flaming Fist in the city of Baldur\'s Gate and was one of the most important strategic locations in the city. The fortress was built of white marble and featured a number of towers that were used to guard the crossing.\",
    \"npc\":[\"Flaming Fist Guard\",\"Flaming Fist Captain\",\"Abdel Adrian\"]
}

input: Structure name: %s
Parent Site: %s

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


def prompt_background(context, players, map):
    return """You are a narrator of a role-playing game.

According to the input world setting, world map, and adventurers, answer each question:
- how are the adventurer before the adventure?
- why do the adventurers come together?
- what problems are they facing?

input: Adventurers: Kevin, Ricky
World Setting:{
 \"name\":\"The Great Desert of Axan\"
 \"geography\": \"The Great Desert of Axan is a vast and unforgiving desert that covers much of the eastern continent of Aetheria. The desert is home to a wide variety of creatures, including nomads, bandits, and monsters. The desert is also home to a number of ancient ruins, which are said to contain great treasures.\",
 \"economic and technology\": \"The Great Desert of Axan is a major trade route between the eastern and western continents of Aetheria. Merchants from all over the world travel through the desert, bringing with them goods from all corners of the world. The desert is also home to a number of caravans, which travel through the desert carrying goods and people.\",
 \"society\":\"The people of the Great Desert of Axan are a diverse group. There are the nomadic tribes, who live in tents and travel the desert in search of water and food. There are also the bandits, who prey on the caravans that travel through the desert. And there are the merchants, who trade goods from all over the world.\",
 \"inhabitants\":\"The people of the Great Desert of Axan are a hardy people. They are accustomed to the harsh conditions of the desert and they are skilled in survival. They are also a resourceful people, and they have learned to use the resources of the desert to their advantage.\",a
 \"ability-system\":\"The people of the Great Desert of Axan have a variety of abilities that help them survive in the desert. They are able to withstand the heat and the harsh conditions of the desert. They are also able to find water and food in the most inhospitable places.\",
 \"history\":\"The history of the Great Desert of Axan is long and complex. The desert has been a crossroads for trade and travel for centuries. It has also been the site of many battles and wars. The desert is a dangerous place, but it is also a place of opportunity.\"}

World Map {
  \"name\":\"The Great Desert of Axan\",
  \"type\":[\"Desert\"],
  \"size\":\"large\",
  \"description\":\"The Great Desert of Axan is a vast and unforgiving desert that covers much of the eastern continent of Aetheria. The desert is home to a wide variety of creatures, including nomads, bandits, and monsters. The desert is also home to a number of ancient ruins, which are said to contain great treasures.\",
  \"sub-regions\":[\"The Oasis of Al-Hazim\",\"The Ruins of Ur-Dum\",\"The Valley of the Serpents\",\"The Mountains of Madness\",\"The Great City of Al-Kharim\"],
  \"structures\":[\"The Oasis of Al-Hazim\",\"The Ruins of Ur-Dum\",\"The Valley of the Serpents\",\"The Mountains of Madness\",\"The Great City of Al-Kharim\"],
  \"inhabitants\":[\"Nomads\",\"Bandits\",\"Monsters\",\"Merchants\",\"Tribes\",\"Explorers\",\"Smugglers\"]
}


output: {
\"position\":\"The Great City of Al-Kharim\",
\"before-adventure\":\"Kevin and Ricky are two adventurers who have come together to explore the Great Desert of Axan.\",
\"why\":\"They are both looking for a challenge, and they believe that the desert holds many secrets that are waiting to be discovered. They have heard rumors of ancient ruins, hidden treasures, and dangerous creatures, and they are eager to find out if these rumors are true.\",
\"problem\":\"However, the desert is a dangerous place. The heat, the sand, and the lack of water can all be deadly. And there are also the creatures that live in the desert. The bandits, the nomads, and the monsters are all a threat to the adventurers.
Kevin and Ricky will have to use all their skills and abilities to survive in the desert. They will have to work together to find food and water, to build shelter, and to defend themselves from their enemies. But if they can survive, they will be rewarded with a journey that they will never forget.\"}


input: Adventurers: John, Kevin
World Setting:{
\"name\":\"Necropolis\"
 \"geography\": \"Necropolis is a vast, ocean-going city of the dead, populated by the undead, both artificial and organic. The city is powered by the energy of a dying star, which is slowly being consumed by the necroplasmic energies of the undead.\",
 \"economic and technology\": \"Necropolis is a city of commerce and industry, where the undead trade in the resources of the ocean and the technology of the past. The city is home to a number of powerful guilds, each of which controls a different aspect of the city\'s economy.\",
 \"society\":\"The society of Necropolis is stratified, with the undead aristocracy at the top and the undead working class at the bottom. The undead are divided into two main castes: the mortuary and the living dead. The mortuary is a caste of undead who have been granted immortality by the death god, Nekrozoth. The living dead are the vast majority of the undead population, and they are subject to the rule of the mortuary.\",
 \"inhabitants\":\"The inhabitants of Necropolis are a diverse mix of undead creatures, including vampires, zombies, ghouls, liches, and skeletons. The city is also home to a number of artificial undead, such as constructs and warforged.\",
 \"ability-system\":\"The undead of Necropolis have a variety of supernatural abilities, including the ability to raise the dead, to control the minds of others, and to drain the life energy of their victims.\",
 \"history\":\"Necropolis was founded by a group of ancient mages who sought to create a city where the dead could live in peace. The city was built on the ruins of a sunken city, and it was powered by the energy of a dying star. The mages who founded Necropolis were eventually overthrown by the undead, and the city became a haven for the undead.\"}
World map: {
  \"name\":\"Necropolis\",
  \"type\":[\"City\",\"Ocean\"],
  \"size\":\"large\",
  \"description\":\"Necropolis is a vast, ocean-going city of the dead, populated by the undead, both artificial and organic. The city is powered by the energy of a dying star, which is slowly being consumed by the necroplasmic energies of the undead. The city is a place of commerce and industry, where the undead trade in the resources of the ocean and the technology of the past. The society of Necropolis is stratified, with the undead aristocracy at the top and the undead working class at the bottom. The undead are divided into two main castes: the mortuary and the living dead. The mortuary is a caste of undead who have been granted immortality by the death god, Nekrozoth. The living dead are the vast majority of the undead population, and they are subject to the rule of the mortuary. The undead of Necropolis have a variety of supernatural abilities, including the ability to raise the dead, to control the minds of others, and to drain the life energy of their victims. The city was founded by a group of ancient mages who sought to create a city where the dead could live in peace. The city was built on the ruins of a sunken city, and it was powered by the energy of a dying star. The mages who founded Necropolis were eventually overthrown by the undead, and the city became a haven for the undead.\",
  \"sub-regions\":[\"The Catacombs\",\"The Docks\",\"The Market Square\",\"The Mortuary\",\"The Temple of Nekrozoth\",\"The Underworld\"],
  \"structures\":[\"The Bone Palace\",\"The Death Ship\",\"The Tower of Skulls\",\"The Vault of Souls\"],
  \"inhabitants\":[\"Vampires\",\"Zombies\",\"Ghouls\",\"Liches\",\"Skeletons\",\"Constructs\",\"Warforged\"]
}

output: {
\"position\":\"The Bone Palace\",
\"before-adventure\":\"John and Kevin are two adventurers who have come together to explore the city of Necropolis.\",
\"why\":\"They are both drawn to the city\'s mystery and danger, and they are eager to experience its many wonders. They know that the city is a dangerous place, but they are also confident in their abilities to survive.\",
\"problem\":\"However, the city is not without its challenges. The undead inhabitants of Necropolis are not to be trifled with, and they will stop at nothing to protect their city. John and Kevin will have to be careful not to attract too much attention, or they will find themselves in grave danger.\"}


input: Adventurers: %s
World Setting: %s
World map: %s

output: 
""" % (
        players,
        context,
        map,
    )


def prompt_region(
    context,
    name="default",
    parent_region="default",
    size="default",
    keywords=[],
    types=[],
):
    return """World setting: %s

You are a dungeon master for a D&D or COC-styled game.
Based on the information provided, generate a setting for a region.
Consider the following and combine them into a detailed description with at least 400 words:
Environment, 
Inhabitants and fractions,
Cultural and Social background,
Map,
History,
Give the answer in JSON format. Remember to add space after the period.
Hits:
inhabitants mean the types of common species in this region.
The type of the region determines its size. For example, a continent would be a large region, a forest/sea/ocean would be a median region, and a city would be a small region.
Then based on the size, generate the sub-regions and structures. 
A large region has no structures and at least 5 sub-regions.
A median region has around 3 sub-regions and 0-3 landmarks (as structures). 
A small region has at least 3 buildings (as structures) and 0-2 sub-regions. 
sub-regions mean the sub-region or cities or biomes within this region. 
structures mean the famous building and landmarks in this region.

input: Keywords: dungeon and dragon, magic, dimension, god. 
Size: Large
output: {
  \"name\":\"Faerûn\",
  \"type\":[\"Continent\"],
  \"size\":\"large\",
  \"description\":\"Faerûn was a major continent on the planet of Toril. Besides the exterior coastline to the west and south, the most dominant feature on the continent was the Sea of Fallen Stars. Next in significance was the Shaar, a broad region of grasslands in the south that, together with the Lake of Steam, separated the area around the inland sea from the coastal nations at the southern edge of the continent. Economically and technologically, Faerûn is comparable to Western Europe during the late Middle Ages. A major difference between the setting and Earth is the presence of magic. The system of magic is subdivided into divine and arcane categories, with the former empowered by a Faerûnian deity, and the latter by rituals or innate abilities which manipulate a mystical field called the Weave, the source of magical energies on Toril. There are a number of organized alliances in Faerûn, with each pursuing their own particular agenda. A few are dedicated to decent and honest causes, such as the Harpers, who protect the good-natured races and seek a balance between civilization and nature.\",
  \"sub-regions\":[\"Sword Coast\",\"High Forest\",\"Silver Marches\",\"Anauroch\",\"Waterdeep\",\"Moonshae Isles\",\"Sea of Fallen Stars\",\"Underdark\"],
  \"structures\":[],
  \"inhabitants\":[\"Human\",\"Elies\",\"Goblins\",\"Dragons\",\"Half-elves\",\"Dwarves\",\"Gnomes\",\"Orcs\",\"Giants\"]
}

input: Name: The Forgotten Isle
Size: large
Keywords: dragon, pirate, forest, island
output: {
  \"name\":\"The Forgotten Isle\",
  \"type\":[\"Continent\",\"Isle\"],
  \"size\":\"large\",
  \"description\":\"The Forgotten Isle is a vast landmass covered in thick forests, rolling hills and mountains. The coastline is jagged and rocky, with many hidden coves and inlets. The climate is temperate, with mild winters and warm summers. The people of the Forgotten Isle are a mix of humans, elves, dwarves, gnomes and halflings. They live in small villages and towns scattered throughout the land. The largest city on the island is Avalon, a bustling port city that is home to a diverse population of people from all over the world. The Forgotten Isle is a place of mystery and adventure. There are many hidden treasures to be found, as well as dangerous creatures such as dragons, trolls and sea monsters. The island is also home to a number of pirates, who sail the seas in search of treasure and adventure.\",
  \"sub-regions\":[\"Avalon\",\"The Forest of Mirkwood\",\"The Misty Mountains\",\"The Isle of Dragons\",\"The Sea of Monsters\"],
  \"structures\":[\"The Siren\'s Tower\",\"The Kraken\'s Lair\"],
  \"inhabitants\":[\"Human\",\"Elves\",\"Dwarves\",\"Gnomes\",\"Halflings\",\"Dragons\",\"Trolls\",\"Sea Monsters\",\"Pirates\"]
}


input: Location name: Baldur\'s Gate
Size: median
Parent Region: Sword Coast
output: {
    \"name\":\"Baldur\'s Gate\",
    \"type\":[\"City\"],
  \"size\":\"small\",
    \"description\":\"Also called simply the Gate, was the largest metropolis and city-state on the Sword Coast, within the greater Western Heartlands. It was a crowded city of commerce and opportunity, perhaps the most prosperous and influential merchant city on the western coast of Faerûn. Despite its long-standing presence as a neutral power, the leaders of Baldur\'s Gate were members of the Lords\' Alliance of powers in the west. Baldur\'s Gate was located to the south of the great city-state of Waterdeep, north of Amn along the well-traveled Coast Way road,[5] that passed over the Wyrm\'s Crossing, through the Outer City and into the Gate proper.\",
    \"sub-regions\":[\"Wyrm\'s Crossing\"],
    \"structures\":[\"Elfsong Tavern\",\"High House of Wonders\",\"Watch Citadel\"],
    \"inhabitants\":[\"Human\", \"Half-elves\",\"Dwarves\"]
}

input: %s
%s
%s
%s
%s
output:
""" % (
        context,
        ("Name: " + name) if name != "default" else "",
        ("Parent Region:" + parent_region) if parent_region != "default" else "",
        ("Size: " + size) if size != "default" else "",
        ("Keywords: " + keywords) if len(keywords) > 0 else "",
        ("Types: " + types) if len(types) > 0 else "",
    )


def prompt_worldsetting(keywords):
    return """Based on the information provided, generate a setting for a large world for a role-playing game.
The world should be large, for example, an ocean, a continent, a planet, or a dimension.
Use upper-level wording and sentence that are beautiful and elegant, similar to a novel.
Consider the following and write at least 400 words:
Geography,
Economic,
Technology,
Society
Inhabitants,
Ability System,
History or lore
Give the answer in JSON format. 
Remember to add space after the period. 
The name should be special.

input: D&D
output: {
\"name\":\"Faerûn\",
 \"geography\": \"The sub-continent of Faerûn is set in the northern hemisphere of the planet Toril, or, more formally, \"Abeir-Toril.\" The continent has a \"landmass of approximately nine and a half million square miles\". Faerûn is the western part of an unnamed supercontinent that is quite similar to real-world Afro-Eurasia. Sub-arctic extremes chill its northern reaches, where ice sheets like the Great Glacier dominate the landscape in blinding white.\",
 \"economic and technology\": \"Faerûn is comparable to Western Europe during the late Middle Ages, giving most new players using this campaign setting an intuitive grasp of the way the society functions. Gunpowder, known here as the magical substance smoke powder and different in its composition from historical gunpowder, is starting to make an appearance, but much of the armament is still dominated by pre-gunpowder weaponry such as swords, spears, and bows.\",
 \"inhabitants\": \"Faerûn is home to a number of non-human creatures of varying degrees of civilization or barbarism. Among these are several different races of dwarves, gnomes, halflings and elves, as well as goblins, orcs, lizardmen, ogres, various giants, and even dragons.\",
 \"ability-system\": \"A major difference between the setting and Earth is the presence of magic. The system of magic is subdivided into divine and arcane categories, with the former empowered by a Faerûnian deity, and the latter by rituals or innate abilities which manipulate a mystical field called the Weave, the source of magical energies on Toril. Faerûn has a pantheon of deities that are worshipped by the followers of this region. These are comparable to mythological deities of the ancient Greek pantheon, and cover a range of ethical beliefs and portfolios of interests.\",
\"society\":\"Most of the population of Faerûn consists of farmers, who are organized somewhat loosely in a semi-feudal system. There are also a number of notable cities, and trade between nations is common, as in the Renaissance era. Likewise, there are regions where more barbaric tribes and customs persist.\",
\"history\":\"\"}


input: steampunk, forest
output: {
\"name\":\"The Great Forest of Elvenholm\",
 \"geography\": \"The Great Forest of Elvenholm is a vast and dense woodland that covers much of the northern continent of Aelwyn. The forest is home to a wide variety of plant and animal life, including many species that are found nowhere else in the world. The trees in the forest are massive and ancient, and their branches are so thick that they form a canopy that blocks out the sun. The forest floor is covered in a thick layer of leaves and moss, and the air is filled with the sound of birdsong and the smell of flowers.\",
 \"economic and technology\": \"The people of Elvenholm live in harmony with the forest. They build their homes in the trees and use the natural resources of the forest to meet their needs. They have developed a sophisticated system of agriculture that allows them to grow crops and raise livestock without harming the environment. They also have a deep understanding of the natural world, and they use this knowledge to create medicines, tools, and other items that they need.\",
 \"society\":\"The people of Elvenholm are a peaceful and spiritual people. They believe that the forest is a sacred place, and they treat it with respect. They live in small, close-knit communities, and they value cooperation and mutual aid. They have a strong sense of community identity, and they are fiercely protective of their home.\",
 \"inhabitants\":\"The people of Elvenholm are a race of elves who are known for their beauty, grace, and wisdom. They are a long-lived people, and they have a deep understanding of the natural world. They are also skilled artisans and craftsmen, and they create beautiful works of art and architecture.\",
 \"ability-system\":\"The people of Elvenholm have a natural connection to the forest, and they can use their magic to manipulate the natural world. They can create illusions, control the weather, and even heal the sick. They also have a strong connection to the spirits of the forest, and they can call upon them for help.\",
 \"history\":\"The history of Elvenholm is long and complex, but it is a story of peace and harmony. The elves have lived in the forest for many centuries, and they have always lived in harmony with nature. They have never been involved in war, and they have always been willing to help others. They are a peaceful and spiritual people, and they are a source of hope for the future.\"}


input: fish, fossil, cyberpunk
output: {
\"name\":\"Necropolis\",
 \"geography\": \"Necropolis is a vast, ocean-going city of the dead, populated by the undead, both artificial and organic. The city is powered by the energy of a dying star, which is slowly being consumed by the necroplasmic energies of the undead.\",
 \"economic and technology\": \"Necropolis is a city of commerce and industry, where the undead trade in the resources of the ocean and the technology of the past. The city is home to a number of powerful guilds, each of which controls a different aspect of the city\'s economy.\",
 \"society\":\"The society of Necropolis is stratified, with the undead aristocracy at the top and the undead working class at the bottom. The undead are divided into two main castes: the mortuary and the living dead. The mortuary is a caste of undead who have been granted immortality by the death god, Nekrozoth. The living dead are the vast majority of the undead population, and they are subject to the rule of the mortuary.\",
 \"inhabitants\":\"The inhabitants of Necropolis are a diverse mix of undead creatures, including vampires, zombies, ghouls, liches, and skeletons. The city is also home to a number of artificial undead, such as constructs and warforged.\",
 \"ability-system\":\"The undead of Necropolis have a variety of supernatural abilities, including the ability to raise the dead, to control the minds of others, and to drain the life energy of their victims.\",
 \"history\":\"Necropolis was founded by a group of ancient mages who sought to create a city where the dead could live in peace. The city was built on the ruins of a sunken city, and it was powered by the energy of a dying star. The mages who founded Necropolis were eventually overthrown by the undead, and the city became a haven for the undead.\"}

input: %s
output:
""" % (
        keywords
    )


def narrator_example():
    return [
        InputOutputTextPair(
            input_text="""
Decision: Start

Information: {
\"position\":\"The Bone Palace\",
\"before-adventure\":\"John and Kevin are two adventurers who have come together to explore the city of Necropolis.\",
\"why\":\"They are both drawn to the city\'s mystery and danger, and they are eager to experience its many wonders. They know that the city is a dangerous place, but they are also confident in their abilities to survive.\",
\"problem\":\"However, the city is not without its challenges. The undead inhabitants of Necropolis are not to be trifled with, and they will stop at nothing to protect their city. John and Kevin will have to be careful not to attract too much attention, or they will find themselves in grave danger.\"}

""",
            output_text="""Encounter : 1

<area>The Bone Palace<area> is a towering structure that looms over the city of <area>Necropolis<area>. It is a place of mystery and danger, and many adventurers have come to explore its depths. John and Kevin are two such adventurers, and they are eager to see what secrets the Bone Palace holds.

The entrance to the Bone Palace is a large, arched doorway. The door is made of black iron, and it is covered in intricate carvings. John and Kevin approach the door cautiously, their weapons drawn. They know that they are entering a dangerous place, but they are determined to find out what lies within.

John takes a deep breath and opens the door. He steps inside, and Kevin follows close behind. The door slams shut behind them, and they are plunged into darkness.

John and Kevin can hear the sound of their own breathing in the silence. They stand there for a moment, waiting for their eyes to adjust to the darkness. As they adjust, they begin to make out their surroundings.

They are in a large, open chamber. The walls are made of smooth, white stone. The floor is covered in a thick layer of dust. There are several large pillars in the chamber, and each pillar is topped with a skull.

John and Kevin look around, their eyes wide with wonder. They have never seen anything like this place before. They know that they are in a special place, and they can\'t wait to explore it further.

Suggestions:

Explore the chamber.
1. Inspect the floor.
2. Stop and rest.
3. Leave the Bone Palace and return to the city.""",
        ),
        InputOutputTextPair(
            input_text="""
Decision: Start

Information: {
Kevin and Ricky are two adventurers who have come together to explore the Great Desert of Axan.
They are both looking for a challenge, and they believe that the desert holds many secrets that are waiting to be discovered. They have heard rumors of ancient ruins, hidden treasures, and dangerous creatures, and they are eager to find out if these rumors are true.
However, the desert is a dangerous place. The heat, the sand, and the lack of water can all be deadly. And there are also the creatures that live in the desert. The bandits, the nomads, and the monsters are all a threat to the adventurers.
Kevin and Ricky will have to use all their skills and abilities to survive in the desert. They will have to work together to find food and water, to build shelter, and to defend themselves from their enemies. But if they can survive, they will be rewarded with a journey that they will never forget.}""",
            output_text="""Encounter : 1

Kevin and Ricky set foot in <area>the Great Desert of Axan<area>. The sun beat down on them relentlessly, and the sand scorched their skin. They had been walking for hours, and their water was running low. They were starting to lose hope.

Suddenly, they saw something in the distance. It was a dark shape, moving against the sand. As they got closer, they could see that it was a group of people. They were dressed in strange clothes, and they were riding on camels.

The two adventurers approached the group cautiously. They did not know if these people were friendly or hostile.

Suggestions:

1. Approach the group cautiously.
2. Attack the group.
3. Run away.""",
        ),
    ]
