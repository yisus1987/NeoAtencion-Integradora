import tkinter as tk
import tkinter.font as tkfont

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