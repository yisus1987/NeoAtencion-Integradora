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
        return Noneclass RepositorioTutor:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar_tutor_padre(self, nombre, apellido, correo_electronico, telefono, parentesco, id_usuario):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO crear_Tutor_Padre (nombre, apellido, correo_electronico, telefono, Parentesco, id_Usuario) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, apellido, correo_electronico, telefono, parentesco, id_usuario)
        cursor.execute(sql, valores)
        self.conexion.commit()

class RepositorioDocente:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar_docente(self, nombre, apellido, correo_electronico, telefono, id_usuario):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO crear_Docente (nombre, apellido, correo_electronico, telefono, id_Usuario) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre, apellido, correo_electronico, telefono, id_usuario)
        cursor.execute(sql, valores)
        self.conexion.commit()

class RepositorioPaciente:
    def __init__(self, conexion):
        self.conexion = conexion

    def registrar_historial_clinico(self, id_paciente, fecha, puntaje_inatencion, puntaje_hiperactividad, grupos_tdah, nivel_tdah):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO resultado_test (id_Paciente, fecha, puntaje_inatencion, puntaje_hiperactividad, grupos_TDAH, nivel_TDAH) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (id_paciente, fecha, puntaje_inatencion, puntaje_hiperactividad, grupos_tdah, nivel_tdah)
        cursor.execute(sql, valores)
        self.conexion.commit()

class RepositorioActividad:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar_actividad(self, nombre_actividad, descripcion, tipo_actividad, designacion_actividad, objetivo):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO Actividades (nombre_actividad, descripcion, Tipo_actividad, Designacion_actividad, objetivo) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre_actividad, descripcion, tipo_actividad, designacion_actividad, objetivo)
        cursor.execute(sql, valores)
        self.conexion.commit()

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
