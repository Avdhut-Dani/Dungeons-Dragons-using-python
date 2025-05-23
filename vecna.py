import pygame
import random

class Vecna:
    def __init__(self, player_level):
        self.name = "Vecna"
        self.max_hp = 150 + player_level * 20
        self.hp = self.max_hp
        self.attack = 15 + player_level * 2
        self.special_used = False
        self.sprite_sheet = pygame.image.load("assets/vecna_sprites.png").convert_alpha()
        self.frames = [pygame.transform.scale(self.sprite_sheet.subsurface((i * 200, 0, 200, 300)), (200, 300)) for i in range(4)]
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0

    def draw(self, surface, x, y):
        surface.blit(self.frames[self.current_frame], (x, y))
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = 0

    def take_turn(self, player, player_blocking=False):
        if self.hp <= 0:
            return "Vecna is defeated."
        
        attacks = [
            ("shadow_bolt", random.randint(self.attack, self.attack + 10), 0),
            ("curse", 0, "curse"),
            ("finger_of_death", random.randint(25, 40), 0) if self.hp < self.max_hp / 2 and not self.special_used else None
        ]
        attacks = [a for a in attacks if a]
        attack_type, dmg, status = random.choice(attacks)

        if attack_type == "curse":
            message = player.apply_status("curse")
            return f"Vecna casts Curse! {message}"
        if player_blocking:
            dmg = int(dmg * 0.4)
            message = "You block part of the attack! "
        else:
            message = ""
        player.hp -= dmg
        if attack_type == "finger_of_death":
            self.special_used = True
        return message + f"Vecna uses {attack_type.replace('_', ' ').title()} for {dmg} damage."
    
    def is_alive(self):
        return self.hp > 0