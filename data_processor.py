import pandas as pd
from statistics import median

class DataProcessor:
    def __init__(self, df):
        self.df = df

    def calcular_intervalos(self, columnas):
        resultados = []
        df_melted = self.df.melt(id_vars=['IdSorteo'], value_vars=columnas, var_name='Grupo', value_name='Numero')
        df_melted = df_melted.dropna().sort_values(by=['Numero', 'IdSorteo'])
        sorteos = self.df['IdSorteo'].unique()

        for num in df_melted['Numero'].unique():
            subset = df_melted[df_melted['Numero'] == num]
            apariciones = subset['IdSorteo'].values

            if len(apariciones) > 0:
                segmentos = [apariciones[0] - sorteos[0]] + [apariciones[i] - apariciones[i-1] for i in range(1, len(apariciones))]
                if apariciones[-1] < sorteos[-1]:
                    segmentos.append(sorteos[-1] - apariciones[-1])

                promedio = sum(segmentos) / len(segmentos)
                mediana_valor = median(segmentos)
                ultimos_sorteos = sorteos[-1] - apariciones[-1]

                probabilidad_avg = ultimos_sorteos / promedio if ultimos_sorteos <= promedio else promedio / ultimos_sorteos
                probabilidad_mediana = ultimos_sorteos / mediana_valor if ultimos_sorteos <= mediana_valor else mediana_valor / ultimos_sorteos
                probabilidad_fusion = (probabilidad_avg + probabilidad_mediana) / 2

                resultados.append((num, segmentos, promedio, mediana_valor, ultimos_sorteos, probabilidad_avg, probabilidad_mediana, probabilidad_fusion))

        return pd.DataFrame(resultados, columns=['Numero', 'Intervalos', 'Promedio', 'Mediana', 'UltimosSorteos', 'Probabilidad_Avg', 'Probabilidad_Mediana', 'Probabilidad_Fusion'])
