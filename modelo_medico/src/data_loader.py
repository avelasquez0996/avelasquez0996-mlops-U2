"""
Módulo de carga y gestión de datos.
Simula la carga de datos desde diferentes fuentes (EHRs, bases de datos abiertas, sintéticos).
"""


class DataLoader:
    """
    Cargador de datos que simula diferentes fuentes de datos clínicos.
    
    Fuentes de datos simuladas:
    - Registros clínicos electrónicos (EHRs)
    - Bases de datos abiertas
    - Datos sintéticos para enfermedades raras
    """
    
    def __init__(self):
        self.datos_cargados = []
    
    def cargar_datos_sinteticos(self, cantidad=1000):
        """
        Carga datos sintéticos generados para simular registros clínicos.
        Simula el Dataset de EHRs con anonimización.
        
        Args:
            cantidad (int): Número de registros a generar
            
        Returns:
            list: Lista de diccionarios con datos de pacientes
        """
        import random
        import numpy as np
        
        random.seed(42)
        np.random.seed(42)
        
        datos = []
        
        # Distribuciones realistas de síntomas
        for i in range(cantidad):
            registro = {
                "id_paciente": f"PAC_{i:06d}",  # Anonimizado
                "edad": np.random.randint(1, 85),
                "fiebre": round(np.random.normal(37.2, 1.5), 1),
                "dolor": np.random.randint(0, 11),
                "diagnostico": self._asignar_diagnostico_sintetico()
            }
            
            # Asegurar valores válidos
            registro["fiebre"] = max(35, min(45, registro["fiebre"]))
            registro["dolor"] = max(0, min(10, registro["dolor"]))
            
            datos.append(registro)
        
        self.datos_cargados = datos
        return datos
    
    @staticmethod
    def _asignar_diagnostico_sintetico():
        """
        Asigna diagnósticos sintéticos de manera balanceada.
        
        Returns:
            str: Categoría de diagnóstico
        """
        import random
        
        categorias = [
            "NO ENFERMO",
            "ENFERMEDAD LEVE",
            "ENFERMEDAD AGUDA",
            "ENFERMEDAD CRÓNICA"
        ]
        
        # Distribución más realista: menos enfermedades severas
        pesos = [0.4, 0.35, 0.15, 0.1]
        return random.choices(categorias, weights=pesos, k=1)[0]
    
    def limpiar_datos(self, datos):
        """
        Limpia los datos removiendo valores nulos y normalizando formatos.
        
        Args:
            datos (list): Lista de registros
            
        Returns:
            list: Datos limpios
        """
        datos_limpios = []
        
        for registro in datos:
            # Remover registros incompletos
            if all(k in registro for k in ["edad", "fiebre", "dolor"]):
                # Estandarizar tipos
                registro_limpio = {
                    "id_paciente": str(registro.get("id_paciente", "")),
                    "edad": int(registro["edad"]),
                    "fiebre": float(registro["fiebre"]),
                    "dolor": int(registro["dolor"]),
                    "diagnostico": str(registro.get("diagnostico", ""))
                }
                datos_limpios.append(registro_limpio)
        
        return datos_limpios
    
    def anonimizar_datos(self, datos):
        """
        Anonimiza los datos removiendo identificadores sensibles.
        
        Args:
            datos (list): Lista de registros
            
        Returns:
            list: Datos anonimizados
        """
        datos_anonimos = []
        
        for i, registro in enumerate(datos):
            registro_anonimo = {
                # Remover ID original y asignar uno genérico
                "registro_id": i,
                "edad": registro.get("edad"),
                "fiebre": registro.get("fiebre"),
                "dolor": registro.get("dolor"),
                "diagnostico": registro.get("diagnostico")
            }
            datos_anonimos.append(registro_anonimo)
        
        return datos_anonimos
    
    def obtener_datos_procesados(self, cantidad=1000):
        """
        Obtiene datos completamente procesados: cargados, limpios y anonimizados.
        
        Args:
            cantidad (int): Cantidad de registros a generar
            
        Returns:
            list: Datos listos para entrenamiento
        """
        # Cargar datos sintéticos
        datos = self.cargar_datos_sinteticos(cantidad)
        
        # Limpiar
        datos = self.limpiar_datos(datos)
        
        # Anonimizar
        datos = self.anonimizar_datos(datos)
        
        return datos
