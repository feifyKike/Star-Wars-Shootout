import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, ai_settings, screen, ship):
        """Creating a bullet object at the ship's current location"""
        super().__init__()
        self.screen = screen

        # Create bullet at set location and then assign to ships location
        self.rect = pygame.Rect(0,0, ai_settings.bullet_width, ai_settings.bullet_height)

        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.right

        # Store the bullet's position as a decimal value
        self.x = float(self.rect.x)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        """Move the bullet to the right."""
        # Update the decimal position of the bullet.
        self.x += self.speed_factor
        # Update the rect position
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
