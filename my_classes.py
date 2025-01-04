# Meng-import library dan module yg digunakan
import math
import pygame # Versi 2.5.2
from pygame.font import Font
from pygame.sprite import Sprite
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button, ButtonArray
from pygame_widgets.slider import Slider

# Menginisialisasi mixer dan me-load sound
pygame.mixer.init()
collision_sound = pygame.mixer.Sound(r"assets\sounds\bounce.mpeg")
collision_sound.set_volume(1.0)

class Ball(Sprite):
    """
    Class Ball merupakan subclass dari Sprite yang merepresentasikan bola dalam game fisika.

    Args:
        img (str): Path ke file gambar bola.
        pos (tuple): Posisi awal bola dalam format (x, y).
        massa (float): Massa bola.
        x_speed (float): Kecepatan awal bola dalam sumbu x.
        y_speed (float): Kecepatan awal bola dalam sumbu y.

    Attributes:
        pos (tuple): Posisi bola dalam format (x, y).
        image (Surface): Objek Surface yang berisi gambar bola.
        rect (Rect): Objek Rect yang berisi posisi dan ukuran bola.
        mask (Mask): Objek Mask yang berisi mask dari gambar bola.
        _massa (float): Massa bola.
        _x_speed (float): Kecepatan bola dalam sumbu x.
        _y_speed (float): Kecepatan bola dalam sumbu y.
    """
    def __init__(self, img, pos:tuple, massa:float, x_speed:float, y_speed:float):
        super().__init__()
        # Posisi
        self.pos = pos

        original_img = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale_by(original_img, 3)
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.mask = pygame.mask.from_surface(self.image)

        # Massa 
        self._massa = massa

        # Kecepatan (actual speed)
        self._x_speed = x_speed * 10
        self._y_speed = y_speed * 10

    @property
    def massa(self):
        return self._massa
    
    @massa.setter
    def massa(self, value):
        self._massa = value

    @property
    def xpos(self):
        return ((self.rect.centerx-525/2)) / 10
    
    @property
    def ypos(self):
        return ((self.rect.centery-480/2)) / -10

    @property
    def x_speed(self):
        return self._x_speed
    
    @x_speed.setter
    def x_speed(self, value):
        self._x_speed = value

    @property
    def y_speed(self):
        return self._y_speed
    
    @y_speed.setter
    def y_speed(self, value):
        self._y_speed = value

    @property
    def x_speed_display(self):
        return round(self.x_speed/10, 2)

    @property
    def y_speed_display(self):
        return round((self.y_speed*-1) / 10, 2)

    @property
    def momentum(self):
        v = math.sqrt(self.x_speed_display**2 + self.y_speed_display**2)
        return round(self.massa * v, 2)

    @property
    def energy(self):
        return round(0.5 * self.massa * (self.x_speed_display**2 + self.y_speed_display**2), 2)

    def update(self, area, e_border):
        """"
        Metode untuk memperbarui posisi bola berdasarkan kecepatannya dan menangani tabrakan dengan dinding area.

        Args:
            area (Rect): Objek Rect yang merepresentasikan area permainan.
        """
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.right > area.right:
            collision_sound.play()
            self.rect.right = area.right
            self.x_speed *= -e_border

        if self.rect.left < area.left:
            collision_sound.play()
            self.rect.left = area.left
            self.x_speed *= -e_border

        if self.rect.bottom > area.bottom:
            collision_sound.play()
            self.rect.bottom = area.bottom
            self.y_speed *= -e_border

        if self.rect.top < area.top:
            collision_sound.play()
            self.rect.top = area.top
            self.y_speed *= -e_border

    def collision_with_ball(self, bola2, e_ball):
        """
        Metode untuk menangani tabrakan antara bola ini dan bola lain.

        Args:
            bola2 (Sprite): Bola lain yang mungkin bertabrakan dengan bola ini.
            e_ball (float): Koefisien restitusi tabrakan antara dua bola.
        """
        if pygame.sprite.spritecollide(self.sprite, bola2, False):
            if pygame.sprite.spritecollide(self.sprite, bola2, False, pygame.sprite.collide_mask):
                collision_sound.play()
                self.sprite.speed_after_collision(bola2.sprite, e_ball)
                
                overlap = True
                while overlap:
                    self.sprite.rect.x += self.sprite.x_speed
                    self.sprite.rect.y += self.sprite.y_speed
                    bola2.sprite.rect.x += bola2.sprite.x_speed
                    bola2.sprite.rect.y += bola2.sprite.y_speed

                    if not pygame.sprite.spritecollide(self.sprite, bola2, False, pygame.sprite.collide_mask):
                        overlap = False

    def speed_after_collision(self, bola2, e_ball):
        """
        Metode untuk menghitung kecepatan bola setelah tabrakan berdasarkan hukum kekekalan momentum dan energi kinetik.

        Args:
            bola2 (Sprite): Bola lain yang bertabrakan dengan bola ini.
            e_ball (float): Koefisien restitusi tabrakan antara dua bola.
        """
        vx1_before = self.x_speed
        vx2_before = bola2.x_speed
        vy1_before = self.y_speed
        vy2_before = bola2.y_speed
        self.x_speed = ((self.massa-bola2.massa)*vx1_before + (1+e_ball)*bola2.massa*vx2_before)/(self.massa+bola2.massa)
        bola2.x_speed = ((bola2.massa-self.massa)*vx2_before + (1+e_ball)*self.massa*vx1_before)/(self.massa+bola2.massa)
        self.y_speed = ((self.massa-bola2.massa)*vy1_before + (1+e_ball)*bola2.massa*vy2_before)/(self.massa+bola2.massa)
        bola2.y_speed = ((bola2.massa-self.massa)*vy2_before + (1+e_ball)*self.massa*vy1_before)/(self.massa+bola2.massa)
        

class MyFont(Font):
    """
    Kelas MyFont merupakan subclass dari Font yang menyesuaikan perilaku metode render.
    """
    
    def render(self, text, color="black"):
        """
        Metode untuk merender teks dengan antialiasing dan warna yang bisa disesuaikan.

        Args:
            text (str): Teks yang akan dirender.
            color (str, optional): Warna teks. Default adalah "black".
        """
        return super().render(text, True, color)
    

class MyTextBox(TextBox):
    """
    Kelas MyTextBox merupakan subclass dari TextBox dengan ukuran dan atribut default yang telah disesuaikan.
    """

    def __init__(self, win, x, y, width=30, height=18):
        """
        Konstruktor untuk kelas MyTextBox.

        Args:
            win: Window tempat TextBox ditempatkan.
            x (int): Koordinat x TextBox.
            y (int): Koordinat y TextBox.
            width (int, optional): Lebar TextBox. Default adalah 30.
            height (int, optional): Tinggi TextBox. Default adalah 18.
        """
        super().__init__(win=win, x=x, y=y, width=width, height=height, fontSize=12, borderThickness=1)


class MySlider(Slider):
    """
    Kelas MySlider merupakan subclass dari Slider dengan ukuran default yang telah disesuaikan.
    """

    def __init__(self, win, x, y, **kwargs):
        """
        Konstruktor untuk kelas MySlider.

        Args:
            win: Window tempat Slider ditempatkan.
            x (int): Koordinat x Slider.
            y (int): Koordinat y Slider.
            **kwargs: Argumen tambahan untuk kelas Slider.
        """
        super().__init__(win=win, x=x, y=y, width=180, height=10, **kwargs)


class MyButton(Button):
    """
    Kelas MyButton merupakan subclass dari Button dengan warna dan ukuran default yang telah disesuaikan.
    """

    def __init__(self, win, x, y, width, height, **kwargs):
        """
        Konstruktor untuk kelas MyButton.

        Args:
            win: Window tempat Button ditempatkan.
            x (int): Koordinat x Button.
            y (int): Koordinat y Button.
            width (int): Lebar Button.
            height (int): Tinggi Button.
            **kwargs: Argumen tambahan untuk kelas Button.
        """
        super().__init__(
            win=win, x=x, 
            y=y, width=width, 
            height=height, 
            **kwargs, 
            colour=(134, 152, 255), 
            hoverColour=(184, 202, 255), 
            pressedColour=(84, 102, 205), 
            textColour="white",
            borderColour="darkslateblue",
            borderThickness=2)
        
        self.font = kwargs.get('font', pygame.font.Font(r"assets\fonts\pixeloid_bold.ttf", self.fontSize))
        self.text = self.font.render(self.string, True, self.textColour)

        self.inactiveBorderColour = kwargs.get('inactiveBorderColour', "darkslateblue")
        self.hoverBorderColour = kwargs.get('hoverBorderColour', "darkslateblue")
        self.pressedBorderColour = kwargs.get('pressedBorderColour', "darkslateblue")
        self.borderColour = kwargs.get('borderColour', self.inactiveBorderColour)
        self.inactiveBorderColour = self.borderColour

    
    def set_properties(self, x, y, width, height):
        """
        Metode untuk mengatur posisi dan ukuran Button.

        Args:
            x (int): Koordinat x Button.
            y (int): Koordinat y Button.
            width (int): Lebar Button.
            height (int): Tinggi Button.
        """
        self.setX(x)
        self.setY(y)
        self.setWidth(width)
        self.setHeight(height)


class MyButtonArray(ButtonArray):
    """
    Kelas MyButtonArray merupakan subclass dari ButtonArray dengan konfigurasi tombol yang telah disesuaikan.
    """

    def __init__(self, win, x, y, onClicks, **kwargs):
        """
        Konstruktor untuk kelas MyButtonArray.

        Args:
            win: Window tempat ButtonArray ditempatkan.
            x (int): Koordinat x ButtonArray.
            y (int): Koordinat y ButtonArray.
            onClicks: Fungsi yang akan dipanggil saat tombol ditekan.
        """
        super().__init__(
            win=win, 
            x=x, 
            y=y, 
            width=150, 
            height=200, 
            shape=(3, 6),
            colour=(230, 227, 220),
            separationThickness=2,
            borderRadius=4,
            texts=(
                '7', '4', '1', '0', '.', 'Enter', 
                '8', '5', '2', '', '', '',
                '9', '6', '3', '+/-', '←', ''
                ),
            onClicks=onClicks,)
        
        for button in self.buttons:
            button.inactiveColour = (134, 152, 255)
            button.hoverColour = (184, 202, 255) 
            button.pressedColour = (84, 102, 205)
            button.borderThickness=0

        self.buttons[9].hide()
        self.buttons[10].hide()
        self.buttons[11].hide()
        self.buttons[-1].hide()
        self.buttons[3].setWidth(86)
        self.buttons[5].setWidth(130)

    def createButtons(self):
        """
        Metode untuk membuat button-button di dalam buttonarray.
        """
        across, down = self.shape
        width = (self._width - self.separationThickness * (across - 1) - self.leftBorder - self.rightBorder) // across
        height = (self._height - self.separationThickness * (down - 1) - self.topBorder - self.bottomBorder) // down

        count = 0
        for i in range(across):
            for j in range(down):
                x = self._x + i * (width + self.separationThickness) + self.leftBorder
                y = self._y + j * (height + self.separationThickness) + self.topBorder
                self.buttons.append(MyButton(self.win, x, y, width, height, isSubWidget=True,
                                           **{k: v[count] for k, v in self.buttonAttributes.items() if v is not None})
                                    )
                count += 1

    def draw(self):
        """
        Metode untuk menampilkan ButtonArray ke permukaan.
        """
        if not self._hidden:
            FONT_KETERANGAN = MyFont(r"assets\fonts\pixeloid_sans.ttf", 11)
            text_input_value = FONT_KETERANGAN.render("-2 s.d. 2 m/s")
            rects = [

                (self._x + self.borderRadius, self._y, self._width - self.borderRadius * 2, self._height),
                (self._x, self._y + self.borderRadius, self._width, self._height - self.borderRadius * 2)
            ]

            circles = [
                (self._x + self.borderRadius, self._y + self.borderRadius),
                (self._x + self.borderRadius, self._y + self._height - self.borderRadius),
                (self._x + self._width - self.borderRadius, self._y + self.borderRadius),
                (self._x + self._width - self.borderRadius, self._y + self._height - self.borderRadius)
            ]
            
            pygame.draw.rect(self.win, self.colour, (self._x, self._y - 38, 150, 238), border_radius=self.borderRadius)

            for rect in rects:
                pygame.draw.rect(self.win, self.colour, rect)

            for circle in circles:
                pygame.draw.circle(self.win, self.colour, circle, self.borderRadius)

            for button in self.buttons:
                button.draw()
            
            pygame.draw.rect(self.win, "black", (self._x, self._y - 38, 150, 238), width=1, border_radius=self.borderRadius)
            self.win.blit(text_input_value, (text_input_value.get_rect(center=(400, 175))))