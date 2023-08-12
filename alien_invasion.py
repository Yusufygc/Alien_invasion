import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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
        # self.screen = pygame.display.set_mode((1200,700))
        # 1200x700 boyutunda bir ekran oluşturur.
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        # create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self) # create a scoreboard to store game statistics.
        self.ship = Ship(self)
        
        # bullet part
        self.bullets = pygame.sprite.Group()
        
        # alien part
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        # Set the background color.
        self.bg_color = (255,255,255)


        # Make the Play button.
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
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

            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    

    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score() # score reset

            # reset game settings.
            self.settings.initialize_dynamic_settings() # oyun ayarlarını sıfırlar.


            # Get rid of any remaining aliens and bullets.
            # Kalan uzaylılardan ve mermilerden kurtulun.
            self.aliens.empty() 
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


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
        self._check_bullet_alien_collisions()

        
    def _check_bullet_alien_collisions(self):# çarpışma kontrolü

        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        # collisions sözlük oluşturur
        # True True yazmamızın sebebi çarpışan mermi ve uzaylıyı silmek
        # ilk True mermi için ikinci True uzaylı için
        # ilk ture yu false yaparsak mermi çarpıştıktan sonra yok olmaz
        # yani güçlü mermi olur ekrandan yukarı çıkana kadar çarpışmaya devam edersonra silinir

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            # her bir çarpışma için puan ekler
            self.sb.prep_score()
            self.sb.check_high_score()
          

        # yeni filo oluşturmak için
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect() 
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                # uzaylılar ekranın altına ulaşırsa gemiye çarpmış gibi davranır.
                self._ship_hit() 
                break


    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        # Check if the fleet is at an edge, then 
        # update the positions of all aliens in the fleet.
        # filonun kenarda olup olmadığını kontrol eder, 
        # ardından filonun tüm uzaylılarının pozisyonlarını güncelle.
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        # uzaylı-gemi çarpışmaları için
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            # fonksiyon harektli öğe ve grup arasında çarpışma olup olmadığını kontrol eder
            # çarpışma varsa çarpışan uzaylıyı döndürür yoksa None döndürür
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        # ekranın altına ulaşan uzaylıları kontrol eder
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement ships_left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True) # oyun bittiğinde mouse görünür olur


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


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        # herhangi bir uzaylı kenara ulaştıysa uygun şekilde yanıt verin. 
        for alien in self.aliens.sprites(): 
            if alien.check_edges(): 
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        # Bütün filoyu düşürün(yani alt satıra) ve filonun yönünü değiştirin.
        for alien in self.aliens.sprites(): 
            alien.rect.y += self.settings.fleet_drop_speed 
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
       
        for bullet in self.bullets.sprites(): 
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
    
        # bullets.sprites() methodu ile bullets içindeki
        # bütün hareketli öğe grafiklerinin bir listesini döndürür.
        # ateşlenmiş bütün mermileri ekrana çizdirmek için bullets deki
        # hareketli öğe grafikleri üzerinden döngü kuruyoruz
        # ve her bir hareketli öğe grafiği üzerinde draw_bullet() methodunu çağırıyoruz.

        self.sb.show_score()
        
        # oyun aktif değilse play butonunu çizdiriyoruz
        if not self.stats.game_active: 
            self.play_button.draw_button()
                 
        # Make the most recently drawn screen visible.
        # En son çizilen ekranı görünür hale getirin.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()