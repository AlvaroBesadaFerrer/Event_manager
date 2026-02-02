def get_text_color(hex_color):
    """Devuelve el color que debe tener el texto de cada elemento de la línea del tiempo según el color de fondo"""

    hex_color = hex_color.lstrip('#')

    # Convertir el color de hexadecimal a RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b)  # Cálculo de la luminancia para saber si el color es claro u oscuro
    
    if luminance < 140:
        return "#FFFFFF"
    else:
        return "#000000"