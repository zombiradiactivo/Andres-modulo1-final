class Libro:
    def __init__(self, isbn, titulo, autor):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.prestado = False

    def __str__(self):
        estado = "Prestado" if self.prestado else "Disponible"
        return f"[{self.isbn}] {self.titulo} - {self.autor} ({estado})"


class Biblioteca:
    def __init__(self):
        self.libros = {}

    def agregar_libro(self, libro):
        self.libros[libro.isbn] = libro

    def prestar_libro(self, isbn):
        if isbn not in self.libros:
            return "Error: El libro no existe."
        if self.libros[isbn].prestado:
            return "Error: El libro ya está prestado."
        
        self.libros[isbn].prestado = True
        return f"Libro '{self.libros[isbn].titulo}' prestado con éxito."

    def devolver_libro(self, isbn):
        if isbn not in self.libros:
            return "Error: El libro no existe."
        if not self.libros[isbn].prestado:
            return "Error: El libro no estaba prestado."
        
        self.libros[isbn].prestado = False
        return f"Libro '{self.libros[isbn].titulo}' devuelto con éxito."

    def listar_libros(self):
        return [str(libro) for libro in self.libros.values()]