# this module contains a single function
import sys
import pygame
from settings import Settings
import game_functions as gf
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from asteroid import Asteroid


def play_game():
    """Initializing and executing pygame settings"""
    pygame.init()

    # Allowing access to the settings module
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion Game")

    # Making the Play button
    play_button = Button(ai_settings, screen, "Play")

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Make a group of asteroids
    asteroids = Group()
    gf.create_asteroid_belt1(ai_settings, screen, asteroids)

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create an instance to store the necessary game stats
    # And create a scoreboard
    stats = GameStats(ai_settings)    
    sb = Scoreboard(ai_settings, screen, stats)

    # Starting the main game loop
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        ship, aliens, bullets)

        # Checking for game activity and deactivating unecessary items
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship,
                              aliens, bullets, asteroids)
            gf.update_aliens(ai_settings, stats, sb, screen,
                             ship, aliens, bullets, asteroids)
            gf.update_asteroid(ai_settings, stats,
                               sb, screen, ship, aliens, bullets, asteroids)
            
        gf.update_screen(ai_settings, screen, stats, sb,
                         ship, aliens, bullets, play_button, asteroids)

play_game()
