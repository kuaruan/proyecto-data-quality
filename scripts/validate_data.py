import pandas as pd
import sys
import os

def validate_csv(file_path):
    if not os.path.exists(file_path): # El archivo existe? 
        print(f"Error: El archivo {file_path} no existe.")
        sys.exit(1)

    print(f"--- Iniciando validación de archivo: {file_path} ---")
    df = pd.read_csv(file_path)

    expected_columns = ['fecha', 'producto', 'cantidad', 'precio'] # Las columnas existen? 
    if not all(col in df.columns for col in expected_columns):
        print(f"Columnas faltantes. Se esperaba: {expected_columns}")
        sys.exit(1)

    if df.isnull().values.any(): # Existen nulos? 
        print("Se encontraron valores nulos en el CSV.")
        print(df.isnull().sum()) # Cantidad de nulos por columna
        sys.exit(1)

    if (df['cantidad'] <= 0).any(): # Registros mayores a cero? 
        print("Hay registros con cantidad menor o igual a cero.")
        sys.exit(1)

    if (df['precio'] < 0).any(): # Valores de precios positivos
        print("Hay precios negativos en la columna de precio.")
        sys.exit(1)

    print("Todos los checks han sido validados. El archivo está apto para el uso")

if __name__ == "__main__":
    validate_csv('data/ventas.csv') # Archivo a validar