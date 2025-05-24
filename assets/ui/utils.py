import pygame
from entities.player import Player

def get_default_font(size=24):
    return pygame.font.SysFont('timesnewroman', size)

def draw_text_centered(surface, text, rect, font=None, color=(255, 255, 255), shadow=True):
    if font is None:
        font = get_default_font()
    if shadow:
        shadow_surface = font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(rect.centerx + 2, rect.centery + 2))
        surface.blit(shadow_surface, shadow_rect)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_message_box(surface, messages, x, y, w, h, font=None):
    if font is None:
        font = get_default_font()
    pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h))
    pygame.draw.rect(surface, (100, 100, 100), (x, y, w, h), 2)
    for i, msg in enumerate(messages[-5:]):
        draw_text_centered(surface, msg, pygame.Rect(x + 10, y + 10 + i * 25, w - 20, 25), font=font)

def draw_health_bar(surface, x, y, width, height, player):
    black = (0, 0, 0)
    gradient = pygame.Surface((width, height))
    for i in range(width):
        ratio = i / width
        color = (int(200 * (1 - ratio)), int(200 * ratio), 0)
        pygame.draw.line(gradient, color, (i, 0), (i, height))
    pygame.draw.rect(surface, black, (x, y, width, height))
    pygame.draw.rect(surface, (100, 0, 0), (x, y, width, height))
    ratio = max(0, player.hp / player.max_hp)
    surface.blit(gradient, (x, y), (0, 0, width * ratio, height))