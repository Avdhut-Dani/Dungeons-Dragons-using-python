import pygame
import random
from ui.button import Button
from ui.utils import draw_text_centered, draw_message_box

def crypt_scene(screen, clock, next_scene_callback, game_state):
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont('timesnewroman', 36)
    font_text = pygame.font.SysFont('timesnewroman', 24)
    bg_image = pygame.image.load("assets/crypt_bg.png").convert()
    ambient_sound = pygame.mixer.Sound("assets/crypt_ambient.wav")
    success_sound = pygame.mixer.Sound("assets/success.wav")
    fail_sound = pygame.mixer.Sound("assets/fail.wav")
    ambient_sound.play(-1)

    messages = [
        "You step into the ancient crypt, its air heavy with death.",
        "A magical trap glows ahead, tiles pulsing with arcane symbols."
    ]
    progress = 0
    # 4x2 grid: 8 tiles, 4 unique symbols (each appears twice)
    symbols = ["★", "★", "☽", "☽", "☀", "☀", "♦", "♦"]
    random.shuffle(symbols)
    tiles = [{"symbol": s, "revealed": False, "matched": False} for s in symbols]
    first_tile = None
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
        messages.append("The trap hums: match the tiles to disable it!")
        progress = 1

    def click_tile(index):
        nonlocal first_tile, progress, timer
        if progress != 1 or timer <= 0 or tiles[index]["matched"] or tiles[index]["revealed"]:
            return
        tiles[index]["revealed"] = True
        if first_tile is None:
            first_tile = index
        else:
            if tiles[first_tile]["symbol"] == tiles[index]["symbol"]:
                tiles[first_tile]["matched"] = tiles[index]["matched"] = True
                add_particles(WIDTH // 2, HEIGHT // 2, (0, 255, 0))
                success_sound.play()
                if all(t["matched"] for t in tiles):
                    messages.append("Trap disabled! You find a key and 20 gold.")
                    game_state.inventory["keys"] = game_state.inventory.get("keys", 0) + 1
                    game_state.player.gold += 20
                    progress = 2
            else:
                pygame.time.delay(500)  # Brief pause to show mismatch
                tiles[first_tile]["revealed"] = tiles[index]["revealed"] = False
            first_tile = None

    def advance():
        nonlocal progress
        if progress == 1:  # Timeout or manual advance during minigame
            messages.append("The trap triggers! You take 15 damage.")
            game_state.player.hp -= 15
            progress = 2
        else:  # progress == 2
            progress = 3
            messages.append("The dungeon entrance lies ahead.")
            ambient_sound.stop()
            next_scene_callback("dungeon")

    buttons = [Button(300, 500, 200, 50, "Inspect Trap", start_minigame)]
    tile_buttons = [
        Button(200 + (i % 4) * 100, 300 + (i // 4) * 100, 80, 80, "", lambda i=i: click_tile(i))
        for i in range(8)
    ]

    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        particle_surface = update_particles()
        screen.blit(particle_surface, (0, 0))

        draw_text_centered(screen, "Ancient Crypt", pygame.Rect(0, 30, WIDTH, 50), font=font_title, color=(180, 180, 255))
        draw_message_box(screen, messages, 50, 120, 700, 180)
        if progress == 1:
            draw_text_centered(screen, f"Time: {timer // 60} sec", pygame.Rect(0, 80, WIDTH, 30), font=font_text)
            for i, btn in enumerate(tile_buttons):
                btn.text = tiles[i]["symbol"] if tiles[i]["revealed"] or tiles[i]["matched"] else "?"
                btn.update(mouse_pos)
                btn.draw(screen)
            timer -= 1
            if timer <= 0:
                advance()
        elif progress == 2:
            buttons = [Button(300, 500, 200, 50, "Continue", advance)]

        for btn in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons + (tile_buttons if progress == 1 else []):
                    if btn.rect.collidepoint(mouse_pos):
                        btn.click()

        pygame.display.update()
        clock.tick(60)

    ambient_sound.stop()