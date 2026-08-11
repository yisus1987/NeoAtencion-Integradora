from abc import ABC, abstractmethod
import mysql.connector
from modelos import ConfiguracionBD

class ConexionBD(ABC):
    @abstractmethod
    def cursor(self): ...
    @abstractmethod
    def commit(self) -> None: ...
    @abstractmethod
    def cerrar(self) -> None: ...

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
