## Prompt 1     

Ayúdame a programar un sistema sencillo en python de gestión de biblioteca: libros, préstamos, devoluciones, etc.

Estructura mínima del proyecto (puedes adaptarla, pero esta es la
base):
o src/biblioteca.py (o similar)
o test_biblioteca.py
o README.md

## Respuesta 1

```
¡Claro! Vamos a construir un sistema de gestión de biblioteca sólido pero sencillo. Utilizaremos **Programación Orientada a Objetos (POO)** para que el código sea escalable y fácil de testear.

Aquí tienes una propuesta de estructura que cumple con tus requisitos:

---

## 1. Lógica del Sistema (`src/biblioteca.py`)

En este archivo definiremos las clases `Libro` y `Biblioteca`. La lógica de préstamos se manejará mediante un atributo de estado en el libro.

--Codigo--

## 2. Pruebas Unitarias (`test_biblioteca.py`)

Es vital asegurar que las devoluciones y préstamos funcionen como se espera. Usaremos el framework `unittest` que viene incluido en Python.

--Codigo--

## 3. Documentación (`README.md`)

Un buen proyecto siempre explica cómo ejecutarse.

--Documentacion--

---

### ¿Por qué esta estructura?

* **Diccionario para libros:** Usar `self.libros = {}` permite buscar libros por su ISBN de forma instantánea (), lo cual es mucho más eficiente que buscar en una lista si la biblioteca crece.
* **Encapsulamiento:** La clase `Libro` sabe su estado, y la clase `Biblioteca` coordina las acciones.
* **Testeabilidad:** Al separar la lógica de la interfaz (no hay `inputs` ni `prints` dentro de las clases), puedes probar cada función automáticamente.


```

## Prompt 2 

Genera 5 historias de usuario para el sistema de biblioteca. Y también genera un diagrama de flujo (en texto) del proceso de préstamo.

## Respuesta 2
```
Para que el desarrollo sea realmente profesional, las **historias de usuario** nos ayudan a entender qué necesita el bibliotecario o el usuario final, mientras que el **diagrama de flujo** asegura que no olvidemos ninguna validación lógica.

---

## 1. Historias de Usuario

He diseñado estas historias siguiendo el formato estándar: *“Como [rol], quiero [acción] para [beneficio]”*.

--Tabla--

---

## 2. Diagrama de Flujo: Proceso de Préstamo

Este diagrama describe la lógica que debería seguir tu función `prestar_libro` en `src/biblioteca.py`:

--Diagrama--

---

### ¿Qué te parece este enfoque?

He mantenido la lógica simple para que encaje con el código que ya tenemos. Si quieres subir de nivel, **¿te gustaría que añadamos la clase `Usuario` para que el préstamo no solo sea "marcar como prestado", sino asociar el libro a una persona específica?**
```

## Commit to Github

## Prompt 3

Añadamos una base de datos real

## Respuesta 3

```
¡Excelente decisión! Pasar de una lista en memoria a una **base de datos real** es el salto de "script" a "aplicación".

Utilizaremos **SQLite**, que es ideal porque ya viene incluido en Python, no requiere instalación de servidores y guarda todo en un archivo único (ej. `biblioteca.db`).

### 1. Refactorización de `src/biblioteca.py`

Modificaremos la clase para que realice consultas SQL. Usaremos el bloque `with` para asegurar que la conexión se cierre correctamente.

--Codigo--

### 2. Actualización de `test_biblioteca.py`

Para los tests, es una buena práctica usar una base de datos en memoria (`:memory:`) para que las pruebas sean rápidas y no ensucien tu archivo real.

--Codigo--

### 3. Modelo de Datos (ERD Simple)

Para visualizar cómo se guardan los datos ahora:
```
| Campo | Tipo | Descripción |
| --- | --- | --- |
| **isbn** | TEXT (PK) | Identificador único del libro. |
| **titulo** | TEXT | Nombre de la obra. |
| **autor** | TEXT | Creador de la obra. |
| **prestado** | INT | Booleano (0 = Disponible, 1 = Prestado). |

---
```
### Ventajas de este cambio:

1. **Persistencia:** Si apagas la computadora, los libros siguen ahí al abrir el programa.
2. **Escalabilidad:** Ahora podrías tener 10,000 libros y el sistema seguiría siendo rápido.
3. **Integridad:** El ISBN como `PRIMARY KEY` evita por software que registres dos veces el mismo libro.

**¿Te gustaría que cree un pequeño menú interactivo en consola (`main.py`) para que puedas usar el sistema escribiendo comandos?**
```

## Prompt 4 

Vale, añade a la base de datos el id de los usuarios que tomaron prestado el libro y el numero de copias de un mismo libro que hay disponible 

## Respuesta 4

```
Para implementar estos cambios, necesitamos modificar la estructura de la tabla libros para incluir la columna copias y crear una nueva tabla de prestamos (para saber qué usuario tiene qué libro).

Aquí tienes la actualización del sistema:
1. src/biblioteca.py (Versión con Usuarios y Copias)

He añadido lógica para que el número de copias disminuya al prestar y aumente al devolver.

--Codigo--

2. Actualización de test_biblioteca.py

Ahora probamos que varias personas puedan tomar el mismo libro si hay copias suficientes.

--Codigo--

Principales cambios realizados:

    Tabla prestamos: Ahora guardamos quién se llevó qué y cuándo. Esto permite que un mismo libro (ISBN) sea prestado a diferentes personas simultáneamente.

    Lógica de Stock: Ya no usamos un booleano prestado. Ahora usamos un número entero copias_disponibles.

    Identificación de Usuario: Las funciones de préstamo y devolución ahora exigen un id_usuario, lo cual hace el sistema mucho más real.

¿Te gustaría que añadiera una función para generar un informe de morosos o libros que llevan más de X días prestados?

```

## Prompt 5 

Al ejecutar el test me da este error:

--Codigo de Error--

## Respuesta 5
```
Ese error sqlite3.OperationalError: no such table: libros es un clásico. Lo que está ocurriendo es que, aunque definiste la función _crear_tablas(), algo falló en la inicialización o el orden de ejecución, y Python intentó insertar datos antes de que las tablas existieran físicamente en la base de datos (incluso si es en memoria).

Aquí tienes la solución directa para arreglar tu src/biblioteca.py. El cambio clave es asegurar que el método __init__ llame correctamente a la creación de tablas y que las consultas SQL usen la sintaxis exacta de las tablas creadas.
1. Corrige src/biblioteca.py

Asegúrate de que tu método _crear_tablas se vea exactamente así:

--Codigo--

2. Por qué falló (y cómo evitarlo)

El error suele darse por dos motivos comunes en SQLite:

    Ruta del archivo: Si ejecutas el test desde una carpeta distinta, a veces Python crea un archivo .db vacío en el lugar equivocado antes de ejecutar el SQL de creación.

    Transacciones pendientes: Si una consulta falla silenciosamente, las tablas no se crean. Al usar with sqlite3.connect(...), nos aseguramos de que el commit() se haga de verdad.

Visualización del flujo corregido
3. Prueba esto en tu test_biblioteca.py

Para descartar problemas de archivos locales, asegúrate de que el setUp de tu test sea exactamente así:

--Codigo--

Tip adicional: Si el error persiste, borra cualquier archivo biblioteca.db que veas en tu carpeta de GitHub para que el sistema lo genere de nuevo desde cero.

¿Quieres que te pase el código completo de prestar_libro ajustado para manejar bien los errores de stock?

```

## Prompt 6

Crea una interfaz sencilla con tk 

## Respuesta 6

```
¡Excelente idea! Integrar una interfaz gráfica con Tkinter hará que tu sistema pase de ser un conjunto de scripts a una aplicación real que cualquiera puede usar.

Vamos a crear un archivo nuevo llamado main_gui.py. Esta interfaz permitirá registrar libros y ver el catálogo actual.
1. Interfaz Gráfica con Tkinter (main_gui.py)

He diseñado una ventana dividida en dos secciones: Formulario para añadir libros y Lista para visualizar la base de datos en tiempo real.

--Codigo--

2. Estructura Visual de la App
3. Cómo usarla

    Asegúrate de tener tu archivo src/biblioteca.py con la clase BibliotecaDB corregida.

    Ejecuta el archivo de la interfaz:
    Bash

    python main_gui.py

    Al escribir un ISBN y Título y darle a "Guardar", verás cómo se actualiza la tabla inferior automáticamente.

Detalles técnicos añadidos:

    Treeview: He usado este componente de ttk porque permite mostrar datos en columnas como si fuera una hoja de Excel, lo cual es mucho más profesional para una biblioteca.

    Gestión de errores: Si intentas meter letras en el campo de "Copias", la aplicación no se cerrará, sino que mostrará un cuadro de diálogo con un mensaje de error.

¿Te gustaría que añadamos un botón en la tabla para que al seleccionar un libro puedas darle a "Prestar" y te pida el ID del usuario?
```

## Commit to Github

## Prompt 7 

biblioteca.py no tiene la funcion listar_libros

## Respuesta 7

```
Es verdad, con tantos cambios en la lógica de la base de datos se nos quedó fuera esa función en la última explicación.

Para que la interfaz de Tkinter pueda mostrar los datos, necesitamos que listar_libros realice un SELECT a la tabla. Aquí tienes el código que debes añadir (o reemplazar) en tu archivo src/biblioteca.py:
1. Función listar_libros para src/biblioteca.py

Añade este método dentro de la clase BibliotecaDB:

--Codigo--

2. Archivo src/biblioteca.py Completo (Revisado)

Para evitar más errores de "tabla no encontrada" o funciones faltantes, aquí tienes la versión definitiva y limpia:

--Codigo--

¿Por qué fallaba la interfaz?

En el código de la interfaz (main_gui.py), la función actualizar_tabla hacía esta llamada:
for libro in self.db.listar_libros():

Si la función no existía en biblioteca.py, Python lanzaba un AttributeError. Con este cambio, al ejecutar de nuevo main_gui.py, la tabla debería llenarse con los datos de tu archivo biblioteca.db.

¿Pudiste ejecutar ya la ventana de Tkinter correctamente?

```

## Prompt 8 

La interfaz ahora funciona, pero sigue sin funcionar el unittest da este error, pero la tabla "libros" si existe el la db

## Respuesta 8

```
Entiendo perfectamente la frustración. El error no such table: libros en el unittest mientras la interfaz sí funciona tiene una explicación técnica muy específica de cómo trabaja SQLite con las conexiones.
¿Por qué falla el test?

Cuando usas ":memory:" en el setUp, SQLite crea una base de datos nueva y privada en cada conexión.
En tu función _ejecutar_consulta, estás usando with sqlite3.connect(self.db_name) as conn:. Esto significa que:

    Se conecta (crea una DB vacía en RAM).

    Crea las tablas.

    Se desconecta (¡y al ser en memoria, la DB desaparece instantáneamente!).

    Cuando llamas a agregar_libro, se conecta de nuevo a una DB en RAM completamente nueva y vacía, donde la tabla libros ya no existe.

La Solución: Mantener una conexión persistente

Para que los tests funcionen con bases de datos en memoria, debemos mantener la conexión abierta mientras el objeto BibliotecaDB exista.

Modifica tu src/biblioteca.py así:

--Codigo--

¿Cómo verificar que esto arregló el problema?

    En el Test: Al usar self.db = BibliotecaDB(":memory:"), la conexión se abrirá en el __init__ y se mantendrá viva en la variable self.db durante todo el test, permitiendo que las tablas "sobrevivan" entre una consulta y otra.

    En la Interfaz (Tk): Funcionará exactamente igual, pero de forma más eficiente al no abrir y cerrar el archivo .db en cada click de botón.

Prueba a ejecutar de nuevo python test_biblioteca.py. Debería darte el glorioso mensaje de OK.

¿Quieres que te ayude a añadir una validación para que no se puedan devolver libros que no existen o que el usuario no tiene?

```

## Prompt 9

En la gui crea la opcion de poder cambiar el frame "añadir nuevo libro" para poder prestar los libros

## Respuesta 9

```

Para que la interfaz sea dinámica y no se llene de botones, lo ideal es usar un menú de navegación o un sistema de cambio de frames.

Vamos a modificar main_gui.py para añadir una barra lateral (o superior) que permita alternar entre "Gestión de Inventario" y "Préstamos".
1. Modificación de la GUI (main_gui.py)

He reorganizado el código para que los "frames" se oculten y muestren según tu elección.

--Codigo--

¿Cómo funciona el cambio?

He utilizado el método .pack_forget(). Es como "apagar la luz" de una sección de la interfaz para encender otra en el mismo espacio.
Mejoras clave aplicadas:

    Navegación: Ahora tienes botones superiores para elegir qué quieres hacer.

    Modularidad: Los campos de texto para Préstamos son independientes de los de Inventario.

    Persistencia: Al usar la versión corregida de BibliotecaDB (la que guarda la conexión en self.conn), tanto la GUI como los Tests ahora funcionarán sin errores de "tabla no encontrada".

¿Te gustaría que al hacer clic en un libro de la tabla se rellene automáticamente el ISBN en el formulario de préstamo? Sería un toque muy útil para el usuario.

```

## Prompt 10 

Se puede añadir el poder copiar el texto de la tabla para no tener que escribir a mano el isbn

## Respuesta 10

```

¡Claro que sí! Esa es una mejora de usabilidad clave. En Tkinter, el componente Treeview (la tabla) no permite copiar texto con Ctrl+C de forma nativa como un editor de texto, pero podemos programarlo fácilmente.

La mejor forma de hacerlo es capturar el evento de selección. Cuando el usuario haga clic en una fila de la tabla, extraeremos el ISBN y lo pegaremos automáticamente en los campos correspondientes.
1. Actualización de la GUI (main_gui.py)

Añadiremos un "vínculo" (binding) a la tabla. Busca la sección setup_tabla y añade la línea del bind:

--Codigo--

2. Cómo funciona esta mejora

    Selección inteligente: Al hacer un solo clic sobre cualquier fila de la tabla, el sistema detecta qué libro es.

    Portapapeles: El ISBN se guarda en la memoria de Windows/Linux/Mac (Ctrl+V funcionará en cualquier otro programa).

    Auto-rellenado: Los campos ent_isbn (Inventario) y ent_pres_isbn (Préstamos) se actualizan al instante. Ya no tienes que escribir ni una cifra.

3. Un último detalle de robustez

Para evitar que el programa falle si la tabla está vacía o el usuario hace clic en un espacio en blanco, el bloque if seleccion: se asegura de que solo actúe si realmente hay un libro marcado.

¿Te gustaría que también añadamos un botón de "Eliminar Libro" que funcione seleccionando la fila de la tabla? Sería el complemento perfecto para terminar el CRUD (Crear, Leer, Actualizar, Borrar).

```

## Prompt 11 

Añade el boton de eliminar 


## Respuesta 11

```

Para añadir la funcionalidad de eliminar, necesitamos actualizar tanto la lógica de la base de datos (para que sepa borrar el registro) como la interfaz gráfica (para tener el botón y la acción).

Aquí tienes los cambios necesarios:
1. Actualización de src/biblioteca.py

Añade este método a tu clase BibliotecaDB. Es importante verificar que no eliminemos un libro que tiene préstamos activos para mantener la integridad de los datos.

--Codigo--

2. Actualización de la GUI (main_gui.py)

Vamos a añadir el botón "Eliminar" en la sección de inventario y la función que lo conecta con la base de datos.
En el método setup_inventario:

Añade el botón debajo del de "Añadir Libro":

--Codigo--

Añade la función borrar_libro:

Esta función tomará el ISBN directamente de lo que esté escrito en el campo de texto (que se rellena solo al hacer clic en la tabla gracias a la mejora anterior).

--Codigo--

¿Cómo queda el flujo ahora?

    Seleccionas un libro en la tabla (el ISBN se copia automáticamente al campo de texto).

    Pulsas el botón rojo "Eliminar Seleccionado".

    El sistema te pide una confirmación (para evitar sustos).

    Si el libro no tiene deudas/préstamos pendientes, se borra de la base de datos y de la tabla visual.

Un pequeño detalle para el test_biblioteca.py

Si quieres probar esta función automáticamente, añade este test:

--Codigo--

Con esto ya tienes un CRUD completo (Create, Read, Update, Delete) con persistencia real y una interfaz funcional. ¿Hay alguna otra funcionalidad que quieras pulir? Por ejemplo, ¿un buscador por título?

```

## Commit to Github
