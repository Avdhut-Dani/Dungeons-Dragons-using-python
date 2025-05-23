import pygame
import random
from ui.button import Button
from ui.utils import draw_text_centered, draw_message_box

def forest_scene(screen, clock, next_scene_callback, game_state):
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont('timesnewroman', 36)
    font_text = pygame.font.SysFont('timesnewroman', 24)
    bg_image = pygame.image.load("assets/forest_bg.png").convert()
    ambient_sound = pygame.mixer.Sound("assets/forest_ambient.wav")
    success_sound = pygame.mixer.Sound("assets/success.wav")
    fail_sound = pygame.mixer.Sound("assets/fail.wav")
    ambient_sound.play(-1)

    messages = [
        "You enter the Enchanted Forest, where ancient magic lingers.",
        "A glowing barrier blocks your path to the dungeon."
    ]
    progress = 0
    pattern = [random.randint(0, 3) for _ in range(4)]  # Random sequence of 4 runes
    player_input = []
    timer = 20 * 60  # 20 seconds at 60 FPS
    particles = []

    def add_particles(x, y, color):
        for _ in range(20):
            particles.append({
                "pos": [x, y],
                "vel": [random.uniform(-3, 3), random.uniform(-3, 3)],
                "life": 20,
                "color": color
            })

    def update_particles():
        nonlocal particles
        new_particles = []
        particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for p in particles:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["life"] -= 1
            if p["life"] > 0:
                new_particles.append(p)
                pygame.draw.circle(particle_surface, p["color"], (int(p["pos"][0]), int(p["pos"][1])), 3)
        particles = new_particles
        return particle_surface

    def start_minigame():
        nonlocal progress
        messages.append("A spirit appears: 'Match the rune sequence!'")
        progress = 1

    def input_rune(index):
        nonlocal player_input, timer
        if progress == 1 and timer > 0:
            player_input.append(index)
            if len(player_input) == len(pattern):
                check_pattern()

    def check_pattern():
        nonlocal progress, timer
        if player_input == pattern:
            messages.append("Correct sequence! The barrier fades.")
            game_state.player.potions += 1
            game_state.inventory["runes"] = game_state.inventory.get("runes", 0) + 1
            add_particles(WIDTH // 2, HEIGHT // 2, (0, 255, 0))
            success_sound.play()
            progress = 2
        else:
            messages.append("Wrong sequence! The barrier shocks you.")
            game_state.player.hp -= 10
            add_particles(WIDTH // 2, HEIGHT // 2, (255, 0, 0))
            fail_sound.play()
            progress = 2
        player_input.clear()

    def advance():
        nonlocal progress
        progress += 1
        if progress == 3:
            messages.append("The path to the dungeon is clear.")
            ambient_sound.stop()
            next_scene_callback("dungeon")

    buttons = [Button(300, 500, 200, 50, "Approach Barrier", start_minigame)]
    rune_buttons = [
        Button(200 + i * 100, 400, 80, 80, f"Rune {i+1}", lambda i=i: input_rune(i))
        for i in range(4)
    ]

    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        particle_surface = update_particles()
        screen.blit(particle_surface, (0, 0))

        draw_text_centered(screen, "Enchanted Forest", pygame.Rect(0, 30, WIDTH, 50), font=font_title, color=(180, 180, 255))
        draw_message_box(screen, messages, 50, 120, 700, 280)
        if progress == 1:
            draw_text_centered(screen, f"Time: {timer // 60} sec", pygame.Rect(0, 80, WIDTH, 30), font=font_text)
            sequence_text = "Sequence: " + " ".join(str(i + 1) for i in pattern)
            draw_text_centered(screen, sequence_text, pygame.Rect(0, 350, WIDTH, 30), font=font_text)
            for btn in rune_buttons:
                btn.update(mouse_pos)
                btn.draw(screen)
            timer -= 1
            if timer <= 0:
                messages.append("Time's up! The barrier shocks you.")
                game_state.player.hp -= 10
                add_particles(WIDTH // 2, HEIGHT // 2, (255, 0, 0))
                fail_sound.play()
                progress = 2
        elif progress == 2:
            buttons = [Button(300, 500, 200, 50, "Continue", advance)]

        for btn in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons + (rune_buttons if progress == 1 else []):
                    if btn.rect.collidepoint(mouse_pos):
                        btn.click()

        pygame.display.update()
        clock.tick(60)

    ambient_sound.stop()