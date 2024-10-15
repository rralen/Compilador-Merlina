import tkinter as tk

# Función para capturar los puntos con los clics del ratón
def capturar_punto(event):
    global puntos
    # Almacena el punto como una tupla (x, y)
    puntos.append((event.x, event.y))
    
    # Si ya tenemos dos puntos, dibuja la línea
    if len(puntos) == 2:
        dibujar_linea()

# Función para dibujar una línea entre los dos puntos capturados
def dibujar_linea():
    x1, y1 = puntos[0]
    x2, y2 = puntos[1]
    
    # Dibuja una línea entre los dos puntos
    canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
    
    # Resetea la lista de puntos
    puntos.clear()

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Dibujo de Conexión Eficiente")

# Crear un canvas donde se dibujarán los puntos y la línea
canvas = tk.Canvas(ventana, width=400, height=400, bg="white")
canvas.pack()

# Inicializamos una lista para almacenar los puntos
puntos = []

# Vinculamos el evento de clic con la función capturar_punto
canvas.bind("<Button-1>", capturar_punto)

# Inicia el loop principal de la aplicación
ventana.mainloop()