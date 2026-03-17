# =============================================================
# IGNACIO 
# =============================================================
class Tablero(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ajedrez - Diseño de Ignacio")
        self.geometry("600x600")
        
        # Matriz lógica guardaremos lo de Pepe y el  Diccionario  guardar  botones  de la pantalla
        self.matriz = [[None for _ in range(8)] for _ in range(8)]
        self.botones = {}
        
#ejec metedos de diseños
        self.inicializar_piezas()
        self.crear_tablero_visual()
        self.dibujar_piezas_en_botones()

    def inicializar_piezas(self):
        """Coloca los objetos de Pepe en la matriz según las reglas del ajedrez"""
#piezas neg
        orden_piezas = [Torre, Caballo, Alfil, Reina, Rey, Alfil, Caballo, Torre]
        for c in range(8):
            self.matriz[0][c] = orden_piezas[c]("negro")
            self.matriz[1][c] = Peon("negro")
            
#piezas bla
        for c in range(8):
            self.matriz[6][c] = Peon("blanco")
            self.matriz[7][c] = orden_piezas[c]("blanco")

    def crear_tablero_visual(self):
        """Crea la cuadrícula de botones con los colores blanco y gris"""
        for f in range(8):
            for c in range(8):
#colores
                color_casilla = "white" if (f + c) % 2 == 0 else "gray"
                
#creacion de boton
                btn = tk.Button(
                    self, 
                    bg=color_casilla, 
                    font=("Arial", 32),
                    relief="flat"
                )
                
                btn.grid(row=f, column=c, sticky="nsew")
                self.botones[(f, c)] = btn

# estira las casillas para que quede simetrico
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

    def dibujar_piezas_en_botones(self):
        """Lee la matriz de Pepe y pone los símbolos en los botones de Ignacio"""
        for f in range(8):
            for c in range(8):
                pieza = self.matriz[f][c]
                if pieza != None:
                    self.botones[(f, c)].config(text=pieza.simb)

#lanzamiento
if __name__ == "__main__":
    app = Tablero()
    app.mainloop()