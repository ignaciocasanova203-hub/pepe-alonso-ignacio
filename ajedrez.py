class Pieza:
    def __init__(self, color):
        self.color = color
        self.tipo = "Base"
        self.simb = " " 
        self.ha_movido = False 

    def mov_ok(self, orig, dest):
        raise NotImplementedError("Este método debe ser sobrescrito en las subclases.")


class Rey(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.tipo = "Rey"
        self.simb = "♔" if color == "blanco" else "♚"

    def mov_ok(self, orig, dest):
        f_orig, c_orig = orig
        f_dest, c_dest = dest
        return abs(f_dest - f_orig) <= 1 and abs(c_dest - c_orig) <= 1


class Reina(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.tipo = "Reina"
        self.simb = "♕" if color == "blanco" else "♛"

    def mov_ok(self, orig, dest):
        f_orig, c_orig = orig
        f_dest, c_dest = dest
        mov_recto = (f_orig == f_dest) or (c_orig == c_dest)
        mov_diag = abs(f_dest - f_orig) == abs(c_dest - c_orig)
        return mov_recto or mov_diag


class Alfil(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.tipo = "Alfil"
        self.simb = "♗" if color == "blanco" else "♝"

    def mov_ok(self, orig, dest):
        f_orig, c_orig = orig
        f_dest, c_dest = dest
        return abs(f_dest - f_orig) == abs(c_dest - c_orig)


class Caballo(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.tipo = "Caballo"
        self.simb = "♘" if color == "blanco" else "♞"

    def mov_ok(self, orig, dest):
        f_orig, c_orig = orig
        f_dest, c_dest = dest
        dif_f = abs(f_dest - f_orig)
        dif_c = abs(c_dest - c_orig)
        return (dif_f == 2 and dif_c == 1) or (dif_f == 1 and dif_c == 2)


class Torre(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.tipo = "Torre"
        self.simb = "♖" if color == "blanco" else "♜"

    def mov_ok(self, orig, dest):
        f_orig, c_orig = orig
        f_dest, c_dest = dest
        return (f_orig == f_dest) or (c_orig == c_dest)


class Peon(Pieza):
    def __init__(self, color):
        super().__init__(color)
        self.tipo = "Peon"
        self.simb = "♙" if color == "blanco" else "♟"

    def mov_ok(self, orig, dest):
        f_orig, c_orig = orig
        f_dest, c_dest = dest
        
        direccion = -1 if self.color == "blanco" else 1 
        
        if c_orig == c_dest and f_dest == f_orig + direccion:
            return True
        if c_orig == c_dest and f_dest == f_orig + (2 * direccion) and not self.ha_movido:
            return True
        if abs(c_dest - c_orig) == 1 and f_dest == f_orig + direccion:
            return True
            
        return False


def crear_matriz_tablero():
    tablero = [[None for _ in range(8)] for _ in range(8)]
    
    orden_piezas = [Torre, Caballo, Alfil, Reina, Rey, Alfil, Caballo, Torre]
    
    for i in range(8):
        tablero[0][i] = orden_piezas[i]("negro")
        tablero[1][i] = Peon("negro")
        
        tablero[6][i] = Peon("blanco")
        tablero[7][i] = orden_piezas[i]("blanco")
        
    return tablero