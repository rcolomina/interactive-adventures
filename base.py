import random
import uuid

# Abstraction for items
class Item:
    def __init__(self, name: str):
        self.id = uuid.uuid4
        self.name = name

class Potion(Item):
    def __init__(self):
        super().__init__("Potion")

class Treasure(Item):
    def __init__(self, value):
        super().__init__(f"Treasure worth {value} gold pieces")
        self.value = value

class Weapon(Item):
    def __init__(self, name: str, damage: int):
        super().__init__(f"Weapon of class '{name}'")
        self.damage = damage

class Armor(Item):
    def __init__(self, name:str, defense: int, bonus_against_weapons=None):
        super().__init__(f"Armor of class '{name}'")
        self.defense = defense
        self.bonus_against_weapons = None

# Abstraction for monsters
class Monster:
    def __init__(self, name, skill, stamina, damage = 2):
        self.name = name
        self.skill = skill
        self.stamina = stamina
        self.damage = damage
    def roar(self):
        return ""

        
    def display(self):
        return "\n".join([f"===== Monster Stats =====", 
                          f"Class: {self.name}", 
                          f"Stamina: {self.stamina}",   
                          f"Skill: {self.skill}", 
                          f"Damage: {self.damage}", 
                          f"========================="])

# Abstraction for a scene in the game, with an optional ASCII image
class Scene:
    def __init__(self, description, ascii_image=None, monsters=None, treasures=None, next_scenes=None):
        self.description = description
        self.ascii_image = ascii_image
        self.monsters = monsters if monsters else []
        self.treasures = treasures if treasures else []
        self.next_scenes = next_scenes if next_scenes else {}

    def display(self):
        if self.ascii_image:
            print(self.ascii_image)
        print(self.description)
        if self.monsters:
            print("Monsters here: " + ", ".join([m.name for m in self.monsters]))
        if self.treasures:
            print("You found: " + ", ".join([t.name for t in self.treasures]))
        if self.next_scenes:
            directions = ", ".join(self.next_scenes.keys())
            print(f"Possible paths forward: {directions}")


# Abstraction for the player character
class Character:
    def __init__(self):
        self.skill = 6 + random.randint(1, 6)
        self.luck = 6 + random.randint(1, 6)
        self.stamina = 6 + random.randint(2, 12)
        self.initial_stamina = self.stamina
        self.gold = 10  # Starting gold pieces
        self.inventory = []
        self.potions = 3  # Starting potions
        self.provisions = 5  # Starting provisions
        self.bare_hands = 1
        
        self.left_hand = None
        self.right_hand = None
        
        self.armor = None
    
    
    def use_weapon(self, weapon: Weapon, right_hand=False):
        if not right_hand:
            self.left_hand = weapon
        else:
            self.right_hand = weapon
        self.pick_object(weapon)

    def use_armor(self, armor: Armor):
        self.armor = armor
        self.pick_object(armor)
        
    def pick_object(self,item: Item):
        if item.id not in [x.id for x in self.inventory]:        
            self.inventory.append(item)
        
    def drop_object(self, item: Item):
        try:
            self.inventory.remove(item)
        except Exception as err:
            print(f"Error: Item with id {item.id} does not exist on inventory {err}")
        
    def damage(self):
        #weapons = [w for w in self.inventory if isinstance(w,Weapon)]
        if self.left_hand is None and self.right_hand is None:
            print(f"You don't hold any weapon. Using your bare hands to attack (damage = {self.bare_hands}.")
            return self.bare_hands
        else:
            total = self.right_hand.damage if self.right_hand is not None else 0 + \
                self.left_hand.damage if self.left_hand is not None else 0 
            print(f"Your weapon reduces monster stamina points by {total}")
            return total

    def display_stats(self):
        
        display_msg = [
            "\n===== Your Stats =====",
            f"Skill: {self.skill}",
            f"Stamina: {self.stamina}",
            f"Luck: {self.luck}",
            f"Gold: {self.gold}",
            f"Potions: {self.potions}",
            f"Provisions: {self.provisions}",
            f"Inventory: {', '.join([item.name for item in self.inventory]) if self.inventory else 'None'}",
            "======================\n"]
        return "\n".join(display_msg)

    def use_luck(self, action):
        """Luck can modify the outcome of an action (combat or healing)."""
        luck_roll = random.randint(1, 6) + random.randint(1, 6)
        if luck_roll <= self.luck:
            if action == "reduce_damage":
                print("You used luck! Incoming damage reduced by 1.")
                return True
            elif action == "increase_damage":
                print("You used luck! Outgoing damage increased by 1.")
                return True
            elif action == "heal":
                print("You used luck to heal 1 stamina.")
                self.stamina = min(self.stamina + 1, self.initial_stamina)
                return True
        else:
            print("Your luck failed.")
        self.luck -= 1
        return False
    
    def restore_stamina(self):
        if self.potions > 0:
            print("You drink a potion restoring your stamina. You feel stronger now!")
            self.potions -= 1
            self.stamina = self.initial_stamina
        else:
            print("You don't have more potions to drink.")
            
    def use_provision(self):
        if self.provisions > 0:
            print("You eat a provision and restore 4 stamina points.")
            self.stamina = min(self.stamina + 4, self.initial_stamina)
            self.provisions -= 1
        else:
            print("You have no provisions left.")
