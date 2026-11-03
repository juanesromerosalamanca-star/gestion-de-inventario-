from datetime import datetime
from Administrador import Administrador
from equipo import Equipo
from Estudiante import Estudiante
from prestamo import Prestamo
from registro_historial import RegistroHistorial


class Inventario:
    def __init__(self):
        self.equipos = []
        self.estudiantes = []
        self.encargados = []
        self.prestamos = []
        self.historial = []
      
    def fecha_hora_actual(self):
        ahora = datetime.now()
        return ahora.strftime("%d/%m/%Y"), ahora.strftime("%H:%M:%S")

    def siguiente_id(self, lista):
        mayor = 0
        for elemento in lista:
            if elemento.id.isdigit() and int(elemento.id) > mayor:
                mayor = int(elemento.id)
        return str(mayor + 1)

    def recalcular_stock(self):
        """Recalcula cuantas unidades de cada equipo estan prestadas,
        sumando los prestamos que siguen 'Activo'. Asi el total del equipo
        nunca cambia y el numero de disponibles siempre es correcto."""
        for equipo in self.equipos:
            equipo.prestados = 0
        for prestamo in self.prestamos:
            if prestamo.estado == "Activo":
                equipo = self.buscar_equipo(prestamo.id_equipo)
                if equipo is not None:
                    equipo.prestados += prestamo.cantidad
        for equipo in self.equipos:
            equipo.actualizar_estado()

  
    def cargar_equipos(self, archivo):
        try:
            archivo_equipos = open(archivo, "r", encoding="utf-8")
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
        archivo_equipos = open(archivo, "w", encoding="utf-8")
        for equipo in self.equipos:
            archivo_equipos.write(equipo.id + "\n")
            archivo_equipos.write(equipo.nombre + "\n")
            archivo_equipos.write(equipo.categoria + "\n")
            archivo_equipos.write(str(equipo.cantidad) + "\n")   
            archivo_equipos.write(equipo.estado + "\n")
        archivo_equipos.close()

    def cargar_estudiantes(self, archivo):
        try:
            archivo_estudiantes = open(archivo, "r", encoding="utf-8")
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
            nuevo_est = Estudiante(id_estudiante.strip(), estado.strip(), contrasena.strip(), correo.strip(), rol.strip(), telefono.strip())
            self.estudiantes.append(nuevo_est)
        archivo_estudiantes.close()

    def guardar_estudiantes(self, archivo):
        archivo_estudiantes = open(archivo, "w", encoding="utf-8")
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
            archivo_encargados = open(archivo, "r", encoding="utf-8")
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
            encargado = Administrador(id_encargado.strip(), cuenta.strip(), contrasena.strip(), correo.strip(), rol.strip())
            self.encargados.append(encargado)
        archivo_encargados.close()

    def guardar_encargados(self, archivo):
        archivo_encargados = open(archivo, "w", encoding="utf-8")
        for encargado in self.encargados:
            archivo_encargados.write(encargado.id + "\n")
            archivo_encargados.write(encargado.cuenta + "\n")
            archivo_encargados.write(encargado.contrasena + "\n")
            archivo_encargados.write(encargado.correo + "\n")
            archivo_encargados.write(encargado.rol + "\n")
        archivo_encargados.close()

    def cargar_prestamos(self, archivo):
        try:
            archivo_prestamos = open(archivo, "r", encoding="utf-8")
        except FileNotFoundError:
            return
        while True:
            id_prestamo = archivo_prestamos.readline()
            if id_prestamo == "":
                break
            id_equipo = archivo_prestamos.readline()
            id_estudiante = archivo_prestamos.readline()
            cantidad = archivo_prestamos.readline()
            fecha = archivo_prestamos.readline()
            hora = archivo_prestamos.readline()
            estado = archivo_prestamos.readline()
            registrado_por = archivo_prestamos.readline()
            fecha_devolucion = archivo_prestamos.readline()
            hora_devolucion = archivo_prestamos.readline()
            recibido_por = archivo_prestamos.readline()
            prestamo = Prestamo(id_prestamo.strip(), id_equipo.strip(), id_estudiante.strip(), int(cantidad.strip()), fecha.strip(), hora.strip(), estado.strip(), registrado_por.strip(), fecha_devolucion.strip(), hora_devolucion.strip(), recibido_por.strip())
            self.prestamos.append(prestamo)
        archivo_prestamos.close()
        self.recalcular_stock()

    def guardar_prestamos(self, archivo):
        archivo_prestamos = open(archivo, "w", encoding="utf-8")
        for prestamo in self.prestamos:
            archivo_prestamos.write(prestamo.id + "\n")
            archivo_prestamos.write(prestamo.id_equipo + "\n")
            archivo_prestamos.write(prestamo.id_estudiante + "\n")
            archivo_prestamos.write(str(prestamo.cantidad) + "\n")
            archivo_prestamos.write(prestamo.fecha + "\n")
            archivo_prestamos.write(prestamo.hora + "\n")
            archivo_prestamos.write(prestamo.estado + "\n")
            archivo_prestamos.write(prestamo.registrado_por + "\n")
            archivo_prestamos.write(prestamo.fecha_devolucion + "\n")
            archivo_prestamos.write(prestamo.hora_devolucion + "\n")
            archivo_prestamos.write(prestamo.recibido_por + "\n")
        archivo_prestamos.close()

    def cargar_historial(self, archivo):
        try:
            archivo_historial = open(archivo, "r", encoding="utf-8")
        except FileNotFoundError:
            return
        while True:
            id_registro = archivo_historial.readline()
            if id_registro == "":
                break
            fecha = archivo_historial.readline()
            hora = archivo_historial.readline()
            accion = archivo_historial.readline()
            id_prestamo = archivo_historial.readline()
            id_equipo = archivo_historial.readline()
            nombre_equipo = archivo_historial.readline()
            id_estudiante = archivo_historial.readline()
            cantidad = archivo_historial.readline()
            registrado_por = archivo_historial.readline()
            registro = RegistroHistorial(id_registro.strip(), fecha.strip(), hora.strip(), accion.strip(), id_prestamo.strip(), id_equipo.strip(), nombre_equipo.strip(), id_estudiante.strip(), int(cantidad.strip()), registrado_por.strip())
            self.historial.append(registro)
        archivo_historial.close()

    def guardar_historial(self, archivo):
        archivo_historial = open(archivo, "w", encoding="utf-8")
        for registro in self.historial:
            archivo_historial.write(registro.id + "\n")
            archivo_historial.write(registro.fecha + "\n")
            archivo_historial.write(registro.hora + "\n")
            archivo_historial.write(registro.accion + "\n")
            archivo_historial.write(registro.id_prestamo + "\n")
            archivo_historial.write(registro.id_equipo + "\n")
            archivo_historial.write(registro.nombre_equipo + "\n")
            archivo_historial.write(registro.id_estudiante + "\n")
            archivo_historial.write(str(registro.cantidad) + "\n")
            archivo_historial.write(registro.registrado_por + "\n")
        archivo_historial.close()

   
    def registrar_producto(self, equipo):
        if equipo.id == "" or equipo.nombre == "":
            return "ERROR: el ID y el nombre del equipo son obligatorios"
        if equipo.cantidad <= 0:
            return "ERROR: la cantidad debe ser mayor a 0"
        if self.buscar_equipo(equipo.id) is not None:
            return "ERROR: ya existe un equipo con ese ID"
        equipo.prestados = 0
        equipo.actualizar_estado()
        self.equipos.append(equipo)
        return "Equipo registrado correctamente"

    def consultar_inventario(self):
        return self.equipos

    def buscar_equipo(self, id_equipo):
        equipo_encontrado = None
        for equipo in self.equipos:
            if equipo.id == id_equipo:
                equipo_encontrado = equipo
        return equipo_encontrado


    def registrar_evento(self, accion, prestamo, equipo, registrado_por):
        fecha, hora = self.fecha_hora_actual()
        registro = RegistroHistorial(
            self.siguiente_id(self.historial), fecha, hora, accion,
            prestamo.id, equipo.id, equipo.nombre, prestamo.id_estudiante,
            prestamo.cantidad, registrado_por)
        self.historial.append(registro)

    def registrar_prestamo(self, id_equipo, id_estudiante, cantidad_solicitada, registrado_por):
        if cantidad_solicitada <= 0:
            return "ERROR: la cantidad debe ser mayor a 0"

        equipo_encontrado = self.buscar_equipo(id_equipo)
        if equipo_encontrado is None:
            return "ERROR: equipo no encontrado"

        estudiante_encontrado = self.consultar_estudiante(id_estudiante)
        if estudiante_encontrado is None:
            return "ERROR: estudiante no encontrado"
        if estudiante_encontrado.estado != "Activo":
            return "ERROR: el estudiante no esta activo"

   
        if equipo_encontrado.disponibles < cantidad_solicitada:
            return f"ERROR: Cantidad insuficiente. Disponibles: {equipo_encontrado.disponibles}"

    
        equipo_encontrado.prestados += cantidad_solicitada
        equipo_encontrado.actualizar_estado()

        fecha, hora = self.fecha_hora_actual()
        nuevo_id = self.siguiente_id(self.prestamos)
        prestamo = Prestamo(nuevo_id, id_equipo, id_estudiante, cantidad_solicitada, fecha, hora, "Activo", registrado_por)
        self.prestamos.append(prestamo)
        self.registrar_evento("PRESTAMO", prestamo, equipo_encontrado, registrado_por)

        return (f"Prestamo registrado con ID {nuevo_id}\n"
                f"Equipo: {equipo_encontrado.nombre}\n"
                f"Fecha y hora: {fecha} {hora}\n"
                f"Quedan {equipo_encontrado.disponibles} disponibles de {equipo_encontrado.cantidad} "
                f"({equipo_encontrado.prestados} prestados)")

    def registrar_devolucion(self, id_prestamo, recibido_por):
        prestamo_encontrado = None
        for prestamo in self.prestamos:
            if prestamo.id == id_prestamo:
                prestamo_encontrado = prestamo
        if prestamo_encontrado is None:
            return "ERROR: prestamo no encontrado"
        if prestamo_encontrado.estado == "Devuelto":
            return "ERROR: el prestamo ya fue devuelto"

        fecha, hora = self.fecha_hora_actual()
        prestamo_encontrado.estado = "Devuelto"
        prestamo_encontrado.fecha_devolucion = fecha
        prestamo_encontrado.hora_devolucion = hora
        prestamo_encontrado.recibido_por = recibido_por

     
        equipo_encontrado = self.buscar_equipo(prestamo_encontrado.id_equipo)
        if equipo_encontrado is not None:
            equipo_encontrado.prestados -= prestamo_encontrado.cantidad
            if equipo_encontrado.prestados < 0:
                equipo_encontrado.prestados = 0
            equipo_encontrado.actualizar_estado()
            self.registrar_evento("DEVOLUCION", prestamo_encontrado, equipo_encontrado, recibido_por)
            return (f"Devolucion registrada\n"
                    f"Equipo: {equipo_encontrado.nombre}\n"
                    f"Ahora hay {equipo_encontrado.disponibles} disponibles de {equipo_encontrado.cantidad}")
        return "Devolucion registrada"

    def solicitar_prestamo(self, id_estudiante, id_equipo, cantidad):
        return self.registrar_prestamo(id_equipo, id_estudiante, cantidad, "Estudiante " + id_estudiante)

    def consultar_prestamos_activos(self):
        lista_prestamos = []
        for prestamo in self.prestamos:
            if prestamo.estado == "Activo":
                lista_prestamos.append(prestamo)
        return lista_prestamos

    def consultar_estado_prestamo(self, id_estudiante):
        lista_prestamos = []
        for prestamo in self.prestamos:
            if prestamo.id_estudiante == id_estudiante:
                lista_prestamos.append(prestamo)
        return lista_prestamos

    def consultar_historial(self, encargado):
        if encargado is None or encargado not in self.encargados:
            raise PermissionError("Solo el encargado puede consultar el historial")
        return self.historial

  
    def consultar_estudiante(self, id_estudiante):
        estudiante_encontrado = None
        for est in self.estudiantes:
            if est.id == id_estudiante:
                estudiante_encontrado = est
        return estudiante_encontrado

    def registrar_estudiante(self, id_estudiante, contrasena, correo, telefono):
        for est in self.estudiantes:
            if est.id == id_estudiante:
                return "ERROR: El estudiante ya se encuentra registrado."
        nuevo_estudiante = Estudiante(id_estudiante, "Activo", contrasena, correo, "Estudiante", telefono)
        self.estudiantes.append(nuevo_estudiante)
        return "Estudiante registrado exitosamente."

    def actualizar_info_estudiante(self, id_estudiante, correo, telefono):
        estudiante_encontrado = self.consultar_estudiante(id_estudiante)
        if estudiante_encontrado is None:
            return "ERROR: estudiante no encontrado"
        estudiante_encontrado.correo = correo
        estudiante_encontrado.telefono = telefono
        return "Informacion actualizada"
