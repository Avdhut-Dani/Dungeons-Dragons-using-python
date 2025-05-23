import pygame
import sys
import asyncio
import platform
from scenes.intro import intro_scene
from scenes.village import village_scene
from scenes.dungeon import dungeon_scene
from scenes.battle import battle_scene
from scenes.forest import forest_scene
from scenes.crypt import crypt_scene 
from entities.player import Player
from ui.button import Button

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rise Against Vecna")
clock = pygame.time.Clock()

class GameState:
    def __init__(self):
        self.player = Player("Hero")
        self.quests = {"main": "Defeat Vecna", "side": []}
        self.inventory = {"potions": 2, "keys": 0, "artifacts": [], "runes": 0, "gold": 50}
        self.current_scene = "main_menu"

pygame.mixer.music.load("assets/background_music.mp3")
pygame.mixer.music.play(-1)
click_sound = pygame.mixer.Sound("assets/click.wav")

def main_menu(screen, clock, scene_router):
    font = pygame.font.SysFont('timesnewroman', 36)
    buttons = [
        Button(300, 200, 200, 50, "Start Game", lambda: scene_router("intro")),
        Button(300, 300, 200, 50, "Settings", lambda: None),
        Button(300, 400, 200, 50, "Quit", lambda: sys.exit())
    ]
    bg_image = pygame.image.load("assets/main_menu_bg.png").convert()
    running = True
    while running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                for btn in buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        btn.click()
        pygame.display.update()
        clock.tick(60)

def scene_router(scene_name, game_state):
    if scene_name == "main_menu":
        main_menu(screen, clock, lambda s: scene_router(s, game_state))
    elif scene_name == "intro":
        intro_scene(screen, clock, lambda s: scene_router(s, game_state), game_state)
    elif scene_name == "village":
        village_scene(screen, clock, lambda s: scene_router(s, game_state), game_state)
    elif scene_name == "dungeon":
        dungeon_scene(screen, clock, lambda s: scene_router(s, game_state), game_state)
    elif scene_name == "battle":
        battle_scene(screen, clock, game_state, lambda s: scene_router(s, game_state))
    elif scene_name == "forest":
        forest_scene(screen, clock, lambda s: scene_router(s, game_state), game_state)
    elif scene_name == "crypt":
        crypt_scene(screen, clock, lambda s: scene_router(s, game_state), game_state)
    else:
        pygame.quit()
        sys.exit()

async def main():
    game_state = GameState()
    scene_router("main_menu", game_state)
    while True:
        await asyncio.sleep(1.0 / 60)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())