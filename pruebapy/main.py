import tkinter as tk
from mainFrame import MainFrame
import mysql.connector, time

db_config = {
    'host': 'localhost',
    'user': 'root',  # Usuario por defecto de XAMPP
    'database': 'sensado',
}

def abrirmain():
    ventana.withdraw()  # Oculta la ventana actual
    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = "INSERT INTO acceso (usuario) VALUES (%s)"
    data = (entrada_usuario.get(),)                
    cursor.execute(sql, data)
    conn.commit()         
        
    conn.close()
    
    main()

def cerrarventana():
    ventana.destroy()

def main():
    root = tk.Toplevel()  # Crea una nueva ventana superior
    root.wm_title("proyecto programacion")
    icon_path = "pruebapy/uscoico.ico"
    root.iconbitmap(icon_path)
    app = MainFrame(root)
    app.mainloop()

ventana = tk.Tk()
ventana.title("Acceso al programa")
ventana.geometry('380x300')
ventana.configure(background='#87CEEB')
ventana.iconbitmap('pruebapy/uscoico.ico')

# Etiqueta para usuario
label_usuario = tk.Label(ventana, text="Usuario:", bg="#00FFFF", fg="blue")
label_usuario.grid(row=0, column=0, padx=5, pady=25, sticky=tk.E+tk.W)

# Espacio para escribir (Entry)
entrada_usuario = tk.Entry(ventana)
entrada_usuario.grid(row=0, column=1, padx=5, pady=25, sticky=tk.E+tk.W)  # Ajusta pady


ventana.grid_rowconfigure(1, minsize=40)  # Ajusta minsize


ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)

boton = tk.Button(ventana, text="Siguiente ventana", fg="blue", command=abrirmain)
boton.grid(row=2, column=0, columnspan=2, pady=25)  # Ajusta pady


ventana.mainloop()

if __name__== "__main__":
    main()