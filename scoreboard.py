import pygame.font

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
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
        self.level_rect.left = self.score_rect.left # level'i score'un sağ tarafına yerleştiriyoruz.
        self.level_rect.top = self.score_rect.topleft # level'i score'un altına yerleştiriyoruz.


    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect) # score'u ekrana yazdırıyoruz.
        # bu method score_rect in belirlediği koordinatlarda score_image'ı ekrana yazdırır.
        self.screen.blit(self.high_score_image, self.high_score_rect) # high score'u ekrana yazdırıyoruz.
        self.screen.blit(self.level_image, self.level_rect) # level'i ekrana yazdırıyoruz.

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score: # eğer score high score'dan büyükse
            self.stats.high_score = self.stats.score # high score'u score'a eşitle
            self.prep_high_score() # high score'u güncelleriz.
   