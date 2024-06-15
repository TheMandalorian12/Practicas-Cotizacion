import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ruta al archivo CSV exportado de Yahoo Finance
file_path = r'C:\Users\sosak\Lucas\portafolio.csv'  # Usando r'' para evitar problemas con los caracteres de escape

# Leer el archivo CSV
df = pd.read_csv(file_path)

# Mostrar las primeras filas del DataFrame para verificar que se haya leído correctamente
print(df.head())

# Convertir la columna de fecha a tipo datetime
df['Date'] = pd.to_datetime(df['Date'])

# Seleccionar las columnas necesarias
df = df[['Date', 'Symbol', 'Current Price']]

# Pivotar el DataFrame para tener una columna por cada ticker
df_pivot = df.pivot(index='Date', columns='Symbol', values='Current Price')

# Crear un gráfico de la evolución de los precios
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_pivot)
plt.title('Evolución de los precios de las acciones')
plt.xlabel('Fecha')
plt.ylabel('Precio de cierre')
plt.legend(title='Symbol')
plt.grid(True)
plt.show()
