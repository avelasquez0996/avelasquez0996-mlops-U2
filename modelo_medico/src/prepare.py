import pandas as pd
import yaml
from src.preprocessor import Preprocessor

def main():
    # Load params
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    max_samples = params['raw']['max_samples']
    
    # Load raw data
    df = pd.read_csv('data/raw.csv')
    
    if max_samples and max_samples < len(df):
        df = df.sample(n=max_samples, random_state=42).reset_index(drop=True)
    
    # Add registro_id
    df['registro_id'] = range(len(df))
    
    # Normalize using Preprocessor logic
    # edad: 0-150
    df['edad_norm'] = (df['edad'] - 0) / 150.0
    # fiebre: 35-45
    df['fiebre_norm'] = (df['fiebre'] - 35) / 10.0
    # dolor: 0-10
    df['dolor_norm'] = df['dolor'] / 10.0
    
    # Select columns
    df_processed = df[['registro_id', 'edad_norm', 'fiebre_norm', 'dolor_norm', 'diagnostico']]
    
    # Save
    df_processed.to_parquet('data/processed.parquet', index=False)
    print(f"Processed data saved: {len(df_processed)} rows")

if __name__ == "__main__":
    main()