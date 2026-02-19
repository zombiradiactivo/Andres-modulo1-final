import sqlite3

class Libro:
    def __init__(self, db_name="biblioteca.db"):
        self.db_name = db_name
        self._crear_tablas()

    def _ejecutar_consulta(self, consulta, parametros=()):
        # Usamos context managers para asegurar que la conexión se cierre
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(consulta, parametros)
            conn.commit()
            return cursor

    def _crear_tablas(self):
        # Usamos múltiples ejecuciones para asegurar claridad
        consultas = [
            """
            CREATE TABLE IF NOT EXISTS libros (
                isbn TEXT PRIMARY KEY,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                copias_disponibles INTEGER NOT NULL DEFAULT 1
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT NOT NULL,
                id_usuario TEXT NOT NULL,
                fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (isbn) REFERENCES libros (isbn)
            )
            """
        ]
        for sql in consultas:
            self._ejecutar_consulta(sql)

    def agregar_libro(self, isbn, titulo, autor, copias=1):
        try:
            sql = "INSERT INTO libros (isbn, titulo, autor, copias_disponibles) VALUES (?, ?, ?, ?)"
            self._ejecutar_consulta(sql, (isbn, titulo, autor, copias))
            return f"Libro '{titulo}' agregado con {copias} copias."
        except sqlite3.IntegrityError:
            # Si el libro ya existe, podrías querer sumar las copias nuevas a las existentes
            sql = "UPDATE libros SET copias_disponibles = copias_disponibles + ? WHERE isbn = ?"
            self._ejecutar_consulta(sql, (copias, isbn))
            return f"Se han añadido {copias} copias al libro con ISBN {isbn}."

    def prestar_libro(self, isbn, id_usuario):
        libro = self.buscar_libro(isbn)
        if not libro:
            return "Error: El libro no existe."
        
        copias_actuales = libro[3] # Índice 3 es 'copias_disponibles'
        if copias_actuales <= 0:
            return "Error: No hay copias disponibles en este momento."

        # Registrar el préstamo
        self._ejecutar_consulta("INSERT INTO prestamos (isbn, id_usuario) VALUES (?, ?)", (isbn, id_usuario))
        # Restar una copia
        self._ejecutar_consulta("UPDATE libros SET copias_disponibles = copias_disponibles - 1 WHERE isbn = ?", (isbn,))
        
        return f"Préstamo registrado para el usuario {id_usuario}."

    def devolver_libro(self, isbn, id_usuario):
        # Verificar si ese usuario realmente tiene ese libro
        sql_verificar = "SELECT id FROM prestamos WHERE isbn = ? AND id_usuario = ? LIMIT 1"
        prestamo = self._ejecutar_consulta(sql_verificar, (isbn, id_usuario)).fetchone()

        if not prestamo:
            return f"Error: No existe un registro de préstamo de este libro para el usuario {id_usuario}."

        # Eliminar el registro de préstamo
        self._ejecutar_consulta("DELETE FROM prestamos WHERE id = ?", (prestamo[0],))
        # Aumentar una copia
        self._ejecutar_consulta("UPDATE libros SET copias_disponibles = copias_disponibles + 1 WHERE isbn = ?", (isbn,))
        
        return "Devolución procesada con éxito."

    def buscar_libro(self, isbn):
        return self._ejecutar_consulta("SELECT * FROM libros WHERE isbn = ?", (isbn,)).fetchone()

    def listar_prestamos_activos(self):
        sql = "SELECT isbn, id_usuario, fecha_prestamo FROM prestamos"
        return self._ejecutar_consulta(sql).fetchall()
    
    def listar_libros(self):
        """Devuelve todos los libros registrados en la base de datos."""
        sql = "SELECT isbn, titulo, autor, copias_disponibles FROM libros"
        cursor = self._ejecutar_consulta(sql)
        return cursor.fetchall()