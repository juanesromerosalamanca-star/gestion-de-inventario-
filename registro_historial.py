class RegistroHistorial:
   

    def __init__(self, id, fecha, hora, accion, id_prestamo,id_equipo,nombre_equipo, id_estudiante, cantidad, registrado_por):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.accion = accion                 
        self.id_prestamo = id_prestamo
        self.id_equipo = id_equipo
        self.nombre_equipo = nombre_equipo
        self.id_estudiante = id_estudiante
        self.cantidad = cantidad
        self.registrado_por = registrado_por
