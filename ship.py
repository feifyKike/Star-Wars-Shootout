# ship.py
import pygame

class Ship():
    def __init__(self, ai_settings, screen):
        """Initializing position on screen and settings"""
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('space_ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Starting each new ship at the center
        self.rect.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centery)

        # Movement Flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Updating the ship's position based on movement"""
        # Update the ship's center value
        if self.moving_up and self.rect.top > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center += self.ai_settings.ship_speed_factor

        # Update rect object from self.center
        self.rect.centery = self.center

    def center_ship(self):
        """Center the ship after alien collision"""
        self.center = self.screen_rect.centery

    def blitme(self):
        self.screen.blit(self.image, self.rect)
