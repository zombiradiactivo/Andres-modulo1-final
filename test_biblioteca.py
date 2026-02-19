import unittest
from src.biblioteca import Biblioteca, Libro

class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        self.biblioteca = Biblioteca()
        self.libro1 = Libro("123", "El Quijote", "Cervantes")
        self.biblioteca.agregar_libro(self.libro1)

    def test_agregar_libro(self):
        self.assertIn("123", self.biblioteca.libros)

    def test_prestar_libro(self):
        resultado = self.biblioteca.prestar_libro("123")
        self.assertTrue(self.libro1.prestado)
        self.assertEqual(resultado, "Libro 'El Quijote' prestado con éxito.")

    def test_prestar_libro_no_existente(self):
        resultado = self.biblioteca.prestar_libro("999")
        self.assertEqual(resultado, "Error: El libro no existe.")

    def test_devolver_libro(self):
        self.biblioteca.prestar_libro("123")
        resultado = self.biblioteca.devolver_libro("123")
        self.assertFalse(self.libro1.prestado)
        self.assertEqual(resultado, "Libro 'El Quijote' devuelto con éxito.")

if __name__ == '__main__':
    unittest.main()