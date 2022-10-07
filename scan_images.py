from PIL import Image
import webcolors
from deep_translator import GoogleTranslator


img = Image.open('89.png')
translator = GoogleTranslator(source="en", target="ru")
def check_bw(img: Image.Image):
    x, y, width, height = img.getbbox()
    for i in range(width):
        for j in range(height):
            r,g,b,a = img.getpixel((i, j))
            difs = []
            difs.append(abs(r-g))
            difs.append(abs(g-b))
            difs.append(abs(b-r))
            if max(difs) > 30:
                return False
    return True


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def get_prime_color(img: Image.Image):
    global get_colour_name
    x, y, width, height = img.getbbox()
    colors = {}
    for i in range(width):
        for j in range(height):
            r,g,b,a = img.getpixel((i, j))
            an,cn = get_colour_name((r,g,b))
            if cn in colors:
                colors[cn] += 1
                continue
            colors[cn] = 1
    k = max(colors, key=colors.get)
    return k

def get_image_data(img: Image.Image):
    global get_colour_name
    x, y, width, height = img.getbbox()
    is_bw = True
    colors = {}
    for i in range(width):
        for j in range(height):
            r,g,b,a = img.getpixel((i, j))
            an,cn = get_colour_name((r,g,b))
            if is_bw:
                difs = []
                difs.append(abs(r-g))
                difs.append(abs(g-b))
                difs.append(abs(b-r))
                if max(difs) > 30:
                    is_bw = False
            if cn in colors:
                colors[cn] += 1
                continue
            colors[cn] = 1
    k = max(colors, key=colors.get)
    colors.pop(k)
    k2 = max(colors, key=colors.get)
    colors.pop(k2)
    k3 = max(colors, key=colors.get)
    return {
        'primary_colors': [k,k2,k3],
        'is_bw': is_bw
    }

image_data = get_image_data(img)

print(f'Black and white: {image_data["is_bw"]} Primary color: {translator.translate(", ".join(image_data["primary_colors"]))}')
