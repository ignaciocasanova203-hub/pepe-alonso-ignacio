class Caballo:
    def __init__(self,blanca=True):
        self.blanca=blanca
        self.movimientos=[[1,2],[2,1]] #Esto en todas direcciones, es decir -1,2; -1,-2; 1,-2. Esto se hace en un for al hacer click y se resaltan aquellas casilla. 