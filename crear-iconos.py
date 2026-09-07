#!/usr/bin/env python3
"""
GymOS · genera los iconos de la app móvil.
Uso:  python3 crear-iconos.py "#f97316"        (color de tu marca)
      python3 crear-iconos.py "#f97316" logo.png   (usa tu propio logo)
"""
import sys, os
from PIL import Image, ImageDraw

COLOR = sys.argv[1] if len(sys.argv) > 1 else '#f97316'
LOGO  = sys.argv[2] if len(sys.argv) > 2 else None
AQUI  = os.path.dirname(os.path.abspath(__file__))
SAL   = os.path.join(AQUI, 'icons')
os.makedirs(SAL, exist_ok=True)

def hex_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def aclarar(rgb, p):
    return tuple(min(255, int(c + (255 - c) * p)) for c in rgb)

BASE = hex_rgb(COLOR)
CLARO = aclarar(BASE, .28)
L = 1024

def fondo(radio_rel):
    """Cuadrado con degradado diagonal y esquinas redondeadas."""
    grad = Image.new('RGB', (L, L))
    d = ImageDraw.Draw(grad)
    for y in range(L):
        t = y / (L - 1)
        c = tuple(int(CLARO[i] + (BASE[i] - CLARO[i]) * t) for i in range(3))
        d.line([(0, y), (L, y)], fill=c)
    if radio_rel <= 0:
        return grad.convert('RGBA')
    mascara = Image.new('L', (L, L), 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, L - 1, L - 1],
                                             radius=int(L * radio_rel), fill=255)
    salida = Image.new('RGBA', (L, L), (0, 0, 0, 0))
    salida.paste(grad, (0, 0), mascara)
    return salida

def mancuerna(img, escala=1.0, color=(255, 255, 255, 255)):
    """Dibuja una mancuerna centrada."""
    d = ImageDraw.Draw(img)
    cx = cy = L / 2
    u = (L / 100) * escala          # unidad de medida

    barra_l, barra_g = 30 * u, 7 * u
    d.rounded_rectangle([cx - barra_l, cy - barra_g / 2, cx + barra_l, cy + barra_g / 2],
                        radius=barra_g / 2, fill=color)

    disco_int_a, disco_int_g = 34 * u, 12 * u
    for s in (-1, 1):
        x = cx + s * 26 * u
        d.rounded_rectangle([x - disco_int_g / 2, cy - disco_int_a / 2,
                             x + disco_int_g / 2, cy + disco_int_a / 2],
                            radius=disco_int_g / 3, fill=color)

    disco_ext_a, disco_ext_g = 22 * u, 10 * u
    for s in (-1, 1):
        x = cx + s * 37 * u
        d.rounded_rectangle([x - disco_ext_g / 2, cy - disco_ext_a / 2,
                             x + disco_ext_g / 2, cy + disco_ext_a / 2],
                            radius=disco_ext_g / 3, fill=color)
    return img

def con_logo(img, ruta, escala=.62):
    logo = Image.open(ruta).convert('RGBA')
    lado = int(L * escala)
    logo.thumbnail((lado, lado), Image.LANCZOS)
    img.paste(logo, ((L - logo.width) // 2, (L - logo.height) // 2), logo)
    return img

def guardar(img, nombre, tam):
    img.resize((tam, tam), Image.LANCZOS).save(os.path.join(SAL, nombre))
    print('  ✓ icons/' + nombre)

print('Generando iconos con el color ' + COLOR + (' y tu logo' if LOGO else ''))

# Icono normal (esquinas redondeadas)
normal = fondo(.22)
normal = con_logo(normal, LOGO, .58) if LOGO else mancuerna(normal, 1.0)
guardar(normal, 'icono-192.png', 192)
guardar(normal, 'icono-512.png', 512)

# Icono "maskable": fondo completo y dibujo más pequeño (Android lo recorta)
mask = fondo(0)
mask = con_logo(mask, LOGO, .44) if LOGO else mancuerna(mask, .74)
guardar(mask, 'icono-maskable-192.png', 192)
guardar(mask, 'icono-maskable-512.png', 512)

# iOS: sin transparencia y sin esquinas (el sistema las redondea)
guardar(fondo(0) if not LOGO else con_logo(fondo(0), LOGO, .58),
        'apple-touch-icon.png', 180) if LOGO else guardar(mancuerna(fondo(0), .9), 'apple-touch-icon.png', 180)

# Badge de la barra de notificaciones: blanco sobre transparente
badge = Image.new('RGBA', (L, L), (0, 0, 0, 0))
mancuerna(badge, .82, (255, 255, 255, 255))
guardar(badge, 'badge-96.png', 96)

print('Listo. Reemplaza los archivos en la carpeta icons/ si quieres otro diseño.')
