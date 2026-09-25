from equipo import Equipo
from estudiante import Estudiante
from encargado import Encargado
from prestamo import Prestamo


class Inventario:
    def __init__(self):
        self.equipos = []
        self.estudiantes = []
        self.encargados = []
        self.prestamos = []

    def cargar_equipos(self, archivo):
        try:
            archivo_equipos = open(archivo, "r")
        except FileNotFoundError:
            return
        while True:
            id_equipo = archivo_equipos.readline()
            if id_equipo == "":
                break
            nombre = archivo_equipos.readline()
            categoria = archivo_equipos.readline()
            cantidad = archivo_equipos.readline()
            estado = archivo_equipos.readline()
            equipo = Equipo(id_equipo.strip(), nombre.strip(), categoria.strip(), int(cantidad.strip()), estado.strip())
            self.equipos.append(equipo)
        archivo_equipos.close()

    def guardar_equipos(self, archivo):
        archivo_equipos = open(archivo, "w")
        for equipo in self.equipos:
            archivo_equipos.write(equipo.id + "\n")
            archivo_equipos.write(equipo.nombre + "\n")
            archivo_equipos.write(equipo.categoria + "\n")
            archivo_equipos.write(str(equipo.cantidad) + "\n")
            archivo_equipos.write(equipo.estado + "\n")
        archivo_equipos.close()

    def cargar_estudiantes(self, archivo):
        try:
            archivo_estudiantes = open(archivo, "r")
        except FileNotFoundError:
            return
        while True:
            id_estudiante = archivo_estudiantes.readline()
            if id_estudiante == "":
                break
            estado = archivo_estudiantes.readline()
            contrasena = archivo_estudiantes.readline()
            correo = archivo_estudiantes.readline()
            rol = archivo_estudiantes.readline()
            telefono = archivo_estudiantes.readline()
            estudiante = Estudiante(id_estudiante.strip(), estado.strip(), contrasena.strip(), correo.strip(), rol.strip(), telefono.strip())
            self.estudiantes.append(estudiante)
        archivo_estudiantes.close()

    def guardar_estudiantes(self, archivo):
        archivo_estudiantes = open(archivo, "w")
        for estudiante in self.estudiantes:
            archivo_estudiantes.write(estudiante.id + "\n")
            archivo_estudiantes.write(estudiante.estado + "\n")
            archivo_estudiantes.write(estudiante.contrasena + "\n")
            archivo_estudiantes.write(estudiante.correo + "\n")
            archivo_estudiantes.write(estudiante.rol + "\n")
            archivo_estudiantes.write(estudiante.telefono + "\n")
        archivo_estudiantes.close()

    def cargar_encargados(self, archivo):
        try:
            archivo_encargados = open(archivo, "r")
        except FileNotFoundError:
            return
        while True:
            id_encargado = archivo_encargados.readline()
            if id_encargado == "":
                break
            cuenta = archivo_encargados.readline()
            contrasena = archivo_encargados.readline()
            correo = archivo_encargados.readline()
            rol = archivo_encargados.readline()
            encargado = Encargado(id_encargado.strip(), cuenta.strip(), contrasena.strip(), correo.strip(), rol.strip())
            self.encargados.append(encargado)
        archivo_encargados.close()

    def guardar_encargados(self, archivo):
        archivo_encargados = open(archivo, "w")
        for encargado in self.encargados:
            archivo_encargados.write(encargado.id + "\n")
            archivo_encargados.write(encargado.cuenta + "\n")
            archivo_encargados.write(encargado.contrasena + "\n")
            archivo_encargados.write(encargado.correo + "\n")
            archivo_encargados.write(encargado.rol + "\n")
        archivo_encargados.close()

    def cargar_prestamos(self, archivo):
        try:
            archivo_prestamos = open(archivo, "r")
        except FileNotFoundError:
            return
        while True:
            id_prestamo = archivo_prestamos.readline()
            if id_prestamo == "":
                break
            id_equipo = archivo_prestamos.readline()
            id_estudiante = archivo_prestamos.readline()
            fecha = archivo_prestamos.readline()
            estado = archivo_prestamos.readline()
            prestamo = Prestamo(id_prestamo.strip(), id_equipo.strip(), id_estudiante.strip(), fecha.strip(), estado.strip())
            self.prestamos.append(prestamo)
        archivo_prestamos.close()

    def guardar_prestamos(self, archivo):
        archivo_prestamos = open(archivo, "w")
        for prestamo in self.prestamos:
            archivo_prestamos.write(prestamo.id + "\n")
            archivo_prestamos.write(prestamo.id_equipo + "\n")
            archivo_prestamos.write(prestamo.id_estudiante + "\n")
            archivo_prestamos.write(prestamo.fecha + "\n")
            archivo_prestamos.write(prestamo.estado + "\n")
        archivo_prestamos.close()

    def registrar_producto(self, equipo):
        self.equipos.append(equipo)

    def consultar_inventario(self):
        return self.equipos

    def buscar_equipo(self, id_equipo):
        equipo_encontrado = None
        for equipo in self.equipos:
            if equipo.id == id_equipo:
                equipo_encontrado = equipo
        return equipo_encontrado

    def registrar_prestamo(self, id_equipo, id_estudiante, fecha):
        equipo_encontrado = self.buscar_equipo(id_equipo)
        if equipo_encontrado is None:
            return "ERROR: equipo no encontrado"
        if equipo_encontrado.estado == "Prestado":
            return "ERROR: el equipo no esta disponible"
        equipo_encontrado.estado = "Prestado"
        nuevo_id = str(len(self.prestamos) + 1)
        prestamo = Prestamo(nuevo_id, id_equipo, id_estudiante, fecha, "Activo")
        self.prestamos.append(prestamo)
        return "Prestamo registrado con id " + nuevo_id

    def registrar_devolucion(self, id_prestamo):
        prestamo_encontrado = None
        for prestamo in self.prestamos:
            if prestamo.id == id_prestamo:
                prestamo_encontrado = prestamo
        if prestamo_encontrado is None:
            return "ERROR: prestamo no encontrado"
        if prestamo_encontrado.estado == "Devuelto":
            return "ERROR: el prestamo ya fue devuelto"
        prestamo_encontrado.estado = "Devuelto"
        equipo_encontrado = self.buscar_equipo(prestamo_encontrado.id_equipo)
        if equipo_encontrado is not None:
            equipo_encontrado.estado = "Disponible"
        return "Devolucion registrada"

    def consultar_estudiante(self, id_estudiante):
        estudiante_encontrado = None
        for estudiante in self.estudiantes:
            if estudiante.id == id_estudiante:
                estudiante_encontrado = estudiante
        return estudiante_encontrado

    def solicitar_prestamo(self, id_estudiante, id_equipo, fecha):
        return self.registrar_prestamo(id_equipo, id_estudiante, fecha)

    def actualizar_info_estudiante(self, id_estudiante, correo, telefono):
        estudiante_encontrado = self.consultar_estudiante(id_estudiante)
        if estudiante_encontrado is None:
            return "ERROR: estudiante no encontrado"
        estudiante_encontrado.correo = correo
        estudiante_encontrado.telefono = telefono
        return "Informacion actualizada"

    def consultar_estado_prestamo(self, id_estudiante):
        lista_prestamos = []
        for prestamo in self.prestamos:
            if prestamo.id_estudiante == id_estudiante:
                lista_prestamos.append(prestamo)
        return lista_prestamos