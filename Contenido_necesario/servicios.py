import csv
from abc import ABC, abstractmethod
from dataclasses import dataclass
from modelos import Campo, Usuario
from repositorios import IRepositorioUsuario

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