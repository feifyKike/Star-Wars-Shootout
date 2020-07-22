class GameStats():
    """Keeping track of the game statistics"""
    def __init__(self, ai_settings):
        """Initialize the statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start the game in inactive mode using a flag
        self.game_active = False

        # High score should never be reset
        self.high_score = ''
        self.report_high_score()

    def report_high_score(self):
        """Retrieve previous games high score"""
        try:
            filename = 'high_score_store.txt'
            with open(filename) as f_object:
                 file = f_object.readlines()
            for line in file:
                self.high_score += line
                
        except FileNotFoundError:
            self.high_score += '0'

    def reset_stats(self):
        """
        Initializing the ever changing statistic
        throughout the game
        """
        self.ships_left = self.ai_settings.ship_limit
        
        # initializing the score
        self.score = 0

        # initializing the players level
        self.level = 1

        
