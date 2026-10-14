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


