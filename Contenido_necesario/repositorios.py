from abc import ABC, abstractmethod
from dataclasses import dataclass
from modelos import Usuario, Paciente, Actividad
from conexion import ConexionBD

class IRepositorioUsuario(ABC):
    @abstractmethod
    def crear(self, usuario: Usuario) -> int: ...
    @abstractmethod
    def autenticar(self, correo: str, contrasena: str) -> Usuario | None: ...

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
                id_especialista INT,
                fecha DATE,
                FOREIGN KEY (id_Paciente) REFERENCES Paciente(id),
                FOREIGN KEY (id_actividad) REFERENCES Actividades(id),
                FOREIGN KEY (id_especialista) REFERENCES Especialista(id)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS resultado_test (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_Paciente INT,
                fecha DATE,
                puntaje_inatencion INT,
                puntaje_hiperactividad INT,
                grupos_TDAH VARCHAR(50),
                nivel_TDAH VARCHAR(50),
                FOREIGN KEY (id_Paciente) REFERENCES Paciente(id)
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
            "INSERT INTO crear_Tutor_Padre (nombre, apellido, correo_electronico, telefono, Parentesco, id_Usuario) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                datos.get("nombre"), 
                datos.get("apellido"), 
                datos.get("correo_electronico"),
                datos.get("telefono"), 
                datos.get("parentesco"), 
                id_usuario
            )
        )
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
            "INSERT INTO crear_Docente (nombre, apellido, correo_electronico, telefono, nombre_escuela, id_Usuario) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                datos.get("nombre"), 
                datos.get("apellido"), 
                datos.get("correo_electronico"),
                datos.get("telefono"), 
                datos.get("nombre_escuela"), 
                id_usuario
            )
        )
        self._conexion.commit()
        cur.close()

class RepositorioEspecialista:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, datos: dict) -> None:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO Especialista (nombre, descripcion) "
            "VALUES (%s, %s)",
            (datos.get("nombre"), datos.get("descripcion"))
        )
        self._conexion.commit()
        cur.close()

    def listar(self) -> list[tuple]:
        cur = self._conexion.cursor()
        cur.execute("SELECT id, nombre FROM Especialista")
        filas = cur.fetchall()
        cur.close()
        return filas

class RepositorioPaciente:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, paciente: Paciente) -> None:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO Paciente (nombre, apellido, edad, Nivel_escolar, id_tutor_padre) "
            "VALUES (%s, %s, %s, %s, %s)",
            (paciente.nombre, paciente.apellido, paciente.edad, paciente.nivel_escolar, paciente.id_tutor_padre)
        )
        self._conexion.commit()
        cur.close()

    def listar(self) -> list[Paciente]:
        cur = self._conexion.cursor()
        cur.execute("SELECT id, nombre, apellido, edad, Nivel_escolar, id_tutor_padre, cuestionario, grupo_TDAH, nivel_TDAH FROM Paciente")
        filas = cur.fetchall()
        cur.close()
        pacientes = []
        i = 0
        while i < len(filas):
            f = filas[i]
            pacientes.append(Paciente(id=f[0], nombre=f[1], apellido=f[2], edad=f[3], nivel_escolar=f[4], id_tutor_padre=f[5], cuestionario=f[6], grupo_TDAH=f[7], nivel_TDAH=f[8]))
            i += 1
        return pacientes

    def actualizar_cuestionario(self, id_paciente: int, resumen: str, grupo: str, nivel: str) -> None:
        cur = self._conexion.cursor()
        cur.execute(
            "UPDATE Paciente SET cuestionario = %s, grupo_TDAH = %s, nivel_TDAH = %s WHERE id = %s",
            (resumen, grupo, nivel, id_paciente)
        )
        self._conexion.commit()
        cur.close()

class RepositorioResultadoTest:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion
        
    def crear(self, id_paciente: int, fecha: str, p_ina: int, p_hip: int, grupo: str, nivel: str) -> None:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO resultado_test (id_Paciente, fecha, puntaje_inatencion, puntaje_hiperactividad, grupos_TDAH, nivel_TDAH) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (id_paciente, fecha, p_ina, p_hip, grupo, nivel)
        )
        self._conexion.commit()
        cur.close()

class RepositorioActividad:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def crear(self, actividad: Actividad) -> None:
        cur = self._conexion.cursor()
        cur.execute(
            "INSERT INTO Actividades (nombre_actividad, descripcion, Tipo_actividad, Designacion_actividad, objetivo) "
            "VALUES (%s, %s, %s, %s, %s)",
            (actividad.nombre, actividad.descripcion, actividad.tipo, actividad.designacion, actividad.objetivo)
        )
        self._conexion.commit()
        cur.close()

    def listar(self) -> list[Actividad]:
        cur = self._conexion.cursor()
        cur.execute("SELECT id, nombre_actividad, descripcion, Tipo_actividad, Designacion_actividad, objetivo FROM Actividades")
        filas = cur.fetchall()
        cur.close()
        actividades = []
        i = 0
        while i < len(filas):
            f = filas[i]
            actividades.append(Actividad(id=f[0], nombre=f[1], descripcion=f[2], tipo=f[3], designacion=f[4], objetivo=f[5]))
            i += 1
        return actividades

class RepositorioAgenda:
    def __init__(self, conexion: ConexionBD):
        self._conexion = conexion

    def agendar(self, id_paciente: int, id_actividad: int, id_especialista: int, fecha: str) -> None:
        cur = self._conexion.cursor()
        cur.execute("INSERT INTO agenda_actividad (id_Paciente, id_actividad, id_especialista, fecha) "
                    "VALUES (%s, %s, %s, %s)", (id_paciente, id_actividad, id_especialista, fecha))
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
    resultado_test: RepositorioResultadoTest
