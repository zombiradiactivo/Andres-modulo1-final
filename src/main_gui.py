import tkinter as tk
from tkinter import messagebox, ttk
from biblioteca import Libro

class BibliotecaApp:
    def __init__(self, root):
        self.db = Libro("biblioteca.db")
        self.root = root
        self.root.title("Gestión de Biblioteca Pro")
        self.root.geometry("700x500")

        # --- BARRA DE NAVEGACIÓN ---
        nav_bar = tk.Frame(self.root, bg="#2c3e50", height=40)
        nav_bar.pack(side="top", fill="x")

        btn_inv = tk.Button(nav_bar, text="Inventario", command=self.show_inventario)
        btn_inv.pack(side="left", padx=10, pady=5)

        btn_pres = tk.Button(nav_bar, text="Préstamos / Devoluciones", command=self.show_prestamos)
        btn_pres.pack(side="left", padx=10, pady=5)

        # --- CONTENEDOR PRINCIPAL ---
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Inicializar ambos frames
        self.frame_inventario = tk.LabelFrame(self.container, text="Añadir Nuevo Libro")
        self.frame_prestamos = tk.LabelFrame(self.container, text="Gestionar Préstamo")

        self.setup_inventario()
        self.setup_prestamos()

        # --- TABLA GLOBAL (Siempre visible abajo) ---
        self.setup_tabla()
        
        # Mostrar inventario por defecto
        self.show_inventario()

    def setup_inventario(self):
        tk.Label(self.frame_inventario, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_isbn = tk.Entry(self.frame_inventario)
        self.ent_isbn.grid(row=0, column=1)

        tk.Label(self.frame_inventario, text="Título:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_titulo = tk.Entry(self.frame_inventario)
        self.ent_titulo.grid(row=0, column=3)

        tk.Label(self.frame_inventario, text="Autor:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_autor = tk.Entry(self.frame_inventario)
        self.ent_autor.grid(row=1, column=1)

        tk.Label(self.frame_inventario, text="Copias:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_copias = tk.Entry(self.frame_inventario)
        self.ent_copias.grid(row=1, column=3)

        btn_del = tk.Button(self.frame_inventario, text="Eliminar Seleccionado", command=self.borrar_libro, bg="#e74c3c", fg="white")
        btn_del.grid(row=1, column=5, padx=120, pady=10)

        btn_add = tk.Button(self.frame_inventario, text="Añadir Libro", command=self.guardar_libro, bg="green", fg="white")
        btn_add.grid(row=0, column=5, padx=90, pady=10)

    def setup_prestamos(self):
        tk.Label(self.frame_prestamos, text="ISBN del Libro:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_pres_isbn = tk.Entry(self.frame_prestamos)
        self.ent_pres_isbn.grid(row=0, column=1)

        tk.Label(self.frame_prestamos, text="ID Usuario:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_user = tk.Entry(self.frame_prestamos)
        self.ent_user.grid(row=0, column=3)

        btn_p = tk.Button(self.frame_prestamos, text="Prestar", command=self.prestar_libro, bg="blue", fg="white")
        btn_p.grid(row=1, column=1, pady=10)

        btn_d = tk.Button(self.frame_prestamos, text="Devolver", command=self.devolver_libro, bg="orange")
        btn_d.grid(row=1, column=2, pady=10)

    def setup_tabla(self):
        self.tree = ttk.Treeview(self.root, columns=("ISBN", "Título", "Autor", "Stock"), show='headings')
        for col in ("ISBN", "Título", "Autor", "Stock"):
            self.tree.heading(col, text=col)
        
        # --- NUEVA LÍNEA: Vincular clic con la función de copiar ---
        self.tree.bind("<<TreeviewSelect>>", self.copiar_isbn_al_clicar)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.actualizar_tabla()

    # --- NUEVA FUNCIÓN ---
    def copiar_isbn_al_clicar(self, event):
        # Obtener el item seleccionado
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']
            isbn_seleccionado = valores[0] # El ISBN es la primera columna

            # 1. Copiar al portapapeles del sistema por si quieren pegarlo fuera
            self.root.clipboard_clear()
            self.root.clipboard_append(isbn_seleccionado)

            # 2. Rellenar automáticamente los campos de texto de la GUI
            # Para la pestaña de inventario
            self.ent_isbn.delete(0, tk.END)
            self.ent_isbn.insert(0, isbn_seleccionado)
            
            # Para la pestaña de préstamos
            self.ent_pres_isbn.delete(0, tk.END)
            self.ent_pres_isbn.insert(0, isbn_seleccionado)
            
            # Opcional: un pequeño aviso visual en la barra de estado o consola
            print(f"ISBN {isbn_seleccionado} copiado y cargado.")

    # --- LÓGICA DE CAMBIO DE VISTA ---
    def show_inventario(self):
        self.frame_prestamos.pack_forget()
        self.frame_inventario.pack(fill="x", padx=10, pady=10)

    def show_prestamos(self):
        self.frame_inventario.pack_forget()
        self.frame_prestamos.pack(fill="x", padx=10, pady=10)

    # --- ACCIONES ---
    def guardar_libro(self):
        res = self.db.agregar_libro(self.ent_isbn.get(), self.ent_titulo.get(), self.ent_autor.get(), self.ent_copias.get())
        messagebox.showinfo("Info", res)
        self.actualizar_tabla()

    def borrar_libro(self):
        isbn = self.ent_isbn.get()
        if not isbn:
            messagebox.showwarning("Atención", "Por favor, selecciona un libro de la tabla primero.")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el libro con ISBN: {isbn}?")
        if confirmar:
            mensaje = self.db.eliminar_libro(isbn)
            if "Error" in mensaje:
                messagebox.showerror("Error", mensaje)
            else:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_tabla()

    def prestar_libro(self):
        res = self.db.prestar_libro(self.ent_pres_isbn.get(), self.ent_user.get())
        messagebox.showinfo("Préstamo", res)
        self.actualizar_tabla()

    def devolver_libro(self):
        res = self.db.devolver_libro(self.ent_pres_isbn.get(), self.ent_user.get())
        messagebox.showinfo("Devolución", res)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for libro in self.db.listar_libros(): self.tree.insert("", "end", values=libro)

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()