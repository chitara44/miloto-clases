import os
import pandas as pd

class FileManager:
    def __init__(self):
        pass

    def guardar_prospectos(self, df_prospectos, metodo_calculo, id_sorteo):
        filename = f'prospectos_{id_sorteo}_{metodo_calculo}.csv'
        if os.path.exists(filename):
            df_existente = pd.read_csv(filename)
            df_combined = pd.concat([df_existente, df_prospectos]).drop_duplicates().reset_index(drop=True)
        else:
            df_combined = df_prospectos

        df_combined.to_csv(filename, index=False)
        print(f'Prospectos guardados en {filename}')

    def cargar_prospectos(self, metodo_calculo, id_sorteo):
        filename = f'prospectos_{id_sorteo}_{metodo_calculo}.csv'
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f'No se encontraron prospectos previos para {metodo_calculo}')
            return pd.DataFrame()
