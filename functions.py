# Meng-import library dan module yg digunakan
import pygame # Versi 2.5.2

def draw_rects(win, rects):
    """
    Fungsi untuk menggambar banyak rect sekaligus sesuai dengan peroperty yg diinginkan
    """
    for color, rect, width, border_radius in rects:
        pygame.draw.rect(win, color, rect, width, border_radius)

def hide_props(props):
    """
    Fungsi untuk menyembunyikan banyak property sekaligus
    """
    for prop in props:
        prop.hide()

def show_props(props):
    """
    Fungsi untuk menampilkan banyak property sekaligus
    """
    for prop in props:
        prop.show()

def disable_textboxes(textboxes):
    """
    Fungsi untuk men-disable banyak property sekaligus
    """
    for textbox in textboxes:
        textbox.disable()

def get_sliders_value(sliders, textboxes):
    """
    Fungsi untuk menangkap value dari slider
    """
    values = []
    for i, (slider, textbox) in enumerate(zip(sliders, textboxes)):
        value = round(slider.getValue(), 2)
        if i == 0:
            textbox.setText(f"{value:.0%}")
        else:
            textbox.setText(f"{value:.2f}")
        values.append(value)
    return values

def blit_texts(win, texts, coordinates):
    """
    Fungsi untuk menampilkan teks berdasarkan koordinatnya
    """
    for text, coor in zip(texts, coordinates):
        win.blit(text, coor)