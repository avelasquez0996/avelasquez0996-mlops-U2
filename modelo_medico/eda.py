"""
Análisis Exploratorio de Datos (EDA)
Etapa 3 del pipeline: Análisis exploratorio
Estudia correlaciones entre variables y visualiza síntomas frecuentes.
"""

from src.data_loader import DataLoader
import numpy as np


class ExploratoryDataAnalysis:
    """Realiza análisis exploratorio de los datos"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.datos = None
    
    def cargar_y_analizar(self, cantidad=1000):
        """
        Carga datos y realiza análisis exploratorio.
        
        Args:
            cantidad (int): Cantidad de registros a analizar
            
        Returns:
            dict: Resumen del análisis
        """
        # Cargar datos procesados
        self.datos = self.data_loader.obtener_datos_procesados(cantidad)
        
        resumen = {
            "cantidad_registros": len(self.datos),
            "estadisticas_descriptivas": self._estadisticas_descriptivas(),
            "correlaciones": self._analizar_correlaciones(),
            "distribucion_diagnosticos": self._distribucion_diagnosticos()
        }
        
        return resumen
    
    def _estadisticas_descriptivas(self):
        """
        Calcula estadísticas descriptivas de las variables.
        
        Returns:
            dict: Estadísticas por variable
        """
        campos = ["edad", "fiebre", "dolor"]
        estadisticas = {}
        
        for campo in campos:
            valores = [r[campo] for r in self.datos]
            
            estadisticas[campo] = {
                "media": round(np.mean(valores), 2),
                "std": round(np.std(valores), 2),
                "min": round(np.min(valores), 2),
                "max": round(np.max(valores), 2),
                "mediana": round(np.median(valores), 2)
            }
        
        return estadisticas
    
    def _analizar_correlaciones(self):
        """
        Analiza correlaciones entre variables.
        
        Returns:
            dict: Matriz de correlaciones
        """
        campos = ["edad", "fiebre", "dolor"]
        datos_array = np.array([[r[c] for c in campos] for r in self.datos])
        
        # Calcular matriz de correlación
        matriz_corr = np.corrcoef(datos_array.T)
        
        correlaciones = {}
        for i, campo1 in enumerate(campos):
            for j, campo2 in enumerate(campos):
                clave = f"{campo1}_vs_{campo2}"
                correlaciones[clave] = round(matriz_corr[i, j], 3)
        
        return correlaciones
    
    def _distribucion_diagnosticos(self):
        """
        Analiza la distribución de diagnósticos.
        
        Returns:
            dict: Conteos y porcentajes por diagnóstico
        """
        diagnosticos = {}
        
        for registro in self.datos:
            diag = registro.get("diagnostico", "DESCONOCIDO")
            diagnosticos[diag] = diagnosticos.get(diag, 0) + 1
        
        total = len(self.datos)
        distribucion = {
            diag: {
                "count": count,
                "porcentaje": round((count / total) * 100, 2)
            }
            for diag, count in diagnosticos.items()
        }
        
        return distribucion
    
    def mostrar_resumen(self, resumen):
        """
        Imprime un resumen legible del análisis.
        
        Args:
            resumen (dict): Resultado de cargar_y_analizar
        """
        print("\n" + "="*60)
        print("ANÁLISIS EXPLORATORIO DE DATOS (EDA)")
        print("="*60)
        
        print(f"\nRegistros analizados: {resumen['cantidad_registros']}")
        
        print("\n--- Estadísticas Descriptivas ---")
        for campo, stats in resumen['estadisticas_descriptivas'].items():
            print(f"\n{campo}:")
            for metrica, valor in stats.items():
                print(f"  {metrica}: {valor}")
        
        print("\n--- Correlaciones entre Variables ---")
        for par, corr in resumen['correlaciones'].items():
            print(f"  {par}: {corr}")
        
        print("\n--- Distribución de Diagnósticos ---")
        for diag, stats in resumen['distribucion_diagnosticos'].items():
            print(f"  {diag}: {stats['count']} casos ({stats['porcentaje']}%)")
        
        print("\n" + "="*60)


if __name__ == "__main__":
    eda = ExploratoryDataAnalysis()
    resumen = eda.cargar_y_analizar(cantidad=1000)
    eda.mostrar_resumen(resumen)
