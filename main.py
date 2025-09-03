import os
import threading
from tkinter import Tk, filedialog, messagebox, ttk, Label, Button, StringVar
from tkinter.scrolledtext import ScrolledText
from rembg import remove
from PIL import Image
from datetime import datetime
from tkinter import IntVar

def procesar_imagenes():
    # Seleccionar carpeta de origen
    input_dir = filedialog.askdirectory(title="Seleccionar carpeta con imágenes")
    if not input_dir:
        return
    
    # Crear carpeta de destino (remove_bg)
    output_dir = os.path.join(input_dir, "remove_bg")
    os.makedirs(output_dir, exist_ok=True)
    
    # Obtener lista de imágenes válidas
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    imagenes = [f for f in os.listdir(input_dir) 
                if f.lower().endswith(extensiones_validas)]
    
    if not imagenes:
        messagebox.showwarning("Advertencia", "No se encontraron imágenes en la carpeta seleccionada.")
        return
    
    # Configurar la barra de progreso
    progress_var.set(0)
    progress_bar['maximum'] = len(imagenes)
    log_text.delete(1.0, "end")
    
    # Deshabilitar botón durante el procesamiento
    procesar_btn['state'] = 'disabled'
    
    # Ejecutar en un hilo separado para no bloquear la interfaz
    threading.Thread(target=procesar_lote, args=(input_dir, output_dir, imagenes)).start()

def procesar_lote(input_dir, output_dir, imagenes):
    total = len(imagenes)
    exitosas = 0
    errores = []
    
    log_text.insert("end", f"Iniciando procesamiento de {total} imágenes...\n")
    log_text.see("end")
    
    for i, nombre_archivo in enumerate(imagenes):
        try:
            # Actualizar progreso
            progress_var.set(i + 1)
            porcentaje = (i + 1) * 100 // total
            status_var.set(f"Procesando: {porcentaje}% ({i+1}/{total})")
            
            # Registrar en el log
            log_text.insert("end", f"Procesando: {nombre_archivo}\n")
            log_text.see("end")
            
            # Ruta completa de la imagen
            input_path = os.path.join(input_dir, nombre_archivo)
            
            # Abrir y procesar imagen
            img = Image.open(input_path)
            output_img = remove(img)
            
            # Guardar resultado
            nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
            output_filename = nombre_sin_ext + ".png"
            output_path = os.path.join(output_dir, output_filename)
            
            output_img.save(output_path, "PNG")
            exitosas += 1
            
        except Exception as e:
            error_msg = f"Error al procesar {nombre_archivo}: {str(e)}"
            log_text.insert("end", error_msg + "\n")
            log_text.see("end")
            errores.append(error_msg)
    
    # Mostrar resumen
    tiempo = datetime.now().strftime("%H:%M:%S")
    resumen = f"\n[{tiempo}] Procesamiento completado:\n"
    resumen += f"- Imágenes procesadas: {exitosas}/{total}\n"
    resumen += f"- Errores: {len(errores)}\n"
    resumen += f"- Resultados guardados en: {output_dir}\n"
    
    log_text.insert("end", resumen)
    log_text.see("end")
    
    # Habilitar botón nuevamente
    procesar_btn['state'] = 'normal'
    
    # Mostrar mensaje de finalización
    if errores:
        messagebox.showwarning("Procesamiento completado con errores", 
                              f"Se procesaron {exitosas} de {total} imágenes.\nRevise el log para más detalles.")
    else:
        messagebox.showinfo("Éxito", 
                           f"Se procesaron exitosamente {exitosas} imágenes.")

# Configurar la interfaz gráfica
root = Tk()
root.title("Removedor de Fondos - Procesamiento por Lote")
root.geometry("700x500")
root.resizable(True, True)

# Marco principal
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=("n", "s", "e", "w"))

# Configurar expansión de filas y columnas
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(3, weight=1)

# Título
title_label = Label(main_frame, text="Removedor de Fondos de Imágenes", 
                   font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, pady=(0, 10))

# Descripción
desc_label = Label(main_frame, text="Selecciona una carpeta con imágenes para remover sus fondos.\nSe creará una subcarpeta 'remove_bg' con los resultados.", 
                  justify="center")
desc_label.grid(row=1, column=0, pady=(0, 20))

# Botón de procesamiento
procesar_btn = Button(main_frame, text="Seleccionar Carpeta y Procesar", 
                     command=procesar_imagenes, bg="#4CAF50", fg="white",
                     font=("Arial", 12), padx=20, pady=10)
procesar_btn.grid(row=2, column=0, pady=(0, 20))

# Variables para estado y progreso
status_var = StringVar(value="Listo para procesar")
progress_var = IntVar(value=0)

# Etiqueta de estado
status_label = Label(main_frame, textvariable=status_var)
status_label.grid(row=3, column=0, sticky="w", pady=(0, 5))

# Barra de progreso
progress_bar = ttk.Progressbar(main_frame, variable=progress_var, mode="determinate")
progress_bar.grid(row=4, column=0, sticky="ew", pady=(0, 10))

# Área de log
log_label = Label(main_frame, text="Registro de procesamiento:", anchor="w")
log_label.grid(row=5, column=0, sticky="w", pady=(0, 5))

log_text = ScrolledText(main_frame, height=15)
log_text.grid(row=6, column=0, sticky="nsew", pady=(0, 10))

# Información de derechos de autor
copyright_label = Label(main_frame, text="© 2023 Herramienta de Procesamiento de Imágenes", 
                       font=("Arial", 8), fg="gray")
copyright_label.grid(row=7, column=0, pady=(10, 0))

# Iniciar la aplicación
root.mainloop()