import pygame
from ui.button import Button
from ui.utils import draw_text_centered, draw_message_box
from scenes.minigames.riddle import riddle_minigame

def village_scene(screen, clock, next_scene_callback, game_state):
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont('timesnewroman', 36)
    font_text = pygame.font.SysFont('timesnewroman', 24)
    bg_image = pygame.image.load("assets/village_bg.png").convert()
    ambient_sound = pygame.mixer.Sound("assets/village_ambient.wav")
    ambient_sound.play(-1)

    messages = [
        "You arrive at a bustling village, alive with hope.",
        "A wise sage offers knowledge of Vecna's lair, but demands a test."
    ]
    progress = 0

    def start_riddle():
        nonlocal progress
        success = riddle_minigame(screen, clock)
        if success:
            messages.append("The sage nods. You gain a potion!")
            game_state.player.potions += 1
            game_state.inventory["potions"] = game_state.player.potions
        else:
            messages.append("The sage frowns. You lose 10 gold.")
            game_state.player.gold = max(0, game_state.player.gold - 10)
            game_state.inventory["gold"] = game_state.player.gold
        progress = 1

    def advance():
        nonlocal progress
        messages.append("The sage reveals the path to the forest.")
        ambient_sound.stop()
        next_scene_callback("forest")

    buttons = [Button(300, 500, 200, 50, "Speak to Sage", start_riddle)]

    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        draw_text_centered(screen, "Village Square", pygame.Rect(0, 30, WIDTH, 50), font=font_title, color=(180, 180, 255))
        draw_message_box(screen, messages, 50, 120, 700, 280)
        if progress == 1:
            buttons = [Button(300, 500, 200, 50, "Continue", advance)]

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

    ambient_sound.stop()