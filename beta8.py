import tkinter as tk
from tkinter import Text, Scrollbar, Button, filedialog, Scale, PanedWindow, Canvas, messagebox, Checkbutton, IntVar, Toplevel, Label
from PIL import Image
import re
import os
from math import cos, sin, pi, radians
import math


# Constantes para el tamaño de la hoja A4 en horizontal y márgenes
DPI = 300  # Dots per inch (puntos por pulgada)
CM_TO_PX = DPI / 2.54  # Conversión de cm a píxeles
MARGIN = int(CM_TO_PX)  # Margen de 1 cm (≈ 118 píxeles)
A4_WIDTH = int(29.7 * CM_TO_PX)  # Ancho A4 en píxeles (≈ 3508 píxeles)
A4_HEIGHT = int(21 * CM_TO_PX)   # Alto A4 en píxeles (≈ 2480 píxeles)
CELL_SIZE = 50  # Tamaño de cada celda en la cuadrícula (en píxeles)
scale_factor = 1.0  # Valor inicial


# Función para dibujar la cuadrícula
def draw_grid():
    canvas.delete("grid")  # Limpiar la cuadrícula anterior
    scale_factor = float(scale.get())  # Obtener el factor de escala actual

    # Dibujar líneas verticales
    for x in range(MARGIN, A4_WIDTH - MARGIN, CELL_SIZE):  # Cada 50 píxeles
        canvas.create_line(x * scale_factor, MARGIN * scale_factor, x * scale_factor, (A4_HEIGHT - MARGIN) * scale_factor, fill='lightgray', tags="grid")

    # Dibujar líneas horizontales
    for y in range(MARGIN, A4_HEIGHT - MARGIN, CELL_SIZE):  # Cada 50 píxeles
        canvas.create_line(MARGIN * scale_factor, y * scale_factor, (A4_WIDTH - MARGIN) * scale_factor, y * scale_factor, fill='lightgray', tags="grid")

# Función para escalar el canvas
def scale_canvas(value):
    global scale_factor  # Hacer que scale_factor sea global
    scale_factor = float(value)

    # Actualizar el tamaño del canvas
    canvas.config(width=A4_WIDTH * scale_factor, height=A4_HEIGHT * scale_factor)

    # Actualizar la región de desplazamiento
    canvas.config(scrollregion=(0, 0, A4_WIDTH * scale_factor, A4_HEIGHT * scale_factor))

    # Limpiar el canvas
    canvas.delete("all")

    # Redibujar el rectángulo del margen
    canvas.create_rectangle(
        MARGIN * scale_factor, MARGIN * scale_factor, 
        (A4_WIDTH - MARGIN) * scale_factor, 
        (A4_HEIGHT - MARGIN) * scale_factor, 
        outline='gray', width=2
    )

    draw_grid()  # Dibujar la cuadrícula nuevamente
    process_code()  # Redibujar las formas con la nueva escala

# Función para procesar el código y dibujar las formas

# Función para dibujar formas
def draw_shapes(code):
    canvas.delete("shape")  # Limpiar formas anteriores

    # Expresiones regulares para las formas
    rect_pattern = r'rectangulo\((\d+)\)\[\s*([\dº]+),\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'
    circle_pattern = r'circulo\((\d+)\)\[\s*([\dº]+),\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'
    triangle_pattern = r'triangulo\((\d+)\)\[\s*([\dº]+),\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'
    pentagon_pattern = r'pentagono\((\d+)\)\[\s*([\dº]+),\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'
    hexagon_pattern = r'hexagono\((\d+)\)\[\s*([\dº]+),\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'
    line_pattern = r'linea\((\d+)\)\[0,\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'
    spiral_pattern = r'espiral\((\d+),\s*vueltas=([\d]+),\s*radio=([\d]+)\)\[posicion\(x=([-\d]+),\s*y=([-\d]+)\)\]'  # Patrón de espiral


    # Eliminar comentarios de línea
    code = re.sub(r'//.*', '', code)  # Remover comentarios

    # Buscar coincidencias
    rect_matches = re.findall(rect_pattern, code)
    circle_matches = re.findall(circle_pattern, code)
    triangle_matches = re.findall(triangle_pattern, code)
    pentagon_matches = re.findall(pentagon_pattern, code)
    hexagon_matches = re.findall(hexagon_pattern, code)
    line_matches = re.findall(line_pattern, code)
    spiral_matches = re.findall(spiral_pattern, code)  # Buscar espirales


    # Dibujar líneas
    for match in line_matches:
        length = float(match[0])  # Longitud de la línea en cm
        orientation = int(match[1])  # Orientación (0=vertical, 1=horizontal)
        pos_x = int(match[2])  # Posición en x
        pos_y = int(match[3])  # Posición en y

        # Calcular la posición en píxeles desde la cuadrícula
        scale_factor = float(scale.get())
        start_x = MARGIN + (pos_x * CELL_SIZE)
        start_y = MARGIN + (pos_y * CELL_SIZE)

        # Dibuja la línea según la orientación
        if orientation == 0:  # Línea vertical
            draw_line(start_x, start_y, length, scale_factor, orientation='vertical')
        else:  # Línea horizontal
            draw_line(start_x, start_y, length, scale_factor, orientation='horizontal')



    # Dibujar rectángulos
    for match in rect_matches:
        size = float(match[0])  # El tamaño (en cm)
        pos_x = int(match[2])  # Posición en x
        pos_y = int(match[3])  # Posición en y

        # Convertir tamaño de cm a píxeles
        rect_width = size * CM_TO_PX
        rect_height = (size / 1.5) * CM_TO_PX  # Asumiendo una proporción de 3x2

        # Calcular la posición en píxeles desde la cuadrícula
        scale_factor = float(scale.get())  # Obtener la escala actual
        start_x = MARGIN + (pos_x * CELL_SIZE)  # Sin escalar aquí
        start_y = MARGIN + (pos_y * CELL_SIZE)  # Sin escalar aquí

        # Dibujo del rectángulo
        canvas.create_rectangle(
            start_x * scale_factor, start_y * scale_factor,
            (start_x + rect_width) * scale_factor,
            (start_y + rect_height) * scale_factor,
            outline='blue', width=2, tags="shape"
        )

    # Dibujar círculos
    for match in circle_matches:
        radius = float(match[0])  # Radio en cm
        pos_x = int(match[2])  # Posición en x
        pos_y = int(match[3])  # Posición en y

        # Convertir tamaño de cm a píxeles
        circle_radius = radius * CM_TO_PX

        # Calcular la posición en píxeles desde la cuadrícula
        scale_factor = float(scale.get())
        start_x = MARGIN + (pos_x * CELL_SIZE)
        start_y = MARGIN + (pos_y * CELL_SIZE)

        # Dibujo del círculo
        canvas.create_oval(
            (start_x - circle_radius) * scale_factor, (start_y - circle_radius) * scale_factor,
            (start_x + circle_radius) * scale_factor, (start_y + circle_radius) * scale_factor,
            outline='red', width=2, tags="shape"
        )

    # Dibujar triángulos
    for match in triangle_matches:
        side = float(match[0])  # Lado del triángulo en cm
        pos_x = int(match[2])  # Posición en x
        pos_y = int(match[3])  # Posición en y

        # Convertir tamaño de cm a píxeles
        triangle_side = side * CM_TO_PX

        # Calcular la posición en píxeles desde la cuadrícula
        scale_factor = float(scale.get())
        start_x = MARGIN + (pos_x * CELL_SIZE)
        start_y = MARGIN + (pos_y * CELL_SIZE)

        # Calcular los puntos del triángulo equilátero
        half_side = triangle_side / 2
        height = (triangle_side * (3**0.5)) / 2  # Altura de un triángulo equilátero

        points = [
            (start_x * scale_factor, (start_y - height / 2) * scale_factor),  # Vértice superior
            ((start_x - half_side) * scale_factor, (start_y + height / 2) * scale_factor),  # Vértice inferior izquierdo
            ((start_x + half_side) * scale_factor, (start_y + height / 2) * scale_factor)   # Vértice inferior derecho
        ]

        # Dibujo del triángulo
        canvas.create_polygon(points, outline='green', width=2, fill='', tags="shape")

    # Dibujar pentágonos
# Dibujar pentágonos
# Dibujar pentágonos
    for match in pentagon_matches:
        size = float(match[0])  # Tamaño del pentágono en cm
        pos_x = int(match[2])  # Posición en x
        pos_y = int(match[3])  # Posición en y

        # Calcular la posición en píxeles desde la cuadrícula
        scale_factor = float(scale.get())
        start_x = MARGIN + (pos_x * CELL_SIZE)
        start_y = MARGIN + (pos_y * CELL_SIZE)

        draw_pentagon(start_x, start_y, size, scale_factor)  # Asegúrate de pasar scale_factor aquí

     # Dibujar hexágonos
    for match in hexagon_matches:
        size = float(match[0])  # Lado del hexágono en cm
        pos_x = int(match[2])  # Posición en x
        pos_y = int(match[3])  # Posición en y

        # Convertir tamaño de cm a píxeles
        hexagon_side = size * CM_TO_PX

        # Calcular la posición en píxeles desde la cuadrícula
        scale_factor = float(scale.get())
        start_x = MARGIN + (pos_x * CELL_SIZE)
        start_y = MARGIN + (pos_y * CELL_SIZE)

        # Calcular los puntos del hexágono
        points = []
        for i in range(6):
            angle = i * (360 / 6) * (3.14159 / 180)  # Convertir grados a radianes
            x = start_x + hexagon_side * cos(angle)
            y = start_y + hexagon_side * sin(angle)
            points.append((x * scale_factor, y * scale_factor))

        # Dibujo del hexágono
        canvas.create_polygon(points, outline='orange', width=2, fill='', tags="shape")

    # Dibujar espirales
    # Dentro de draw_shapes
# Dentro de draw_shapes
    for match in spiral_matches:
        radio = float(match[0])  # Radio en cm
        vueltas = int(match[1])   # Número de vueltas
        pos_x = int(match[3])      # Posición en x
        pos_y = int(match[4])      # Posición en y

        # Calcular la posición en píxeles desde la cuadrícula
        center_x = MARGIN + (pos_x * CELL_SIZE * scale_factor)
        center_y = MARGIN + (pos_y * CELL_SIZE * scale_factor)

        # Llama a la función de dibujo de espirales
        draw_spiral(center_x, center_y, vueltas, radio, sentido=0, scale_factor=scale_factor)


# Función para dibujar líneas
def draw_line(start_x, start_y, length, scale_factor, orientation='vertical'):
    if orientation == 'vertical':
        end_x = start_x  # Mantener la misma x
        end_y = start_y + (length * CM_TO_PX)  # Longitud vertical
    else:
        end_x = start_x + (length * CM_TO_PX)  # Longitud horizontal
        end_y = start_y  # Mantener la misma y

    # Dibujo de la línea
    canvas.create_line(
        start_x * scale_factor, start_y * scale_factor, 
        end_x * scale_factor, end_y * scale_factor, 
        fill='black', tags="shape"
    )

# Función para dibujar una espiral
# Función para dibujar una espiral
def draw_spiral(x, y, vueltas, radio, sentido=0, scale_factor=1):
    # Aumentar el tamaño de la espiral basado en el factor de escala
    paso = (radio * scale_factor) / 20  # Ajustar el tamaño del paso según el factor de escala
    angulo = 0
    
    for i in range(vueltas * 360):  # 360 grados por vuelta
        # Calcula la posición de cada punto de la espiral
        radianes = math.radians(angulo)
        # Las posiciones se escalan según el factor de escala
        px = x + (radio + paso * i) * math.cos(radianes) * scale_factor
        py = y + (radio + paso * i) * math.sin(radianes) * scale_factor
        
        # Dibuja el punto
        canvas.create_oval(px, py, px + 1, py + 1, fill="black")
        
        # Incrementa el ángulo
        angulo += 1  # Ajusta el incremento del ángulo si es necesario

def draw_pentagon(start_x, start_y, size, scale_factor):
    # Convertir tamaño de cm a píxeles y aplicar el factor de escala
    pentagon_size = size * CM_TO_PX * scale_factor  
    points = []

    # Calcular los puntos del pentágono
    for i in range(5):
        angle = pi / 2 + 2 * pi * i / 5  # Rotar 90 grados hacia la izquierda
        x = (start_x * scale_factor) + (pentagon_size * cos(angle))  # Escalar start_x
        y = (start_y * scale_factor) + (pentagon_size * sin(angle))  # Escalar start_y
        points.append((x, y))

    # Dibujar el pentágono
    canvas.create_polygon(points, outline='purple', width=2, fill='', tags="shape")

# Función para guardar el código en un archivo
def save_code():
    code = text_area.get("1.0", tk.END)
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if filename:
        with open(filename, 'w') as f:
            f.write(code)

# Función para exportar el canvas a PDF
def export_to_pdf():
    try:
        ps_file = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps")])
        if not ps_file:
            return

        # Si el usuario no quiere la cuadrícula, la eliminamos temporalmente antes de exportar
        if not export_grid_var.get():
            canvas.delete("grid")
        
        # Exportar el contenido del canvas a PostScript
        canvas.postscript(file=ps_file, colormode='color', x=0, y=0, width=A4_WIDTH, height=A4_HEIGHT)

        png_file = ps_file.replace(".ps", ".png")
        try:
            ps_image = Image.open(ps_file)
            ps_image.save(png_file)
            pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not pdf_file:
                return
            
            img = Image.open(png_file)
            img.save(pdf_file, "PDF", resolution=100.0)
        finally:
            if os.path.exists(png_file):
                os.remove(png_file)

        # Si la cuadrícula estaba eliminada, volvemos a dibujarla
        if not export_grid_var.get():
            draw_grid()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar a PDF: {str(e)}")

def show_error_dialog(error_message):
    error_dialog = Toplevel(root)
    error_dialog.title("Error")
    error_dialog.geometry("300x150")

    # Etiqueta para mostrar el mensaje de error
    error_label = Label(error_dialog, text=error_message, wraplength=280)
    error_label.pack(pady=10)

    # Botón para copiar el mensaje al portapapeles
    copy_button = Button(error_dialog, text="Copiar", command=lambda: copy_to_clipboard(error_message))
    copy_button.pack(pady=10)

    # Botón para cerrar el diálogo
    close_button = Button(error_dialog, text="Cerrar", command=error_dialog.destroy)
    close_button.pack(pady=5)

# Función para copiar texto al portapapeles
def copy_to_clipboard(text):
    root.clipboard_clear()  # Limpiar el portapapeles
    root.clipboard_append(text)  # Añadir el nuevo texto al portapapeles
    root.update()  # Asegurar que el portapapeles se actualiza

# Modificar la función process_code
def process_code():
    code = text_area.get("1.0", tk.END)
    try:
        draw_shapes(code)
    except Exception as e:
        show_error_dialog(f"Ocurrió un error al procesar el código: {str(e)}")  # Utilizar el nuevo diálogo
# Configuración de la ventana principal
root = tk.Tk()
root.title("Texto y Cuadrícula")

# Frame superior para los botones
frame_buttons = tk.Frame(root, height=50, bg='lightgray')
frame_buttons.pack(side=tk.TOP, fill=tk.X)

# Botón para exportar a PDF
export_button = Button(frame_buttons, text="Exportar a PDF", command=export_to_pdf)
export_button.pack(side=tk.LEFT, padx=10, pady=10)

# Botón para procesar el código
process_button = Button(frame_buttons, text="Procesar Código", command=process_code)
process_button.pack(side=tk.LEFT, padx=20, pady=10)

# Botón para guardar el código
process_button = Button(frame_buttons, text="Guardar codigo",command=save_code)
process_button.pack(side=tk.LEFT, padx=20, pady=10)

# Checkbox para elegir si se exporta con o sin la cuadrícula
export_grid_var = IntVar(value=1)  # Variable que controla el estado del checkbox (1 = activado, 0 = desactivado)
export_grid_checkbox = Checkbutton(frame_buttons, text="Incluir cuadrícula al exportar", variable=export_grid_var)
export_grid_checkbox.pack(side=tk.LEFT, padx=10, pady=10)

# Escala para ajustar el zoom
scale = Scale(frame_buttons, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
              label="Zoom", command=scale_canvas)
scale.set(1.0)  # Valor inicial
scale.pack(side=tk.LEFT, padx=10, pady=10)

# Crear un PanedWindow para permitir el ajuste dinámico de tamaños, y moverlo a la derecha
paned_window = PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Frame para el área de texto
frame_text = tk.Frame(paned_window, width=300)
paned_window.add(frame_text)

# Frame para el área de dibujo
frame_canvas = tk.Frame(paned_window, width=600)
paned_window.add(frame_canvas)

# Crear el widget de entrada de texto sin numeración
text_area = Text(frame_text, wrap='word', font=('Arial', 12))
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbars para el área de texto
scrollbar_text = Scrollbar(frame_text, orient=tk.VERTICAL, command=text_area.yview)
scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)

# Configuración de la scrollbar en el área de texto
text_area.config(yscrollcommand=scrollbar_text.set)

# Crear el área de cuadrícula (canvas)
canvas = Canvas(frame_canvas, bg='white', width=A4_WIDTH, height=A4_HEIGHT, scrollregion=(0, 0, A4_WIDTH, A4_HEIGHT))
canvas.grid(row=0, column=0, sticky='nsew')

# Dibujar un rectángulo alrededor de la hoja de cuadrícula para representar el margen
canvas.create_rectangle(MARGIN, MARGIN, A4_WIDTH - MARGIN, A4_HEIGHT - MARGIN, outline='gray', width=2)

# Scrollbars para navegar el área de cuadrícula
hbar = Scrollbar(frame_canvas, orient=tk.HORIZONTAL)
hbar.grid(row=1, column=0, sticky='ew')
hbar.config(command=canvas.xview)

vbar = Scrollbar(frame_canvas, orient=tk.VERTICAL)
vbar.grid(row=0, column=1, sticky='ns')
vbar.config(command=canvas.yview)

canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# Asegurarse de que el frame del canvas se expanda correctamente
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)

# Dibujar la cuadrícula inicial
draw_grid()

# Ejecutar la aplicación
root.mainloop()