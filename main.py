from base import Character, Treasure, Monster, Scene, Weapon
from game_engine import GameEngine
from ascii_data import prologue

# Example ASCII art for scenes
weaponery = """

"""

forest_entrance_image = """
     /\\
    /  \\    You stand at the entrance of a dark forest.
   /    \\
  /______\\
     ||
"""

cave_image = """
      ___
    /     \\    You enter a dark cave. Echoes surround you.
   /_______\\
   |       |
"""

beast_image = """
    (\\__/)
    (o.o )    A fearsome beast stands before you!
    (> <)
"""

the_old_road = """



"""

# Example setup of the game world
scene_3 = Scene("A dark cave where you find treasure.", ascii_image=cave_image, treasures=[Treasure(20)], next_scenes={})
scene_2 = Scene("A forest path that leads to a beast.", ascii_image=beast_image, monsters=[Monster("Forest Beast", 6, 8)], next_scenes={"north": scene_3})
init_scene = Scene("You are at the entrance of Grimmoor Forest.", ascii_image=forest_entrance_image, next_scenes={"north": scene_2, "south": scene_3})

# Start the game
character = Character()
item = Weapon("Small Sword",2)
character.use_weapon(item)

game = GameEngine(init_scene, character, prologue)
game.start()
