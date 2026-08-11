import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from modelos import Paciente, Actividad, ResultadoTest, Usuario
from servicios import MENUS_POR_ROL

MENU_POR_DEFECTO = [
    ("Registrar paciente", "registrar_paciente"),
    ("Registrar especialista", "registro_rol"),
    ("Cuestionario", "cuestionario"),
    ("Crear actividad", "crear_actividad"),
    ("Agendar actividad", "agendar"),
    ("Reportes", "reportes"),
]

class Tema:
    FONDO = "#F4F6F9"
    TEXTO = "#333333"
    MARCA = "#2C3E50"
    BOTON = "#3498DB"
    BOTON_TEXTO = "#FFFFFF"

    @staticmethod
    def fuente(tamano, bold=False):
        return ("Helvetica", tamano, "bold" if bold else "normal")

class PantallaBase(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=Tema.FONDO)
        self.app = app
        self.cuerpo = tk.Frame(self, bg=Tema.FONDO)
        self.cuerpo.pack(fill="both", expand=True)

class PantallaLogin(PantallaBase):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.var_usuario = tk.StringVar()
        self.var_clave = tk.StringVar()
        self._construir()

    def _construir(self):
        marco = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(marco, text="Iniciar Sesión", font=Tema.fuente(16, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=20)

        tk.Label(marco, text="Usuario o Correo:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        tk.Entry(marco, textvariable=self.var_usuario, width=30, font=Tema.fuente(10)).pack(pady=5)

        tk.Label(marco, text="Contraseña:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        tk.Entry(marco, textvariable=self.var_clave, show="*", width=30, font=Tema.fuente(10)).pack(pady=5)

        tk.Button(marco, text="Ingresar", bg=Tema.BOTON, fg=Tema.BOTON_TEXTO, font=Tema.fuente(11, bold=True), width=15, command=self._login).pack(pady=20)
        tk.Button(marco, text="Registrarse", bg="#95A5A6", fg=Tema.BOTON_TEXTO, font=Tema.fuente(10), width=15, command=lambda: self.app.mostrar("registro_usuario")).pack(pady=5)

    def _login(self):
        usr = self.var_usuario.get()
        pas = self.var_clave.get()
        usuario = self.app.repos.usuario.autenticar(usr, pas)
        if usuario:
            self.app.usuario_actual = usuario
            self.app.mostrar("menu")
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

class PantallaRegistroUsuario(PantallaBase):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.var_usuario = tk.StringVar()
        self.var_clave = tk.StringVar()
        self.var_correo = tk.StringVar()
        self._construir()

    def _construir(self):
        marco = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(marco, text="Registro de Usuario", font=Tema.fuente(16, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=15)

        tk.Label(marco, text="Nombre de Usuario:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        tk.Entry(marco, textvariable=self.var_usuario, width=30, font=Tema.fuente(10)).pack(pady=5)

        tk.Label(marco, text="Correo Electrónico:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        tk.Entry(marco, textvariable=self.var_correo, width=30, font=Tema.fuente(10)).pack(pady=5)

        tk.Label(marco, text="Contraseña:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        tk.Entry(marco, textvariable=self.var_clave, show="*", width=30, font=Tema.fuente(10)).pack(pady=5)

        tk.Button(marco, text="Registrar", bg=Tema.BOTON, fg=Tema.BOTON_TEXTO, font=Tema.fuente(11, bold=True), width=15, command=self._registrar).pack(pady=15)
        tk.Button(marco, text="Volver", bg="#95A5A6", fg=Tema.BOTON_TEXTO, font=Tema.fuente(10), width=15, command=lambda: self.app.mostrar("login")).pack(pady=5)

    def _registrar(self):
        usr = self.var_usuario.get()
        correo = self.var_correo.get()
        pas = self.var_clave.get()
        if not usr or not correo or not pas:
            messagebox.showwarning("Advertencia", "Complete todos los campos.")
            return

        nuevo_usuario = Usuario(nombre_usuario=usr, correo=correo, contrasena=pas)
        self.app.repos.usuario.crear(nuevo_usuario)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        self.app.mostrar("login")

class PantallaRegistroRol(PantallaBase):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.var_nombre = tk.StringVar()
        self.var_desc = tk.StringVar()
        self._construir()

    def _construir(self):
        marco = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(marco, text="Registrar Especialista", font=Tema.fuente(16, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=15)

        tk.Label(marco, text="Nombre:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        tk.Entry(marco, textvariable=self.var_nombre, width=30, font=Tema.fuente(10)).pack(pady=5)

        tk.Label(marco, text="Descripción / Especialidad:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        tk.Entry(marco, textvariable=self.var_desc, width=30, font=Tema.fuente(10)).pack(pady=5)

        tk.Button(marco, text="Guardar", bg=Tema.BOTON, fg=Tema.BOTON_TEXTO, font=Tema.fuente(11, bold=True), width=15, command=self._guardar).pack(pady=15)
        tk.Button(marco, text="Volver", bg="#95A5A6", fg=Tema.BOTON_TEXTO, font=Tema.fuente(10), width=15, command=lambda: self.app.mostrar("menu")).pack(pady=5)

    def _guardar(self):
        nombre = self.var_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingrese el nombre del especialista.")
            return
        self.app.repos.especialista.crear({"nombre": nombre, "descripcion": self.var_desc.get().strip()})
        messagebox.showinfo("Éxito", f"Especialista '{nombre}' registrado correctamente.")
        self.app.mostrar("menu")

class PantallaMenu(PantallaBase):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self._construir()

    def _construir(self):
        usuario = self.app.usuario_actual
        nombre = usuario.nombre_usuario if usuario else "Invitado"
        rol = usuario.rol if usuario else "Usuario"

        tk.Label(self.cuerpo, text="NeoAtención", font=Tema.fuente(20, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=(40, 5))
        tk.Label(self.cuerpo, text=f"Bienvenido, {nombre}  ·  Rol: {rol}", font=Tema.fuente(11), bg=Tema.FONDO, fg=Tema.TEXTO).pack(pady=(0, 30))

        opciones = MENUS_POR_ROL.get(rol, MENU_POR_DEFECTO)
        marco = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco.pack()
        for texto, vista in opciones:
            if vista == "menu":
                continue
            tk.Button(marco, text=texto, bg=Tema.BOTON, fg=Tema.BOTON_TEXTO,
                      font=Tema.fuente(12, bold=True), width=25,
                      command=lambda v=vista: self.app.mostrar(v)).pack(pady=6)

        tk.Button(self.cuerpo, text="Cerrar sesión", bg="#95A5A6", fg=Tema.BOTON_TEXTO,
                  font=Tema.fuente(10), width=25,
                  command=lambda: self.app.mostrar("login")).pack(pady=(30, 0))

class PantallaRegistrarPaciente(PantallaBase):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_edad = tk.StringVar()
        self.var_nivel = tk.StringVar()
        self._construir()

    def _construir(self):
        marco = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(marco, text="Registrar Paciente", font=Tema.fuente(16, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=15)

        campos = [
            ("Nombre:", self.var_nombre),
            ("Apellido:", self.var_apellido),
            ("Edad:", self.var_edad),
            ("Nivel escolar:", self.var_nivel),
        ]
        for etiqueta, var in campos:
            tk.Label(marco, text=etiqueta, bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
            tk.Entry(marco, textvariable=var, width=30, font=Tema.fuente(10)).pack(pady=5)

        tk.Button(marco, text="Guardar", bg=Tema.BOTON, fg=Tema.BOTON_TEXTO, font=Tema.fuente(11, bold=True), width=15, command=self._guardar).pack(pady=15)
        tk.Button(marco, text="Volver", bg="#95A5A6", fg=Tema.BOTON_TEXTO, font=Tema.fuente(10), width=15, command=lambda: self.app.mostrar("menu")).pack(pady=5)

    def _guardar(self):
        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        edad_txt = self.var_edad.get().strip()
        nivel = self.var_nivel.get().strip()

        if not nombre or not apellido or not edad_txt:
            messagebox.showwarning("Advertencia", "Complete nombre, apellido y edad.")
            return
        if not edad_txt.isdigit():
            messagebox.showwarning("Advertencia", "La edad debe ser un número.")
            return

        usuario = self.app.usuario_actual
        id_tutor = self.app.repos.tutor.id_por_usuario(usuario.id) if usuario else None
        paciente = Paciente(nombre=nombre, apellido=apellido, edad=int(edad_txt),
                            nivel_escolar=nivel, id_tutor_padre=id_tutor)
        self.app.repos.paciente.crear(paciente)
        messagebox.showinfo("Éxito", "Paciente registrado correctamente.")
        self.app.mostrar("menu")

class PantallaCuestionario(PantallaBase):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.vars_ina = []
        self.vars_hip = []
        self.var_pac = tk.StringVar()
        self._construir()

    def _construir(self):
        tk.Label(self.cuerpo, text="Evaluación TDAH", font=Tema.fuente(16, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=20)

        marco_paciente = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco_paciente.pack(pady=10)
        tk.Label(marco_paciente, text="Seleccionar Paciente:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(side="left", padx=5)

        self.combo_pacientes = ttk.Combobox(marco_paciente, textvariable=self.var_pac, state="readonly", width=40)
        self.combo_pacientes.pack(side="left", padx=5)
        self.combo_pacientes.bind("<Button-1>", self._cargar_pacientes)

        marco_preguntas = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco_preguntas.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(marco_preguntas, text="Sección Inatención (0-3)", font=Tema.fuente(12, bold=True), bg=Tema.FONDO).grid(row=0, column=0, pady=10, sticky="w")
        for i in range(9):
            var = tk.IntVar()
            self.vars_ina.append(var)
            tk.Label(marco_preguntas, text=f"Pregunta Inatención {i+1}:", bg=Tema.FONDO).grid(row=i+1, column=0, sticky="w")
            tk.Spinbox(marco_preguntas, from_=0, to=3, textvariable=var, width=5).grid(row=i+1, column=1, padx=10)

        tk.Label(marco_preguntas, text="Sección Hiperactividad (0-3)", font=Tema.fuente(12, bold=True), bg=Tema.FONDO).grid(row=0, column=2, pady=10, sticky="w", padx=(20, 0))
        for i in range(9):
            var = tk.IntVar()
            self.vars_hip.append(var)
            tk.Label(marco_preguntas, text=f"Pregunta Hiperactividad {i+1}:", bg=Tema.FONDO).grid(row=i+1, column=2, sticky="w", padx=(20, 0))
            tk.Spinbox(marco_preguntas, from_=0, to=3, textvariable=var, width=5).grid(row=i+1, column=3, padx=10)

        tk.Button(self.cuerpo, text="Guardar Evaluación", bg=Tema.BOTON, fg=Tema.BOTON_TEXTO, font=Tema.fuente(12, bold=True), command=self._guardar).pack(pady=20)
        tk.Button(self.cuerpo, text="Volver al menú", bg="#95A5A6", fg=Tema.BOTON_TEXTO, font=Tema.fuente(10), command=lambda: self.app.mostrar("menu")).pack(pady=(0, 10))

    def _cargar_pacientes(self, event=None):
        pacientes = self.app.repos.paciente.listar()
        valores = [f"{p.id} - {p.nombre} {p.apellido}" for p in pacientes]
        self.combo_pacientes["values"] = valores

    def _guardar(self):
        if not self.var_pac.get():
            messagebox.showwarning("Advertencia", "Seleccione un paciente.")
            return

        id_paciente = int(self.var_pac.get().split(" - ")[0])
        valores_ina = [v.get() for v in self.vars_ina]
        valores_hip = [v.get() for v in self.vars_hip]

        p_ina, p_hip, grupo, nivel = self.app.servicios.cuestionario.evaluar(valores_ina, valores_hip)
        resumen = f"Ina {p_ina}/27 - Hip {p_hip}/27"

        resultado = ResultadoTest(
            id_paciente=id_paciente,
            fecha=str(date.today()),
            puntaje_inatencion=p_ina,
            puntaje_hiperactividad=p_hip,
            grupos_TDAH=grupo,
            nivel_TDAH=nivel
        )

        self.app.repos.paciente.guardar_resultado_test(resultado)
        self.app.repos.paciente.actualizar_resultados(id_paciente, resumen, grupo, nivel)

        messagebox.showinfo("NeoAtención",
                            f"Evaluación guardada.\nInatención: {p_ina}/27\n"
                            f"Hiperactividad: {p_hip}/27\nGrupo: {grupo}\nNivel: {nivel}")
        self.app.mostrar("reportes", id_paciente=id_paciente)

class PantallaCrearActividad(PantallaBase):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.var_nombre = tk.StringVar()
        self.var_desc = tk.StringVar()
        self.var_tipo = tk.StringVar()
        self.var_desig = tk.StringVar()
        self.var_obj = tk.StringVar()
        self._construir()

    def _construir(self):
        marco = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(marco, text="Crear Actividad", font=Tema.fuente(16, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=15)

        campos = [
            ("Nombre:", self.var_nombre),
            ("Descripción:", self.var_desc),
            ("Tipo:", self.var_tipo),
            ("Designación:", self.var_desig),
            ("Objetivo:", self.var_obj),
        ]
        for etiqueta, var in campos:
            tk.Label(marco, text=etiqueta, bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
            tk.Entry(marco, textvariable=var, width=35, font=Tema.fuente(10)).pack(pady=4)

        tk.Button(marco, text="Guardar", bg=Tema.BOTON, fg=Tema.BOTON_TEXTO, font=Tema.fuente(11, bold=True), width=15, command=self._guardar).pack(pady=15)
        tk.Button(marco, text="Volver", bg="#95A5A6", fg=Tema.BOTON_TEXTO, font=Tema.fuente(10), width=15, command=lambda: self.app.mostrar("menu")).pack(pady=5)

    def _guardar(self):
        nombre = self.var_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingrese el nombre de la actividad.")
            return
        actividad = Actividad(
            nombre=nombre,
            descripcion=self.var_desc.get().strip(),
            tipo=self.var_tipo.get().strip(),
            designacion=self.var_desig.get().strip(),
            objetivo=self.var_obj.get().strip()
        )
        self.app.repos.actividad.crear(actividad)
        messagebox.showinfo("Éxito", "Actividad creada correctamente.")
        self.app.mostrar("menu")

class PantallaAgendar(PantallaBase):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.var_pac = tk.StringVar()
        self.var_act = tk.StringVar()
        self.var_esp = tk.StringVar()
        self.var_fecha = tk.StringVar(value=str(date.today()))
        self._pac_map = {}
        self._act_map = {}
        self._esp_map = {}
        self._construir()

    def _construir(self):
        marco = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(marco, text="Agendar Actividad", font=Tema.fuente(16, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=15)

        pacientes = self.app.repos.paciente.listar()
        actividades = self.app.repos.actividad.listar()
        especialistas = self.app.repos.especialista.listar()

        self._pac_map = {f"{p.id} - {p.nombre} {p.apellido}": p.id for p in pacientes}
        self._act_map = {f"{a.id} - {a.nombre}": a.id for a in actividades}
        self._esp_map = {f"{e[0]} - {e[1]}": e[0] for e in especialistas}

        tk.Label(marco, text="Paciente:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        ttk.Combobox(marco, textvariable=self.var_pac, state="readonly", width=40,
                     values=list(self._pac_map.keys())).pack(pady=5)

        tk.Label(marco, text="Actividad:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        ttk.Combobox(marco, textvariable=self.var_act, state="readonly", width=40,
                     values=list(self._act_map.keys())).pack(pady=5)

        tk.Label(marco, text="Especialista:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        ttk.Combobox(marco, textvariable=self.var_esp, state="readonly", width=40,
                     values=list(self._esp_map.keys())).pack(pady=5)

        tk.Label(marco, text="Fecha (AAAA-MM-DD):", bg=Tema.FONDO, font=Tema.fuente(10)).pack(anchor="w")
        tk.Entry(marco, textvariable=self.var_fecha, width=42, font=Tema.fuente(10)).pack(pady=5)

        tk.Button(marco, text="Agendar", bg=Tema.BOTON, fg=Tema.BOTON_TEXTO, font=Tema.fuente(11, bold=True), width=15, command=self._guardar).pack(pady=15)
        tk.Button(marco, text="Volver", bg="#95A5A6", fg=Tema.BOTON_TEXTO, font=Tema.fuente(10), width=15, command=lambda: self.app.mostrar("menu")).pack(pady=5)

    def _guardar(self):
        if not self.var_pac.get() or not self.var_act.get() or not self.var_esp.get():
            messagebox.showwarning("Advertencia", "Seleccione paciente, actividad y especialista.")
            return
        id_pac = self._pac_map[self.var_pac.get()]
        id_act = self._act_map[self.var_act.get()]
        id_esp = self._esp_map[self.var_esp.get()]
        self.app.repos.agenda.agendar(id_pac, id_act, id_esp, self.var_fecha.get().strip())
        messagebox.showinfo("Éxito", "Actividad agendada correctamente.")
        self.app.mostrar("menu")

class PantallaReportes(PantallaBase):
    def __init__(self, parent, app, id_paciente=None):
        super().__init__(parent, app)
        self.var_pac = tk.StringVar()
        self.combo_pac = None
        self.contenedor_datos = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        self._construir_cabecera()
        if id_paciente is not None:
            self.configurar_id(id_paciente)

    def _construir_cabecera(self):
        tk.Label(self.cuerpo, text="Reportes y Expedientes", font=Tema.fuente(16, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(pady=20)

        marco_busqueda = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        marco_busqueda.pack(pady=10)

        tk.Label(marco_busqueda, text="Seleccionar Paciente:", bg=Tema.FONDO, font=Tema.fuente(10)).pack(side="left", padx=5)
        self.combo_pac = ttk.Combobox(marco_busqueda, textvariable=self.var_pac, state="readonly", width=40)
        self.combo_pac.pack(side="left", padx=5)
        self.combo_pac.bind("<<ComboboxSelected>>", lambda e: self._recargar())
        self.combo_pac.bind("<Button-1>", self._cargar_pacientes)

        tk.Button(self.cuerpo, text="Volver al menú", bg="#95A5A6", fg=Tema.BOTON_TEXTO, font=Tema.fuente(10), command=lambda: self.app.mostrar("menu")).pack(pady=(0, 5))

        self.contenedor_datos.pack(fill="both", expand=True, pady=10)

    def _cargar_pacientes(self, event=None):
        pacientes = self.app.repos.paciente.listar()
        valores = [f"{p.id} - {p.nombre} {p.apellido}" for p in pacientes]
        self.combo_pac["values"] = valores

    def configurar_id(self, id_paciente: int):
        self._cargar_pacientes()
        for val in self.combo_pac["values"]:
            if val.startswith(f"{id_paciente} -"):
                self.var_pac.set(val)
                self._recargar()
                break

    def _recargar(self):
        for h in self.contenedor_datos.winfo_children():
            h.destroy()

        if not self.var_pac.get():
            return

        id_paciente = int(self.var_pac.get().split(" - ")[0])
        pacientes = self.app.repos.paciente.listar()
        paciente_actual = next((p for p in pacientes if p.id == id_paciente), None)

        if paciente_actual:
            tk.Label(self.contenedor_datos, text=f"Paciente: {paciente_actual.nombre} {paciente_actual.apellido}", font=Tema.fuente(12, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(anchor="w", padx=40, pady=(10, 5))
            tk.Label(self.contenedor_datos, text=f"Último diagnóstico: {paciente_actual.grupo_TDAH} ({paciente_actual.nivel_TDAH})", font=Tema.fuente(10, bold=True), bg=Tema.FONDO, fg=Tema.TEXTO).pack(anchor="w", padx=40, pady=(0, 10))

            tk.Label(self.contenedor_datos, text="Historial de Evaluaciones:", font=Tema.fuente(12, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(anchor="w", padx=40, pady=(10, 5))

            resultados = self.app.repos.paciente.obtener_resultados_paciente(id_paciente)
            if resultados:
                for res in resultados:
                    texto = f"[{res.fecha}] Inatención: {res.puntaje_inatencion}/27 | Hiperactividad: {res.puntaje_hiperactividad}/27 | Grupo: {res.grupos_TDAH} | Nivel: {res.nivel_TDAH}"
                    tk.Label(self.contenedor_datos, text=texto, font=Tema.fuente(10), bg=Tema.FONDO, fg=Tema.TEXTO, justify="left").pack(anchor="w", padx=40)
            else:
                tk.Label(self.contenedor_datos, text="No hay cuestionarios previos.", font=Tema.fuente(10), bg=Tema.FONDO, fg=Tema.TEXTO, justify="left").pack(anchor="w", padx=40)

            actividades = self.app.repos.agenda.por_paciente(id_paciente)
            tk.Label(self.contenedor_datos, text="Actividades Agendadas:", font=Tema.fuente(12, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(anchor="w", padx=40, pady=(20, 5))

            if actividades:
                for act in actividades:
                    tk.Label(self.contenedor_datos, text=f"- {act[0]} el {act[1]} (Especialista: {act[2]})", font=Tema.fuente(10), bg=Tema.FONDO, fg=Tema.TEXTO).pack(anchor="w", padx=40)
            else:
                tk.Label(self.contenedor_datos, text="No hay actividades agendadas.", font=Tema.fuente(10), bg=Tema.FONDO, fg=Tema.TEXTO).pack(anchor="w", padx=40)
