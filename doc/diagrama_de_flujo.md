```text
[ INICIO: Solicitud de Préstamo ]
           |
           v
    ¿Existe el ISBN? --------------------( NO )
           |                                |
         ( SÍ )                             v
           |                      [ ERROR: Libro no encontrado ]
           v                                |
    ¿Está disponible? -------------------( NO )
           |                                |
         ( SÍ )                             v
           |                      [ ERROR: Libro ya prestado ]
           v                                |
[ Marcar Libro como PRESTADO ]              |
           |                                |
           v                                |
[ CONFIRMACIÓN: Préstamo exitoso ]          |
           |                                |
           v                                |
        [ FIN ] <---------------------------/

```