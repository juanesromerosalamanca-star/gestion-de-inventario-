Sistema de Gestion de Inventario - Laboratorio de Electronica
Software para la gestion del inventario de un laboratorio de electronica. Permite a un Encargado administrar los equipos y a un Estudiante consultar el inventario y solicitar prestamos.

Como ejecutar
Tener Python instalado.

Ubicar todos los archivos .py en la misma carpeta.

Ejecutar:

python main.py

*Usuario de prueba Encargado: cuenta admin, contrasena 1234.

*Usuario de prueba Estudiante: id ES01, contrasena 1234.

*Al iniciar el programa por primera vez se crean automaticamente 20 equipos del laboratorio, un encargado y un estudiante de prueba.

*Al salir con la opcion 3 del menu principal, todo se guarda en los archivos equipos.txt, estudiantes.txt, encargados.txt y prestamos.txt.




Estructura del proyecto
encargado.py - clase Encargado
estudiante.py - clase Estudiante
equipo.py - clase Equipo

prestamo.py - clase Prestamo

inventario.py - clase Inventario (logica del sistema y persistencia)

main.py - menu principal del programa

Diagrama de casos de uso

graph LR
    Encargado((Encargado))
    Estudiante((Estudiante))
    Encargado --> UC1([Registrar equipo])
    Encargado --> UC2([Consultar inventario])
    Encargado --> UC3([Registrar prestamo])
    Encargado --> UC4([Registrar devolucion])
    Encargado --> UC5([Consultar estudiante])
    Estudiante --> UC2
    Estudiante --> UC6([Solicitar prestamo])
    Estudiante --> UC7([Actualizar informacion])
    Estudiante --> UC8([Consultar estado de prestamo])
Diagrama de clases

classDiagram
    class Encargado {
        +id
        +cuenta
        +contrasena
        +correo
        +rol
    }
    class Estudiante {
        +id
        +estado
        +contrasena
        +correo
        +rol
        +telefono
    }
    class Equipo {
        +id
        +nombre
        +categoria
        +cantidad
        +estado
    }
    class Prestamo {
        +id
        +id_equipo
        +id_estudiante
        +fecha
        +estado
    }
    class Inventario {
        +equipos
        +estudiantes
        +encargados
        +prestamos
        +registrar_producto
        +consultar_inventario
        +registrar_prestamo
        +registrar_devolucion
        +consultar_estudiante
        +solicitar_prestamo
        +actualizar_info_estudiante
        +consultar_estado_prestamo
    }
    Inventario --> "many" Equipo
    Inventario --> "many" Estudiante
    Inventario --> "many" Encargado
    Inventario --> "many" Prestamo
Diagrama de secuencia - Solicitar prestamo

sequenceDiagram
    participant Estudiante
    participant Inventario
    participant Equipo
    participant Prestamo
    Estudiante->>Inventario: solicitar_prestamo(id_estudiante, id_equipo, fecha)
    Inventario->>Equipo: buscar_equipo(id_equipo)
    Equipo-->>Inventario: equipo encontrado
    Inventario->>Equipo: cambiar estado a Prestado
    Inventario->>Prestamo: crear nuevo prestamo
    Prestamo-->>Inventario: prestamo creado
    Inventario-->>Estudiante: confirmacion del prestamo
Diagrama de secuencia - Registrar devolucion

sequenceDiagram
    participant Encargado
    participant Inventario
    participant Prestamo
    participant Equipo
    Encargado->>Inventario: registrar_devolucion(id_prestamo)
    Inventario->>Prestamo: buscar prestamo por id
    Prestamo-->>Inventario: prestamo encontrado
    Inventario->>Prestamo: cambiar estado a Devuelto
    Inventario->>Equipo: cambiar estado a Disponible
    Inventario-->>Encargado: confirmacion de devolucion
