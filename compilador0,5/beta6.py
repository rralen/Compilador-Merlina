import tkinter as tk
from tkinter import Text, Scrollbar, Button, filedialog, Scale, PanedWindow, Canvas, messagebox, Checkbutton, IntVar
from PIL import Image
import re
import os

# Constantes para el tamaño de la hoja A4 en horizontal y márgenes
DPI = 300  # Dots per inch (puntos por pulgada)
CM_TO_PX = DPI / 2.54  # Conversión de cm a píxeles
MARGIN = int(CM_TO_PX)  # Margen de 1 cm (≈ 118 píxeles)
A4_WIDTH = int(29.7 * CM_TO_PX)  # Ancho A4 en píxeles (≈ 3508 píxeles)
A4_HEIGHT = int(21 * CM_TO_PX)   # Alto A4 en píxeles (≈ 2480 píxeles)
CELL_SIZE = 50  # Tamaño de cada celda en la cuadrícula (en píxeles)

# Función para dibujar las coordenadas
def draw_grid():
    canvas.delete("grid")  # Limpiar la cuadrícula anterior
    scale_factor = float(scale.get())  # Obtener el factor de escala actual

    # Dibujar líneas verticales
    for x in range(MARGIN, A4_WIDTH - MARGIN, CELL_SIZE):  # Cada 50 píxeles
        canvas.create_line(x * scale_factor, MARGIN * scale_factor, x * scale_factor, (A4_HEIGHT - MARGIN) * scale_factor, fill='lightgray', tags="grid")

    # Dibujar líneas horizontales
    for y in range(MARGIN, A4_HEIGHT - MARGIN, CELL_SIZE):  # Cada 50 píxeles
        canvas.create_line(MARGIN * scale_factor, y * scale_factor, (A4_WIDTH - MARGIN) * scale_factor, y * scale_factor, fill='lightgray', tags="grid")

# Función para dibujar formas según el código ingresado
def draw_shapes(code):
    canvas.delete("shape")  # Limpiar formas anteriores

    # Expresiones regulares para los rectángulos, círculos y triángulos
    rect_pattern = r'rectangulo\((\d+)\)\[\s*([\dº]+),\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'
    circle_pattern = r'circulo\((\d+)\)\[\s*([\dº]+),\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'
    triangle_pattern = r'triangulo\((\d+)\)\[\s*([\dº]+),\s*posicion\(x=([-\d]+),\s*y=([-\d]+)\)\s*\]'

    # Eliminar comentarios de línea
    code = re.sub(r'//.*', '', code)  # Remover comentarios

    rect_matches = re.findall(rect_pattern, code)
    circle_matches = re.findall(circle_pattern, code)
    triangle_matches = re.findall(triangle_pattern, code)

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
        canvas.create_polygon(points, outline='green', width=2,fill='',tags="shape")

# Función para escalar el canvas
def scale_canvas(value):
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

# Función para exportar el área de texto a PDF
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

# Función para procesar el código y dibujar las formas
def process_code():
    code = text_area.get("1.0", tk.END)
    try:
        draw_shapes(code)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el código: {str(e)}")

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
