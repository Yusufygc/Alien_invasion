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
        
        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3 # 3 pixels
        self.bullet_height = 15 # 15 pixels
        self.bullet_color = (60,60,60) # dark gray
        self.bullets_allowed = 3 # 3 bullets at a time // tek seferde 3 mermi atılabilir.

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10 # 10 pixels
        self.fleet_direction = 1 # 1 represents right; -1 represents left // 1 sağa gider -1 sola gider.