import unittest
from src.biblioteca import Libro

class TestBibliotecaAvanzada(unittest.TestCase):
    def setUp(self):
        self.db = Libro(":memory:")
        self.db.agregar_libro("555", "El Hobbit", "Tolkien", copias=2)

    def test_prestamo_multiples_copias(self):
        # Primer préstamo
        res1 = self.db.prestar_libro("555", "user_01")
        # Segundo préstamo
        res2 = self.db.prestar_libro("555", "user_02")
        # Tercer préstamo (debería fallar porque solo hay 2 copias)
        res3 = self.db.prestar_libro("555", "user_03")

        self.assertIn("registrado", res1)
        self.assertIn("registrado", res2)
        self.assertIn("No hay copias disponibles", res3)

    def test_devolucion_incrementa_stock(self):
        self.db.prestar_libro("555", "user_01")
        libro_antes = self.db.buscar_libro("555") # Debería tener 1 copia
        self.assertEqual(libro_antes[3], 1)

        self.db.devolver_libro("555", "user_01")
        libro_despues = self.db.buscar_libro("555") # Vuelve a tener 2
        self.assertEqual(libro_despues[3], 2)

    def test_eliminar_libro(self):
        self.db.agregar_libro("999", "Para Borrar", "Autor")
        self.db.eliminar_libro("999")
        libro = self.db.buscar_libro("999")
        self.assertIsNone(libro)

if __name__ == '__main__':
    unittest.main()