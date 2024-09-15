import random

from base import Character, Scene


# Game engine to navigate through scenes and handle combat
class GameEngine:
    def __init__(self, starting_scene: Scene, character: Character, prologue: str):
        self.character = character
        self.current_scene = starting_scene
        self._prologue = prologue
        
        
    def prologue(self):
        print("\n===== Prologue: The Curse of Blackthorn Keep =====")
        print(self._prologue)
        input("\nPress Enter to begin your journey...\n")

    def start(self):
        self.prologue()
        self.character.display_stats()
        print("You are about to enter a perilous adventure.")
        
        while self.current_scene:            
            self.current_scene.display()

            # Handle fights if monsters are present
            if self.current_scene.monsters:
                for monster in self.current_scene.monsters:
                    self.fight_monster(monster)

            # Collect treasures
            if self.current_scene.treasures:
                for treasure in self.current_scene.treasures:
                    self.character.gold += treasure.value
                    print(f"You collected {treasure.value} gold pieces.")

            # Move to next scene
            if self.current_scene.next_scenes:
                direction = input(f"Choose the next direction {list(self.current_scene.next_scenes.keys())}: ").strip().lower()
                if direction in self.current_scene.next_scenes:
                    self.current_scene = self.current_scene.next_scenes[direction]
                else:
                    print("Invalid direction. Try again.")
            else:
                print("The adventure ends here.")
                break

    def fight_monster(self, monster):
        print(f"\nYou are fighting a {monster.name}!")
        while monster.stamina > 0 and self.character.stamina > 0:
            
            monster_display = monster.display()
            print(monster_display)
            
            action = input("Do you want to [A]ttack, use [L]uck, or [D]rink potion? (or check your stats [S]) ").strip().lower()

            if action == 'a':
                if self.attack(monster):
                    print(f"You hit the {monster.name}!")
                    monster.stamina -= self.character.damage()
                else:
                    print(f"The {monster.name} hits you!")
                    self.character.stamina -= monster.damage
            elif action == 'l':
                luck_choice = input("Do you want to use luck to reduce damage or increase damage? (reduce/increase) ").strip().lower()
                if luck_choice == "reduce":
                    if self.character.use_luck("reduce_damage"):
                        self.character.stamina -= 1
                elif luck_choice == "increase":
                    if self.character.use_luck("increase_damage"):
                        monster.stamina -= 1
            elif action == 'd':
                self.character.restore_stamina()
            elif action == 's':
                msg = self.character.display_stats()
                print(msg)

        if self.character.stamina > 0:
            print(f"You have defeated the {monster.name}!")
        else:
            print("You have been defeated. Game over.")

    def attack(self, monster):
        print("Rolling dices")
        player_attack_roll = random.randint(2, 12) + self.character.skill
        print(f"player attack roll  = {player_attack_roll}")
        monster_attack_roll = random.randint(2, 12) + monster.skill
        print(f"monster attack roll = {monster_attack_roll}")
        
        return player_attack_roll > monster_attack_roll
