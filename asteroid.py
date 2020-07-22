import pygame
from pygame.sprite import Sprite
import random

class Asteroid(Sprite):
    """Creating a single asteroido to be model after"""
    def __init__(self, ai_settings, screen):
        """Initialize attributes for asteroid"""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Load the asteroid image and get its rect
        self.asteroid_image = pygame.image.load('asteroid_pic.bmp')
        self.rect =  self.asteroid_image.get_rect()

        # Start the position of the asteroid
        #self.screen_rect = self.screen.get_rect()
        #self.rect.right = self.screen_rect.right
        #self.rect.left = self.screen_rect.centery

        # Create a random spawn point on the right side of the screen
        self.screen_rect = self.screen.get_rect()
        self.rect.right = self.screen_rect.right
        spawn_range = ai_settings.screen_height - self.rect.height
        random_positiony = random.uniform(self.rect.height, spawn_range)
        self.rect.centery = random_positiony
        
        # Store the aliens exact position
        self.x = float(self.rect.right)
        self.speed_factor = ai_settings.asteroid_speed_factor

    def update(self):
        """Move bullet to the left of the screen"""
        self.x -= self.speed_factor
        
        # Update the rect position
        self.rect.x = self.x

    def blitme(self):
        """Draw the asteroid at its static location"""
        self.screen.blit(self.asteroid_image, self.rect)
