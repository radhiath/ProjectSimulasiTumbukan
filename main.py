# Meng-import library dan module yg digunakan
import random
import pygame # Versi 2.5.2
import pygame_widgets # Versi 1.1.1
import functions as func
from my_classes import Ball, MyFont, MyTextBox, MyButton, MySlider, MyButtonArray

# Fungsi-fungsi untuk mengontrol tombol utama
def to_1d():
    """
    Fungsi untuk kembali ke mode 1 dimensi
    """
    global mode
    mode = 1 # Pindah ke mode 0

    # Mengubah properties button-button dengan method .set_properties()
    button_1d.set_properties(535, 480, 125, 75)
    button_2d.set_properties(670, 480, 125, 75)
    back_button.set_properties(535, 560, 260, 35)

    # Mengatur button untuk di-show/hide
    back_button.show()
    quit_button.hide()
    button_1d.disable()
    button_2d.enable()
    pause_button.show()

    pygame.mixer.music.stop()

def to_2d():
    """
    Fungsi untuk kembali ke mode 2 dimensi
    """
    global mode
    mode = 2 # Pindah ke mode 2

    # Mengubah properties button-button dengan method .set_properties()
    button_1d.set_properties(535, 480, 125, 75)
    button_2d.set_properties(670, 480, 125, 75)
    back_button.set_properties(535, 560, 260, 35)

    # Mengatur button untuk di-show/hide
    back_button.show()
    quit_button.hide()
    button_2d.disable()
    button_1d.enable()
    pause_button.show()

    pygame.mixer.music.stop()

def back_to_main():
    """
    Fungsi untuk kembali ke mode 1 dimensi
    """
    global mode
    mode = 0 # Pindah ke mode 0

    # Mengubah properties button-button dengan method .set_properties()
    button_1d.set_properties(150, 250, 150, 70)
    button_2d.set_properties(150, 330, 150, 70)

    # Mengatur button untuk di-show/hide
    back_button.hide()
    button_1d.enable()
    button_2d.enable()

    pygame.mixer.music.play(-1, 0.0, 5000)

def keluar():
    """
    Fungsi untuk keluar dari program
    """
    pygame.quit() # Keluar dari program

def pause():
    """
    Fungsi untuk mem-pause program
    """
    global paused
    paused = not paused # Mengatur paused sebagai kebalikannya

    # Mengatur button untuk di-show/hide
    pause_button.hide()
    play_button.show()

def unpause():
    """
    Fungsi untuk menjalankan kembali program
    """
    global paused
    paused = not paused # Mengatur paused sebagai kebalikannya

    # Mengatur button untuk di-show/hide    
    play_button.hide()
    pause_button.show()

# Fungsi-fungsi untuk mengatur window input dari user
def number(text):
    """
    Fungsi untuk mengetikkan karakter (angka)
    """
    dummy_textbox.setText(dummy_textbox.getText() + text)

def backspace():
    """
    Fungsi untuk menghapus karakter (angka)
    """
    dummy_textbox.setText(dummy_textbox.getText()[:-1])

def neg_or_pos():
    """
    Fungsi untuk mengubah angka menjadi positif atau negatif
    """
    value = dummy_textbox.getText() 
    if "-" in value:
        value = value.replace("-", "")
    else:
        value = "-" + value
    dummy_textbox.setText(value)

def enter(tb_input, objek, axis):
    """
    Fungsi untuk men-submit input dari user
    """
    global paused

    # Mengonversi input berupa string dari user menjadi float
    acceptable_char = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "", "-", "."]
    value = dummy_textbox.getText()

    # Cek apakah value kosong
    if value == "":
        # lakukan sesuatu
        value = tb_input.getText()

    # Cek apakah value hanya berisi titik
    elif value == ".":
        # lakukan sesuatu
        value = tb_input.getText()

    # Cek apakah value berisi lebih dari satu titik
    elif value.count(".") > 1:
        # lakukan sesuatu
        value = tb_input.getText()

    # Cek apakah semua karakter dalam value ada dalam acceptable_char
    elif not all(char in acceptable_char for char in value):
        # lakukan sesuatu
        value = tb_input.getText()

    v = float(value) * 10

    if v > 20:
        v = 20.0
    elif v < -20:
        v = -20.0
        
    if axis.lower() == "x":
        objek.x_speed = v
    elif axis.lower() == "y":
        objek.y_speed = v
    dummy_textbox.setText("")

    paused = not paused # Mengatur paused sebagai kebalikannya

    # Mengatur properties dari window input
    dummy_textbox.hide()
    speed_input.hide()
    tb_input.selected = not tb_input.selected

# ==================== PROGRAM UTAMA ====================
# Melakukan pre-inisialisasi dan inisialisasi untuk mixer
pygame.mixer.pre_init()
pygame.mixer.init()

# Menginisialisasi Pygame dan mengatur windownya
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SIMULASI TUMBUKAN LENTING") # Men-set caption window
icon = pygame.image.load(r"assets\images\bola_merah.png").convert_alpha()
pygame.display.set_icon(icon) # Men-set icon window

# Me-load gambar untuk main menu
main_menu_img = pygame.image.load(r"assets\images\main_menu.png")

# Mendeklarasikan dan mendefinisikan clock dari class Clock untuk mengatur FPS
clock = pygame.time.Clock()

# Mendeklarasikan dan mendefinisikan warna-warna menggunakan dictionary
COLORS = {
    "birutombol": (134, 152, 255), 
    "biruhover": (184, 202, 255), 
    "birupressed": (84, 102, 205), 
    "putihtulang": (230, 227, 220), 
    "mymerah": (204, 0, 51), 
    "myabu": (104, 123, 137), 
    "mypink": (255, 140, 197), 
    "myorange": (255, 197, 141),
    "pinkbg": (235, 206, 218)}

# Mendeklarasikan dan mendefinisikan font dari class MyFont untuk tampilan teks
FONT_MAIN_MENU = MyFont(r"assets\fonts\pixeloid_bold.ttf", 34)
FONT_JUDUL = MyFont(r"assets\fonts\pixeloid_bold.ttf", 32)
FONT_KETERANGAN = MyFont(r"assets\fonts\pixeloid_sans.ttf", 11)

# Me-render teks berdasarkan font di atas untuk digunakan di layar
# Me-render teks untuk main menu
title1 = FONT_MAIN_MENU.render("SIMULASI", "white")
title2 = FONT_MAIN_MENU.render("TUMBUKAN LENTING", "white")

# Me-render teks untuk judul simulasi 1 dimensi dan 2 dimensi
judul_1d = FONT_JUDUL.render("SIMULASI 1 DIMENSI", "darkslateblue")
judul_2d = FONT_JUDUL.render("SIMULASI 2 DIMENSI", "darkslateblue")

# Me-render teks untuk kotak input
text1 = FONT_KETERANGAN.render("Reflektivitas Border:")
text2 = FONT_KETERANGAN.render("Koefisien Restitusi Bola:")
text3 = FONT_KETERANGAN.render("Massa Bola 1:")
text4 = FONT_KETERANGAN.render("Massa Bola 2:")
text5 = FONT_KETERANGAN.render("Kecepatan Bola 1 di sb. x:")
text6 = FONT_KETERANGAN.render("Kecepatan Bola 1 di sb. y:")
text7 = FONT_KETERANGAN.render("Kecepatan Bola 2 di sb. x:")
text8 = FONT_KETERANGAN.render("Kecepatan Bola 2 di sb. y:")

# Me-render teks untuk kotak output
text9 = FONT_KETERANGAN.render("x")
text10 = FONT_KETERANGAN.render("y")
text11 = FONT_KETERANGAN.render("m")
text12 = FONT_KETERANGAN.render("vx")
text13 = FONT_KETERANGAN.render("vy")
text14 = FONT_KETERANGAN.render("|P|")
text15 = FONT_KETERANGAN.render("Ek")
text16 = FONT_KETERANGAN.render("(kg)")
text17 = FONT_KETERANGAN.render("(m/s)")
text18 = FONT_KETERANGAN.render("(m/s)")
text19 = FONT_KETERANGAN.render("(kg m/s)")
text20 = FONT_KETERANGAN.render("(J)")
text21 = FONT_KETERANGAN.render("Kecepatan Bola 1:")
text22 = FONT_KETERANGAN.render("Kecepatan Bola 2:")
text23 = FONT_KETERANGAN.render("v")

# Menggabungkan text-text di atas sebagai tuple
# Tuple teks untuk main menu
TEXTS_TO_BLIT_MENU = (title1, title2)

# Tuple teks untuk layar simulasi 1 dimensi
TEXTS_TO_BLIT_1D = (
    judul_1d, text1, text2, text3, text4, text21, text22, 
    text9, text10, text11, text23, text14, text15, text16, 
    text17, text19, text20)

# Tuple teks untuk layar simulasi 2 dimensi
TEXTS_TO_BLIT_2D = (
    judul_2d, text1, text2, text3, text4, text5, text6,
    text7, text8, text9, text10, text11, text12, text13, 
    text14, text15, text16, text17, text18, text19, text20)

# Mendeklarasikan dan mendefinisikan koordinat teks untuk di-blit pada layar
# Koordinat teks untuk main menu
coor_texts_menu = (title1.get_rect(center=(225, 160)), title2.get_rect(center=(225, 210)))

# Koordinat teks untuk layar simulasi 1 dimensi
coor_texts_1d = (
    (191, 10), (550, 70), (550, 116), (550, 229), (550, 274),
    (550, 319), (550, 364), (58, 499), (142, 499), (225, 493),
    (310, 493), (392, 493), (475, 493), (219, 505), (298, 505),
    (374, 505), (475, 505))

# Koordinat teks untuk layar simulasi 2 dimensi
coor_texts_2d = (
    (191, 10), (550, 70), (550, 116), (550, 184), (550, 229),
    (550, 274), (550, 319), (550, 364), (550, 409), (52, 499),
    (123, 499), (193, 493), (262, 493), (333, 493), (405, 493), 
    (475, 493), (187, 505), (253, 505), (324, 505), (387, 505), 
    (475, 505))

# Mengisialisasi objek tombol menggunakan class MyButton dari module "my_classes.py"
play_button_img = pygame.image.load(r"assets\images\play_button.png")  # Gambar untuk tombol mainkan
pause_button_img = pygame.image.load(r"assets\images\pause_button.png")  # Gambar untuk tombol jeda

# Tombol untuk main menu
button_1d = MyButton(SCREEN, 150, 250, 150, 70, text="1D", onClick=to_1d, radius=12)  # Tombol untuk pindah ke mode 1 dimensi
button_2d = MyButton(SCREEN, 150, 330, 150, 70, text="2D", onClick=to_2d, radius=12)  # Tombol untuk pindah ke mode 2 dimensi
quit_button = MyButton(SCREEN, 150, 410, 150, 70, text="QUIT", onClick=keluar, radius=12)  # Tombol untuk keluar dari program
back_button = MyButton(SCREEN, 10, 10, 80, 40, text="Back", onClick=back_to_main, radius=12)  # Tombol untuk kembali ke menu utama

# Tombol kontrol untuk mode simulasi
play_button = MyButton(SCREEN, 247, 425, 31, 31, image=play_button_img, radius=4, onClick=unpause)  # Tombol untuk melanjutkan simulasi
play_button.hide()
pause_button = MyButton(SCREEN, 247, 425, 31, 31, image=pause_button_img, radius=4, onClick=pause)  # Tombol untuk menghentikan simulasi

# Mengisialisasi objek slider menggunakan class MySlider dari module "my_classes.py"
# Menginisialisasi slider (mode 1 dimensi)
slider1d_e_border = MySlider(SCREEN, 595, 92, min=0.01, max=1, step=0.01, initial=1)  # Slider untuk reflektivitas border
slider1d_e_ball = MySlider(SCREEN, 595, 137, min=0.01, max=1, step=0.01, initial=1)  # Slider untuk koefisien restitusi bola
slider1d_massa1 = MySlider(SCREEN, 595, 251, min=0.1, max=3, step=0.1, initial=3, handleColour=COLORS["mymerah"])  # Slider untuk massa bola 1
slider1d_massa2 = MySlider(SCREEN, 595, 296, min=0.1, max=3, step=0.1, initial=2, handleColour=COLORS["myabu"])  # Slider untuk massa bola 2
SLIDERS_1D = (slider1d_e_border, slider1d_e_ball, slider1d_massa1, slider1d_massa2)  # Tuple slider-mode 1 dimensi

# Mengisialisasi slider (mode 2 dimensi)
slider2d_e_border = MySlider(SCREEN, 595, 92, min=0.01, max=1, step=0.01, initial=1)  # Slider untuk reflektivitas border
slider2d_e_ball = MySlider(SCREEN, 595, 137, min=0.01, max=1, step=0.01, initial=1)  # Slider untuk koefisien restitusi bola
slider2d_massa1 = MySlider(SCREEN, 595, 206, min=0.01, max=3, step=0.1, initial=0.5, handleColour=COLORS["myorange"])  # Slider untuk massa bola 1
slider2d_massa2 = MySlider(SCREEN, 595, 251, min=0.01, max=3, step=0.1, initial=1.5, handleColour=COLORS["mypink"])  # Slider untuk massa bola 2
SLIDERS_2D = (slider2d_e_border, slider2d_e_ball, slider2d_massa1, slider2d_massa2)  # Tuple slider-mode 2 dimensi

# Mengisialisasi objek textbox menggunakan class MyTextBox dari module "my_classes.py"
# Menginisialisasi textbox input untuk mode 1 dimensi
input1d_e_border = MyTextBox(SCREEN, 550, 86)  # TextBox untuk reflektivitas border
input1d_e_ball = MyTextBox(SCREEN, 550, 131)  # TextBox untuk koefisien restitusi bola
input1d_massa1 = MyTextBox(SCREEN, 550, 245)  # TextBox untuk massa bola 1
input1d_massa2 = MyTextBox(SCREEN, 550, 290)  # TextBox untuk massa bola 2
input1d_v1 = MyTextBox(SCREEN, 550, 335, 100)  # TextBox untuk kecepatan bola 1
input1d_v2 = MyTextBox(SCREEN, 550, 380, 100)  # TextBox untuk kecepatan bola 2
INPUT_TEXTBOXES_1D = (input1d_e_border, input1d_e_ball, input1d_massa1, input1d_massa2)  # Tuple input textbox-mode 1 dimensi

# Menginisialisasi textbox output untuk mode 1 dimensi (bola 1)
output1d_xpos1 = MyTextBox(SCREEN, 47, 525) # Textbox untuk posisi bola 1 di sb. x
output1d_ypos1 = MyTextBox(SCREEN, 131, 525) # Textbox untuk posisi bola 1 di sb. y
output1d_massa1 = MyTextBox(SCREEN, 215, 525) # Textbox untuk massa bola 1
output1d_v1 = MyTextBox(SCREEN, 299, 525) # TextBox untuk kecepatan bola 1
output1d_momentum1 = MyTextBox(SCREEN, 383, 525) # Textbox untuk momentum bola 1
output1d_energi1 = MyTextBox(SCREEN, 467, 525) # Textbox untuk energi kinetik bola 1

# Menginisialisasi textbox output untuk mode 1 dimensi (bola 2)
output1d_xpos2 = MyTextBox(SCREEN, 47, 560) # Textbox untuk posisi bola 2 di sb. x
output1d_ypos2 = MyTextBox(SCREEN, 131, 560) # Textbox untuk posisi bola 2 di sb. y
output1d_massa2 = MyTextBox(SCREEN, 215, 560) # Textbox untuk massa bola 2
output1d_v2 = MyTextBox(SCREEN, 299, 560) # TextBox untuk kecepatan bola 2
output1d_momentum2 = MyTextBox(SCREEN, 383, 560) # Textbox untuk momentum bola 2
output1d_energi2 = MyTextBox(SCREEN, 467, 560) # Textbox untuk energi kinetik bola 2
OUTPUT_TEXTBOXES_1D = (
    output1d_xpos1, output1d_ypos1, output1d_massa1, output1d_v1,
    output1d_momentum1, output1d_energi1, output1d_xpos2, output1d_ypos2, 
    output1d_massa2, output1d_v2, output1d_momentum2, output1d_energi2) # Tuple output textbox-mode 1 dimensi

# Menginisialisasi textbox input untuk mode 2 dimensi
input2d_e_border = MyTextBox(SCREEN, 550, 86) # TextBox untuk reflektivitas border
input2d_e_ball = MyTextBox(SCREEN, 550, 131) # TextBox untuk koefisien restitusi bola
input2d_massa1 = MyTextBox(SCREEN, 550, 200) # TextBox untuk massa bola 1
input2d_massa2 = MyTextBox(SCREEN, 550, 245) # TextBox untuk massa bola 2
input2d_vx1 = MyTextBox(SCREEN, 550, 290, 100) # TextBox untuk kecepatan di sb. x bola 1
input2d_vy1 = MyTextBox(SCREEN, 550, 335, 100) # TextBox untuk kecepatan di sb. y bola 1
input2d_vx2 = MyTextBox(SCREEN, 550, 380, 100) # TextBox untuk kecepatan di sb. x bola 2
input2d_vy2 = MyTextBox(SCREEN, 550, 425, 100) # TextBox untuk kecepatan di sb. y bola 2
INPUT_TEXTBOXES_2D = (input2d_e_border, input2d_e_ball, input2d_massa1, input2d_massa2) # Tuple input textbox-mode 2 dimensi

output2d_xpos1 = MyTextBox(SCREEN, 41, 525) # Textbox untuk posisi bola 1 di sb. x
output2d_ypos1 = MyTextBox(SCREEN, 112, 525) # Textbox untuk posisi bola 1 di sb. y
output2d_massa1 = MyTextBox(SCREEN, 183, 525) # Textbox untuk massa bola 1
output2d_vx1 = MyTextBox(SCREEN, 254, 525) # TextBox untuk kecepatan di sb. x bola 1
output2d_vy1 = MyTextBox(SCREEN, 325, 525) # TextBox untuk kecepatan di sb. y bola 1
output2d_momentum1 = MyTextBox(SCREEN, 396, 525) # Textbox untuk momentum bola 1
output2d_energi1 = MyTextBox(SCREEN, 467, 525) # Textbox untuk energi kinetik bola 1

output2d_xpos2 = MyTextBox(SCREEN, 41, 560) # Textbox untuk posisi bola 2 di sb. x
output2d_ypos2 = MyTextBox(SCREEN, 112, 560) # Textbox untuk posisi bola 2 di sb. y
output2d_massa2 = MyTextBox(SCREEN, 183, 560) # Textbox untuk massa bola 2
output2d_vx2 = MyTextBox(SCREEN, 254, 560) # TextBox untuk kecepatan di sb. x bola 2
output2d_vy2 = MyTextBox(SCREEN, 325, 560) # TextBox untuk kecepatan di sb. y bola 2
output2d_momentum2 = MyTextBox(SCREEN, 396, 560) # Textbox untuk momentum bola 2
output2d_energi2 = MyTextBox(SCREEN, 467, 560) # Textbox untuk energi kinetik bola 2
OUTPUT_TEXTBOXES_2D = (
    output2d_xpos1, output2d_ypos1, output2d_massa1, output2d_vx1,
    output2d_vy1, output2d_momentum1, output2d_energi1, output2d_xpos2,
    output2d_ypos2, output2d_massa2, output2d_vx2, output2d_vy2,
    output2d_momentum2, output2d_energi2) # Tuple output textbox-mode 2 dimensi

# Menggabungkan sliders, input textboxes, dan output textboxes
PROPS_1D = SLIDERS_1D + INPUT_TEXTBOXES_1D + OUTPUT_TEXTBOXES_1D + (input1d_v1, input1d_v2)
PROPS_2D = SLIDERS_2D + INPUT_TEXTBOXES_2D + OUTPUT_TEXTBOXES_2D + (input2d_vx1, input2d_vy1, input2d_vx2, input2d_vy2)

# Mengisialisasi objek bola menggunakan class MyBall dari module "my_classes.py"
BOLA_MERAH = pygame.sprite.GroupSingle(Ball(r"assets\images\bola_merah.png", (200, 240), 3, 1, 0)) # Bola 1 di mode 1 dimensi
BOLA_ABU = pygame.sprite.GroupSingle(Ball(r"assets\images\bola_abu.png", (460, 240), 3, 0.1, 0)) # Bola 2 di mode 1 dimensi
BOLA_ORANGE = pygame.sprite.GroupSingle(Ball(r"assets\images\bola_oyen.png", (random.randint(50, 300), random.randint(50, 300)), 0.5, 1, 0.3)) # Bola 1 di mode 2 dimensi
BOLA_PINK = pygame.sprite.GroupSingle(Ball(r"assets\images\bola_pink.png", (random.randint(50, 300), random.randint(50, 300)), 1.5, 0.5, 0.5)) # Bola 2 di mode 2 dimensi

# Mengisialisasi objek buttonarray menggunakan class MyButtonArray dari module "my_classes.py"
# Menginisialisasi MyButtonArray untuk input kecepatan
speed_input = MyButtonArray(
                win=SCREEN, 
                x=325, 
                y=200, 
                onClicks=(
                    lambda: number("7"), lambda: number("4"), lambda: number("1"), lambda: number("0"), lambda: number("."), None,
                    lambda: number("8"), lambda: number("5"), lambda: number("2"), None, None, None,
                    lambda: number("9"), lambda: number("6"), lambda: number("3"), neg_or_pos, backspace, None))
speed_input.hide() # Menyembunyikan speed_input

# Menginisialisasi dummy textBox (untuk speed_input)
dummy_textbox = MyTextBox(SCREEN, 337, 185, 126, 20)
dummy_textbox.hide() # Menyembunyikan dummy_textbox

# Menginisialisasi objek Rect
area_img = pygame.image.load(r"assets\images\area.jpeg") # Me-load gambar untuk AREA
AREA = pygame.Rect(5, 60, 515, 360) # Area tempat bola digambar
KOTAK_INPUT = pygame.Rect(535, 60, 260, 360) # Kotak untuk menempatkan semua textbox input
KOTAK_OUTPUT = pygame.Rect(5, 480, 515, 115) # Kotak untuk menempatkan semua textbox ouput

# Menginisialisasi ITEMS sebagai argumen untuk di-pass ke fungsi draw_rects(win, rects)
RECTS = (
    ("black", AREA, 1, -1), (COLORS["putihtulang"], KOTAK_INPUT, 0, 8), 
    (COLORS["putihtulang"], KOTAK_OUTPUT, 0, 8), ("black", KOTAK_INPUT, 1, 8), 
    ("black", KOTAK_OUTPUT, 1, 8))

# Menginisialisasi ITEMS sebagai argumen untuk di-pass ke fungsi enter(tb_input, objek, axis)
ITEMS = (
    (input1d_v1, BOLA_MERAH.sprite, "x"), (input1d_v2, BOLA_ABU.sprite, "x"),
    (input2d_vx1, BOLA_ORANGE.sprite, "x"), (input2d_vy1, BOLA_ORANGE.sprite, "y"), 
    (input2d_vx2, BOLA_PINK.sprite, "x"), (input2d_vy2, BOLA_PINK.sprite, "y"))

# Me-load music untuk main menu
pygame.mixer.music.load(r"assets\sounds\main_menu_music.mpeg")
pygame.mixer.music.play(-1, 0.0, 5000)

mode = 0  # Menginisialisasi mode di 0 (main menu)
paused = False # Menginisialisasi paused sebagai False
running = True # Menginisialisasi running sebagai True
while running: # Main loop

    # Events handler pygame
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
    
    # Menampilkan semuanya jika paused = False
    if not paused:
        SCREEN.fill(COLORS["pinkbg"]) # Mewarnai background

        # Main menu
        if mode == 0:
            # Menampilkan interface main menu
            SCREEN.blit(main_menu_img, (0, 0)) # Menampilkan main_menu_img
            func.blit_texts(SCREEN, TEXTS_TO_BLIT_MENU, coor_texts_menu) # Menampilkan teks

            # Mengatur properties untuk di-show/hide
            button_1d.show()
            button_2d.show()
            quit_button.show()
            play_button.hide()
            pause_button.hide()
            back_button.hide()
            func.hide_props(PROPS_1D + PROPS_2D)

        # Mode 1 dimensi
        elif mode == 1:
            # Mengatur properties objek-objek
            KOTAK_INPUT.height = 360
            BOLA_MERAH.y = 200
            BOLA_ABU.y = 200

            # Menampilkan interface mode 1 dimensi
            SCREEN.blit(area_img, (5, 60)) # Menampilkan area_img
            func.draw_rects(SCREEN, RECTS) # Menggambar semua rects

            # Menggambar semua lingkaran
            pygame.draw.circle(SCREEN, COLORS["mymerah"], (23, 534), 11)
            pygame.draw.circle(SCREEN, COLORS["myabu"], (23, 569), 11)

            # Menampilkan teks
            func.blit_texts(SCREEN, TEXTS_TO_BLIT_1D, coor_texts_1d)
           
            # Mengatur properties untuk di-show/hide/enable/disable
            func.show_props(PROPS_1D)
            func.hide_props(PROPS_2D)
            func.disable_textboxes(INPUT_TEXTBOXES_1D + OUTPUT_TEXTBOXES_1D)
           
            # Menangkap semua nilai dari slider
            values = func.get_sliders_value(SLIDERS_1D, INPUT_TEXTBOXES_1D)

            # Mengatur massa bola berdasarkan nilai dari slider
            BOLA_MERAH.sprite.massa = values[2]
            BOLA_ABU.sprite.massa = values[3]

            # Menggerakkan bola
            BOLA_MERAH.update(AREA, values[0])
            BOLA_ABU.update(AREA, values[0])

            # Menggambar bola di layar
            BOLA_MERAH.draw(SCREEN)
            BOLA_ABU.draw(SCREEN)

            # Mendeteksi tumbukkan antar bola
            Ball.collision_with_ball(BOLA_MERAH, BOLA_ABU, values[1])

            # Mengatur teks untuk semua textbox
            # Mengatur teks untuk input textbox
            input1d_v1.setText(BOLA_MERAH.sprite.x_speed_display) # Kecepatan bola 1 di sb. x
            input1d_v2.setText(BOLA_ABU.sprite.x_speed_display) # kecepatan bola 2 di sb. x

            # Mengatur teks untuk output textbox
            # Output bola 1
            output1d_xpos1.setText(BOLA_MERAH.sprite.xpos) # Posisi di sb. x
            output1d_ypos1.setText(BOLA_MERAH.sprite.ypos) # Posisi di sb. y
            output1d_massa1.setText(BOLA_MERAH.sprite.massa) # Massa
            output1d_v1.setText(BOLA_MERAH.sprite.x_speed_display) # Kecepatan di sb. x
            output1d_momentum1.setText(BOLA_MERAH.sprite.momentum) # Momentum
            output1d_energi1.setText(BOLA_MERAH.sprite.energy) # Energi kinetik
            
            # Output bola 2
            output1d_xpos2.setText(BOLA_ABU.sprite.xpos) # Posisi di sb. x
            output1d_ypos2.setText(BOLA_ABU.sprite.ypos) # Posisi di sb. y
            output1d_massa2.setText(BOLA_ABU.sprite.massa) # Massa
            output1d_v2.setText(BOLA_ABU.sprite.x_speed_display) # Kecepatan di sb. x
            output1d_momentum2.setText(BOLA_ABU.sprite.momentum) # Momentum
            output1d_energi2.setText(BOLA_ABU.sprite.energy) # Energi kinetik

        # Mode 2 dimensi
        elif mode == 2:
            # Mengatur properties objek
            KOTAK_INPUT.height = 405

            # Menampilkan interface mode 2 dimensi
            SCREEN.blit(area_img, (5, 60)) # Menampilkan area_img
            func.draw_rects(SCREEN, RECTS) # Menggambar semua rects

            # Menggambar semua lingkaran
            pygame.draw.circle(SCREEN, COLORS["myorange"], (23, 534), 11)
            pygame.draw.circle(SCREEN, COLORS["mypink"], (23, 569), 11)

            # Menampilkan teks
            func.blit_texts(SCREEN, TEXTS_TO_BLIT_2D, coor_texts_2d)

            # Mengatur properties untuk di-show/hide/enable/disable
            func.show_props(PROPS_2D)
            func.hide_props(PROPS_1D)
            func.disable_textboxes(INPUT_TEXTBOXES_2D + OUTPUT_TEXTBOXES_2D)

            # Menangkap semua nilai dari slider
            values = func.get_sliders_value(SLIDERS_2D, INPUT_TEXTBOXES_2D)

            # Mengatur massa bola berdasarkan nilai dari slider
            BOLA_ORANGE.sprite.massa = values[2]
            BOLA_PINK.sprite.massa = values[3]

            # Menggerakkan bola
            BOLA_ORANGE.update(AREA, values[0])
            BOLA_PINK.update(AREA, values[0])

            # Menggambar bola di layar
            BOLA_ORANGE.draw(SCREEN)
            BOLA_PINK.draw(SCREEN)

            # Mendeteksi tumbukkan antar bola
            Ball.collision_with_ball(BOLA_ORANGE, BOLA_PINK, values[1])

            # Mengatur teks untuk semua textbox
            # Mengatur teks untuk input textbox
            input2d_vx1.setText(BOLA_ORANGE.sprite.x_speed_display) # Kecepatan bola 1 di sb. x
            input2d_vy1.setText(BOLA_ORANGE.sprite.y_speed_display) # Kecepatan bola 1 di sb. y
            input2d_vx2.setText(BOLA_PINK.sprite.x_speed_display) # Kecepatan bola 2 di sb. x
            input2d_vy2.setText(BOLA_PINK.sprite.y_speed_display) # Kecepatan bola 2 di sb. y

            # Mengatur teks untuk output textbox
            # Output bola 1
            output2d_xpos1.setText(BOLA_ORANGE.sprite.xpos) # Posisi di sb. x
            output2d_ypos1.setText(BOLA_ORANGE.sprite.ypos) # Posisi di sb. y
            output2d_massa1.setText(BOLA_ORANGE.sprite.massa) # Massa
            output2d_vx1.setText(BOLA_ORANGE.sprite.x_speed_display) # Kecepatan di sb. x
            output2d_vy1.setText(BOLA_ORANGE.sprite.y_speed_display) # Kecepatan di sb. y
            output2d_momentum1.setText(BOLA_ORANGE.sprite.momentum) # Momentum
            output2d_energi1.setText(BOLA_ORANGE.sprite.energy) # Energi kinetik

            # Output bola 2
            output2d_xpos2.setText(BOLA_PINK.sprite.xpos) # Posisi di sb. x
            output2d_ypos2.setText(BOLA_PINK.sprite.ypos) # Posisi di sb. y
            output2d_massa2.setText(BOLA_PINK.sprite.massa) # Massa
            output2d_vx2.setText(BOLA_PINK.sprite.x_speed_display) # Kecepatan di sb. x
            output2d_vy2.setText(BOLA_PINK.sprite.y_speed_display) # Kecepatan di sb. y
            output2d_momentum2.setText(BOLA_PINK.sprite.momentum) # Momentum
            output2d_energi2.setText(BOLA_PINK.sprite.energy) # Energi kinetik

        # Mengecek kondisi jika textbox input di pilih
        for tb, kotak, attr in ITEMS:
            if tb.selected:
                speed_input.buttons[5].setOnClick(enter, (tb, kotak, attr)) # Mengubah fungsi enter()

                # Mengatur properties untuk di-show/hide
                speed_input.show()
                dummy_textbox.show()

                paused = not paused # Mengatur paused sebagai kebalikannya

    pygame_widgets.update(events) # Menangkap semua event dari module "pygame_widgets"
    pygame.display.flip() # Meng-update seluruh layar
    clock.tick(45) # Mengatur agar gambar di-update 45 Frames per Second