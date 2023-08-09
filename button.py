import pygame.font

class Button:

    def __init__(self, ai_game , msg):
        """ Initialize button attributes. """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width , self.height = 200 , 50
        self.button_color = (0, 255, 0)
        self.text_color = (255 , 255 , 255)
        self.font = pygame.font.SysFont(None , 48) # None = default font , 48 = font size

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0 , 0 , self.width , self.height) 
        # 0,0 = top left corner of the button butonun merkezi ile ekranın merkezini eşitler.
        self.rect.center = self.screen_rect.center 

        # The button message needs to be prepped only once.
        # düğmenin mesajı sadece bir kez hazırlanmalıdır.
        self._prep_msg(msg)

    
    def _prep_msg(self , msg):
        """ Turn msg into a rendered image and center text on the button. """
        # render() metodu msgde saklı bir metin dizesini görüntüye dönüştürür.
        self.msg_image = self.font.render(msg , True , self.text_color , self.button_color) # True = antialiasing, bozulmayı önler.
        # arka plan rengini dahil etmezsek pygame varsayılan olarak şeffaf bir arka plan oluşturur.
        self.msg_image_rect = self.msg_image.get_rect() # mesaj görüntüsünün dikdörtgenini alır.ve mesajın konumunu düğmenin konumuna eşitler.(merkezelerini eşitler.) 
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        """ Draw blank button and then draw message. """
        self.screen.fill(self.button_color , self.rect) # fill() metodu dikdörtgeni renklendirir.
        self.screen.blit(self.msg_image , self.msg_image_rect) # blit() metodu metin resmini ekrana çizdirir
        # blit() metodu iki argüman alır: kopyalanacak görüntü ve kopyalanacak görüntünün sol üst köşesinin koordinatları.
        # msg_image = kopyalanacak görüntü , msg_image_rect = kopyalanacak görüntünün sol üst köşesinin koordinatları.
        