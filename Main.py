import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ruta_archivo = "16BBF41_ALL_LATEST.csv"

# Se leen 80 filas
# sep=';' para indicar que el separador son ";" y no ","
df_raw = pd.read_csv(ruta_archivo, sep=';', nrows=80)

# Seleccionamos 5 columnas de la base de datos
# 1. Geográfica: GEO_NAME_SHORT
# 2. Cantidad de eventos/tasa: RATE_PER_100000_N
# 3. Clasificación: DIM_SEX
# 4 y 5. Complementarias: DIM_TIME y IND_ID
columnas_interes = [
    'GEO_NAME_SHORT', 
    'RATE_PER_100000_N', 
    'DIM_SEX', 
    'DIM_TIME', 
    'IND_ID'
]

#Conservamos unicamente las columnas que nos interesan del DataFrame original
df = df_raw[columnas_interes].copy()

#Transformamos los valores del CSV a un estandar que pueda reconocer pandas, y ponemos una salva contra posibles errores numericos en el CSV
df['TASA_SUICIDIOS'] = pd.to_numeric(
    df['RATE_PER_100000_N'].astype(str).str.replace(',', '.'), 
    errors='coerce'
)

#corregimos los valores transformados para que sean coherentes al estudio
df['TASA_SUICIDIOS'] = df['TASA_SUICIDIOS'].apply(
    lambda x: x / 1e9 if x > 100 else x
)
#Presentamos la información inicial antes de cualquier calculo
print("--- INFORMACIÓN GENERAL ---")
print(f"Filas cargadas: {len(df)}")
print(df[['GEO_NAME_SHORT', 'DIM_SEX', 'TASA_SUICIDIOS']])


