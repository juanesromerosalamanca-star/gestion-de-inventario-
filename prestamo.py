class Prestamo:
    def __init__(self, id, id_equipo, id_estudiante, cantidad, fecha, hora, estado, registrado_por, fecha_devolucion="",hora_devolucion="", recibido_por=""):
        self.id = id
        self.id_equipo = id_equipo
        self.id_estudiante = id_estudiante
        self.cantidad = cantidad
        self.fecha = fecha
        self.hora = hora
        self.estado = estado
        self.registrado_por = registrado_por     
        self.fecha_devolucion = fecha_devolucion
        self.hora_devolucion = hora_devolucion
        self.recibido_por = recibido_por         
