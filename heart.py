import pygame
from pygame.sprite import Sprite

class Heart(Sprite):
    """Create a life meter on the screen"""
    def __init__(self, ai_settings, screen):
        """Initialize needed attributes"""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        
        # Load the asteroid image and get its rect
        self.image = pygame.image.load('lives_image.bmp')
        self.rect = self.image.get_rect()
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)
