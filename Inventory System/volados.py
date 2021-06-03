# Metodo de Volados

class SimulationVolados:
    results = ""
    win = 0
    lose = 0
    initDinero = 0
    initApuesta = 0
    def __init__(self, dinero, apuesta):
        self.initApuesta = apuesta
        self.initDinero = dinero   

    def RecursividadVolados(self, C, dinero, apuesta, num, numbers):
        Gano = "Gano SE REINICIA EL JUEGO\n\n"
        Perdio = "Perdio todo SE GENERA OTRO JUEGO\n\n"
        text1 = str(num[C]) + " tiene: " + str(dinero) + " aposto: " + \
            str(apuesta) + " Y gano, su dinero ahora es: " + \
            str(dinero + apuesta)+"\n\n"
        text2 = str(num[C]) + " tiene: " + str(dinero) + " aposto: " + \
            str(apuesta) + " Y perdio, su dinero ahora es: " + \
            str(dinero - apuesta)+"\n\n"

        if C < numbers-1:
            if dinero == 50:
                self.results+=Gano # Mensaje de ganador
                self.win+=1
                C = C + 1
                dinero = self.initDinero
                apuesta = self.initApuesta
                self.RecursividadVolados(C, dinero, apuesta, num, numbers)
            elif C > 0 and dinero == 0:
                self.results+=Perdio  # Mensaje de perdedor
                self.lose+=1
                C = C + 1
                dinero = self.initDinero
                apuesta = self.initApuesta
                self.RecursividadVolados(C, dinero, apuesta, num, numbers)
            elif dinero >= apuesta:
                if num[C] < 0.5:

                    self.results+=text1 # gano
                    self.win+=1
                    C = C + 1
                    self.RecursividadVolados(C, (dinero + apuesta), 10, num, numbers)
                else:
                    self.results+=text2 # Perdio
                    self.lose+=1
                    self.results +=("tendra que apostar el doble: " + str(apuesta * 2) + "\n\n")
                    C = C + 1
                    self.RecursividadVolados(C, (dinero - apuesta), (apuesta * 2), num, numbers)
            else:
                self.results+=("La apuesta es mayor al dinero que tienes" + "\n\n")
                self.results+=("ahora solo apostaras: " + str(dinero) + "\n\n")

                self.RecursividadVolados(C, dinero, dinero, num, numbers)
        else:
            self.results+="Se terminaron los numeros"
        

        
