import pandas as pd
from itertools import combinations

class ProspectGenerator:
    def __init__(self, resultados_numeros):
        self.resultados_numeros = resultados_numeros

    def generar_prospectos_con_peso(self, metrica, metodo_calculo):
        numeros_prospecto = self.resultados_numeros[self.resultados_numeros[metrica] > 0.65]
        numeros_prospecto = numeros_prospecto.sort_values(by=metrica, ascending=False)

        combinaciones = []
        for comb in combinations(numeros_prospecto['Numero'], 5):
            comb_ordenada = sorted(comb)
            probabilidad_comb = numeros_prospecto[numeros_prospecto['Numero'].isin(comb_ordenada)][metrica].sum()
            combinaciones.append((*comb_ordenada, probabilidad_comb, metodo_calculo))
        
        return pd.DataFrame(combinaciones, columns=['N1', 'N2', 'N3', 'N4', 'N5', 'Peso', 'MetodoCalculo'])
