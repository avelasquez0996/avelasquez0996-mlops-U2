"""
Script para generar datos médicos sintéticos crudos para versionado con DVC.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import DataLoader
import csv

def generar_datos_crudo(output_path='data/raw.csv', num_samples=1000):
    """
    Genera datos sintéticos y los guarda como CSV.
    """
    loader = DataLoader()
    data = loader.cargar_datos_sinteticos(num_samples)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    print(f"Generados {len(data)} filas en {output_path}")

if __name__ == "__main__":
    generar_datos_crudo()