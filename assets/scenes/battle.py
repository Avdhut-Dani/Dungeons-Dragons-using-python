import pygame
import random
from entities.player import Player
from entities.vecna import Vecna
from ui.button import Button
from ui.utils import draw_health_bar, draw_message_box, draw_text_centered
from scenes.minigames.dice_roll import roll_d20

def battle_scene(screen, clock, game_state, next_scene_callback):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.SysFont('timesnewroman', 24)
    title_font = pygame.font.SysFont('timesnewroman', 32)
    bg_image = pygame.image.load("assets/battle_bg.png").convert()
    particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    player = game_state.player
    vecna = Vecna(player.level)
    messages = ["Vecna rises from the shadows..."]
    turn = 1
    blocking = False
    particles = []

    def add_particles(x, y, color):
        for _ in range(10):
            particles.append({"pos": [x, y], "vel": [random.uniform(-2, 2), random.uniform(-2, 2)], "life": 30, "color": color})

    def update_particles():
        nonlocal particles
        new_particles = []
        for p in particles:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["life"] -= 1
            if p["life"] > 0:
                new_particles.append(p)
        particles = new_particles
        particle_surface.fill((0, 0, 0, 0))
        for p in particles:
            pygame.draw.circle(particle_surface, p["color"], (int(p["pos"][0]), int(p["pos"][1])), 3)

    def player_attack():
        nonlocal turn, blocking
        roll, msg = roll_d20(game_state)
        if msg:
            messages.append(msg)
        if roll >= 15:
            dmg = player.basic_attack() + 5
            messages.append(f"You rolled {roll}! A critical hit!")
            add_particles(650, 250, (255, 0, 0))
        elif roll >= 8:
            dmg = player.basic_attack()
            messages.append(f"You rolled {roll}. Hit for {dmg}.")
            add_particles(650, 250, (255, 0, 0))
        else:
            dmg = 0
            messages.append(f"You rolled {roll}. You missed!")
        vecna.hp -= dmg
        blocking = False
        next_turn()

    def player_skill(skill_name):
        nonlocal turn, blocking
        dmg, msg = player.use_skill(skill_name)
        messages.append(msg)
        if dmg > 0:
            vecna.hp -= dmg
            add_particles(650, 250, (255, 165, 0))
        blocking = False
        next_turn()

    def player_block():
        nonlocal blocking
        blocking = True
        messages.append("You brace for Vecna's attack.")
        next_turn()

    def player_potion():
        msg = player.use_potion()
        messages.append(msg)
        add_particles(150, 250, (0, 255, 0))
        next_turn()

    def player_run():
        messages.append("You cannot escape Vecna!")
        next_turn()

    def next_turn():
        nonlocal turn
        player.update_cooldowns()
        messages.extend(player.update_status())
        turn += 1
        if vecna.is_alive():
            vecna_msg = vecna.take_turn(player, blocking)
            messages.append(vecna_msg)
            add_particles(150, 250, (128, 0, 128))

    buttons = [
        Button(50, 500, 120, 50, "Attack", player_attack),
        Button(180, 500, 120, 50, "Fire Slash", lambda: player_skill("fire_slash")),
        Button(310, 500, 120, 50, "Heal", lambda: player_skill("heal")),
        Button(440, 500, 120, 50, "Potion", player_potion),
        Button(570, 500, 120, 50, "Block", player_block),
        Button(700, 500, 120, 50, "Run", player_run),
    ]

    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        update_particles()
        screen.blit(particle_surface, (0, 0))
        player.draw(screen, 100, 130)
        vecna.draw(screen, 550, 130)
        draw_health_bar(screen, 50, 50, 200, 20, player.hp, player.max_hp)
        draw_text_centered(screen, f"{player.name} HP", pygame.Rect(50, 20, 200, 30))
        draw_health_bar(screen, 550, 50, 200, 20, vecna.hp, vecna.max_hp)
        draw_text_centered(screen, "Vecna HP", pygame.Rect(550, 20, 200, 30))
        draw_message_box(screen, messages, 50, 300, 700, 180)
        draw_text_centered(screen, f"Status: {', '.join(player.status_effects) or 'None'}", pygame.Rect(50, 80, 200, 30))
        for btn in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)
        
        if not player.is_alive():
            draw_text_centered(screen, "You have fallen to Vecna...", pygame.Rect(0, 200, WIDTH, 50), font=title_font, color=(255, 0, 0))
            pygame.display.update()
            pygame.time.delay(2000)
            next_scene_callback("dungeon")
            running = False
        elif not vecna.is_alive():
            draw_text_centered(screen, "You have defeated Vecna!", pygame.Rect(0, 200, WIDTH, 50), font=title_font, color=(0, 255, 0))
            game_state.quests["main"] = "Completed"
            game_state.player.gain_exp(200)
            pygame.display.update()
            pygame.time.delay(2000)
            next_scene_callback("village")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player.is_alive() and vecna.is_alive():
                    for btn in buttons:
                        if btn.rect.collidepoint(mouse_pos):
                            btn.click()
        pygame.display.update()
        clock.tick(60)