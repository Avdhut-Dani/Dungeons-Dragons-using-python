import pygame
import random
from ui.utils import draw_text_centered
from ui.button import Button

def lockpicking_minigame(screen, clock):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.SysFont('timesnewroman', 24)
    bg_image = pygame.image.load("assets/lockpicking_bg.png").convert()
    success_sound = pygame.mixer.Sound("assets/success.wav")
    fail_sound = pygame.mixer.Sound("assets/fail.wav")

    tumblers = [{"progress": 0, "target": random.uniform(0.4, 0.6), "speed": random.uniform(0.01, 0.02)} for _ in range(3)]
    current_tumbler = 0
    timer = 20 * 60  # 20 seconds
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

    def attempt_lock():
        nonlocal current_tumbler
        if timer <= 0 or current_tumbler >= len(tumblers):
            return
        tumbler = tumblers[current_tumbler]
        if abs(tumbler["progress"] - tumbler["target"]) < 0.05:
            current_tumbler += 1
            add_particles(WIDTH // 2, HEIGHT // 2, (0, 255, 0))
            success_sound.play()
        else:
            tumbler["progress"] = 0
            add_particles(WIDTH // 2, HEIGHT // 2, (255, 0, 0))
            fail_sound.play()

    buttons = [Button(300, 400, 200, 50, "Attempt Lock", attempt_lock)]

    running = True
    success = False
    while running and timer > 0 and current_tumbler < len(tumblers):
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        particle_surface = update_particles()
        screen.blit(particle_surface, (0, 0))

        draw_text_centered(screen, "Lockpicking Challenge", pygame.Rect(0, 30, WIDTH, 50), font=font, color=(180, 180, 255))
        draw_text_centered(screen, f"Time: {timer // 60} sec", pygame.Rect(0, 80, WIDTH, 30), font=font)
        draw_text_centered(screen, f"Tumbler {current_tumbler + 1}/{len(tumblers)}", pygame.Rect(0, 110, WIDTH, 30), font=font)

        for i, tumbler in enumerate(tumblers):
            bar_x, bar_y = 200, 200 + i * 60
            bar_width, bar_height = 400, 40
            pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            target_x = bar_x + tumbler["target"] * bar_width
            pygame.draw.rect(screen, (0, 255, 0), (target_x - 20, bar_y, 40, bar_height))
            progress_x = bar_x + tumbler["progress"] * bar_width
            pygame.draw.rect(screen, (255, 255, 255), (progress_x - 5, bar_y, 10, bar_height))
            tumbler["progress"] = (tumbler["progress"] + tumbler["speed"]) % 1.0

        for btn in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        btn.click()

        timer -= 1
        pygame.display.update()
        clock.tick(60)

    if current_tumbler >= len(tumblers):
        success = True
        add_particles(WIDTH // 2, HEIGHT // 2, (0, 255, 0))
        success_sound.play()
    else:
        add_particles(WIDTH // 2, HEIGHT // 2, (255, 0, 0))
        fail_sound.play()

    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:
        screen.blit(bg_image, (0, 0))
        particle_surface = update_particles()
        screen.blit(particle_surface, (0, 0))
        draw_text_centered(screen, "Lockpicking Challenge", pygame.Rect(0, 30, WIDTH, 50), font=font, color=(180, 180, 255))
        result_text = "Success!" if success else "Failed or time's up!"
        draw_text_centered(screen, result_text, pygame.Rect(0, 80, WIDTH, 30), font=font, color=(0, 255, 0) if success else (255, 0, 0))
        for btn in buttons:
            btn.draw(screen)
        pygame.display.update()
        clock.tick(60)

    return success