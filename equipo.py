class Equipo:
    def __init__(self, id, nombre, categoria, cantidad, estado, prestados=0):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad = cantidad     
        self.estado = estado
        self.prestados = prestados    

    @property
    def disponibles(self):
        # Ejemplo: 12 en total, 1 prestado -> 11 disponibles
        return self.cantidad - self.prestados

    def actualizar_estado(self):
        if self.disponibles <= 0:
            self.estado = "Agotado/Prestado"
        else:
            self.estado = "Disponible"
