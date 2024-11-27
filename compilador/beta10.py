import tkinter as tk
from tkinter import Text, Scrollbar, Button, filedialog, Scale, PanedWindow, Canvas, messagebox, Checkbutton, IntVar, Toplevel, Label
from PIL import Image, ImageTk
import os
import re

# Constantes para el tamaño de la hoja A4 en horizontal y márgenes
DPI = 300  
CM_TO_PX = DPI / 2.54  
MARGIN = int(CM_TO_PX)  
A4_WIDTH = int(29.7 * CM_TO_PX)  
A4_HEIGHT = int(21 * CM_TO_PX)   
CELL_SIZE = 50  
scale_factor = 1.0  

# Función para dibujar la cuadrícula
def draw_grid():
    canvas.delete("grid")  
    scale_factor = float(scale.get())  

    for x in range(MARGIN, A4_WIDTH - MARGIN, CELL_SIZE):  
        canvas.create_line(x * scale_factor, MARGIN * scale_factor, x * scale_factor, (A4_HEIGHT - MARGIN) * scale_factor, fill='lightgray',tags="grid")

    for y in range(MARGIN, A4_HEIGHT - MARGIN, CELL_SIZE):  
        canvas.create_line(MARGIN * scale_factor, y * scale_factor, (A4_WIDTH - MARGIN) * scale_factor, y * scale_factor, fill='lightgray', tags="grid")

# Función para escalar el canvas
def scale_canvas(value):
    global scale_factor  
    scale_factor = float(value)
    canvas.config(width=A4_WIDTH * scale_factor, height=A4_HEIGHT * scale_factor)
    canvas.config(scrollregion=(0, 0, A4_WIDTH * scale_factor, A4_HEIGHT * scale_factor))
    canvas.delete("all")

    canvas.create_rectangle(
        MARGIN * scale_factor, MARGIN * scale_factor, 
        (A4_WIDTH - MARGIN) * scale_factor, 
        (A4_HEIGHT - MARGIN) * scale_factor, 
        outline='gray', width=2
    )

    draw_grid()  
    process_code()  

def insert_images(code):
    canvas.delete("component")
    for line in code.splitlines():
        match = re.match(r'(\w+)\((\d+),?(\d+)?\)\{(\d+)\}', line.strip())
        if match:
            component, x, y, scale = match.groups()
            x = int(x) * CELL_SIZE  
            y = int(y) * CELL_SIZE  
            scale = int(scale)
            filepath = f"./componentes/{component}.png"  
            
            # Imprimir el nombre de la imagen que se va a cargar
            print(f"Intentando cargar: {filepath}")
            
            if os.path.exists(filepath):
                img = Image.open(filepath)
                img = img.resize((int(img.width * scale / 10), int(img.height * scale / 10)), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                canvas.create_image(x * scale_factor, y * scale_factor, image=img_tk, anchor="nw", tags="component")
                canvas.image_cache.append(img_tk)  
            else:
                print(f"Error: El archivo {filepath} no existe.")


def save_code():
    code = text_area.get("1.0", tk.END)
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if filename:
        with open(filename, 'w') as f:
            f.write(code)

def export_to_pdf():
    # Implementación para exportar el canvas a PDF
    pass

def process_code():
    code = text_area.get("1.0", tk.END)
    try:
        insert_images(code)
    except Exception as e:
         messagebox.showerror(f"Ocurrió un error al procesar el código: {str(e)}")

root = tk.Tk()
root.title("Inserción de Componentes")

frame_buttons = tk.Frame(root, height=50, bg='lightgray')
frame_buttons.pack(side=tk.TOP, fill=tk.X)

export_button = Button(frame_buttons, text="Exportar a PDF", command=export_to_pdf)
export_button.pack(side=tk.LEFT, padx=10, pady=10)

process_button = Button(frame_buttons, text="Procesar Código", command=process_code)
process_button.pack(side=tk.LEFT, padx=20, pady=10)

process_button = Button(frame_buttons, text="Guardar código",command=save_code)
process_button.pack(side=tk.LEFT, padx=20, pady=10)

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

canvas.create_rectangle(MARGIN, MARGIN, A4_WIDTH - MARGIN, A4_HEIGHT - MARGIN, outline='gray', width=2)
canvas.image_cache = []  

hbar = Scrollbar(frame_canvas, orient=tk.HORIZONTAL)
hbar.grid(row=1, column=0, sticky='ew')
hbar.config(command=canvas.xview)

vbar = Scrollbar(frame_canvas, orient=tk.VERTICAL)
vbar.grid(row=0, column=1, sticky='ns')
vbar.config(command=canvas.yview)

canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)

draw_grid()

root.mainloop()
