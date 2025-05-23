import pygame
import random
from ui.utils import draw_text_centered, draw_message_box
from ui.button import Button

def riddle_minigame(screen, clock):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.SysFont('timesnewroman', 24)
    bg_image = pygame.image.load("assets/riddle_bg.png").convert()
    success_sound = pygame.mixer.Sound("assets/success.wav")
    fail_sound = pygame.mixer.Sound("assets/fail.wav")

    riddles = [
        (
            "I am Vecna's strength, hidden in plain sight. I am not flesh, nor bone, but power's light. What am I?",
            ["A sword", "A spell", "A secret", "A crown"],
            2
        ),
        (
            "Born of mortal, yet god I became. Whisper my name, and fear the flame. Who am I?",
            ["A dragon", "Vecna", "A lich", "A mage"],
            1
        ),
        (
            "In shadows I dwell, with knowledge to keep. Answer my call, or in darkness you weep. What am I?",
            ["A book", "A sage", "A rune", "A shadow"],
            1
        )
    ]
    riddle = random.choice(riddles)
    question, options, correct_index = riddle

    timer = 15 * 60
    selected = None
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

    def select_answer(index):
        nonlocal selected, timer
        if timer > 0:
            selected = index
            timer = 0

    buttons = [
        Button(150 + i * 150, 400, 120, 50, options[i], lambda i=i: select_answer(i))
        for i in range(4)
    ]

    running = True
    success = False
    while running and timer > 0:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        particle_surface = update_particles()
        screen.blit(particle_surface, (0, 0))

        draw_text_centered(screen, "Sage's Riddle", pygame.Rect(0, 30, WIDTH, 50), font=font, color=(180, 180, 255))
        draw_text_centered(screen, question, pygame.Rect(0, 100, WIDTH, 50), font=font)
        draw_text_centered(screen, f"Time: {timer // 60} sec", pygame.Rect(0, 160, WIDTH, 30), font=font)

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

    if selected == correct_index:
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
        draw_text_centered(screen, "Sage's Riddle", pygame.Rect(0, 30, WIDTH, 50), font=font, color=(180, 180, 255))
        draw_text_centered(screen, question, pygame.Rect(0, 100, WIDTH, 50), font=font)
        result_text = "Correct!" if success else "Incorrect or time's up!"
        draw_text_centered(screen, result_text, pygame.Rect(0, 160, WIDTH, 30), font=font, color=(0, 255, 0) if success else (255, 0, 0))
        for btn in buttons:
            btn.draw(screen)
        pygame.display.update()
        clock.tick(60)

    return success