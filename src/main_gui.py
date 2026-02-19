import tkinter as tk
from tkinter import messagebox, ttk
from biblioteca import BibliotecaDB

class BibliotecaApp:
    def __init__(self, root):
        self.db = BibliotecaDB("biblioteca.db")
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("600x400")

        # --- Formulario de Entrada ---
        frame_form = tk.LabelFrame(self.root, text="Añadir Nuevo Libro", padx=10, pady=10)
        frame_form.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_form, text="ISBN:").grid(row=0, column=0)
        self.ent_isbn = tk.Entry(frame_form)
        self.ent_isbn.grid(row=0, column=1, padx=5)

        tk.Label(frame_form, text="Título:").grid(row=0, column=2)
        self.ent_titulo = tk.Entry(frame_form)
        self.ent_titulo.grid(row=0, column=3, padx=5)

        tk.Label(frame_form, text="Copias:").grid(row=1, column=0)
        self.ent_copias = tk.Entry(frame_form)
        self.ent_copias.insert(0, "1") # Valor por defecto
        self.ent_copias.grid(row=1, column=1, padx=5, pady=5)

        btn_guardar = tk.Button(frame_form, text="Guardar Libro", command=self.guardar_libro, bg="#4CAF50", fg="white")
        btn_guardar.grid(row=1, column=3, sticky="e")

        # --- Tabla de Libros ---
        frame_lista = tk.LabelFrame(self.root, text="Inventario", padx=10, pady=10)
        frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame_lista, columns=("ISBN", "Título", "Autor", "Copias"), show='headings')
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("Copias", text="Stock")
        self.tree.column("ISBN", width=80)
        self.tree.column("Copias", width=50)
        self.tree.pack(fill="both", expand=True)

        self.actualizar_tabla()

    def guardar_libro(self):
        isbn = self.ent_isbn.get()
        titulo = self.ent_titulo.get()
        copias = self.ent_copias.get()

        if not isbn or not titulo:
            messagebox.showwarning("Error", "ISBN y Título son obligatorios")
            return

        try:
            # Usamos un autor genérico por ahora
            mensaje = self.db.agregar_libro(isbn, titulo, "Autor Desconocido", int(copias))
            messagebox.showinfo("Éxito", mensaje)
            self.actualizar_tabla()
            self.limpiar_formulario()
        except ValueError:
            messagebox.showerror("Error", "Las copias deben ser un número")

    def actualizar_tabla(self):
        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Cargar datos de DB
        for libro in self.db.listar_libros():
            self.tree.insert("", "end", values=libro)

    def limpiar_formulario(self):
        self.ent_isbn.delete(0, tk.END)
        self.ent_titulo.delete(0, tk.END)
        self.ent_copias.delete(0, tk.END)
        self.ent_copias.insert(0, "1")

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()