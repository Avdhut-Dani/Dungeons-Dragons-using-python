import pygame
from ui.button import Button
from ui.utils import draw_text_centered, draw_message_box
from scenes.minigames.lockpicking import lockpicking_minigame

def dungeon_scene(screen, clock, next_scene_callback, game_state):
    WIDTH, HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont('timesnewroman', 36)
    font_text = pygame.font.SysFont('timesnewroman', 24)
    bg_image = pygame.image.load("assets/dungeon_bg.png").convert()
    ambient_sound = pygame.mixer.Sound("assets/dungeon_ambient.wav")
    ambient_sound.play(-1)

    messages = [
        "You enter a dark dungeon, Vecna's lair nearby.",
        "A locked door blocks your path, requiring skill to open."
    ]
    progress = 0

    def start_lockpicking():
        nonlocal progress
        success = lockpicking_minigame(screen, clock)
        if success:
            messages.append("The lock clicks open! You gain 30 gold.")
            game_state.player.gold += 30
            game_state.inventory["gold"] = game_state.player.gold
        else:
            messages.append("The lock jams! You take 10 damage.")
            game_state.player.hp -= 10
            if not game_state.player.is_alive():
                messages.append("You succumb to your wounds...")
                progress = 2
                return
        progress = 1

    def advance():
        nonlocal progress
        if game_state.player.is_alive():
            messages.append("The door opens, revealing Vecna's chamber.")
            ambient_sound.stop()
            next_scene_callback("battle")
        else:
            messages.append("Game Over. Your quest ends here.")
            ambient_sound.stop()
            next_scene_callback("main_menu")

    buttons = [Button(300, 500, 200, 50, "Pick Lock", start_lockpicking)]

    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        draw_text_centered(screen, "Dungeon Depths", pygame.Rect(0, 30, WIDTH, 50), font=font_title, color=(180, 180, 255))
        draw_message_box(screen, messages, 50, 120, 700, 280)
        if progress == 1 or progress == 2:
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