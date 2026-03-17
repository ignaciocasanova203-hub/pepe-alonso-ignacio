import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

class Pieza(ABC):
    def __init__(self, color):
        self.color = color
        self.tipo = "Base"
        self.simb = " " 

    @abstractmethod
    def mov_ok(self, orig, dest):
        pass

class Rey(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.simb = "♔" if color == "blanco" else "♚"

    def mov_ok(self, origen, destino):
        # Si el origen es el mismo que el destino devuelve false para no perder el turno
        if origen == destino: return False
        # Descomprimimos el array de las coordenadas de origen en filas y columnas y lo mismo con el destino
        f_o, c_o = origen 
        f_d, c_d = destino
        # Comporbamos que la resta del movimiento sea menor o igual a uno, es decir, solo se mueva un casilla y es absoluto porque puede moverse en cualquier dirección
        return abs(f_d - f_o) <= 1 and abs(c_o - c_d) <= 1

class Reina(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.simb = "♕" if color == "blanco" else "♛"

    def mov_ok(self, origen, destino):
        f_o, c_o = origen 
        f_d, c_d = destino
        f_diff, c_diff = abs(f_d - f_o), abs(c_d - c_o)
        # El primer parentesis comprueba que se ha movido en horizontal o en vertical (Esto lo hace comprobando que no se ha movido en un eje) y el segundo en diagonal (Comprueba que el movimiento en un eje es igual al del otro)
        return (f_d == f_o or c_o == c_d) or (f_diff == c_diff)

class Alfil(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.simb = "♗" if color == "blanco" else "♝"

    def mov_ok(self, origen, destino):
        f_o, c_o = origen 
        f_d, c_d = destino
        return abs(f_d - f_o) == abs(c_d - c_o)

class Caballo(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.simb = "♘" if color == "blanco" else "♞"

    def mov_ok(self, origen, destino):
        f_o, c_o = origen 
        f_d, c_d = destino
        f_diff, c_diff = abs(f_d - f_o), abs(c_d - c_o)
        #Aquí comprobamos que la diferencia entre el origne y el destino sea de 2 filas y una columna o una fila y dos columnas, como hace el caballo
        return (f_diff == 2 and c_diff == 1) or (f_diff == 1 and c_diff == 2)

class Torre(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.simb = "♖" if color == "blanco" else "♜"

    def mov_ok(self, origen, destino):
        f_o, c_o = origen
        f_d, c_d = destino
        return f_o == f_d or c_o == c_d

class Peon(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.simb = "♙" if color == "blanco" else "♟"
        self.ha_movido=False

    def mov_ok(self, orig, dest):
        f_o, c_o = orig
        f_d, c_d = dest
        #Hacemos que las blancas vayan arriba y las negras abajo
        dir = -1 if self.color == "blanco" else 1
    
        if c_o == c_d and f_d == f_o + dir: return True

        #Salto de dos casillas solo si es el primer movimiento
        if c_o == c_d and f_d == f_o + 2*dir and not self.ha_movido: return True
        #Movimiento diagonal al comer
        if abs(c_d - c_o) == 1 and f_d == f_o + dir: return True
        return False


class Tablero(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ajedrez - Movimientos")
        self.geometry("600x600")
        
        #ejec metedos de diseños
        self.botones = {}
        self.crear_tablero_visual()
        self.reiniciar_partida()

    def reiniciar_partida(self):
        self.matriz = [[None for _ in range(8)] for _ in range(8)]
        self.seleccion = None
        self.turno = "blanco"
        self.inicializar_piezas()
        self.reset_colores()
        self.dibujar_piezas_en_botones()

    def inicializar_piezas(self):
        orden = [Torre, Caballo, Alfil, Reina, Rey, Alfil, Caballo, Torre]
        for c in range(8):
            #piezas neg
            self.matriz[0][c] = orden[c]("negro")
            self.matriz[1][c] = Peon("negro")
            #piezas bla
            self.matriz[6][c] = Peon("blanco")
            self.matriz[7][c] = orden[c]("blanco")

    def crear_tablero_visual(self):
        for f in range(8):
            for c in range(8):
              #colores
                color_bg = "#eeeed2" if (f + c) % 2 == 0 else "#769656"
                #creacion de boton
                btn = tk.Button(
                    self, bg=color_bg, font=("Arial", 32),
                    relief="flat",
                    # Pasamos la posición al hacer clic
                    command=lambda f=f, c=c: self.gestionar_clic(f, c)
                )
                btn.grid(row=f, column=c, sticky="nsew")
                self.botones[(f, c)] = btn

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

    def gestionar_clic(self, f, c):
        if self.seleccion is None:
            # PRIMER CLIC: Seleccionar pieza
            pieza = self.matriz[f][c]
            if pieza and pieza.color == self.turno:
                self.seleccion = (f, c)
                self.botones[(f, c)].config(bg="yellow") # Feedback visual
        else:
            # SEGUNDO CLIC: Intentar mover
            f_orig, c_orig = self.seleccion
            pieza = self.matriz[f_orig][c_orig]
            destino = self.matriz[f][c]
            
            if pieza.mov_ok((f_orig, c_orig), (f, c)):
                # Comprobar si el objetivo es un Rey
                if isinstance(destino, Rey):
                    self.matriz[f][c] = pieza
                    self.matriz[f_orig][c_orig] = None
                    self.dibujar_piezas_en_botones()
                    messagebox.showinfo("Fin del juego", f"¡El equipo {self.turno} ha ganado!")
                    self.reiniciar_partida()
                    return

                # 1. Mover pieza en la matriz
                self.matriz[f][c] = pieza
                self.matriz[f_orig][c_orig] = None
                pieza.ha_movido = True
                
                # 2. Cambiar turno
                self.turno = "negro" if self.turno == "blanco" else "blanco"
            
            # Limpiar selección y redibujar
            self.reset_colores()
            self.seleccion = None
            self.dibujar_piezas_en_botones()

    def reset_colores(self):
        for (f, c), btn in self.botones.items():
            color_bg = "#eeeed2" if (f + c) % 2 == 0 else "#769656"
            btn.config(bg=color_bg)

    def dibujar_piezas_en_botones(self):
      
        #Lee la matriz de Pepe y pone los símbolos en los botones de Ignacio
        for f in range(8):
            for c in range(8):
                pieza = self.matriz[f][c]
                texto = pieza.simb if pieza else ""
                self.botones[(f, c)].config(text=texto)
#lanzamiento
if __name__ == "__main__":
    app = Tablero()
    app.mainloop()
