import os
from tkinter import Tk, filedialog, messagebox
from rembg import remove
from PIL import Image

def quitar_fondo():
    # Seleccionar imagen
    input_path = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    if not input_path:
        return

    # Seleccionar carpeta destino
    output_dir = filedialog.askdirectory(title="Seleccionar carpeta de destino")
    if not output_dir:
        return

    try:
        # Abrir imagen
        img = Image.open(input_path)
        
        # Quitar fondo
        output_img = remove(img)
        
        # Asegurar PNG (mantiene transparencia)
        output_filename = os.path.splitext(os.path.basename(input_path))[0] + ".png"
        output_path = os.path.join(output_dir, output_filename)
        
        output_img.save(output_path, "PNG")
        
        messagebox.showinfo("Éxito", f"Imagen guardada en:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{e}")

# Ventana principal
root = Tk()
root.title("Quitar Fondo de Imagen")
root.geometry("300x150")

# Botón principal
from tkinter import Button
btn = Button(root, text="Cargar Imagen y Quitar Fondo", command=quitar_fondo)
btn.pack(pady=50)

root.mainloop()
