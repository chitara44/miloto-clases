import pandas as pd
from data_processor import DataProcessor
from prospect_generator import ProspectGenerator
from file_manager import FileManager
from comparison import Comparison

class LotteryAnalyzer:
    def __init__(self, df_original):
        self.df_original = df_original
        self.file_manager = FileManager()

    def proceso_completo(self):
        df_sorteos_ordenados = self.df_original.sort_values(by='IdSorteo')
        resultados_comparacion = []

        for idx in range(10, len(df_sorteos_ordenados) + 1):
            df_previos = df_sorteos_ordenados.iloc[:idx]
            id_sorteo = df_sorteos_ordenados.iloc[idx - 1]['IdSorteo']

            # Data Processor
            data_processor = DataProcessor(df_previos)
            resultados_numeros = data_processor.calcular_intervalos(['N1', 'N2', 'N3', 'N4', 'N5'])

            # Cargar prospectos
            df_prospectos_fusion = self.file_manager.cargar_prospectos('Fusión', id_sorteo)
            df_prospectos_promedio = self.file_manager.cargar_prospectos('Promedio', id_sorteo)
            df_prospectos_mediana = self.file_manager.cargar_prospectos('Mediana', id_sorteo)

            # Generar prospectos si no están cargados
            if df_prospectos_fusion.empty:
                prospect_generator = ProspectGenerator(resultados_numeros)
                df_prospectos_fusion = prospect_generator.generar_prospectos_con_peso('Probabilidad_Fusion', 'Fusión')
                self.file_manager.guardar_prospectos(df_prospectos_fusion, 'Fusión', id_sorteo)

            if df_prospectos_promedio.empty:
                prospect_generator = ProspectGenerator(resultados_numeros)
                df_prospectos_promedio = prospect_generator.generar_prospectos_con_peso('Probabilidad_Avg', 'Promedio')
                self.file_manager.guardar_prospectos(df_prospectos_promedio, 'Promedio', id_sorteo)

            if df_prospectos_mediana.empty:
                prospect_generator = ProspectGenerator(resultados_numeros)
                df_prospectos_mediana = prospect_generator.generar_prospectos_con_peso('Probabilidad_Mediana', 'Mediana')
                self.file_manager.guardar_prospectos(df_prospectos_mediana, 'Mediana', id_sorteo)

            # Concatenar prospectos
            df_prospectos = pd.concat([df_prospectos_fusion, df_prospectos_promedio, df_prospectos_mediana], ignore_index=True)

            # Comparar prospectos con el siguiente sorteo
            siguiente_sorteo = df_sorteos_ordenados.iloc[idx] if idx < len(df_sorteos_ordenados) else df_sorteos_ordenados.iloc[-1]
            comparison = Comparison(siguiente_sorteo, df_prospectos)
            resultado_comparacion = comparison.comparar_prospectos_con_resultados()
            resultados_comparacion.append(resultado_comparacion)

        return pd.DataFrame(resultados_comparacion)

if __name__ == "__main__":
    df = pd.read_csv('data.csv')
    analyzer = LotteryAnalyzer(df)
    df_resultados_comparacion = analyzer.proceso_completo()
    df_resultados_comparacion.to_csv('comparing_results.csv', index=False)
