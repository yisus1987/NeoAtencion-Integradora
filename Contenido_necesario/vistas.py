import tkinter as tk
from tkinter import messagebox
from datetime import date
from ui import Tema, FabricaWidgets, GrupoChips
from modelos import Paciente, Actividad
from servicios import REGISTRO_ROLES, MENUS_POR_ROL

class PantallaBase(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg=Tema.FONDO)
        self.app = app

    def cabecera_marca(self, parent):
        cont = tk.Frame(parent, bg=parent["bg"])
        FabricaWidgets.logo_box(cont, self.app.logo, 148).pack()
        tk.Label(cont, text="NeoAtención", font=Tema.fuente(22, bold=True),
                 bg=parent["bg"], fg=Tema.MARCA).pack(pady=(12, 0))
        tk.Label(cont, text="Diferentes formas de pensar,\ninfinitas formas de brillar",
                 font=Tema.fuente(9, bold=True), bg=parent["bg"], fg=Tema.MARCA,
                 justify="center").pack()
        return cont

    def barra_lateral(self):
        rol = self.app.usuario_actual.rol
        lateral = tk.Frame(self, bg=Tema.PRIMARIO, width=248)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)
        FabricaWidgets.logo_box(lateral, self.app.logo_mini, 66, 16).pack(pady=(26, 8))
        tk.Label(lateral, text=self.app.usuario_actual.correo, font=Tema.fuente(10, bold=True),
                 bg=Tema.PRIMARIO, fg=Tema.BLANCO).pack()
        tk.Label(lateral, text=rol.upper(), font=Tema.fuente(8, bold=True),
                 bg=Tema.PRIMARIO, fg="#BDE8F6").pack(pady=(2, 18))
        
        menus = MENUS_POR_ROL.get(rol, [])
        i = 0
        while i < len(menus):
            etiqueta = menus[i][0]
            destino = menus[i][1]
            FabricaWidgets.boton(lateral, etiqueta, lambda d=destino: self.app.mostrar(d),
                                 color=Tema.FONDO_SUAVE, color_texto=Tema.PRIMARIO,
                                 ancho=198, alto=40, size=11).pack(pady=5)
            i += 1

        cerrar = tk.Label(lateral, text="Cerrar sesión", font=Tema.fuente(10, bold=True),
                          bg=Tema.PRIMARIO, fg="#BDE8F6", cursor="hand2")
        cerrar.pack(side="bottom", pady=22)
        cerrar.bind("<Button-1>", lambda e: self._cerrar_sesion())
        return lateral

    def _cerrar_sesion(self):
        self.app.usuario_actual = None
        self.app.mostrar("login")

class PantallaConMenu(PantallaBase):
    def __init__(self, master, app, titulo: str):
        super().__init__(master, app)
        self.barra_lateral()
        self.contenido = tk.Frame(self, bg=Tema.FONDO)
        self.contenido.pack(side="left", fill="both", expand=True)
        tk.Label(self.contenido, text=titulo, font=Tema.fuente(18, bold=True),
                 bg=Tema.FONDO, fg=Tema.MARCA).pack(anchor="w", padx=40, pady=(28, 10))

class PantallaLogin(PantallaBase):
    def __init__(self, master, app):
        super().__init__(master, app)
        wrap = tk.Frame(self, bg=Tema.FONDO)
        wrap.place(relx=0.5, rely=0.5, anchor="center")
        self.cabecera_marca(wrap).pack(pady=(0, 16))

        card = FabricaWidgets.tarjeta(wrap, 380, 380)
        card.pack()
        tk.Label(card, text="Bienvenido a NeoAtención", font=Tema.fuente(15, bold=True),
                 bg=Tema.CARD, fg=Tema.TEXTO).place(relx=0.5, y=36, anchor="center")
        self.e_user = FabricaWidgets.campo_form(card, "Nombre de usuario / correo", 40, 70, 300)
        self.e_pass = FabricaWidgets.campo_form(card, "Contraseña", 40, 142, 300, oculto=True)
        tk.Label(card, text="¿Olvidaste la contraseña?", font=Tema.fuente(9),
                 bg=Tema.CARD, fg=Tema.ACENTO).place(relx=0.5, y=222, anchor="center")
        FabricaWidgets.boton(card, "Confirmar", self._entrar).place(relx=0.5, y=278, anchor="center")
        crear = tk.Label(card, text="¿No tienes cuenta?  Crear una cuenta",
                         font=Tema.fuente(10, bold=True), bg=Tema.CARD, fg=Tema.ACENTO, cursor="hand2")
        crear.place(relx=0.5, y=338, anchor="center")
        crear.bind("<Button-1>", lambda e: self.app.mostrar("registro_usuario"))

    def _entrar(self):
        usuario = self.app.servicios.autenticacion.iniciar_sesion(
            self.e_user.get().strip(), self.e_pass.get().strip())
        if usuario:
            self.app.usuario_actual = usuario
            self.app.mostrar("menu")
        else:
            messagebox.showerror("NeoAtención", "Usuario o contraseña incorrectos.")

class PantallaRegistroUsuario(PantallaBase):
    def __init__(self, master, app):
        super().__init__(master, app)
        wrap = tk.Frame(self, bg=Tema.FONDO)
        wrap.place(relx=0.5, rely=0.5, anchor="center")
        self.cabecera_marca(wrap).pack(pady=(0, 14))

        card = FabricaWidgets.tarjeta(wrap, 420, 470)
        card.pack()
        tk.Label(card, text="Registro de Usuario", font=Tema.fuente(15, bold=True),
                 bg=Tema.CARD, fg=Tema.TEXTO).place(relx=0.5, y=34, anchor="center")
        self.e_correo = FabricaWidgets.campo_form(card, "Correo electrónico", 45, 66, 330)
        self.e_pass = FabricaWidgets.campo_form(card, "Contraseña", 45, 128, 330, oculto=True)
        self.e_conf = FabricaWidgets.campo_form(card, "Confirmar Contraseña", 45, 190, 330, oculto=True)

        tk.Label(card, text="Ingresar como", font=Tema.fuente(10, bold=True),
                 bg=Tema.CARD, fg=Tema.TEXTO).place(relx=0.5, y=258, anchor="center")
        
        claves_roles = list(REGISTRO_ROLES.keys())
        self.chips = GrupoChips(card, claves_roles)
        self.chips.place(relx=0.5, y=292, anchor="center")
        FabricaWidgets.boton(card, "Confirmar", self._continuar).place(relx=0.5, y=356, anchor="center")
        volver = tk.Label(card, text="Volver al inicio de sesión", font=Tema.fuente(9),
                          bg=Tema.CARD, fg=Tema.ACENTO, cursor="hand2")
        volver.place(relx=0.5, y=422, anchor="center")
        volver.bind("<Button-1>", lambda e: self.app.mostrar("login"))

    def _continuar(self):
        correo = self.e_correo.get().strip()
        p1 = self.e_pass.get().strip()
        p2 = self.e_conf.get().strip()
        rol = self.chips.valor()
        if not correo or not p1:
            messagebox.showwarning("NeoAtención", "Completa correo y contraseña.")
            return
        if p1 != p2:
            messagebox.showwarning("NeoAtención", "Las contraseñas no coinciden.")
            return
        if not rol:
            messagebox.showwarning("NeoAtención", "Selecciona un rol.")
            return
        try:
            id_usuario = self.app.servicios.autenticacion.registrar_usuario(correo, p1, rol)
        except Exception as e:
            messagebox.showerror("NeoAtención", f"No se pudo crear la cuenta:\n{e}")
            return
        self.app.mostrar("registro_rol", id_usuario=id_usuario, rol=rol)

class PantallaRegistroRol(PantallaBase):
    def __init__(self, master, app, id_usuario: int, rol: str):
        super().__init__(master, app)
        self.id_usuario = id_usuario
        self.estrategia = REGISTRO_ROLES[rol]
        wrap = tk.Frame(self, bg=Tema.FONDO)
        wrap.place(relx=0.5, rely=0.5, anchor="center")
        self.cabecera_marca(wrap).pack(pady=(0, 14))

        card = FabricaWidgets.tarjeta(wrap, 420, 500)
        card.pack()
        tk.Label(card, text=f"Registro de {rol}", font=Tema.fuente(15, bold=True),
                 bg=Tema.CARD, fg=Tema.TEXTO).place(relx=0.5, y=34, anchor="center")

        self.entradas: dict[str, object] = {}
        y = 78
        
        campos_estrategia = self.estrategia.campos()
        i = 0
        while i < len(campos_estrategia):
            campo = campos_estrategia[i]
            if campo.tipo == "chips":
                tk.Label(card, text=campo.etiqueta, font=Tema.fuente(9), bg=Tema.CARD,
                         fg=Tema.TEXTO_TENUE).place(x=51, y=y)
                chips = GrupoChips(card, campo.opciones)
                chips.place(x=45, y=y + 20)
                self.entradas[campo.clave] = chips
                y += 78
            else:
                self.entradas[campo.clave] = FabricaWidgets.campo_form(card, campo.etiqueta, 45, y, 330)
                y += 74
            i += 1

        FabricaWidgets.boton(card, "Confirmar", self._guardar).place(relx=0.5, y=460, anchor="center")

    def _guardar(self):
        datos = {}
        claves = list(self.entradas.keys())
        i = 0
        while i < len(claves):
            clave = claves[i]
            w = self.entradas[clave]
            if isinstance(w, GrupoChips):
                datos[clave] = w.valor()
            else:
                datos[clave] = w.get().strip()
            i += 1
            
        try:
            self.estrategia.guardar(self.app.repos, datos, self.id_usuario)
        except Exception as e:
            messagebox.showerror("NeoAtención", f"Error al guardar:\n{e}")
            return
        messagebox.showinfo("NeoAtención", "¡Cuenta creada con éxito!")
        self.app.mostrar("login")

class PantallaMenu(PantallaBase):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.barra_lateral()
        centro = tk.Frame(self, bg=Tema.FONDO)
        centro.pack(side="left", fill="both", expand=True)
        card = FabricaWidgets.tarjeta(centro, 520, 300)
        card.place(relx=0.5, rely=0.5, anchor="center")
        FabricaWidgets.logo_box(card, self.app.logo, 110).place(relx=0.5, y=95, anchor="center")
        tk.Label(card, text="¡Bienvenido!", font=Tema.fuente(20, bold=True),
                 bg=Tema.CARD, fg=Tema.MARCA).place(relx=0.5, y=190, anchor="center")
        tk.Label(card, text="Selecciona una opción del menú de la izquierda",
                 font=Tema.fuente(11), bg=Tema.CARD, fg=Tema.TEXTO_TENUE).place(relx=0.5, y=228, anchor="center")

class PantallaRegistrarPaciente(PantallaConMenu):
    def __init__(self, master, app):
        super().__init__(master, app, "Registro de Paciente")
        card = FabricaWidgets.tarjeta(self.contenido, 420, 400)
        card.pack(padx=40, pady=10, anchor="w")
        self.entradas = {}
        y = 34
        
        campos_paciente = [("nombre", "Nombre"), ("apellido", "Apellido"), ("edad", "Edad"), ("nivel", "Nivel escolar")]
        i = 0
        while i < len(campos_paciente):
            clave = campos_paciente[i][0]
            etiqueta = campos_paciente[i][1]
            self.entradas[clave] = FabricaWidgets.campo_form(card, etiqueta, 45, y, 330)
            y += 78
            i += 1
            
        FabricaWidgets.boton(card, "Confirmar", self._guardar).place(relx=0.5, y=360, anchor="center")

    def _guardar(self):
        try:
            edad = int(self.entradas["edad"].get().strip())
        except ValueError:
            messagebox.showwarning("NeoAtención", "La edad debe ser un número.")
            return
        id_tutor = self.app.repos.tutor.id_por_usuario(self.app.usuario_actual.id)
        p = Paciente(
            nombre=self.entradas["nombre"].get().strip(),
            apellido=self.entradas["apellido"].get().strip(),
            edad=edad, nivel_escolar=self.entradas["nivel"].get().strip(),
            id_tutor_padre=id_tutor)
        self.app.repos.paciente.crear(p)
        messagebox.showinfo("NeoAtención", "Paciente registrado con éxito.")
        self.app.mostrar("menu")

class PantallaCuestionario(PantallaConMenu):
    def __init__(self, master, app):
        super().__init__(master, app, "Cuestionario TDAH")
        serv = app.servicios.cuestionario
        pacientes = app.repos.paciente.listar()
        if not pacientes:
            tk.Label(self.contenido, text="Primero registra un paciente.",
                     font=Tema.fuente(12), bg=Tema.FONDO, fg=Tema.MARCA).pack(padx=40)
            return
        sel = tk.Frame(self.contenido, bg=Tema.FONDO)
        sel.pack(anchor="w", padx=40)
        tk.Label(sel, text="Paciente:", font=Tema.fuente(10, bold=True),
                 bg=Tema.FONDO, fg=Tema.MARCA).pack(side="left")
        self.var_pac = tk.StringVar(value=f"{pacientes[0].id} - {pacientes[0].nombre}")
        
        lista_pacientes = []
        i_pac = 0
        while i_pac < len(pacientes):
            p = pacientes[i_pac]
            lista_pacientes.append(f"{p.id} - {p.nombre} {p.apellido}")
            i_pac += 1
            
        tk.OptionMenu(sel, self.var_pac, *lista_pacientes).pack(side="left", padx=8)

        cont = tk.Frame(self.contenido, bg=Tema.FONDO)
        cont.pack(fill="both", expand=True, padx=40, pady=10)
        canvas = tk.Canvas(cont, bg=Tema.FONDO, highlightthickness=0)
        scroll = tk.Scrollbar(cont, orient="vertical", command=canvas.yview)
        interno = tk.Frame(canvas, bg=Tema.FONDO)
        interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=interno, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.vars_ina = self._bloque(interno, "Parte 1: Inatención",
                                     serv.PREGUNTAS_INATENCION, serv.ESCALA)
        self.vars_hip = self._bloque(interno, "Parte 2: Hiperactividad",
                                     serv.PREGUNTAS_HIPERACTIVIDAD, serv.ESCALA)
        FabricaWidgets.boton(interno, "Guardar Evaluación", self._guardar).pack(pady=16)

    def _bloque(self, parent, titulo, preguntas, escala):
        tk.Label(parent, text=titulo, font=Tema.fuente(13, bold=True),
                 bg=Tema.FONDO, fg=Tema.MARCA).pack(anchor="w", pady=(10, 4))
        variables = []
        
        i_preg = 0
        while i_preg < len(preguntas):
            texto = preguntas[i_preg]
            card = tk.Frame(parent, bg=Tema.CARD, padx=14, pady=8)
            card.pack(fill="x", pady=4)
            tk.Label(card, text=texto, font=Tema.fuente(10), bg=Tema.CARD,
                     fg=Tema.TEXTO, wraplength=560, justify="left").pack(anchor="w")
            v = tk.IntVar(value=0)
            fila = tk.Frame(card, bg=Tema.CARD)
            fila.pack(anchor="w", pady=(4, 0))
            
            i_esc = 0
            while i_esc < len(escala):
                op = escala[i_esc]
                tk.Radiobutton(fila, text=op, variable=v, value=i_esc, bg=Tema.CARD,
                               fg=Tema.TEXTO, selectcolor=Tema.FONDO_SUAVE,
                               font=Tema.fuente(9), activebackground=Tema.CARD).pack(side="left", padx=4)
                i_esc += 1
                
            variables.append(v)
            i_preg += 1
            
        return variables

    def _guardar(self):
        id_paciente = int(self.var_pac.get().split(" - ")[0])
        
        valores_ina = []
        i = 0
        while i < len(self.vars_ina):
            valores_ina.append(self.vars_ina[i].get())
            i += 1
            
        valores_hip = []
        j = 0
        while j < len(self.vars_hip):
            valores_hip.append(self.vars_hip[j].get())
            j += 1
            
        p_ina, p_hip, grupo, nivel = self.app.servicios.cuestionario.evaluar(valores_ina, valores_hip)
        resumen = f"Ina {p_ina}/27 - Hip {p_hip}/27"
        
        self.app.repos.paciente.actualizar_cuestionario(id_paciente, resumen, grupo, nivel)
        self.app.repos.resultado_test.crear(id_paciente, str(date.today()), p_ina, p_hip, grupo, nivel)
        
        messagebox.showinfo("NeoAtención",
                            f"Evaluación guardada.\nInatención: {p_ina}/27\n"
                            f"Hiperactividad: {p_hip}/27\nGrupo: {grupo}\nNivel: {nivel}")
        self.app.mostrar("reportes", id_paciente=id_paciente)

class PantallaCrearActividad(PantallaConMenu):
    def __init__(self, master, app):
        super().__init__(master, app, "Crear Actividad")
        card = FabricaWidgets.tarjeta(self.contenido, 480, 500)
        card.pack(padx=40, pady=10, anchor="w")
        self.e_nombre = FabricaWidgets.campo_form(card, "Nombre de la Actividad", 45, 28, 390)
        self.e_desc = FabricaWidgets.campo_form(card, "Descripción", 45, 100, 390)
        tk.Label(card, text="Tipo de Actividad", font=Tema.fuente(10, bold=True),
                 bg=Tema.CARD, fg=Tema.TEXTO).place(x=51, y=176)
        self.chips_tipo = GrupoChips(card, ["Visual", "Cognitivo", "Motriz", "Auditivo"])
        self.chips_tipo.place(x=45, y=200)
        tk.Label(card, text="Designación", font=Tema.fuente(10, bold=True),
                 bg=Tema.CARD, fg=Tema.TEXTO).place(x=51, y=256)
        self.chips_desig = GrupoChips(card, ["Escolar", "Recreativa", "Familiar"])
        self.chips_desig.place(x=45, y=280)
        self.e_obj = FabricaWidgets.campo_form(card, "Objetivo", 45, 330, 390)
        FabricaWidgets.boton(card, "Crear Actividad", self._crear).place(relx=0.5, y=455, anchor="center")

    def _crear(self):
        a = Actividad(
            nombre=self.e_nombre.get().strip(), descripcion=self.e_desc.get().strip(),
            tipo=self.chips_tipo.valor(), designacion=self.chips_desig.valor(),
            objetivo=self.e_obj.get().strip())
        if not a.nombre:
            messagebox.showwarning("NeoAtención", "Escribe el nombre de la actividad.")
            return
        self.app.repos.actividad.crear(a)
        messagebox.showinfo("NeoAtención", "Actividad creada y disponible en la agenda.")
        self.app.mostrar("menu")

class PantallaAgendar(PantallaConMenu):
    def __init__(self, master, app):
        super().__init__(master, app, "Agendar Actividad")
        pacientes = app.repos.paciente.listar()
        actividades = app.repos.actividad.listar()
        especialistas = app.repos.especialista.listar()
        
        if not pacientes or not actividades or not especialistas:
            tk.Label(self.contenido, text="Faltan pacientes, actividades o especialistas registrados.",
                     font=Tema.fuente(12), bg=Tema.FONDO, fg=Tema.MARCA).pack(padx=40)
            return
            
        card = FabricaWidgets.tarjeta(self.contenido, 460, 410)
        card.pack(padx=40, pady=10, anchor="w")
        
        tk.Label(card, text="Paciente", font=Tema.fuente(9), bg=Tema.CARD,
                 fg=Tema.TEXTO_TENUE).place(x=51, y=30)
        self.var_pac = tk.StringVar(value=f"{pacientes[0].id} - {pacientes[0].nombre}")
        lista_pacientes = []
        i = 0
        while i < len(pacientes):
            p = pacientes[i]
            lista_pacientes.append(f"{p.id} - {p.nombre} {p.apellido}")
            i += 1
        tk.OptionMenu(card, self.var_pac, *lista_pacientes).place(x=45, y=50)
        
        tk.Label(card, text="Actividad", font=Tema.fuente(9), bg=Tema.CARD,
                 fg=Tema.TEXTO_TENUE).place(x=51, y=90)
        self.var_act = tk.StringVar(value=f"{actividades[0].id} - {actividades[0].nombre}")
        lista_actividades = []
        j = 0
        while j < len(actividades):
            a = actividades[j]
            lista_actividades.append(f"{a.id} - {a.nombre}")
            j += 1
        tk.OptionMenu(card, self.var_act, *lista_actividades).place(x=45, y=110)
        
        tk.Label(card, text="Especialista", font=Tema.fuente(9), bg=Tema.CARD,
                 fg=Tema.TEXTO_TENUE).place(x=51, y=150)
        self.var_esp = tk.StringVar(value=f"{especialistas[0][0]} - {especialistas[0][1]}")
        lista_especialistas = []
        k = 0
        while k < len(especialistas):
            e = especialistas[k]
            lista_especialistas.append(f"{e[0]} - {e[1]}")
            k += 1
        tk.OptionMenu(card, self.var_esp, *lista_especialistas).place(x=45, y=170)
        
        self.e_fecha = FabricaWidgets.campo_form(card, "Fecha (AAAA-MM-DD)", 45, 220, 300)
        self.e_fecha.insert(0, str(date.today()))
        FabricaWidgets.boton(card, "Agendar", self._agendar).place(relx=0.5, y=350, anchor="center")

    def _agendar(self):
        id_p = int(self.var_pac.get().split(" - ")[0])
        id_a = int(self.var_act.get().split(" - ")[0])
        id_e = int(self.var_esp.get().split(" - ")[0])
        self.app.repos.agenda.agendar(id_p, id_a, id_e, self.e_fecha.get().strip())
        messagebox.showinfo("NeoAtención", "Actividad agendada con éxito.")
        self.app.mostrar("menu")

class PantallaReportes(PantallaConMenu):
    def __init__(self, master, app, id_paciente: int | None = None):
        super().__init__(master, app, "Reporte del paciente")
        
        pacientes = app.repos.paciente.listar()
        
        if not pacientes:
            tk.Label(self.contenido, text="No hay pacientes registrados.",
                     font=Tema.fuente(12), bg=Tema.FONDO, fg=Tema.MARCA).pack(padx=40)
            return
            
        sel = tk.Frame(self.contenido, bg=Tema.FONDO)
        sel.pack(anchor="w", padx=40)
        tk.Label(sel, text="Paciente:", font=Tema.fuente(10, bold=True),
                 bg=Tema.FONDO, fg=Tema.MARCA).pack(side="left")
        
        inicial = pacientes[0]
        i_busq = 0
        while i_busq < len(pacientes):
            if pacientes[i_busq].id == id_paciente:
                inicial = pacientes[i_busq]
                break
            i_busq += 1
            
        self.var_pac = tk.StringVar(value=f"{inicial.id} - {inicial.nombre} {inicial.apellido}")
        
        lista_pacientes = []
        i = 0
        while i < len(pacientes):
            p = pacientes[i]
            lista_pacientes.append(f"{p.id} - {p.nombre} {p.apellido}")
            i += 1
            
        tk.OptionMenu(sel, self.var_pac, *lista_pacientes,
                      command=lambda _: self._recargar()).pack(side="left", padx=8)
                      
        self.cuerpo = tk.Frame(self.contenido, bg=Tema.FONDO)
        self.cuerpo.pack(fill="both", expand=True)
        
        self._recargar()

    def _recargar(self):
        hijos = self.cuerpo.winfo_children()
        i_limpieza = 0
        while i_limpieza < len(hijos):
            hijos[i_limpieza].destroy()
            i_limpieza += 1
            
        id_paciente = int(self.var_pac.get().split(" - ")[0])
        
        pacientes = self.app.repos.paciente.listar()
        paciente_actual = None
        i_pac = 0
        while i_pac < len(pacientes):
            if pacientes[i_pac].id == id_paciente:
                paciente_actual = pacientes[i_pac]
                break
            i_pac += 1
            
        if paciente_actual:
            tk.Label(self.cuerpo, text="Resultados del Cuestionario:", font=Tema.fuente(12, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(anchor="w", padx=40, pady=(20, 5))
            texto_cuestionario = f"Puntuación: {paciente_actual.cuestionario}\nGrupo: {paciente_actual.grupo_TDAH}\nNivel: {paciente_actual.nivel_TDAH}"
            
            if not paciente_actual.cuestionario:
                texto_cuestionario = "Aún no se ha realizado el cuestionario."
                
            tk.Label(self.cuerpo, text=texto_cuestionario, font=Tema.fuente(10), bg=Tema.FONDO, fg=Tema.TEXTO, justify="left").pack(anchor="w", padx=40)

            actividades = self.app.repos.agenda.por_paciente(id_paciente)
            tk.Label(self.cuerpo, text="Actividades Agendadas:", font=Tema.fuente(12, bold=True), bg=Tema.FONDO, fg=Tema.MARCA).pack(anchor="w", padx=40, pady=(20, 5))
            
            if actividades:
                i_act = 0
                while i_act < len(actividades):
                    act = actividades[i_act]
                    tk.Label(self.cuerpo, text=f"- {act[0]} ({act[1]})", font=Tema.fuente(10), bg=Tema.FONDO, fg=Tema.TEXTO).pack(anchor="w", padx=40)
                    i_act += 1
            else:
                tk.Label(self.cuerpo, text="No hay actividades agendadas.", font=Tema.fuente(10), bg=Tema.FONDO, fg=Tema.TEXTO).pack(anchor="w", padx=40)