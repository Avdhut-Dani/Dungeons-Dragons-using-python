import pygame
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.gold = 50
        self.potions = 2
        self.attack = 10
        self.level = 1
        self.exp = 0
        self.skills = {
            "fire_slash": {"damage": 15, "cooldown": 0, "max_cooldown": 3},
            "heal": {"amount": 20, "cooldown": 0, "max_cooldown": 2}
        }
        self.status_effects = []
        self.inventory = {}
        self.sprite = pygame.image.load("assets/player_sprite.png").convert_alpha()

    def is_alive(self):
        return self.hp > 0

    def basic_attack(self):
        return random.randint(self.attack, self.attack + 5)

    def use_skill(self, skill_name):
        if skill_name not in self.skills or self.skills[skill_name]["cooldown"] > 0:
            return 0, f"{skill_name} is on cooldown or invalid!"
        skill = self.skills[skill_name]
        if skill_name == "fire_slash":
            skill["cooldown"] = skill["max_cooldown"]
            return skill["damage"], f"You used Fire Slash for {skill['damage']} damage!"
        elif skill_name == "heal":
            skill["cooldown"] = skill["max_cooldown"]
            heal_amount = skill["amount"]
            self.hp = min(self.max_hp, self.hp + heal_amount)
            return 0, f"You healed for {heal_amount} HP!"
        return 0, "Unknown skill!"

    def use_potion(self):
        if self.potions > 0:
            self.potions -= 1
            heal_amount = 30
            self.hp = min(self.max_hp, self.hp + heal_amount)
            return f"You used a potion and healed for {heal_amount} HP!"
        return "No potions left!"

    def gain_exp(self, exp):
        self.exp += exp
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack += 2
            return f"Level up! You are now level {self.level}."

    def update_cooldowns(self):
        for skill in self.skills.values():
            if skill["cooldown"] > 0:
                skill["cooldown"] -= 1

    def update_status(self):
        messages = []
        new_effects = []
        for effect in self.status_effects:
            if effect["duration"] > 0:
                if effect["type"] == "poison":
                    self.hp -= 5
                    messages.append("Poison deals 5 damage!")
                effect["duration"] -= 1
                new_effects.append(effect)
        self.status_effects = new_effects
        return messages

    def draw(self, surface, x, y):
        surface.blit(self.sprite, (x, y))