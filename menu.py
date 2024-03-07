import tkinter as tk
import subprocess
import math

def boton_presionado(numero):
    print(f"Botón {numero} presionado")
    if numero == 1:
        # Código a ejecutar cuando se presiona el botón uno
        ejecutar_pingpong()

def ejecutar_pingpong():
    try:
        # Reemplaza "python" con "python3" si es necesario
        subprocess.run(["python", "pingpong.py"])
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'pingpong.py'.")

def boton_presionado(numero):
    print(f"Botón {numero} presionado")
    if numero == 2:
        # Código a ejecutar cuando se presiona el botón uno
        ejecutar_plataforma()

def ejecutar_plataforma():
    try:
        # Reemplaza "python" con "python3" si es necesario
        subprocess.run(["python", "plataforma.py"])
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'plataforma.py'.")

def boton_presionado(numero):
    print(f"Botón {numero} presionado")
    if numero == 3:
        # Código a ejecutar cuando se presiona el botón uno
        ejecutar_snake()

def ejecutar_snake():
    try:
        # Reemplaza "python" con "python3" si es necesario
        subprocess.run(["python", "snake.py"])
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'snake.py'.")



# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ventana Arcade")
ventana.geometry("600x400")
ventana.configure(bg="black")

# Etiqueta con la palabra "Arcade" en el centro
etiqueta_arcade = tk.Label(ventana, text="Arcade", font=("Arial", 24), fg="white", bg="black")
etiqueta_arcade.place(relx=0.5, rely=0.5, anchor="center")

# Crear seis botones alrededor de la etiqueta
for i in range(1, 7):
    texto_boton = f"Botón {i}"
    if i == 1:
        boton = tk.Button(ventana, text=texto_boton, command=lambda i=i: boton_presionado(i), bg="white")
    else:
        boton = tk.Button(ventana, text=texto_boton, command=lambda i=i: boton_presionado(i), bg="white")
    angulo = i * (2 * 3.14159 / 6)  # Distribuir los botones uniformemente en un círculo
    x = 0.5 + 0.4 * math.cos(angulo)
    y = 0.5 + 0.4 * math.sin(angulo)
    boton.place(relx=x, rely=y, anchor="center")

# Iniciar el bucle de eventos
ventana.mainloop()