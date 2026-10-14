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
print("--INFORMACIÓN GENERAL--")
print(f"Filas cargadas: {len(df)}")
print(df[['GEO_NAME_SHORT', 'DIM_SEX', 'TASA_SUICIDIOS']].round(4))


# Estadísticas generales (Promedio y desviación estandar generales)
promedio_tasa = df['TASA_SUICIDIOS'].mean()
desviacion_tasa = df['TASA_SUICIDIOS'].std()

print("\n--ESTADÍSTICAS BÁSICAS--")
print(f"Promedio de la tasa: {promedio_tasa:.2f}") # ":" para separar la variable de modificaciones en su formato, ".2" para indicar cuantos decimales se usaran, "f" para indicar float como tipo de dato
print(f"Desviación estándar: {desviacion_tasa:.2f}")

# Exportación a Excel
df.to_excel("tasas_suicidio_procesadas.xlsx", index=False)
print("\nArchivo 'tasas_suicidio_procesadas.xlsx' generado correctamente.")

#Aplicación de filtros.

# Filtro 1: Casos con tasa superior al promedio
df_superior_promedio = df[df['TASA_SUICIDIOS'] > promedio_tasa]

# Filtro 2: Registros del año 2000 en adelante
df_año_filtrado = df[df['DIM_TIME'] >= 2000]

# Filtro 3: Hombres con tasa superior al promedio
df_hombres_alta_tasa = df[(df['DIM_SEX'] == 'MALE') & (df['TASA_SUICIDIOS'] > promedio_tasa)]

print("\n--RESULTADOS DE FILTRADO--")
print(f"Casos superiores al promedio: {len(df_superior_promedio)}")
print(f"Casos en año >= 2000: {len(df_año_filtrado)}")
print(f"Hombres con tasa superior al promedio: {len(df_hombres_alta_tasa)}")


#Generación de graficos

# Gráfico 1: Histograma
plt.figure(figsize=(8, 5))
plt.hist(df['TASA_SUICIDIOS'].dropna(), bins=10, color='skyblue', edgecolor='black')
plt.axvline(promedio_tasa, color='red', linestyle='dashed', linewidth=1.5, label=f'Promedio ({promedio_tasa:.2f})')
plt.title("Distribución de la Tasa de Suicidios por 100,000 Habitantes")
plt.xlabel("Tasa (por 100,000 hab.)")
plt.ylabel("Frecuencia")
plt.legend()
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()

#Gráfico 2: Barras por país
df_total = df[df['DIM_SEX'] == 'TOTAL']
plt.figure(figsize=(12, 6))
plt.bar(df_total['GEO_NAME_SHORT'], df_total['TASA_SUICIDIOS'], color='royalblue', edgecolor='black')
plt.title("Tasa Total de Suicidios por País")
plt.xlabel("País")
plt.ylabel("Tasa Total (por 100,000 hab.)")
plt.xticks(rotation=75, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Gráfico 3: Barras por Género
df_generos = df[df['DIM_SEX'].isin(['FEMALE', 'MALE'])]
promedio_generos = df_generos.groupby('DIM_SEX')['TASA_SUICIDIOS'].mean().reset_index()

etiquetas = ['Mujeres', 'Hombres']
alturas = promedio_generos['TASA_SUICIDIOS']
plt.figure(figsize=(6, 5))
colores = ['red', 'blue'] 
barras = plt.bar(etiquetas, alturas, color=colores, edgecolor='black', width=0.5)
plt.title("Tasa Promedio de Suicidios: Hombres vs Mujeres")
plt.xlabel("Género")
plt.ylabel("Tasa Promedio (por 100,000 hab.)")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Gráfico 4: Dispersión
