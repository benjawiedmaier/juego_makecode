from PIL import Image
import numpy as np
import colorsys
import math

# Paleta de colores exacta proporcionada por el usuario
palette_rgb = [
    (255, 255, 255), (255, 33, 33), (255, 147, 196), (255, 129, 53), (255, 246, 9),
    (36, 156, 163), (120, 220, 82), (0, 63, 173), (135, 242, 255), (142, 46, 196),
    (164, 131, 159), (92, 64, 108), (229, 205, 196), (145, 70, 61), (0, 0, 0)
]

def circular_hue_difference(h1, h2):
    """
    Calcula la diferencia mínima entre dos ángulos (en grados)
    considerando la circularidad del espectro de tonalidades.
    """
    diff = abs(h1 - h2)
    return min(diff, 360 - diff)

def color_difference_rgb_to_hsv(color1, color2, weight_h=1.0, weight_s=1.0, weight_v=1.0):
    """
    Calcula una métrica de distancia entre dos colores usando el espacio HSV.
    
    - Se convierten los colores de RGB (0-255) a HSV.
    - Se calcula la diferencia circular para el hue y diferencias simples para saturación y valor.
    - Se normaliza el hue (el mayor rango relevante es 180° en sentido circular).
    - Los pesos permiten ajustar la importancia de cada componente.
    """
    # Convertir de RGB (0-255) a valores entre 0 y 1
    r1, g1, b1 = [x / 255.0 for x in color1]
    r2, g2, b2 = [x / 255.0 for x in color2]
    
    # Conversión a HSV
    h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
    h2, s2, v2 = colorsys.rgb_to_hsv(r2, g2, b2)
    
    # Convertir hue de [0, 1] a grados [0, 360)
    h1 *= 360
    h2 *= 360

    # Diferencia circular en hue
    hue_diff = circular_hue_difference(h1, h2)
    normalized_hue_diff = hue_diff / 180.0  # Normalizamos para un rango comparable
    
    # Diferencia en saturación y valor
    sat_diff = abs(s1 - s2)
    val_diff = abs(v1 - v2)
    
    # Métrica combinada (se pueden ajustar los pesos para cada componente)
    distance = math.sqrt((weight_h * normalized_hue_diff) ** 2 +
                         (weight_s * sat_diff) ** 2 +
                         (weight_v * val_diff) ** 2)
    return distance

def closest_color(rgb_value, palette):
    """
    Retorna el índice del color en la paleta que resulta 
    más cercano a rgb_value según la métrica basada en HSV.
    """
    best_index = None
    best_distance = float('inf')
    for i, color in enumerate(palette):
        dist = color_difference_rgb_to_hsv(rgb_value, color)
        if dist < best_distance:
            best_distance = dist
            best_index = i
    return best_index

# Cargar imagen
img_path = "imagen2.png"
img = Image.open(img_path)

# Redimensionar la imagen (puedes ajustar la resolución a tus necesidades)
img_resized = img.resize((160, 120), Image.NEAREST)  # Ejemplo: 160 x 120

# Convertir la imagen a modo RGB para trabajar con valores exactos
img_rgb = img_resized.convert("RGB")
pixels = np.array(img_rgb)

# Mapeo hexadecimal para la paleta (se suma 1 para evitar usar el 0)
hex_map = {i: format(i + 1, 'x') for i in range(len(palette_rgb))}

# Conversión de la imagen a la cadena MakeCode utilizando la nueva comparación de colores
makecode_lines_hex = []
for y in range(pixels.shape[0]):
    row = ''.join(hex_map[closest_color(tuple(pixels[y, x]), palette_rgb)]
                  for x in range(pixels.shape[1]))
    makecode_lines_hex.append(row)

# Combinar las líneas en un bloque de string
makecode_image_str_hex = "\n".join(makecode_lines_hex)

# Impresión del resultado final en formato MakeCode
print("const uint8_t my_image[] = {")
print(makecode_image_str_hex)
print("};")
