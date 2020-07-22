import pygame.font
from pygame.sprite import Group
from heart import Heart

class Scoreboard():
    """A class to report the current score info"""
    def __init__(self, ai_settings, screen, stats):
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # Font settings for scoring info
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        #-------UNDER QUESTION-------#
        
        # Setting the position of the score board
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn high score inot a rendered image"""
        high_score = round(int(self.stats.high_score), -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.ai_settings.bg_color)
        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image"""
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.ai_settings.bg_color)

        # Position the level below the score in bottom right corner
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    #def prep_lives(self):
        #"""Show the amount of lives left"""
        #self.lives_image = self.font.render(str(self.stats.ships_left), True,
                                            #self.text_color, self.ai_settings.bg_color)

        # Setting the position of the numer of lives the ship has left
        #self.screen_rect = self.screen.get_rect()
        #self.lives_rect = self.lives_image.get_rect()
        #self.lives_rect.right = self.score_rect.right
        #self.lives_rect.bottom = self.screen_rect.bottom - 20

    def prep_lives(self):
        """Graphically display the number of lives left"""
        self.hearts = Group()
        for heart_number in range(self.stats.ships_left):
            heart = Heart(self.ai_settings, self.screen)
            heart.rect.x = self.screen_rect.right - 60 - (heart_number * heart.rect.width)
            heart.rect.bottom = self.screen_rect.bottom - 10
            self.hearts.add(heart)

    def show_score(self):
        """Draw the score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #self.screen.blit(self.lives_image, self.lives_rect)
        self.hearts.draw(self.screen)


        

    
                            











