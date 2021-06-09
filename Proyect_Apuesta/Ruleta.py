import pandas as pd


class ApuestaRuleta:
    nJuegos = 0
    pseudo = None

    apuesta1 = 1
    apuesta2 = 1
    Ainicial1 = 0  # Valor que se pide
    Ainicial2 = 0
    ganancia1 = 0
    ganancia2 = 0
    Vganadas1 = 0
    Vperdidas1 = 0
    empate = 0
    gana = True

    data_simulation = {
        "número de juego": [],
        "resultado": [],
        "jugador 1": [],
        "jugador 2": [],
    }

    #Resultado='Se Gano ', str(Vganadas1) +' juegos y perdio ', str(Vperdidas1), ' juegos'
    Resultado = ""

    def __init__(self, pseudo, nJuegos, Ainicial):
        self.pseudo = pseudo
        self.nJuegos = nJuegos
        self.Ainicial1 = Ainicial
        self.Ainicial2 = Ainicial
        self.Resultado = ""
        self.data_simulation = {
            "número de juego": [],
            "resultado": [],
            "jugador 1": [],
            "jugador 2": [],
        }
        self.Vperdidas1 = 0
        self.Vganadas1 = 0
        self.empate = 0

    def ApuestaNegro(self):

        ##num = [0.11399, 0.52632, 0.17152, 0.33645, 0.99453, 0.46050, 0.52373, 0.91012, 0.93542, 0.48997]

        for i in range(0, self.nJuegos):
            self.data_simulation["número de juego"].append(i+1)
            if(self.pseudo[i] > 0 and self.pseudo[i] <= 0.4545):
                self.gana = False
                # print()
                self.data_simulation["resultado"].append('Pierde')
                self.Vperdidas1 += 1
                self.ganancia1 -= 1
                self.data_simulation["jugador 1"].append(self.apuesta1)
            elif(self.pseudo[i] > 0.4545 and self.pseudo[i] <= 0.9090):
                self.gana = True
                #print('Gana '+ str(self.apuesta))
                self.data_simulation["resultado"].append('Gana')
                self.ganancia1 += 1
                self.Vganadas1 += 1
                self.data_simulation["jugador 1"].append(self.apuesta1)
            elif(self.pseudo[i] > 0.9090 and self.pseudo[i] <= 1):
                #print('Se mantiene la apuesta '+ str(self.apuesta))
                self.apuesta1 = self.apuesta1
                self.data_simulation['resultado'].append(
                    'Se mantiene la apuesta')
                self.empate+=1
                self.data_simulation["jugador 1"].append(self.apuesta1)

            if(self.gana):
                self.ganancia2 += self.apuesta2
                self.data_simulation["jugador 2"].append(self.apuesta2)
                self.apuesta2 = 1
            else:
                if(self.apuesta2 < 500):
                    self.ganancia2 -= self.apuesta2
                    self.data_simulation["jugador 2"].append(self.apuesta2)
                    self.apuesta2 = 2*self.apuesta2
                else:
                    self.ganancia2 -= self.apuesta2
                    self.data_simulation["jugador 2"].append(self.apuesta2)
                    self.apuesta2 = 1

        if(self.ganancia1 > 1):
            self.Resultado += f"El jugador num 1 obtuvo {str(self.Ainicial1+self.ganancia1)}\n y obtuvo ganancias de {str(self.ganancia1)}"
        else:
            self.Resultado += f"El jugador num 1 obtuvo {str(self.Ainicial1+self.ganancia1)}\n y obtuvo perdidas de {str(self.ganancia1)}"

        if(self.ganancia2 > 1):
            self.Resultado += f"El jugador num 2 obtuvo {str(self.Ainicial2+self.ganancia2)}\n y obtuvo ganancias de {str(self.ganancia2)}"
        else:
            self.Resultado += f"El jugador num 2 obtuvo {str(self.Ainicial2+self.ganancia2)}\n y obtuvo perdidas de {str(self.ganancia2)}"

        self.Resultado += f"Se Gano {str(self.Vganadas1)} juegos y perdio {str(self.Vperdidas1)} juegos"
        df = pd.DataFrame(self.data_simulation)
        print(df)

    def ApuestaRojo(self):

        for i in range(0, self.nJuegos):
            self.data_simulation["número de juego"].append(i+1)
            if(self.pseudo[i] > 0 and self.pseudo[i] <= 0.4545):
                self.gana = True
                ##print('Gana '+ str(self.apuesta))
                self.data_simulation["resultado"].append('Gana')
                self.ganancia1 += 1
                self.Vganadas1 += 1
                self.data_simulation["jugador 1"].append(self.apuesta1)
            elif(self.pseudo[i] > 0.4545 and self.pseudo[i] <= 0.9090):
                self.gana = False
                ##print('Pierde '+ str(self.apuesta))

                self.data_simulation["resultado"].append('Pierde')
                self.ganancia1 -= 1
                self.Vperdidas1 += 1
                self.data_simulation["jugador 1"].append(self.apuesta1)
            elif(self.pseudo[i] > 0.9090 and self.pseudo[i] <= 1):
                self.apuesta1 = self.apuesta1
                self.data_simulation['resultado'].append(
                    'Se mantiene la apuesta')
                self.empate+=1
                self.data_simulation["jugador 1"].append(self.apuesta1)

            if(self.gana):
                self.ganancia2 += self.apuesta2
                self.data_simulation["jugador 2"].append(self.apuesta2)
                self.apuesta2 = 1
            else:
                if(self.apuesta2 < 500):
                    self.ganancia2 -= self.apuesta2
                    self.data_simulation["jugador 2"].append(self.apuesta2)
                    self.apuesta2 = 2*self.apuesta2
                else:
                    self.ganancia2 -= self.apuesta2
                    self.data_simulation["jugador 2"].append(self.apuesta2)
                    self.apuesta2 = 1

        if(self.ganancia1 > 1):
            self.Resultado += f"\nEl jugador num 1 obtuvo {str(self.Ainicial1+self.ganancia1)} y obtuvo ganancias de {str(self.ganancia1)}"

        else:
            self.Resultado += f"\nEl jugador num 1 obtuvo {str(self.Ainicial1+self.ganancia1)} y obtuvo perdidas de {str(self.ganancia1)}"

        if(self.ganancia2 > 1):
            self.Resultado += f"\nEl jugador num 2 obtuvo {str(self.Ainicial2+self.ganancia2)} y obtuvo ganancias de {str(self.ganancia2)}"
        else:
            self.Resultado += f"\nEl jugador num 2 obtuvo {str(self.Ainicial2+self.ganancia2)} y obtuvo perdidas de {str(self.ganancia2)}"

        self.Resultado += f"\nSe Gano {str(self.Vganadas1)} juegos y perdio {str(self.Vperdidas1)} juegos"
        df = pd.DataFrame(self.data_simulation)
        print(df)

# test= [0.11399, 0.52632, 0.17152, 0.33645, 0.99453, 0.46050, 0.52373, 0.91012, 0.93542, 0.48997]
# A = ApuestaRuleta(test, 5, 200) #Declarando un objeto de clase
# B = ApuestaRuleta(test, 5, 200) #Declarando un objeto de clase
# A.ApuestaRojo()
# B.ApuestaNegro()
