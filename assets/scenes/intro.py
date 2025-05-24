import pygame
from ui.button import Button
from ui.utils import draw_text_centered, draw_message_box

def intro_scene(screen, clock, next_scene_callback, game_state):
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont('timesnewroman', 48)
    font_text = pygame.font.SysFont('timesnewroman', 24)
    bg_image = pygame.image.load("assets/intro_bg.png").convert()
    music = pygame.mixer.Sound("assets/intro_music.wav")
    music.play(-1)
    title_alpha = 0
    alpha_speed = 2

    title = "Rise Against Vecna"
    lore = [
        "The Forgotten Realms tremble under Vecna's shadow.",
        "Once a mortal, now a god, he seeks to dominate all.",
        "You, a lone wanderer, carry the spark of hope.",
        "Choose your path: warrior or mage?"
    ]

    def choose_warrior():
        game_state.player.attack += 5
        messages.append("You choose the path of the warrior.")
        next_scene_callback("village")

    def choose_mage():
        game_state.player.skills["fire_slash"]["damage"] += 10
        messages.append("You choose the path of the mage.")
        next_scene_callback("village")

    messages = []
    buttons = [
        Button(WIDTH // 2 - 250, HEIGHT - 100, 200, 50, "Warrior", choose_warrior),
        Button(WIDTH // 2 + 50, HEIGHT - 100, 200, 50, "Mage", choose_mage)
    ]

    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        title_alpha = min(255, title_alpha + alpha_speed)
        title_surface = font_title.render(title, True, (255, 215, 0))
        title_surface.set_alpha(title_alpha)
        draw_text_centered(screen, title, pygame.Rect(0, 30, WIDTH, 60), font=font_title, color=(255, 215, 0))
        for i, line in enumerate(lore):
            draw_text_centered(screen, line, pygame.Rect(0, 120 + i * 35, WIDTH, 30), font=font_text)
        draw_message_box(screen, messages, 50, 300, 700, 180)
        for btn in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        btn.click()
        pygame.display.update()
        clock.tick(60)
    music.stop()