import tkinter as tk
from tkinter import Text, Scrollbar, Button, filedialog, Scale, PanedWindow, Canvas, messagebox, Checkbutton, IntVar, Toplevel, Label
from PIL import Image, ImageTk
import re
import os

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
    for x in range(MARGIN, A4_WIDTH - MARGIN, CELL_SIZE):
        canvas.create_line(x * scale_factor, MARGIN * scale_factor, x * scale_factor, (A4_HEIGHT - MARGIN) * scale_factor, fill='lightgray', tags="grid")
    for y in range(MARGIN, A4_HEIGHT - MARGIN, CELL_SIZE):
        canvas.create_line(MARGIN * scale_factor, y * scale_factor, (A4_WIDTH - MARGIN) * scale_factor, y * scale_factor, fill='lightgray', tags="grid")

# Función para escalar el canvas
def scale_canvas(value):
    global scale_factor
    scale_factor = float(value)
    canvas.config(width=A4_WIDTH * scale_factor, height=A4_HEIGHT * scale_factor)
    canvas.config(scrollregion=(0, 0, A4_WIDTH * scale_factor, A4_HEIGHT * scale_factor))
    canvas.delete("all")
    canvas.create_rectangle(MARGIN * scale_factor, MARGIN * scale_factor, (A4_WIDTH - MARGIN) * scale_factor, (A4_HEIGHT - MARGIN) * scale_factor, outline='gray', width=2)
    draw_grid()
    process_code()

# Función para procesar el código e insertar imágenes en el lienzo
def process_code():
    code = text_area.get("1.0", tk.END)
    try:
        insert_images(code)
    except Exception as e:
        show_error_dialog(f"Ocurrió un error al procesar el código: {str(e)}")

# Función para insertar imágenes basadas en el código de texto
def insert_images(code):
    canvas.delete("transistor")
    pattern = r"transistor\((\d+)\)\{([\d.]+)\}"
    matches = re.findall(pattern, code)

    for match in matches:
        transistor_num = match[0]
        scale_cm = float(match[1])

        # Ruta de la imagen del transistor
        image_path = f"transistor{transistor_num}.png"
        if not os.path.exists(image_path):
            show_error_dialog(f"No se encontró la imagen: {image_path}")
            continue

        # Cargar y escalar la imagen
        image = Image.open(image_path)
        scale_px = scale_cm * CM_TO_PX * scale_factor
        image = image.resize((int(scale_px), int(scale_px)), Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(image)

        # Insertar la imagen en el lienzo en el margen
        canvas.create_image(MARGIN * scale_factor, MARGIN * scale_factor, anchor="nw", image=tk_image, tags="transistor")
        canvas.image = tk_image  # Guardar referencia para evitar que se elimine

# Guardar el código en un archivo
def save_code():
    code = text_area.get("1.0", tk.END)
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if filename:
        with open(filename, 'w') as f:
            f.write(code)

# Exportar el contenido del canvas a PDF
def export_to_pdf():
    try:
        ps_file = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript files", "*.ps")])
        if not ps_file:
            return

        if not export_grid_var.get():
            canvas.delete("grid")
        
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
        if not export_grid_var.get():
            draw_grid()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al exportar a PDF: {str(e)}")

# Mostrar un cuadro de diálogo de error
def show_error_dialog(error_message):
    error_dialog = Toplevel(root)
    error_dialog.title("Error")
    error_dialog.geometry("300x150")
    error_label = Label(error_dialog, text=error_message, wraplength=280)
    error_label.pack(pady=10)
    copy_button = Button(error_dialog, text="Copiar", command=lambda: copy_to_clipboard(error_message))
    copy_button.pack(pady=10)
    close_button = Button(error_dialog, text="Cerrar", command=error_dialog.destroy)
    close_button.pack(pady=5)

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Texto y Cuadrícula")

# Frame superior para los botones
frame_buttons = tk.Frame(root, height=50, bg='lightgray')
frame_buttons.pack(side=tk.TOP, fill=tk.X)

export_button = Button(frame_buttons, text="Exportar a PDF", command=export_to_pdf)
export_button.pack(side=tk.LEFT, padx=10, pady=10)

process_button = Button(frame_buttons, text="Procesar Código", command=process_code)
process_button.pack(side=tk.LEFT, padx=20, pady=10)

save_button = Button(frame_buttons, text="Guardar código", command=save_code)
save_button.pack(side=tk.LEFT, padx=20, pady=10)

export_grid_var = IntVar(value=1)
export_grid_checkbox = Checkbutton(frame_buttons, text="Incluir cuadrícula al exportar", variable=export_grid_var)
export_grid_checkbox.pack(side=tk.LEFT, padx=10, pady=10)

scale = Scale(frame_buttons, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, label="Zoom", command=scale_canvas)
scale.set(1.0)
scale.pack(side=tk.LEFT, padx=10, pady=10)

paned_window = PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frame_text = tk.Frame(paned_window, width=300)
paned_window.add(frame_text)
frame_canvas = tk.Frame(paned_window, width=600)
paned_window.add(frame_canvas)

text_area = Text(frame_text, wrap='word', font=('Arial', 12))
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_text = Scrollbar(frame_text, orient=tk.VERTICAL, command=text_area.yview)
scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)
text_area.config(yscrollcommand=scrollbar_text.set)

canvas = Canvas(frame_canvas, bg='white', width=A4_WIDTH, height=A4_HEIGHT, scrollregion=(0, 0, A4_WIDTH, A4_HEIGHT))
canvas.grid(row=0, column=0, sticky='nsew')

hbar = Scrollbar(frame_canvas, orient=tk.HORIZONTAL)
hbar.grid(row=1, column=0, sticky='ew')
hbar.config(command=canvas.xview)

vbar = Scrollbar(frame_canvas, orient=tk.VERTICAL)
vbar.grid(row=0, column=1, sticky='ns')
vbar.config(command=canvas.yview)

canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
frame_canvas.rowconfigure(0, weight=1)
frame_canvas.columnconfigure(0, weight=1)

root.mainloop()
