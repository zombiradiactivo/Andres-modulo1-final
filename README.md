# Sistema de Gestión de Biblioteca (v2.0)

Este es un sistema de escritorio desarrollado en Python que permite gestionar el inventario de libros, el control de stock por copias y el registro de préstamos por usuario. Utiliza una base de datos SQLite para la persistencia de datos y una interfaz gráfica construida con Tkinter.

## Uso de IA en este proyecto
    Fue usado Google Gemini 3 Flash para crear el codigo (con revision humana) y la documentacion.
    Aproximadamente un 95% fue crado con IA.
    
    Mis 3 reglas personales para usar IA de forma responsable.
        Regla 1: Garantizar que el código funciona.
        Regla 2: Garantizar que el código es seguro.
        Regla 3: Comprobar que el código no incumpla con la ley.


## Características Actuales

    Gestión de Inventario (CRUD): Añadir, listar y eliminar libros.

    Control de Stock: Manejo de múltiples copias para un mismo ISBN.

    Sistema de Préstamos: Registro de préstamos y devoluciones vinculados a un ID de usuario.

    Interfaz Dinámica: Cambio entre paneles de Inventario y Préstamos sin cerrar la aplicación.

    Usabilidad: Auto-rellenado de campos e integración con el portapapeles al seleccionar un libro en la tabla.

    Persistencia Real: Los datos se guardan en un archivo local biblioteca.db.

## Estructura
    ├── src/
    │   └── biblioteca.py     # Lógica de negocio y conexión a SQLite
    ├── main_gui.py           # Interfaz gráfica (Tkinter)
    ├── test_biblioteca.py    # Pruebas unitarias automáticas
    └── biblioteca.db         # Base de datos local (se genera al iniciar)

## Instalación y Ejecución
### Requisitos previos

    Python 3.10 o superior instalado.

    No requiere librerías externas (usa sqlite3 y tkinter incluidos en Python).

## Ejecutar la aplicación

Para iniciar la interfaz gráfica, ejecuta:
```bash
python main_gui.py
```
## Cómo ejecutar las pruebas
Para validar la integridad del sistema y la base de datos:
```bash
python -m unittest test_biblioteca.py
```

## Modelo de Datos

El sistema utiliza dos tablas relacionadas para mantener la integridad:

    Libros: Almacena isbn (PK), titulo, autor y copias_disponibles.

    Prestamos: Rastrea cada ejemplar fuera de la biblioteca con id_usuario y fecha_prestamo.
