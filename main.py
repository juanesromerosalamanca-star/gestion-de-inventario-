from encargado import Encargado
from estudiante import Estudiante
from equipo import Equipo
from inventario import Inventario


inventario = Inventario()
inventario.cargar_equipos("equipos.txt")
inventario.cargar_estudiantes("estudiantes.txt")
inventario.cargar_encargados("encargados.txt")
inventario.cargar_prestamos("prestamos.txt")

if len(inventario.equipos) == 0:
    inventario.registrar_producto(Equipo("E01", "Multimetro Digital", "Medicion", 5, "Disponible"))
    inventario.registrar_producto(Equipo("E02", "Osciloscopio", "Medicion", 3, "Disponible"))
    inventario.registrar_producto(Equipo("E03", "Fuente de Poder DC", "Alimentacion", 4, "Disponible"))
    inventario.registrar_producto(Equipo("E04", "Generador de Funciones", "Medicion", 2, "Disponible"))
    inventario.registrar_producto(Equipo("E05", "Protoboard", "Montaje", 10, "Disponible"))
    inventario.registrar_producto(Equipo("E06", "Soldador de Estano", "Herramienta", 6, "Disponible"))
    inventario.registrar_producto(Equipo("E07", "Pinza Amperimetrica", "Medicion", 3, "Disponible"))
    inventario.registrar_producto(Equipo("E08", "Kit de Resistencias", "Componentes", 15, "Disponible"))
    inventario.registrar_producto(Equipo("E09", "Kit de Capacitores", "Componentes", 15, "Disponible"))
    inventario.registrar_producto(Equipo("E10", "Kit de Transistores NPN", "Componentes", 10, "Disponible"))
    inventario.registrar_producto(Equipo("E11", "Kit de Diodos LED", "Componentes", 20, "Disponible"))
    inventario.registrar_producto(Equipo("E12", "Arduino Uno", "Microcontrolador", 8, "Disponible"))
    inventario.registrar_producto(Equipo("E13", "ESP32", "Microcontrolador", 6, "Disponible"))
    inventario.registrar_producto(Equipo("E14", "Sensor Ultrasonico HC-SR04", "Sensor", 10, "Disponible"))
    inventario.registrar_producto(Equipo("E15", "Servo Motor SG90", "Actuador", 8, "Disponible"))
    inventario.registrar_producto(Equipo("E16", "Motor DC", "Actuador", 6, "Disponible"))
    inventario.registrar_producto(Equipo("E17", "Cautin de Aire Caliente", "Herramienta", 2, "Disponible"))
    inventario.registrar_producto(Equipo("E18", "Kit de Cables Dupont", "Montaje", 12, "Disponible"))
    inventario.registrar_producto(Equipo("E19", "Cargador de Baterias", "Alimentacion", 4, "Disponible"))
    inventario.registrar_producto(Equipo("E20", "Analizador Logico", "Medicion", 2, "Disponible"))

if len(inventario.encargados) == 0:
    inventario.encargados.append(Encargado("EN01", "admin", "1234", "admin@lab.com", "Encargado"))

if len(inventario.estudiantes) == 0:
    inventario.estudiantes.append(Estudiante("ES01", "Activo", "1234", "estudiante1@correo.com", "Estudiante", "3001234567"))

while True:
    print("")
    print("1. Ingresar como Encargado")
    print("2. Ingresar como Estudiante")
    print("3. Salir")
    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        cuenta = input("Cuenta: ")
        contrasena = input("Contrasena: ")
        encargado_encontrado = None
        for encargado in inventario.encargados:
            if encargado.cuenta == cuenta and encargado.contrasena == contrasena:
                encargado_encontrado = encargado
        if encargado_encontrado is None:
            print("Cuenta o contrasena incorrecta")
        else:
            while True:
                print("")
                print("1. Registrar equipo")
                print("2. Consultar inventario")
                print("3. Registrar prestamo")
                print("4. Registrar devolucion")
                print("5. Consultar estudiante")
                print("6. Volver")
                sub_opcion = input("Seleccione una opcion: ")

                if sub_opcion == "1":
                    id_equipo = input("Id del equipo: ")
                    nombre = input("Nombre: ")
                    categoria = input("Categoria: ")
                    cantidad = int(input("Cantidad: "))
                    equipo = Equipo(id_equipo, nombre, categoria, cantidad, "Disponible")
                    inventario.registrar_producto(equipo)
                    print("Equipo registrado")

                elif sub_opcion == "2":
                    for equipo in inventario.consultar_inventario():
                        print(equipo.id + " - " + equipo.nombre + " - " + equipo.categoria + " - Cantidad: " + str(equipo.cantidad) + " - Estado: " + equipo.estado)

                elif sub_opcion == "3":
                    id_equipo = input("Id del equipo: ")
                    id_estudiante = input("Id del estudiante: ")
                    fecha = input("Fecha (dd/mm/aaaa): ")
                    resultado = inventario.registrar_prestamo(id_equipo, id_estudiante, fecha)
                    print(resultado)

                elif sub_opcion == "4":
                    id_prestamo = input("Id del prestamo: ")
                    resultado = inventario.registrar_devolucion(id_prestamo)
                    print(resultado)

                elif sub_opcion == "5":
                    id_estudiante = input("Id del estudiante: ")
                    estudiante_encontrado = inventario.consultar_estudiante(id_estudiante)
                    if estudiante_encontrado is None:
                        print("Estudiante no encontrado")
                    else:
                        print("Id: " + estudiante_encontrado.id + " Estado: " + estudiante_encontrado.estado + " Correo: " + estudiante_encontrado.correo + " Telefono: " + estudiante_encontrado.telefono)

                elif sub_opcion == "6":
                    break

                else:
                    print("Opcion invalida")

    elif opcion == "2":
        id_estudiante = input("Id de estudiante: ")
        contrasena = input("Contrasena: ")
        estudiante_encontrado = None
        for estudiante in inventario.estudiantes:
            if estudiante.id == id_estudiante and estudiante.contrasena == contrasena:
                estudiante_encontrado = estudiante
        if estudiante_encontrado is None:
            print("Cuenta o contrasena incorrecta")
        else:
            while True:
                print("")
                print("1. Consultar inventario")
                print("2. Solicitar prestamo")
                print("3. Actualizar informacion")
                print("4. Consultar estado de prestamos")
                print("5. Volver")
                sub_opcion = input("Seleccione una opcion: ")

                if sub_opcion == "1":
                    for equipo in inventario.consultar_inventario():
                        print(equipo.id + " - " + equipo.nombre + " - " + equipo.categoria + " - Estado: " + equipo.estado)

                elif sub_opcion == "2":
                    id_equipo = input("Id del equipo a solicitar: ")
                    fecha = input("Fecha (dd/mm/aaaa): ")
                    resultado = inventario.solicitar_prestamo(estudiante_encontrado.id, id_equipo, fecha)
                    print(resultado)

                elif sub_opcion == "3":
                    correo = input("Nuevo correo: ")
                    telefono = input("Nuevo telefono: ")
                    resultado = inventario.actualizar_info_estudiante(estudiante_encontrado.id, correo, telefono)
                    print(resultado)

                elif sub_opcion == "4":
                    lista_prestamos = inventario.consultar_estado_prestamo(estudiante_encontrado.id)
                    if len(lista_prestamos) == 0:
                        print("No tiene prestamos registrados")
                    else:
                        for prestamo in lista_prestamos:
                            print("Id: " + prestamo.id + " Equipo: " + prestamo.id_equipo + " Fecha: " + prestamo.fecha + " Estado: " + prestamo.estado)

                elif sub_opcion == "5":
                    break

                else:
                    print("Opcion invalida")

    elif opcion == "3":
        inventario.guardar_equipos("equipos.txt")
        inventario.guardar_estudiantes("estudiantes.txt")
        inventario.guardar_encargados("encargados.txt")
        inventario.guardar_prestamos("prestamos.txt")
        print("Datos guardados. Hasta luego.")
        break

    else:
        print("Opcion invalida")