import csv
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox, filedialog
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
import mysql.connector

LOGO_B64 = "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"


@dataclass
class ConfiguracionBD:
    host: str = "localhost"
    port: int = 3307
    user: str = "root"
    password: str = "patho2325"
    database: str = "gestion_tdah"


@dataclass
class Usuario:
    correo: str
    contrasena: str
    rol: str
    id: int | None = None


@dataclass
class Paciente:
    nombre: str
    apellido: str
    edad: int
    nivel_escolar: str
    id_tutor_padre: int | None = None
    cuestionario: str = ""
    grupo_TDAH: str = ""
    nivel_TDAH: str = ""
    id: int | None = None


@dataclass
class Actividad:
    nombre: str
    descripcion: str
    tipo: str
    designacion: str
    objetivo: str
    id: int | None = None


@dataclass
class Campo:
    clave: str
    etiqueta: str
    tipo: str = "texto"
    opciones: list[str] = field(default_factory=list)


class ConexionBD(ABC):
    @abstractmethod
    def cursor(self): ...
    @abstractmethod
    def commit(self) -> None: ...
    @abstractmethod
    def cerrar(self) -> None: ...


class IRepositorioUsuario(ABC):
    @abstractmethod
    def crear(self, usuario: Usuario) -> int: ...
    @abstractmethod
    def autenticar(self, correo: str, contrasena: str) -> Usuario | None: ...


class EstrategiaRegistroRol(ABC):
    nombre_rol: str = ""
    @abstractmethod
    def campos(self) -> list[Campo]: ...
    @abstractmethod
    def guardar(self, repos, datos: dict, id_usuario: int) -> None: ...


class ExportadorReporte(ABC):
    etiqueta: str = ""
    extension: str = ""
    @abstractmethod
    def exportar(self, ruta: str, encabezado: dict, tareas: list) -> None: ...


class ConexionMariaDB(ConexionBD):
    def __init__(self, config: ConfiguracionBD):
        self._config = config
        self._conexion = None

    def conectar(self) -> None:
        temp = mysql.connector.connect(
            host=self._config.host, port=self._config.port,
            user=self._config.user, password=self._config.password)
        cur = temp.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {self._config.database}")
        cur.close()
        temp.close()
        self._conexion = mysql.connector.connect(
            host=self._config.host, port=self._config.port,
            user=self._config.user, password=self._config.password,
            database=self._config.database)

    def cursor(self):
        return self._conexion.cursor()

    def commit(self) -> None:
        self._conexion.commit()

    def cerrar(self) -> None:
        if self._conexion is not None and self._conexion.is_connected():
            self._conexion.close()


class InicializadorEsquema:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear_tablas(self) -> None:
        cur = self._conexion.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(50),
                contrasena VARCHAR(50),
                correo_electronico VARCHAR(100)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS crear_Docente (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50),
                apellido VARCHAR(50),
                correo_electronico VARCHAR(100),
                telefono VARCHAR(15),
                nombre_escuela VARCHAR(100),
                id_Usuario INT,
                FOREIGN KEY (id_Usuario) REFERENCES Usuario(id)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Especialista (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50),
                descripcion VARCHAR(255)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS crear_Tutor_Padre (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50),
                apellido VARCHAR(50),
                correo_electronico VARCHAR(100),
                telefono VARCHAR(15),
                Parentesco VARCHAR(50),
                id_Usuario INT,
                FOREIGN KEY (id_Usuario) REFERENCES Usuario(id)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Paciente (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50),
                apellido VARCHAR(50),
                edad INT,
                Nivel_escolar VARCHAR(50),
                id_tutor_padre INT,
                cuestionario VARCHAR(50),
                grupo_TDAH VARCHAR(50),
                nivel_TDAH VARCHAR(50),
                FOREIGN KEY (id_tutor_padre) REFERENCES crear_Tutor_Padre(id)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Actividades (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_actividad VARCHAR(50),
                descripcion VARCHAR(255),
                Tipo_actividad VARCHAR(50),
                Designacion_actividad VARCHAR(50),
                objetivo VARCHAR(30)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS agenda_actividad (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_Paciente INT,
                id_actividad INT,
                fecha DATE,
                FOREIGN KEY (id_Paciente) REFERENCES Paciente(id),
                FOREIGN KEY (id_actividad) REFERENCES Actividades(id)
            );
        """)
        cur.close()
        self._conexion.commit()


class RepositorioUsuario(IRepositorioUsuario):
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, usuario: Usuario) -> int:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO Usuario (nombre_usuario, contrasena, correo_electronico) "
            "VALUES (%s, %s, %s)",
            (usuario.correo, usuario.contrasena, usuario.correo))
        self._conexion.commit()
        nuevo_id = cur.lastrowid
        cur.close()
        return nuevo_id

    def _rol(self, id_usuario: int) -> str:
        cur = self._conexion.cursor()
        cur.execute("SELECT id FROM crear_Tutor_Padre WHERE id_Usuario = %s", (id_usuario,))
        if cur.fetchone():
            cur.close()
            return "Tutor / Padre"
        cur.execute("SELECT id FROM crear_Docente WHERE id_Usuario = %s", (id_usuario,))
        if cur.fetchone():
            cur.close()
            return "Docente"
        cur.close()
        return "Especialista"

    def autenticar(self, correo: str, contrasena: str) -> Usuario | None:
        cur = self._conexion.cursor()
        cur.execute(
            "SELECT id, correo_electronico FROM Usuario "
            "WHERE (correo_electronico = %s OR nombre_usuario = %s) AND contrasena = %s",
            (correo, correo, contrasena))
        fila = cur.fetchone()
        cur.close()
        if fila:
            return Usuario(id=fila[0], correo=fila[1], contrasena="", rol=self._rol(fila[0]))
        return None


class RepositorioTutor:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, datos: dict, id_usuario: int) -> None:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO crear_Tutor_Padre (nombre, apellido, telefono, Parentesco, id_Usuario) "
            "VALUES (%s, %s, %s, %s, %s)",
            (datos["nombre"], datos["apellido"], datos["telefono"],
             datos["parentesco"], id_usuario))
        self._conexion.commit()
        cur.close()

    def id_por_usuario(self, id_usuario: int) -> int | None:
        cur = self._conexion.cursor()
        cur.execute("SELECT id FROM crear_Tutor_Padre WHERE id_Usuario = %s", (id_usuario,))
        fila = cur.fetchone()
        cur.close()
        return fila[0] if fila else None


class RepositorioDocente:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, datos: dict, id_usuario: int) -> None:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO crear_Docente (nombre, apellido, telefono, nombre_escuela, id_Usuario) "
            "VALUES (%s, %s, %s, %s, %s)",
            (datos["nombre"], datos["apellido"], datos["telefono"],
             datos["nombre_escuela"], id_usuario))
        self._conexion.commit()
        cur.close()


class RepositorioEspecialista:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, datos: dict, id_usuario: int) -> None:
        nombre = f"{datos['nombre']} {datos.get('apellido', '')}".strip()
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO Especialista (nombre, descripcion) VALUES (%s, %s)",
            (nombre, datos["datos_profesional"]))
        self._conexion.commit()
        cur.close()


class RepositorioPaciente:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, p: Paciente) -> int:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO Paciente (nombre, apellido, edad, Nivel_escolar, id_tutor_padre) "
            "VALUES (%s, %s, %s, %s, %s)",
            (p.nombre, p.apellido, p.edad, p.nivel_escolar, p.id_tutor_padre))
        self._conexion.commit()
        nuevo = cur.lastrowid
        cur.close()
        return nuevo

    def listar(self) -> list[Paciente]:
        cur = self._conexion.cursor()
        cur.execute("SELECT id, nombre, apellido, edad, Nivel_escolar, grupo_TDAH, nivel_TDAH FROM Paciente")
        pacientes = [
            Paciente(id=f[0], nombre=f[1], apellido=f[2], edad=f[3],
                     nivel_escolar=f[4], grupo_TDAH=f[5] or "", nivel_TDAH=f[6] or "")
            for f in cur.fetchall()]
        cur.close()
        return pacientes

    def obtener(self, id_paciente: int) -> Paciente | None:
        cur = self._conexion.cursor()
        cur.execute("SELECT id, nombre, apellido, edad, Nivel_escolar, cuestionario, grupo_TDAH, nivel_TDAH "
                    "FROM Paciente WHERE id = %s", (id_paciente,))
        f = cur.fetchone()
        cur.close()
        if not f:
            return None
        return Paciente(id=f[0], nombre=f[1], apellido=f[2], edad=f[3],
                        nivel_escolar=f[4], cuestionario=f[5] or "",
                        grupo_TDAH=f[6] or "", nivel_TDAH=f[7] or "")

    def actualizar_cuestionario(self, id_paciente: int, resumen: str, grupo: str, nivel: str) -> None:
        cur = self._conexion.cursor()
        cur.execute("UPDATE Paciente SET cuestionario = %s, grupo_TDAH = %s, nivel_TDAH = %s WHERE id = %s",
                    (resumen, grupo, nivel, id_paciente))
        self._conexion.commit()
        cur.close()


class RepositorioActividad:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, a: Actividad) -> None:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO Actividades (nombre_actividad, descripcion, Tipo_actividad, "
            "Designacion_actividad, objetivo) VALUES (%s, %s, %s, %s, %s)",
            (a.nombre, a.descripcion, a.tipo, a.designacion, a.objetivo))
        self._conexion.commit()
        cur.close()

    def listar(self) -> list[Actividad]:
        cur = self._conexion.cursor()
        cur.execute("SELECT id, nombre_actividad, descripcion, Tipo_actividad, "
                    "Designacion_actividad, objetivo FROM Actividades")
        acts = [Actividad(id=f[0], nombre=f[1], descripcion=f[2], tipo=f[3],
                          designacion=f[4], objetivo=f[5]) for f in cur.fetchall()]
        cur.close()
        return acts


class RepositorioAgenda:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def agendar(self, id_paciente: int, id_actividad: int, fecha: str) -> None:
        cur = self._conexion.cursor()
        cur.execute("INSERT INTO agenda_actividad (id_Paciente, id_actividad, fecha) "
                    "VALUES (%s, %s, %s)", (id_paciente, id_actividad, fecha))
        self._conexion.commit()
        cur.close()

    def por_paciente(self, id_paciente: int) -> list[tuple]:
        cur = self._conexion.cursor()
        cur.execute("""
            SELECT act.nombre_actividad, aa.fecha
            FROM agenda_actividad aa
            JOIN Actividades act ON aa.id_actividad = act.id
            WHERE aa.id_Paciente = %s
            ORDER BY aa.fecha DESC
        """, (id_paciente,))
        filas = cur.fetchall()
        cur.close()
        return filas


@dataclass
class Repositorios:
    usuario: RepositorioUsuario
    tutor: RepositorioTutor
    docente: RepositorioDocente
    especialista: RepositorioEspecialista
    paciente: RepositorioPaciente
    actividad: RepositorioActividad
    agenda: RepositorioAgenda


class ServicioAutenticacion:
    def __init__(self, repo_usuario: IRepositorioUsuario):
        self._repo = repo_usuario

    def iniciar_sesion(self, correo: str, contrasena: str) -> Usuario | None:
        return self._repo.autenticar(correo, contrasena)

    def registrar_usuario(self, correo: str, contrasena: str, rol: str) -> int:
        return self._repo.crear(Usuario(correo=correo, contrasena=contrasena, rol=rol))


class ServicioCuestionario:
    PREGUNTAS_INATENCION = [
        "¿Tiene dificultad para mantener la atención en tareas o juegos?",
        "¿Comete errores por descuido en las tareas escolares?",
        "¿Parece no escuchar cuando se le habla directamente?",
        "¿No sigue instrucciones o no termina los quehaceres/deberes?",
        "¿Tiene dificultades para organizar tareas y actividades?",
        "¿Evita o posterga tareas que requieren esfuerzo mental sostenido?",
        "¿Pierde cosas necesarias para sus actividades (lápices, cuadernos)?",
        "¿Se distrae fácilmente con estímulos externos?",
        "¿Olvida hacer las actividades de la rutina diaria?",
    ]
    PREGUNTAS_HIPERACTIVIDAD = [
        "¿Juguetea con las manos o los pies o se retuerce en el asiento?",
        "¿Se levanta de su sitio cuando debería quedarse sentado?",
        "¿Corre o trepa en situaciones donde es inapropiado?",
        "¿Tiene dificultades para jugar tranquilamente?",
        "¿Está en marcha constante o actúa como si tuviera un motor?",
        "¿Habla de manera excesiva?",
        "¿Suele responder antes de que terminen de hacerle la pregunta?",
        "¿Le es muy difícil esperar su turno en filas o juegos?",
        "¿Interrumpe a otros en conversaciones o actividades?",
    ]
    ESCALA = ["0 - Nunca", "1 - A veces", "2 - Frecuentemente", "3 - Siempre"]

    def evaluar(self, inatencion: list[int], hiperactividad: list[int]) -> tuple[int, int, str, str]:
        p_ina = sum(inatencion)
        p_hip = sum(hiperactividad)
        if p_ina >= 15 and p_hip >= 15:
            grupo = "Combinado"
        elif p_ina > p_hip:
            grupo = "Predominio Inatención"
        else:
            grupo = "Predominio Hiperactividad"
        total = p_ina + p_hip
        if total < 18:
            nivel = "Bajo"
        elif total < 36:
            nivel = "Moderado"
        else:
            nivel = "Elevado"
        return p_ina, p_hip, grupo, nivel


class RegistroTutorPadre(EstrategiaRegistroRol):
    nombre_rol = "Tutor / Padre"

    def campos(self) -> list[Campo]:
        return [
            Campo("nombre", "Nombre"),
            Campo("apellido", "Apellido"),
            Campo("telefono", "Teléfono"),
            Campo("parentesco", "Parentesco", "chips", ["Padre", "Madre", "Tutor"]),
        ]

    def guardar(self, repos, datos, id_usuario):
        repos.tutor.crear(datos, id_usuario)


class RegistroDocente(EstrategiaRegistroRol):
    nombre_rol = "Docente"

    def campos(self) -> list[Campo]:
        return [
            Campo("nombre", "Nombre"),
            Campo("apellido", "Apellido"),
            Campo("telefono", "Teléfono"),
            Campo("nombre_escuela", "Nombre de la escuela"),
        ]

    def guardar(self, repos, datos, id_usuario):
        repos.docente.crear(datos, id_usuario)


class RegistroEspecialista(EstrategiaRegistroRol):
    nombre_rol = "Especialista"

    def campos(self) -> list[Campo]:
        return [
            Campo("nombre", "Nombre"),
            Campo("apellido", "Apellido"),
            Campo("datos_profesional", "Datos del Profesional"),
        ]

    def guardar(self, repos, datos, id_usuario):
        repos.especialista.crear(datos, id_usuario)


REGISTRO_ROLES: dict[str, EstrategiaRegistroRol] = {
    e.nombre_rol: e for e in (RegistroTutorPadre(), RegistroDocente(), RegistroEspecialista())
}

MENUS_POR_ROL: dict[str, list[tuple[str, str]]] = {
    "Tutor / Padre": [
        ("Inicio", "menu"), ("Registrar paciente", "registrar_paciente"),
        ("Cuestionario", "cuestionario"), ("Agenda", "agendar"), ("Reportes", "reportes"),
    ],
    "Docente": [
        ("Inicio", "menu"), ("Registrar alumno", "registrar_paciente"),
        ("Cuestionario", "cuestionario"), ("Agenda", "agendar"), ("Reportes", "reportes"),
    ],
    "Especialista": [
        ("Inicio", "menu"), ("Registrar paciente", "registrar_paciente"),
        ("Cuestionario", "cuestionario"), ("Crear actividad", "crear_actividad"),
        ("Agenda", "agendar"), ("Reportes", "reportes"),
    ],
}


class ExportadorTexto(ExportadorReporte):
    etiqueta = "Texto (.txt)"
    extension = ".txt"

    def exportar(self, ruta, encabezado, tareas):
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("REPORTE DEL PACIENTE - NeoAtención\n")
            f.write("=" * 45 + "\n")
            for k, v in encabezado.items():
                f.write(f"{k}: {v}\n")
            f.write("\nTAREAS AGENDADAS\n" + "-" * 45 + "\n")
            for t in tareas:
                f.write(f"{t[0]} | {t[1]}\n")


class ExportadorCSV(ExportadorReporte):
    etiqueta = "CSV (.csv)"
    extension = ".csv"

    def exportar(self, ruta, encabezado, tareas):
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Reporte del paciente - NeoAtención"])
            for k, v in encabezado.items():
                w.writerow([k, v])
            w.writerow([])
            w.writerow(["Actividad", "Fecha"])
            for t in tareas:
                w.writerow(list(t))


EXPORTADORES: list[ExportadorReporte] = [ExportadorTexto(), ExportadorCSV()]


@dataclass
class Servicios:
    autenticacion: ServicioAutenticacion
    cuestionario: ServicioCuestionario


class Tema:
    FONDO = "#40BEEE"
    FONDO_SUAVE = "#CCEEFA"
    CARD = "#FFFFFF"
    CARD_ALT = "#EEF0FC"
    PRIMARIO = "#0E7FA6"
    PRIMARIO_HOVER = "#0B6486"
    ACENTO = "#118AB5"
    TEXTO = "#0B3B4A"
    TEXTO_TENUE = "#5A7A86"
    MARCA = "#0B4A5E"
    CHIP = "#CCEEFA"
    CHIP_SEL = "#40BEEE"
    PENDIENTE = "#F5A623"
    COMPLETADA = "#2ECC71"
    BLANCO = "#FFFFFF"

    _familia = None

    @classmethod
    def familia(cls):
        if cls._familia is None:
            disponibles = set(tkfont.families())
            for f in ("Nunito", "Segoe UI", "Verdana", "Helvetica"):
                if f in disponibles:
                    cls._familia = f
                    break
            else:
                cls._familia = "TkDefaultFont"
        return cls._familia

    @classmethod
    def fuente(cls, size=11, bold=False):
        return (cls.familia(), size, "bold" if bold else "normal")


class FabricaWidgets:
    @staticmethod
    def _rect_redondeado(canvas, x1, y1, x2, y2, r, **kw):
        pts = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2,
               x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1]
        return canvas.create_polygon(pts, smooth=True, **kw)

    @classmethod
    def boton(cls, master, texto, comando, color=Tema.ACENTO, color_texto="#FFFFFF",
              ancho=280, alto=48, size=12):
        c = tk.Canvas(master, width=ancho, height=alto, bg=master["bg"],
                      highlightthickness=0, cursor="hand2")
        cls._rect_redondeado(c, 2, 2, ancho-2, alto-2, alto//2, fill=color, outline=color)
        c.create_text(ancho//2, alto//2, text=texto, fill=color_texto,
                      font=Tema.fuente(size, bold=True))
        c.bind("<Button-1>", lambda e: comando())
        return c

    @classmethod
    def campo(cls, master, ancho=300, alto=44, oculto=False):
        cont = tk.Canvas(master, width=ancho, height=alto, bg=master["bg"], highlightthickness=0)
        cls._rect_redondeado(cont, 1, 1, ancho-1, alto-1, alto//2,
                             fill=Tema.CARD_ALT, outline="#D9DEF5")
        entry = tk.Entry(cont, bd=0, bg=Tema.CARD_ALT, fg=Tema.TEXTO,
                         font=Tema.fuente(11), show="•" if oculto else "", justify="left")
        cont.create_window(alto//2, alto//2, anchor="w", window=entry,
                           width=ancho-alto, height=alto-14)
        return cont, entry

    @classmethod
    def campo_form(cls, card, etiqueta, x, y, ancho=330, oculto=False):
        tk.Label(card, text=etiqueta, font=Tema.fuente(9), bg=Tema.CARD,
                 fg=Tema.TEXTO_TENUE).place(x=x + 6, y=y)
        cont, entry = cls.campo(card, ancho, oculto=oculto)
        cont.place(x=x, y=y + 18)
        return entry

    @classmethod
    def tarjeta(cls, master, ancho, alto, color=Tema.CARD, radio=26):
        c = tk.Canvas(master, width=ancho, height=alto, bg=master["bg"], highlightthickness=0)
        cls._rect_redondeado(c, 2, 2, ancho-2, alto-2, radio, fill=color, outline=color)
        return c

    @classmethod
    def logo_box(cls, master, imagen, lado=150, radio=28):
        c = tk.Canvas(master, width=lado, height=lado, bg=master["bg"], highlightthickness=0)
        cls._rect_redondeado(c, 2, 2, lado-2, lado-2, radio, fill=Tema.CARD, outline=Tema.CARD)
        c.create_image(lado//2, lado//2, image=imagen)
        return c

    @classmethod
    def insignia(cls, master, texto, color_fondo, color_texto="#FFFFFF", ancho=64, alto=26, size=9):
        c = tk.Canvas(master, width=ancho, height=alto, bg=master["bg"], highlightthickness=0)
        cls._rect_redondeado(c, 1, 1, ancho-1, alto-1, alto//2, fill=color_fondo, outline=color_fondo)
        c.create_text(ancho//2, alto//2, text=texto, fill=color_texto, font=Tema.fuente(size, bold=True))
        return c


class GrupoChips(tk.Frame):
    def __init__(self, master, opciones: list[str], **kw):
        super().__init__(master, bg=master["bg"], **kw)
        self._valor = tk.StringVar(value="")
        self._botones: dict[str, tk.Label] = {}
        for op in opciones:
            lbl = tk.Label(self, text=op, font=Tema.fuente(10, bold=True),
                           bg=Tema.CHIP, fg=Tema.TEXTO, padx=14, pady=6, cursor="hand2")
            lbl.pack(side="left", padx=4)
            lbl.bind("<Button-1>", lambda e, o=op: self.seleccionar(o))
            self._botones[op] = lbl

    def seleccionar(self, opcion: str):
        self._valor.set(opcion)
        for op, lbl in self._botones.items():
            if op == opcion:
                lbl.config(bg=Tema.CHIP_SEL, fg=Tema.BLANCO)
            else:
                lbl.config(bg=Tema.CHIP, fg=Tema.TEXTO)

    def valor(self) -> str:
        return self._valor.get()


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
        for etiqueta, destino in MENUS_POR_ROL.get(rol, []):
            FabricaWidgets.boton(lateral, etiqueta, lambda d=destino: self.app.mostrar(d),
                                 color=Tema.FONDO_SUAVE, color_texto=Tema.PRIMARIO,
                                 ancho=198, alto=40, size=11).pack(pady=5)
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
        self.chips = GrupoChips(card, list(REGISTRO_ROLES.keys()))
        self.chips.place(relx=0.5, y=292, anchor="center")
        FabricaWidgets.boton(card, "Confirmar", self._continuar).place(relx=0.5, y=356, anchor="center")
        volver = tk.Label(card, text="Volver al inicio de sesión", font=Tema.fuente(9),
                          bg=Tema.CARD, fg=Tema.ACENTO, cursor="hand2")
        volver.place(relx=0.5, y=422, anchor="center")
        volver.bind("<Button-1>", lambda e: self.app.mostrar("login"))

    def _continuar(self):
        correo = self.e_correo.get().strip()
        p1, p2 = self.e_pass.get().strip(), self.e_conf.get().strip()
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
        for campo in self.estrategia.campos():
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

        FabricaWidgets.boton(card, "Confirmar", self._guardar).place(relx=0.5, y=460, anchor="center")

    def _guardar(self):
        datos = {}
        for clave, w in self.entradas.items():
            datos[clave] = w.valor() if isinstance(w, GrupoChips) else w.get().strip()
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
        for clave, etiqueta in [("nombre", "Nombre"), ("apellido", "Apellido"),
                                ("edad", "Edad"), ("nivel", "Nivel escolar")]:
            self.entradas[clave] = FabricaWidgets.campo_form(card, etiqueta, 45, y, 330)
            y += 78
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
        tk.OptionMenu(sel, self.var_pac,
                      *[f"{p.id} - {p.nombre} {p.apellido}" for p in pacientes]).pack(side="left", padx=8)

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
        for texto in preguntas:
            card = tk.Frame(parent, bg=Tema.CARD, padx=14, pady=8)
            card.pack(fill="x", pady=4)
            tk.Label(card, text=texto, font=Tema.fuente(10), bg=Tema.CARD,
                     fg=Tema.TEXTO, wraplength=560, justify="left").pack(anchor="w")
            v = tk.IntVar(value=0)
            fila = tk.Frame(card, bg=Tema.CARD)
            fila.pack(anchor="w", pady=(4, 0))
            for i, op in enumerate(escala):
                tk.Radiobutton(fila, text=op, variable=v, value=i, bg=Tema.CARD,
                               fg=Tema.TEXTO, selectcolor=Tema.FONDO_SUAVE,
                               font=Tema.fuente(9), activebackground=Tema.CARD).pack(side="left", padx=4)
            variables.append(v)
        return variables

    def _guardar(self):
        id_paciente = int(self.var_pac.get().split(" - ")[0])
        p_ina, p_hip, grupo, nivel = self.app.servicios.cuestionario.evaluar(
            [v.get() for v in self.vars_ina], [v.get() for v in self.vars_hip])
        resumen = f"Ina {p_ina}/27 - Hip {p_hip}/27"
        self.app.repos.paciente.actualizar_cuestionario(id_paciente, resumen, grupo, nivel)
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
        if not pacientes or not actividades:
            tk.Label(self.contenido, text="Se necesitan pacientes y actividades registrados.",
                     font=Tema.fuente(12), bg=Tema.FONDO, fg=Tema.MARCA).pack(padx=40)
            return
        card = FabricaWidgets.tarjeta(self.contenido, 460, 340)
        card.pack(padx=40, pady=10, anchor="w")
        tk.Label(card, text="Paciente", font=Tema.fuente(9), bg=Tema.CARD,
                 fg=Tema.TEXTO_TENUE).place(x=51, y=35)
        self.var_pac = tk.StringVar(value=f"{pacientes[0].id} - {pacientes[0].nombre}")
        tk.OptionMenu(card, self.var_pac,
                      *[f"{p.id} - {p.nombre} {p.apellido}" for p in pacientes]).place(x=45, y=55)
        tk.Label(card, text="Actividad", font=Tema.fuente(9), bg=Tema.CARD,
                 fg=Tema.TEXTO_TENUE).place(x=51, y=110)
        self.var_act = tk.StringVar(value=f"{actividades[0].id} - {actividades[0].nombre}")
        tk.OptionMenu(card, self.var_act,
                      *[f"{a.id} - {a.nombre}" for a in actividades]).place(x=45, y=130)
        self.e_fecha = FabricaWidgets.campo_form(card, "Fecha (AAAA-MM-DD)", 45, 180, 300)
        self.e_fecha.insert(0, str(date.today()))
        FabricaWidgets.boton(card, "Agendar", self._agendar).place(relx=0.5, y=300, anchor="center")

    def _agendar(self):
        id_p = int(self.var_pac.get().split(" - ")[0])
        id_a = int(self.var_act.get().split(" - ")[0])
        self.app.repos.agenda.agendar(id_p, id_a, self.e_fecha.get().strip())
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
        inicial = next((p for p in pacientes if p.id == id_paciente), pacientes[0])
        self.var_pac = tk.StringVar(value=f"{inicial.id} - {inicial.nombre} {inicial.apellido}")
        tk.OptionMenu(sel, self.var_pac,
                      *[f"{p.id} - {p.nombre} {p.apellido}" for p in pacientes],
                      command=lambda _: self._recargar()).pack(side="left", padx=8)
        self.cuerpo = tk.Frame(self.contenido, bg=Tema.FONDO)
        self.cuerpo.pack(fill="both", expand=True, padx=40, pady=10)
        self._pintar(inicial.id)

    def _recargar(self):
        for w in self.cuerpo.winfo_children():
            w.destroy()
        self._pintar(int(self.var_pac.get().split(" - ")[0]))

    def _pintar(self, id_paciente: int):
        repos = self.app.repos
        paciente = repos.paciente.obtener(id_paciente)
        tareas = repos.agenda.por_paciente(id_paciente)

        card = tk.Frame(self.cuerpo, bg=Tema.CARD, padx=20, pady=16)
        card.pack(fill="x")
        tk.Label(card, text=f"{paciente.nombre} {paciente.apellido}",
                 font=Tema.fuente(16, bold=True), bg=Tema.CARD, fg=Tema.TEXTO).pack(anchor="w")
        tk.Label(card, text=f"{paciente.edad} años · {paciente.nivel_escolar}",
                 font=Tema.fuente(10), bg=Tema.CARD, fg=Tema.TEXTO_TENUE).pack(anchor="w")

        tk.Label(card, text="Resultado del Test", font=Tema.fuente(12, bold=True),
                 bg=Tema.CARD, fg=Tema.ACENTO).pack(anchor="w", pady=(14, 4))
        if paciente.cuestionario or paciente.nivel_TDAH:
            fila = tk.Frame(card, bg=Tema.CARD)
            fila.pack(anchor="w", pady=2, fill="x")
            tk.Label(fila, text=f"{paciente.grupo_TDAH} - {paciente.nivel_TDAH}",
                     font=Tema.fuente(10), bg=Tema.CARD, fg=Tema.TEXTO).pack(side="left")
            if paciente.cuestionario:
                FabricaWidgets.insignia(fila, paciente.cuestionario, Tema.ACENTO, ancho=140).pack(side="left", padx=10)
        else:
            tk.Label(card, text="Sin evaluaciones registradas.", font=Tema.fuente(10),
                     bg=Tema.CARD, fg=Tema.TEXTO_TENUE).pack(anchor="w")

        tk.Label(card, text="Tareas Agendadas", font=Tema.fuente(12, bold=True),
                 bg=Tema.CARD, fg=Tema.ACENTO).pack(anchor="w", pady=(14, 4))
        if tareas:
            for nombre, fecha in tareas:
                fila = tk.Frame(card, bg=Tema.CARD)
                fila.pack(anchor="w", pady=3, fill="x")
                FabricaWidgets.insignia(fila, "Agendada", Tema.PENDIENTE, ancho=84).pack(side="left", padx=(0, 10))
                tk.Label(fila, text=f"{nombre}  ·  {fecha}", font=Tema.fuente(10),
                         bg=Tema.CARD, fg=Tema.TEXTO).pack(side="left")
        else:
            tk.Label(card, text="Sin tareas agendadas.", font=Tema.fuente(10),
                     bg=Tema.CARD, fg=Tema.TEXTO_TENUE).pack(anchor="w")

        barra = tk.Frame(self.cuerpo, bg=Tema.FONDO)
        barra.pack(anchor="w", pady=12)
        tk.Label(barra, text="Formato:", font=Tema.fuente(10, bold=True),
                 bg=Tema.FONDO, fg=Tema.MARCA).pack(side="left")
        self.var_fmt = tk.StringVar(value=EXPORTADORES[0].etiqueta)
        tk.OptionMenu(barra, self.var_fmt, *[e.etiqueta for e in EXPORTADORES]).pack(side="left", padx=8)
        FabricaWidgets.boton(barra, "IMPRIMIR / EXPORTAR REPORTES",
                             lambda: self._exportar(paciente, tareas), ancho=300).pack(side="left", padx=8)

    def _exportar(self, paciente, tareas):
        exportador = next(e for e in EXPORTADORES if e.etiqueta == self.var_fmt.get())
        ruta = filedialog.asksaveasfilename(defaultextension=exportador.extension,
                                            initialfile=f"reporte_{paciente.nombre}")
        if not ruta:
            return
        encabezado = {
            "Paciente": f"{paciente.nombre} {paciente.apellido}",
            "Edad": paciente.edad, "Nivel escolar": paciente.nivel_escolar,
            "Cuestionario": paciente.cuestionario, "Grupo TDAH": paciente.grupo_TDAH,
            "Nivel TDAH": paciente.nivel_TDAH,
        }
        exportador.exportar(ruta, encabezado, tareas)
        messagebox.showinfo("NeoAtención", f"Reporte exportado en:\n{ruta}")


class AplicacionNeoAtencion(tk.Tk):
    def __init__(self, repos, servicios):
        super().__init__()
        self.repos = repos
        self.servicios = servicios
        self.usuario_actual = None
        self.title("NeoAtención")
        self.geometry("960x680")
        self.configure(bg=Tema.FONDO)
        self.logo = tk.PhotoImage(data=LOGO_B64)
        self.logo_mini = self.logo.subsample(3, 3)
        self._contenedor = tk.Frame(self, bg=Tema.FONDO)
        self._contenedor.pack(fill="both", expand=True)
        self._rutas = {
            "login": PantallaLogin,
            "registro_usuario": PantallaRegistroUsuario,
            "registro_rol": PantallaRegistroRol,
            "menu": PantallaMenu,
            "registrar_paciente": PantallaRegistrarPaciente,
            "cuestionario": PantallaCuestionario,
            "crear_actividad": PantallaCrearActividad,
            "agendar": PantallaAgendar,
            "reportes": PantallaReportes,
        }
        self._pantalla_actual = None
        self.mostrar("login")

    def mostrar(self, nombre: str, **kwargs):
        if self._pantalla_actual is not None:
            self._pantalla_actual.destroy()
        clase = self._rutas[nombre]
        self._pantalla_actual = clase(self._contenedor, self, **kwargs)
        self._pantalla_actual.pack(fill="both", expand=True)


def main():
    conexion = ConexionMariaDB(ConfiguracionBD())
    try:
        conexion.conectar()
        InicializadorEsquema(conexion).crear_tablas()
    except Exception as e:
        raiz = tk.Tk()
        raiz.withdraw()
        messagebox.showerror(
            "NeoAtención - Error de conexión",
            "No se pudo conectar a la base de datos. Revisa host/puerto/usuario/contraseña "
            f"en la clase ConfiguracionBD.\n\nDetalle:\n{e}")
        raiz.destroy()
        return
    repos = Repositorios(
        usuario=RepositorioUsuario(conexion),
        tutor=RepositorioTutor(conexion),
        docente=RepositorioDocente(conexion),
        especialista=RepositorioEspecialista(conexion),
        paciente=RepositorioPaciente(conexion),
        actividad=RepositorioActividad(conexion),
        agenda=RepositorioAgenda(conexion))
    servicios = Servicios(
        autenticacion=ServicioAutenticacion(repos.usuario),
        cuestionario=ServicioCuestionario())
    app = AplicacionNeoAtencion(repos, servicios)
    try:
        app.mainloop()
    finally:
        conexion.cerrar()


if __name__ == "__main__":
    main()
