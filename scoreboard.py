import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect() # get_rect() methodu ile ekranın dört bir köşesinin koordinatlarını alıyoruz.
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (30,30,30) # dark gray
        self.font = pygame.font.SysFont(None, 48) # None parametresi default font kullanılacağını belirtir.

        # Prepare the initial score image.
        self.prep_score() # score'u hazırla
        self.prep_high_score() # high score'u hazırla
        self.prep_level() # level'i hazırla
        self.prep_ships() # gemileri hazırla



    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1) # score'u 10'luk basamağa yuvarlıyoruz.
        score_str = "score : {:,}".format(rounded_score) # score'u stringe çeviriyoruz ve virgülden sonra 3 basamaklı sayılar için virgül koyuyoruz.
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color) # score'u fonta göre render ediyoruz.

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect() # score'un koordinatlarını alıyoruz.
        self.score_rect.right = self.screen_rect.right - 20 # score'u sağ üst köşeye yerleştiriyoruz.
        self.score_rect.top = 20 # score'u sağ üst köşeye yerleştiriyoruz.

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1) # high score'u 10'luk basamağa yuvarlıyoruz.
        high_score_str = "high score : {:,}".format(high_score) # high score'u stringe çeviriyoruz ve virgülden sonra 3 basamaklı sayılar için virgül koyuyoruz.
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color) # high score'u fonta göre render ediyoruz.

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect() # high score'un koordinatlarını alıyoruz.
        self.high_score_rect.centerx = self.screen_rect.centerx # high score'u ekranın ortasına yerleştiriyoruz.
        self.high_score_rect.top = self.score_rect.top # high score'u score'un üstüne yerleştiriyoruz.

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = "level : {}".format(self.stats.level) # level'i stringe çeviriyoruz.
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color) # level'i fonta göre render ediyoruz.

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect() # level'in koordinatlarını alıyoruz.
        self.level_rect.right = self.score_rect.right # level'i ekranın sağ tarafına yerleştiriyoruz.
        self.level_rect.top =self.score_rect.bottom + 10 # level'i scorun 10piksel altına yerleştiriyoruz.


    def prep_ships(self):
        """Show how many ships are left."""
        ships_str = "Gardaşlar :" # gemileri stringe çeviriyoruz.
        self.ships_image = self.font.render(ships_str, True, self.text_color, self.settings.bg_color) # gemileri fonta göre render ediyoruz.

        # Position the ships left of the screen.
        self.ships_rect = self.ships_image.get_rect() # gemilerin koordinatlarını alıyoruz.
        self.ships_rect.left = 10 # gemileri ekranın sol tarafına yerleştiriyoruz.
        self.ships_rect.top = 40 
        
        self.ships = Group() # gemileri grup olarak tutuyoruz.
        for ship_number in range(self.stats.ships_left): # gemileri for döngüsü ile ekliyoruz.
            ship = Ship(self.ai_game) # gemi oluşturuyoruz.
            ship.rect.x = 200 + ship_number * ship.rect.width # gemileri birbirinden 10piksel aralıklarla ekliyoruz.
            ship.rect.y = 2 # gemileri 5 piksel yukarıdan ekliyoruz.
            self.ships.add(ship) # gemileri gruba ekliyoruz.


    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect) # score'u ekrana yazdırıyoruz.
        # bu method score_rect in belirlediği koordinatlarda score_image'ı ekrana yazdırır.
        self.screen.blit(self.high_score_image, self.high_score_rect) # high score'u ekrana yazdırıyoruz.
        self.screen.blit(self.level_image, self.level_rect) # level'i ekrana yazdırıyoruz.
        self.screen.blit(self.ships_image, self.ships_rect) # gemileri ekrana yazdırıyoruz.
        self.ships.draw(self.screen) # gemileri ekrana yazdırıyoruz. self.screen gemilerin ekrana yazdırılacağı yeri belirtir.

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score: # eğer score high score'dan büyükse
            self.stats.high_score = self.stats.score # high score'u score'a eşitle
            self.prep_high_score() # high score'u güncelleriz.
   