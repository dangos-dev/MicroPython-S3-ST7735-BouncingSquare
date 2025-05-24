# -----------------------------------------------------------------------------
# Script: ST7735 Bouncing Square Animation
# Autor: Jabes Rivas (Dango)
# Fecha: 24 de mayo de 2025
# Descripción: Demuestra una animación de un cuadrado rebotando en una
#              pantalla TFT ST7735 utilizando MicroPython en un ESP32-S3.
# Hardware:
#   - ESP32-S3
#   - Pantalla TFT ST7735 1.8" (128x160) RGB
# Librerías:
#   - st7735.py (Driver para el controlador ST7735, adaptado por boochow)
# Configuración de Pines: Ver las constantes PIN_*.
# -----------------------------------------------------------------------------

import machine
import time
import st7735

# Configuración de Pines
PIN_CS   = 10
PIN_DC   = 6
PIN_RST  = 7
PIN_SCLK = 12
PIN_MOSI = 11

# Periférico SPI
SPI_BUS_ID = 2  # 1 para HSPI, 2 para VSPI

# Configuración de la Pantalla
DISPLAY_WIDTH_NATIVE = 128
DISPLAY_HEIGHT_NATIVE = 160


def setup_display():
    """Inicializa la comunicación SPI y el controlador de la pantalla."""
    print("Inicializando SPI...")
    spi = None
    try:
        spi = machine.SPI(SPI_BUS_ID,
                          baudrate=20000000,
                          polarity=0,
                          phase=0,
                          sck=machine.Pin(PIN_SCLK),
                          mosi=machine.Pin(PIN_MOSI))
        print(f"SPI bus {SPI_BUS_ID} inicializado con SCLK={PIN_SCLK}, MOSI={PIN_MOSI}.")
    except Exception as e:
        print(f"Error inicializando SPI: {e}")
        return None

    print("Creando instancia del controlador TFT ST7735...")
    try:
        tft_display = st7735.TFT(spi, PIN_DC, PIN_RST, PIN_CS)
        tft_display.initb2()
        return tft_display
    except Exception as e:
        print(f"Error inicializando la instancia TFT: {e}")
        return None

def main():
    tft = setup_display()

    if not tft:
        print("Fallo al inicializar la pantalla. Deteniendo.")
        return

    try:
        tft.rotation(1) # Rota la pantalla a Landscape: 160W x 128H
        effective_width, effective_height = tft.size()
    except Exception as e:
        print(f"Error estableciendo rotación: {e}")
        effective_width = DISPLAY_WIDTH_NATIVE
        effective_height = DISPLAY_HEIGHT_NATIVE

    BG_COLOR     = st7735.TFT.BLACK
    SQUARE_COLOR = st7735.TFT.GREEN

    # Limpiar la pantalla
    tft.fill(BG_COLOR)

    # Configuración del cuadrado rebotando
    square_size = 20

    x = effective_width // 2 - square_size // 2     # Posición inicial (en el centro)
    y = effective_height // 2 - square_size // 2    # Posición inicial (en el centro)

    dx = 2 # Movimiento en X por fotograma
    dy = 2 # Movimiento en Y por fotograma

    print("Iniciando animación del cuadrado rebotando...")

    while True:
        # 1. Borrar la posición anterior del cuadrado
        tft.fillrect((x, y), (square_size, square_size), BG_COLOR)

        # 2. Actualizar la posición del cuadrado
        x += dx
        y += dy

        # 3. Comprobar colisiones con los bordes y rebotar
        if x <= 0:  # Colisión con borde izquierdo o derecho?
            x  = 0                                  # Asegurar que no se salga
            dx = -dx                                # Invertir dirección X
            SQUARE_COLOR = st7735.TFT.RED           # Cambiar color a rojo
        elif x + square_size >= effective_width:
            x  = effective_width - square_size      # Asegurar que no se salga
            dx = -dx                                # Invertir dirección X
            SQUARE_COLOR = st7735.TFT.BLUE          # Cambiar color a azul

        if y <= 0:  # Colisión con borde superior o inferior?
            y  = 0                                  # Asegurar que no se salga
            dy = -dy                                # Invertir dirección Y
            SQUARE_COLOR = st7735.TFT.YELLOW        # Cambiar color a amarillo
        elif y + square_size >= effective_height:
            y  = effective_height - square_size     # Asegurar que no se salga
            dy = -dy                                # Invertir dirección Y
            SQUARE_COLOR = st7735.TFT.CYAN          # Cambiar color a cyan

        # 4. Dibujar el cuadrado en la nueva posición
        tft.fillrect((x, y), (square_size, square_size), SQUARE_COLOR)

        time.sleep_ms(30)


# Ejecutar el programa principal
if __name__ == "__main__":
    main()

