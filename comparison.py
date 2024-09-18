class Comparison:
    def __init__(self, df_sorteo, df_prospectos):
        self.df_sorteo = df_sorteo
        self.df_prospectos = df_prospectos

    def comparar_prospectos_con_resultados(self):
        numeros_sorteo = set(self.df_sorteo[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())
        numeros_prospecto = set(self.df_prospectos[['N1', 'N2', 'N3', 'N4', 'N5']].values.flatten())

        aciertos = len(numeros_sorteo & numeros_prospecto)
        numeros_acertados = list(numeros_sorteo & numeros_prospecto)

        return {
            'Numeros_Sorteo': numeros_sorteo,
            'Numeros_Prospecto': numeros_prospecto,
            'Aciertos': aciertos,
            'Numeros_Acertados': numeros_acertados,
        }
