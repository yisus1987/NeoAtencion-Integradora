import tkinter as tk
from conexion import ConexionMariaDB, ConfiguracionBD
from repositorios import (
    InicializadorEsquema, RepositorioUsuario, RepositorioTutor,
    RepositorioDocente, RepositorioEspecialista, RepositorioPaciente,
    RepositorioActividad, RepositorioAgenda, RepositorioResultadoTest, Repositorios
)
from servicios import ServicioAutenticacion, ServicioCuestionario, Servicios
from vistas import (
    PantallaLogin, PantallaRegistroUsuario, PantallaRegistroRol,
    PantallaMenu, PantallaRegistrarPaciente, PantallaCuestionario,
    PantallaCrearActividad, PantallaAgendar, PantallaReportes
)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NeoAtención")
        self.geometry("1000x700")
        self.configure(bg="#40BEEE")

        self.logo = tk.PhotoImage(file="Logo_final.png").subsample(2, 2)
        self.logo_mini = tk.PhotoImage(file="Logo_final.png").subsample(4, 4)

        config = ConfiguracionBD()
        conexion = ConexionMariaDB(config)
        conexion.conectar()

        inicializador = InicializadorEsquema(conexion)
        inicializador.crear_tablas()

        self.repos = Repositorios(
            usuario=RepositorioUsuario(conexion),
            tutor=RepositorioTutor(conexion),
            docente=RepositorioDocente(conexion),
            especialista=RepositorioEspecialista(conexion),
            paciente=RepositorioPaciente(conexion),
            actividad=RepositorioActividad(conexion),
            agenda=RepositorioAgenda(conexion),
            resultado_test=RepositorioResultadoTest(conexion)
        )

        self.servicios = Servicios(
            autenticacion=ServicioAutenticacion(self.repos.usuario),
            cuestionario=ServicioCuestionario()
        )

        self.usuario_actual = None
        self.pantalla_actual = None
        self.mostrar("login")

    def mostrar(self, nombre_vista, **kwargs):
        if self.pantalla_actual is not None:
            self.pantalla_actual.destroy()

        vistas = {
            "login": PantallaLogin,
            "registro_usuario": PantallaRegistroUsuario,
            "registro_rol": PantallaRegistroRol,
            "menu": PantallaMenu,
            "registrar_paciente": PantallaRegistrarPaciente,
            "cuestionario": PantallaCuestionario,
            "crear_actividad": PantallaCrearActividad,
            "agendar": PantallaAgendar,
            "reportes": PantallaReportes
        }

        clase_vista = vistas.get(nombre_vista)
        if clase_vista:
            self.pantalla_actual = clase_vista(self, self, **kwargs)
            self.pantalla_actual.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
