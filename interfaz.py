import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from Administrador import Administrador
from equipo import Equipo
from Estudiante import Estudiante
from inventario import Inventario


class SistemaInventarioApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema de Gestión de Inventario y Préstamos")
    self.root.geometry("750x600")

  
    self.inventario = Inventario()
    self.inventario.cargar_equipos("equipos.txt")
    self.inventario.cargar_estudiantes("estudiantes.txt")
    self.inventario.cargar_encargados("encargados.txt")
    self.inventario.cargar_prestamos("prestamos.txt")
    self.inventario.cargar_historial("historial.txt")

    self.inicializar_datos_defecto()
    self.inventario.recalcular_stock()

    
    self.encargado_actual = None



    self.lbl_reloj = tk.Label(
        self.root, font=("Arial", 10)
    )
    self.lbl_reloj.place(relx=0.5, rely=0.99, anchor="s")
    self.actualizar_reloj()

    self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
    self.mostrar_menu_principal()

  def inicializar_datos_defecto(self):
    if len(self.inventario.equipos) == 0:
      equipos_def = [
          Equipo("E01", "Multimetro Digital", "Medicion", 5, "Disponible"),
          Equipo("E02", "Osciloscopio", "Medicion", 3, "Disponible"),
          Equipo("E03", "Fuente de Poder DC", "Alimentacion", 4, "Disponible"),
          Equipo("E04", "Generador de Funciones", "Medicion", 2, "Disponible"),
          Equipo("E05", "Protoboard", "Montaje", 10, "Disponible"),
          Equipo("E06", "Soldador de Estano", "Herramienta", 6, "Disponible"),
          Equipo("E07", "Pinza Amperimetrica", "Medicion", 3, "Disponible"),
          Equipo("E08", "Kit de Resistencias", "Componentes", 15, "Disponible"),
          Equipo("E09", "Kit de Capacitores", "Componentes", 15, "Disponible"),
          Equipo("E10", "Kit de Transistores NPN", "Componentes", 10, "Disponible"),
      ]
      for eq in equipos_def:
        self.inventario.registrar_producto(eq)

    if len(self.inventario.encargados) == 0:
      self.inventario.encargados.append(
          Administrador("EN01", "admin", "1234", "admin@lab.com", "Encargado")
      )

    if len(self.inventario.estudiantes) == 0:
      self.inventario.estudiantes.append(
          Estudiante(
              "ES01",
              "Activo",
              "1234",
              "estudiante1@correo.com",
              "Estudiante",
              "3001234567",
          )
      )

  def actualizar_reloj(self):
    self.lbl_reloj.config(text=datetime.now().strftime("%d/%m/%Y   %H:%M:%S"))
    self.root.after(1000, self.actualizar_reloj)

  def limpiar_ventana(self):
    for widget in self.root.winfo_children():
      if widget is not self.lbl_reloj:
        widget.destroy()

  def guardar_todo(self):

    self.inventario.guardar_equipos("equipos.txt")
    self.inventario.guardar_estudiantes("estudiantes.txt")
    self.inventario.guardar_encargados("encargados.txt")
    self.inventario.guardar_prestamos("prestamos.txt")
    self.inventario.guardar_historial("historial.txt")

  def mostrar_resultado(self, res):

    if res.startswith("ERROR"):
      messagebox.showerror("Error", res)
      return False
    messagebox.showinfo("Resultado", res)
    return True

  def boton_menu(self, frame, texto, comando):
    tk.Button(
        frame,
        text=texto,
        command=comando,
        font=("Arial", 10),
        width=32,
        pady=6,
    ).pack(pady=5)

  def tabla_en_vivo(self, parent, columnas, obtener_filas, anchos=None,
                    intervalo=1000):
    """Crea una tabla que se vuelve a llenar sola cada 'intervalo' ms,
    así siempre muestra el estado real del inventario."""
    if anchos is None:
      anchos = {}

    contenedor = tk.Frame(parent)
    contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree = ttk.Treeview(contenedor, columns=columnas, show="headings")
    for col in columnas:
      tree.heading(col, text=col)
      tree.column(col, width=anchos.get(col, 90), anchor="center")

    scroll = ttk.Scrollbar(contenedor, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def refrescar():
      if not tree.winfo_exists():
        return
      seleccionado = None
      if tree.selection():
        seleccionado = str(tree.item(tree.selection()[0])["values"][0])
      tree.delete(*tree.get_children())
      for fila in obtener_filas():
        item = tree.insert("", tk.END, values=fila)
        if seleccionado is not None and str(fila[0]) == seleccionado:
          tree.selection_set(item)
      tree.after(intervalo, refrescar)

    refrescar()
    return tree

  def vincular_disponibilidad(self, top, entry_equipo):

    lbl = tk.Label(top, text="", font=("Arial", 9))
    lbl.pack(pady=2)

    def actualizar(event=None):
      id_equipo = entry_equipo.get().strip()
      if id_equipo == "":
        lbl.config(text="")
        return
      eq = self.inventario.buscar_equipo(id_equipo)
      if eq is None:
        lbl.config(text="Equipo no encontrado")
      else:
        lbl.config(
            text=f"{eq.nombre}: {eq.disponibles} disponibles de {eq.cantidad} ({eq.prestados} prestados)",
        )

    entry_equipo.bind("<KeyRelease>", actualizar)


  def mostrar_menu_principal(self):
    self.limpiar_ventana()
    self.encargado_actual = None  

    frame = tk.Frame(self.root, bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=420, height=300)

    tk.Label(
        frame,
        text="Sistema de Laboratorio",
        font=("Arial", 16, "bold"),
    ).pack(pady=20)

    tk.Button(
        frame,
        text="Ingresar como Encargado",
        font=("Arial", 11),
        width=28,
        pady=8,
        command=self.login_encargado,
    ).pack(pady=8)

    tk.Button(
        frame,
        text="Ingresar como Estudiante",
        font=("Arial", 11),
        width=28,
        pady=8,
        command=self.login_estudiante,
    ).pack(pady=8)

    tk.Button(
        frame,
        text="Guardar y Salir",
        font=("Arial", 11),
        width=28,
        pady=8,
        command=self.guardar_y_salir,
    ).pack(pady=8)

  def guardar_y_salir(self):
    self.guardar_todo()
    messagebox.showinfo("Guardado", "Datos guardados exitosamente. Hasta luego.")
    self.root.quit()

  def cerrar_ventana(self):
    self.guardar_todo()
    self.root.destroy()

  def login_encargado(self):
    self.limpiar_ventana()

    frame = tk.Frame(self.root, bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=300)

    tk.Label(
        frame,
        text="Login Encargado",
        font=("Arial", 14, "bold"),
    ).pack(pady=15)

    tk.Label(frame, text="Cuenta:", font=("Arial", 10)).pack(
        anchor="w", padx=40
    )
    entry_cuenta = tk.Entry(frame, font=("Arial", 11), width=28)
    entry_cuenta.pack(pady=5, padx=40)

    tk.Label(
        frame, text="Contraseña:", font=("Arial", 10)
    ).pack(anchor="w", padx=40)
    entry_pass = tk.Entry(frame, font=("Arial", 11), width=28, show="*")
    entry_pass.pack(pady=5, padx=40)

    def verificar():
      cuenta = entry_cuenta.get()
      contrasena = entry_pass.get()
      encargado_encontrado = None
      for enc in self.inventario.encargados:
        if enc.cuenta == cuenta and enc.contrasena == contrasena:
          encargado_encontrado = enc
          break

      if encargado_encontrado:
        self.encargado_actual = encargado_encontrado
        self.panel_encargado()
      else:
        messagebox.showerror("Error", "Cuenta o contraseña incorrecta")

    tk.Button(
        frame,
        text="Ingresar",
        font=("Arial", 10, "bold"),
        width=20,
        command=verificar,
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Volver",
        font=("Arial", 10),
        width=20,
        command=self.mostrar_menu_principal,
    ).pack(pady=2)

  def panel_encargado(self):
    self.limpiar_ventana()

    frame = tk.Frame(self.root, bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=460)

    tk.Label(
        frame,
        text="Panel de Administrador / Encargado",
        font=("Arial", 14, "bold"),
    ).pack(pady=15)

    self.boton_menu(frame, "1. Registrar Equipo", self.v_registrar_equipo)
    self.boton_menu(frame, "2. Consultar Inventario", self.v_consultar_inventario_encargado)
    self.boton_menu(frame, "3. Registrar Préstamo", self.v_registrar_prestamo)
    self.boton_menu(frame, "4. Registrar Devolución", self.v_registrar_devolucion)
    self.boton_menu(frame, "5. Consultar Estudiante", self.v_consultar_estudiante_encargado)
    self.boton_menu(frame, "6. Historial de Préstamos", self.v_historial)

    tk.Button(
        frame,
        text="Cerrar sesión / Menú Principal",
        font=("Arial", 10),
        width=32,
        command=self.mostrar_menu_principal,
    ).pack(pady=10)

  def v_registrar_equipo(self):
    top = tk.Toplevel(self.root)
    top.title("Registrar Equipo")
    top.geometry("350x320")

    tk.Label(top, text="ID del equipo:").pack(pady=5)
    e_id = tk.Entry(top, width=30)
    e_id.pack()

    tk.Label(top, text="Nombre:").pack(pady=5)
    e_nom = tk.Entry(top, width=30)
    e_nom.pack()

    tk.Label(top, text="Categoría:").pack(pady=5)
    e_cat = tk.Entry(top, width=30)
    e_cat.pack()

    tk.Label(top, text="Cantidad total:").pack(pady=5)
    e_cant = tk.Entry(top, width=30)
    e_cant.pack()

    def guardar():
      try:
        cant = int(e_cant.get())
      except ValueError:
        messagebox.showerror("Error", "La cantidad debe ser un número entero.")
        return
      eq = Equipo(e_id.get().strip(), e_nom.get().strip(), e_cat.get().strip(), cant, "Disponible")
      res = self.inventario.registrar_producto(eq)
      if self.mostrar_resultado(res):
        self.guardar_todo()
        top.destroy()

    tk.Button(
        top,
        text="Guardar",
        command=guardar,
        width=15,
    ).pack(pady=15)

  def v_consultar_inventario_encargado(self):
    top = tk.Toplevel(self.root)
    top.title("Inventario de Equipos (en tiempo real)")
    top.geometry("760x380")

    columnas = ("ID", "Nombre", "Categoría", "Total", "Prestados", "Disponibles", "Estado")

    def filas():
      return [
          (eq.id, eq.nombre, eq.categoria, eq.cantidad, eq.prestados, eq.disponibles, eq.estado)
          for eq in self.inventario.consultar_inventario()
      ]

    self.tabla_en_vivo(top, columnas, filas, {"Nombre": 180, "Estado": 130})

  def v_registrar_prestamo(self):
    top = tk.Toplevel(self.root)
    top.title("Registrar Préstamo")
    top.geometry("400x320")

    tk.Label(top, text="ID del equipo:").pack(pady=5)
    e_eq = tk.Entry(top, width=30)
    e_eq.pack()
    self.vincular_disponibilidad(top, e_eq)

    tk.Label(top, text="ID del estudiante:").pack(pady=5)
    e_est = tk.Entry(top, width=30)
    e_est.pack()

    tk.Label(top, text="Cantidad a prestar:").pack(pady=5)
    e_cant = tk.Entry(top, width=30)
    e_cant.insert(0, "1")
    e_cant.pack()

    tk.Label(
        top,
        text="La fecha y la hora se registran automáticamente.",
        font=("Arial", 9),
    ).pack(pady=8)

    def registrar():
      try:
        cantidad = int(e_cant.get())
      except ValueError:
        messagebox.showerror("Error", "La cantidad debe ser un número entero.")
        return
      res = self.inventario.registrar_prestamo(
          e_eq.get().strip(),
          e_est.get().strip(),
          cantidad,
          self.encargado_actual.cuenta,
      )
      if self.mostrar_resultado(res):
        self.guardar_todo()
        top.destroy()

    tk.Button(
        top,
        text="Registrar Préstamo",
        command=registrar,
    ).pack(pady=10)

  def v_registrar_devolucion(self):
    top = tk.Toplevel(self.root)
    top.title("Registrar Devolución - Préstamos activos")
    top.geometry("700x400")


    panel = tk.Frame(top)
    panel.pack(side=tk.BOTTOM, fill=tk.X, pady=8)

    tk.Label(panel, text="ID del préstamo:").pack(side=tk.LEFT, padx=8)
    e_pres = tk.Entry(panel, width=10)
    e_pres.pack(side=tk.LEFT)

    columnas = ("ID Préstamo", "Equipo", "Estudiante", "Cantidad", "Fecha", "Hora")

    def filas():
      resultado = []
      for p in self.inventario.consultar_prestamos_activos():
        eq = self.inventario.buscar_equipo(p.id_equipo)
        nombre = eq.nombre if eq is not None else p.id_equipo
        resultado.append((p.id, nombre, p.id_estudiante, p.cantidad, p.fecha, p.hora))
      return resultado

    tree = self.tabla_en_vivo(top, columnas, filas, {"Equipo": 170})

    def al_seleccionar(event):
      seleccion = tree.selection()
      if seleccion:
        e_pres.delete(0, tk.END)
        e_pres.insert(0, str(tree.item(seleccion[0])["values"][0]))

    tree.bind("<<TreeviewSelect>>", al_seleccionar)

    def devolver():
      res = self.inventario.registrar_devolucion(
          e_pres.get().strip(), self.encargado_actual.cuenta
      )
      if self.mostrar_resultado(res):
        self.guardar_todo()
        e_pres.delete(0, tk.END)

    tk.Button(
        panel,
        text="Procesar Devolución",
        command=devolver,
    ).pack(side=tk.LEFT, padx=10)

  def v_consultar_estudiante_encargado(self):
    top = tk.Toplevel(self.root)
    top.title("Consultar Estudiante")
    top.geometry("350x220")

    tk.Label(top, text="ID del estudiante:").pack(pady=5)
    e_est = tk.Entry(top, width=25)
    e_est.pack(pady=5)

    lbl_resultado = tk.Label(top, text="", font=("Arial", 10), justify="left")
    lbl_resultado.pack(pady=5)

    def buscar():
      est = self.inventario.consultar_estudiante(e_est.get().strip())
      if est is None:
        lbl_resultado.config(text="Estudiante no encontrado")
      else:
        texto = f"ID: {est.id}\nEstado: {est.estado}\nCorreo: {est.correo}\nTeléfono: {est.telefono}"
        lbl_resultado.config(text=texto)

    tk.Button(
        top, text="Buscar", command=buscar
    ).pack(pady=5)

  def v_historial(self):

    try:
      self.inventario.consultar_historial(self.encargado_actual)
    except PermissionError:
      messagebox.showerror(
          "Acceso denegado", "Solo el encargado puede ver el historial."
      )
      return

    top = tk.Toplevel(self.root)
    top.title("Historial de Préstamos y Devoluciones (en tiempo real)")
    top.geometry("1250x520")

    barra = tk.Frame(top)
    barra.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)
    tk.Label(barra, text="Buscar (estudiante, equipo, fecha, acción...):").pack(side=tk.LEFT)
    e_buscar = tk.Entry(barra, width=35)
    e_buscar.pack(side=tk.LEFT, padx=8)
    lbl_total = tk.Label(barra, text="", font=("Arial", 9))
    lbl_total.pack(side=tk.RIGHT)

    columnas = (
        "ID", "Fecha", "Hora", "Acción", "ID Préstamo", "ID Equipo", "Equipo",
        "Cantidad", "ID Estudiante", "Correo", "Teléfono", "Registrado por",
    )
    anchos = {
        "ID": 40, "Fecha": 85, "Hora": 75, "Acción": 90, "ID Préstamo": 80,
        "ID Equipo": 70, "Equipo": 170, "Cantidad": 65, "ID Estudiante": 90,
        "Correo": 180, "Teléfono": 95, "Registrado por": 120,
    }

    def filas():
      filtro = e_buscar.get().strip().lower()
      resultado = []
  
      for h in reversed(self.inventario.consultar_historial(self.encargado_actual)):
        est = self.inventario.consultar_estudiante(h.id_estudiante)
        correo = est.correo if est is not None else "-"
        telefono = est.telefono if est is not None else "-"
        fila = (
            h.id, h.fecha, h.hora, h.accion, h.id_prestamo, h.id_equipo,
            h.nombre_equipo, h.cantidad, h.id_estudiante, correo, telefono,
            h.registrado_por,
        )
        texto = " ".join(str(dato).lower() for dato in fila)
        if filtro == "" or filtro in texto:
          resultado.append(fila)
      lbl_total.config(text=f"Registros mostrados: {len(resultado)}")
      return resultado

    self.tabla_en_vivo(top, columnas, filas, anchos)


  def login_estudiante(self):
    self.limpiar_ventana()

    frame = tk.Frame(self.root, bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=300)

    tk.Label(
        frame,
        text="Login Estudiante",
        font=("Arial", 14, "bold"),
    ).pack(pady=15)

    tk.Label(frame, text="ID Estudiante:", font=("Arial", 10)).pack(
        anchor="w", padx=40
    )
    entry_id = tk.Entry(frame, font=("Arial", 11), width=28)
    entry_id.pack(pady=5, padx=40)

    tk.Label(
        frame, text="Contraseña:", font=("Arial", 10)
    ).pack(anchor="w", padx=40)
    entry_pass = tk.Entry(frame, font=("Arial", 11), width=28, show="*")
    entry_pass.pack(pady=5, padx=40)

    def verificar():
      id_est = entry_id.get()
      contrasena = entry_pass.get()
      est_encontrado = None
      for est in self.inventario.estudiantes:
        if est.id == id_est and est.contrasena == contrasena:
          est_encontrado = est
          break

      if est_encontrado:
        self.panel_estudiante(est_encontrado)
      else:
        messagebox.showerror("Error", "Cuenta o contraseña incorrecta")

    tk.Button(
        frame,
        text="Ingresar",
        font=("Arial", 10, "bold"),
        width=20,
        command=verificar,
    ).pack(pady=10)

    tk.Button(
        frame,
        text="Volver",
        font=("Arial", 10),
        width=20,
        command=self.mostrar_menu_principal,
    ).pack(pady=2)

  def panel_estudiante(self, estudiante_actual):
    self.limpiar_ventana()

    frame = tk.Frame(self.root, bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=380)

    tk.Label(
        frame,
        text=f"Panel Estudiante: {estudiante_actual.id}",
        font=("Arial", 13, "bold"),
    ).pack(pady=15)

    self.boton_menu(frame, "1. Consultar Inventario", self.v_consultar_inventario_estudiante)
    self.boton_menu(frame, "2. Solicitar Préstamo", lambda: self.v_solicitar_prestamo(estudiante_actual))
    self.boton_menu(frame, "3. Actualizar Información", lambda: self.v_actualizar_info(estudiante_actual))
    self.boton_menu(frame, "4. Consultar Estado de Préstamos", lambda: self.v_consultar_prestamos_estudiante(estudiante_actual))

    tk.Button(
        frame,
        text="Volver al Menú Principal",
        font=("Arial", 10),
        width=32,
        command=self.mostrar_menu_principal,
    ).pack(pady=10)

  def v_consultar_inventario_estudiante(self):
    top = tk.Toplevel(self.root)
    top.title("Inventario Disponible (en tiempo real)")
    top.geometry("700x350")

    columnas = ("ID", "Nombre", "Categoría", "Disponibles", "Total", "Estado")

    def filas():
      return [
          (eq.id, eq.nombre, eq.categoria, eq.disponibles, eq.cantidad, eq.estado)
          for eq in self.inventario.consultar_inventario()
      ]

    self.tabla_en_vivo(top, columnas, filas, {"Nombre": 180, "Estado": 130})

  def v_solicitar_prestamo(self, estudiante_actual):
    top = tk.Toplevel(self.root)
    top.title("Solicitar Préstamo")
    top.geometry("400x280")

    tk.Label(top, text="ID del equipo a solicitar:").pack(pady=5)
    e_eq = tk.Entry(top, width=25)
    e_eq.pack(pady=5)
    self.vincular_disponibilidad(top, e_eq)

    tk.Label(top, text="Cantidad:").pack(pady=5)
    e_cant = tk.Entry(top, width=25)
    e_cant.insert(0, "1")
    e_cant.pack(pady=5)

    tk.Label(
        top,
        text="La fecha y la hora se registran automáticamente.",
        font=("Arial", 9),
    ).pack(pady=5)

    def solicitar():
      try:
        cantidad = int(e_cant.get())
      except ValueError:
        messagebox.showerror("Error", "La cantidad debe ser un número entero.")
        return
      res = self.inventario.solicitar_prestamo(
          estudiante_actual.id, e_eq.get().strip(), cantidad
      )
      if self.mostrar_resultado(res):
        self.guardar_todo()
        top.destroy()

    tk.Button(
        top, text="Solicitar", command=solicitar
    ).pack(pady=10)

  def v_actualizar_info(self, estudiante_actual):
    top = tk.Toplevel(self.root)
    top.title("Actualizar Información")
    top.geometry("350x240")

    tk.Label(top, text="Nuevo correo:").pack(pady=5)
    e_corr = tk.Entry(top, width=28)
    e_corr.insert(0, estudiante_actual.correo)
    e_corr.pack(pady=5)

    tk.Label(top, text="Nuevo teléfono:").pack(pady=5)
    e_tel = tk.Entry(top, width=28)
    e_tel.insert(0, estudiante_actual.telefono)
    e_tel.pack(pady=5)

    def actualizar():
      res = self.inventario.actualizar_info_estudiante(
          estudiante_actual.id, e_corr.get().strip(), e_tel.get().strip()
      )
      if self.mostrar_resultado(res):
        self.guardar_todo()
        top.destroy()

    tk.Button(
        top,
        text="Actualizar",
        command=actualizar,
    ).pack(pady=10)

  def v_consultar_prestamos_estudiante(self, estudiante_actual):
    top = tk.Toplevel(self.root)
    top.title("Mis Préstamos (en tiempo real)")
    top.geometry("780x320")

    columnas = (
        "ID Préstamo", "Equipo", "Cantidad", "Fecha", "Hora", "Estado",
        "Devuelto el",
    )

    def filas():
      resultado = []
      for p in self.inventario.consultar_estado_prestamo(estudiante_actual.id):
        eq = self.inventario.buscar_equipo(p.id_equipo)
        nombre = eq.nombre if eq is not None else p.id_equipo
        devuelto = (p.fecha_devolucion + " " + p.hora_devolucion).strip()
        resultado.append((p.id, nombre, p.cantidad, p.fecha, p.hora, p.estado, devuelto if devuelto else "-"))
      return resultado

    self.tabla_en_vivo(top, columnas, filas, {"Equipo": 170, "Devuelto el": 150})
