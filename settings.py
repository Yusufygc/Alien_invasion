class Settings:
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width=1200
        self.screen_height=700
        self.bg_color=(255,255,255)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3 # 3 ships
        
        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 9 # 9 pixels
        self.bullet_height = 20 # 20 pixels
        self.bullet_color = (60,60,60) # dark gray
        self.bullets_allowed = 3 # 3 bullets at a time // tek seferde 3 mermi atılabilir.

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10 # 10 pixels
        self.fleet_direction = 1 # 1 represents right; -1 represents left // 1 sağa gider -1 sola gider.

        # How quickly the game speeds up
        self.speedup_scale = 1.1 # 10% faster each time

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5 # 1.5 pixels
        self.bullet_speed = 3.0 # 3 pixels
        self.alien_speed = 1.0 # 1 pixel

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1 # 1 sağa gider -1 sola gider.

        # Scoring
        self.alien_points = 50 # 50 points for each alien shot down

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale # increase ship speed
        self.bullet_speed *= self.speedup_scale # increase bullet speed
        self.alien_speed *= self.speedup_scale # increase alien speed