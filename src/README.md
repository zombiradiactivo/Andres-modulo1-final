# Documentación Técnica: Sistema de Biblioteca v2.0

Este documento detalla el funcionamiento interno de los módulos que componen el sistema: la lógica de datos (`biblioteca.py`) y la interfaz de usuario (`main_gui.py`).

---

## 1. Módulo de Datos: `src/biblioteca.py`

Este archivo contiene la clase `Libro`, encargada de la persistencia en SQLite y la lógica de negocio.

### Estructura de la Clase
- **`__init__(db_name)`**: Inicializa la conexión persistente (`self.conn`) y llama a la creación de tablas.
- **`_ejecutar_consulta(consulta, parametros)`**: Método privado centralizado para ejecutar SQL. Asegura el `commit()` de las transacciones.

### Métodos Principales
| Función | Descripción |
| :--- | :--- |
| `agregar_libro` | Inserta un nuevo registro. Si el ISBN ya existe, utiliza un `UPDATE` para sumar las nuevas copias al stock actual. |
| `listar_libros` | Ejecuta un `SELECT` para retornar todos los libros. Es la fuente de datos para el Treeview de la GUI. |
| `prestar_libro` | 1. Verifica existencia y stock (`copias_disponibles > 0`). 2. Inserta registro en la tabla `prestamos`. 3. Decrementa el stock en `libros`. |
| `devolver_libro` | 1. Valida que el `id_usuario` tenga ese `isbn`. 2. Elimina el registro de la tabla `prestamos`. 3. Incrementa el stock en `libros`. |
| `eliminar_libro` | Borra el libro de la base de datos. Incluye una validación para impedir el borrado si existen préstamos pendientes (integridad referencial). |

---

## 2. Interfaz Gráfica: `main_gui.py`

Basado en la librería `tkinter`, gestiona la interacción con el usuario mediante una arquitectura dirigida por eventos.

### Componentes de la Interfaz
- **Navegación (Panel Superior):** Utiliza botones que activan `pack_forget()` y `pack()` para alternar entre el frame de **Inventario** y el de **Préstamos**.
- **Visualización (Treeview):** Una tabla dinámica que muestra el estado de la base de datos en tiempo real.

### Funcionalidades Especiales
- **Binding de Eventos (`<<TreeviewSelect>>`):** Al hacer clic en una fila, se dispara la función `copiar_isbn_al_clicar`. Esta extrae el valor de la columna 0 y lo inyecta en los campos de texto y en el portapapeles.
- **Gestión de Diálogos:** Utiliza `messagebox` para confirmaciones críticas (como la eliminación de libros) y para reportar errores de validación (stock agotado o campos vacíos).

---

## 3. Flujo de Trabajo (Workflow)



1. **Persistencia:** Al iniciar, se abre `biblioteca.db`. Si no existe, se crea automáticamente con el esquema de tablas definido.
2. **Ciclo de Préstamo:** - El bibliotecario selecciona un libro de la tabla (el ISBN se auto-rellena).
   - Cambia a la pestaña de "Préstamos", ingresa el ID de usuario y pulsa "Prestar".
   - La GUI llama a `db.prestar_libro()`, que resta 1 al stock en SQLite.
   - La tabla se refresca automáticamente para mostrar el stock actualizado.

---

## 4. Requisitos de Mantenimiento
- **Conexiones:** No cerrar la conexión `self.conn` manualmente, ya que la clase cuenta con un destructor `__del__` para asegurar el cierre limpio.
- **Tests:** Cualquier cambio en la lógica de `biblioteca.py` debe ser validado con `test_biblioteca.py` usando el parámetro `:memory:` para evitar corromper la base de datos de producción.