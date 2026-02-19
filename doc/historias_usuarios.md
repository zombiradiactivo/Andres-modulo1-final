
| ID | Título | Historia de Usuario | Criterio de Aceptación |
| --- | --- | --- | --- |
| **HU01** | Registrar Libros | **Como** bibliotecario, **quiero** registrar nuevos libros con su ISBN, título y autor, **para** que estén disponibles en el catálogo. | El sistema no debe permitir duplicar un ISBN existente. |
| **HU02** | Consultar Catálogo | **Como** usuario, **quiero** ver la lista de todos los libros y su estado (disponible/prestado), **para** saber qué puedo leer. | La lista debe mostrar claramente si el libro está fuera de la biblioteca. |
| **HU03** | Realizar Préstamo | **Como** bibliotecario, **quiero** marcar un libro como prestado, **para** llevar un control de quién tiene cada ejemplar. | No se puede prestar un libro que ya figura como "prestado". |
| **HU04** | Devolver Libro | **Como** bibliotecario, **quiero** registrar la devolución de un libro, **para** que vuelva a estar disponible para otros. | El estado del libro debe cambiar de "prestado" a "disponible". |
| **HU05** | Buscar por ISBN | **Como** usuario, **quiero** buscar un libro específico por su código ISBN, **para** encontrarlo rápidamente sin ver toda la lista. | Si el ISBN no existe, el sistema debe informar que no se encontró el libro. |