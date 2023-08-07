import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        # screen part
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN) 
        #(self.settings.screen_width,self.settings.screen_height)
        # kısıtlı ekran boyutu sağlar fullscreen ile tam ekran olur.
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)
        
        # bullet part
        self.bullets = pygame.sprite.Group()
        
        # alien part
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        # self.screen = pygame.display.set_mode((1200,700))
        # 1200x700 boyutunda bir ekran oluşturur.
        pygame.display.set_caption("Alien Invasion")
        # Set the background color.
        self.bg_color = (255,255,255)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()      
            

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()

            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
    

    def _check_keydown_events(self,event):
        """Respond to keypresses."""
        if event.key ==pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right=True

        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left=True

        elif event.key ==pygame.K_q:
            sys.exit()
        
        elif event.key ==pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
        """Respond to key releases."""
        if event.key ==pygame.K_RIGHT:
            self.ship.moving_right=False
        
        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left=False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy(): 
            if bullet.rect.bottom <= 0: 
                self.bullets.remove(bullet)
        #print(len(self.bullets)) 
        #bullets içindeki mermi sayısını ekrana yazdırır.


    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()


    def _create_fleet(self):
        """create the fleet of aliens.""" 
        # Make an alien.// oluşturuken hem yukardan hem soldan alien widht kadar boşluk bırakıyoruz
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        # sağdan ve soldan 1 alien width kadar boşluk bırakıyoruz
        available_space_x = self.settings.screen_width - (2*alien_width) 

        # 2*alien_width kadar boşluk bırakarak kaç tane alien sığacağını hesaplıyoruz
        number_aliens_x = available_space_x // (2*alien_width) 

        # Determine the number of rows of aliens that fit on the screen.
        # kaç tane alien sığacağını hesaplıyoruz
        ship_height = self.ship.rect.height
        # yukardan 1 alien height kadar boşluk bırakıyoruz
        available_space_y = (self.settings.screen_height - (2*alien_height) - ship_height)
         # 3*alien_height idi ekranı doldurmak için değiştirebilirsiniz

        # 2*alien_height kadar boşluk bırakarak kaç tane alien sığacağını hesaplıyoruz
        number_rows = available_space_y // (alien_height) 
        # 2 *alien_height idi ekranı doldurmak için değiştirebilirsiniz

        # Create all row of aliens. // tüm satırları oluşturuyoruz
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): # her bir satırda kaç tane alien varsa o kadar oluşturuyoruz
                self._create_alien(alien_number,row_number)
   
         
    def _create_alien(self,alien_number,row_number): # alien number o anki alienın numarası
        """create an alien and place it in the row."""
        # Create an alien and place it in the row. 
        # her bir alienı oluşturuyoruz
        alien = Alien(self)
        
        # bu nitelik bir rect nesnesinin genişliğini ve yüksekliğini bir demet olarak döndürür
        alien_width, alien_height = alien.rect.size 
        
        # her bir alienın x koordinatını hesaplıyoruz
        alien.x = alien_width + 2*alien_width*alien_number 
        
        # her bir alienın x koordinatını güncelliyoruz
        alien.rect.x = alien.x
        
        # her bir alienın y koordinatını hesaplıyoruz
        alien.rect.y = alien_height + 2*alien.rect.height*row_number 
        
        # oluşturulan her bir alienı aliens grubuna ekliyoruz
        self.aliens.add(alien) 

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites(): 
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
       
        # Make the most recently drawn screen visible.
        # En son çizilen ekranı görünür hale getirin.
        pygame.display.flip()

        # bullets.sprites() methodu ile bullets içindeki
        # bütün hareketli öğe grafiklerinin bir listesini döndürür.
        # ateşlenmiş bütün mermileri ekrana çizdirmek için bullets deki
        # hareketli öğe grafikleri üzerinden döngü kuruyoruz
        # ve her bir hareketli öğe grafiği üzerinde draw_bullet() methodunu çağırıyoruz.
        


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()