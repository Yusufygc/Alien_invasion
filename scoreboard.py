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


    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score) # score'u stringe çeviriyoruz.
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color) # score'u fonta göre render ediyoruz.

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect() # score'un koordinatlarını alıyoruz.
        self.score_rect.right = self.screen_rect.right - 20 # score'u sağ üst köşeye yerleştiriyoruz.
        self.score_rect.top = 20 # score'u sağ üst köşeye yerleştiriyoruz.

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect) # score'u ekrana yazdırıyoruz.
        # bu method score_rect in belirlediği koordinatlarda score_image'ı ekrana yazdırır.
   