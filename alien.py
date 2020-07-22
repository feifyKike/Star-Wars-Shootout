import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""
    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('star_destroyer.bmp')
        self.rect = self.image.get_rect()

        # Loading the screen rect attribute
        self.screen_rect = self.screen.get_rect()

        # Start each new alien in the right top corner
        self.rect.centerx = self.screen_rect.right - self.rect.width
        self.rect.centery = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.centerx)

    def check_edges(self):
        """Return True if aliens is at endge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True
        elif self.rect.top <= 0:
            return True

    def update(self):
        """Move the alien down."""
        self.y += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.y = self.y

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
