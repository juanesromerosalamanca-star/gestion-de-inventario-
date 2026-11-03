from registro_estudiante import RegistroEstudiante


class BaseDatos:

  def __init__(self, archivo):
    self.archivo = archivo
    self.estudiante = []
    self.cargar_estudiantes()

  def cargar_estudiantes(self):
    try:
      archivo_estudiantes = open(self.archivo, "r")
    except FileNotFoundError:
      return
    while True:
      documento = archivo_estudiantes.readline()
      if documento == "":
        break
      nombre = archivo_estudiantes.readline()
      telefono = archivo_estudiantes.readline()
      direccion = archivo_estudiantes.readline()
      estado = archivo_estudiantes.readline()
      estudiante = RegistroEstudiante(
          documento.strip(),
          nombre.strip(),
          telefono.strip(),
          direccion.strip(),
          estado.strip(),
      )
      self.estudiante.append(estudiante)
    archivo_estudiantes.close()

  def guardar_estudiantes(self):
    archivo_estudiante = open(self.archivo, "w")
    for estudiante in self.estudiante:
      archivo_estudiante.write(estudiante.documento + "\n")
      archivo_estudiante.write(estudiante.nombre + "\n")
      archivo_estudiante.write(estudiante.telefono + "\n")
      archivo_estudiante.write(estudiante.direccion + "\n")
      archivo_estudiante.write(estudiante.estado + "\n")
    archivo_estudiante.close()

  def buscar_estudiante(self, documento):
    estudiante_encontrado = None
    for estudiante in self.estudiante:
      if estudiante.documento == documento:
        estudiante_encontrado = estudiante
    return estudiante_encontrado

  def agregar_estudiante(self, documento, nombre, telefono, direccion):
    estudiante_encontrado = self.buscar_estudiante(documento)
    if estudiante_encontrado is not None:
      return "ERROR: ya existe un estudiante con ese documento"
    estudiante = RegistroEstudiante(
        documento, nombre, telefono, direccion, "Activo"
    )
    self.estudiante.append(estudiante)
    return "Estudiante agregado a la base de datos"

  def consultar_estudiante(self):
    return self.estudiante