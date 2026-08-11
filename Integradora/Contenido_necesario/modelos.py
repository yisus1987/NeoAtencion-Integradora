from dataclasses import dataclass, field

@dataclass
class ConfiguracionBD:
    host: str = "localhost"
    port: int = 3307
    user: str = "root"
    password: str = "patho2325"
    database: str = "gestion_tdah"

@dataclass
class Usuario:
    nombre_usuario: str
    contrasena: str
    correo: str
    id: int | None = None
    rol: str = "Usuario"

@dataclass
class ResultadoTest:
    id_paciente: int
    fecha: str
    puntaje_inatencion: int
    puntaje_hiperactividad: int
    grupos_TDAH: str
    nivel_TDAH: str
    id: int | None = None

@dataclass
class Paciente:
    nombre: str
    apellido: str
    edad: int
    nivel_escolar: str
    id_tutor_padre: int
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