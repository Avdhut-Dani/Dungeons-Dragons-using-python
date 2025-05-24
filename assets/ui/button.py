import pygame

class Button:
    def __init__(self, x, y, width, height, text, action=None, font=None, base_color=(60, 60, 60), hover_color=(100, 100, 100), text_color=(255, 255, 255)):
        self.base_rect = pygame.Rect(x, y, width, height)
        self.rect = self.base_rect.copy()
        self.text = text
        self.action = action
        self.font = font or pygame.font.SysFont('timesnewroman', 24)
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.scale = 1.0

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.base_color
        self.rect = self.base_rect.inflate(self.scale * 10 - 10, self.scale * 10 - 10)
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.base_rect.collidepoint(mouse_pos)
        self.scale = 1.1 if self.hovered else 1.0

    def click(self):
        if self.action:
            self.action()