import random
import pygame

def roll_d20(game_state=None):
    roll = random.randint(1, 20)
    if game_state and "Light Artifact" in game_state.player.inventory["artifacts"]:
        if roll < 5:
            roll = random.randint(1, 20)
            return roll, "Rerolled with Light Artifact!"
    return roll, ""