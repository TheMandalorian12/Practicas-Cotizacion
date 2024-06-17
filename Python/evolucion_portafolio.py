import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Definir los tickers de las acciones sin duplicados
tickers = [
    'GOLDD.BA', 'DISND.BA', 'MELI.BA', 'MELID.BA', 'MRVL.BA', 'BYMA.BA',
    'ARKKD.BA', 'ARKK.BA', 'VIST.BA', 'VISTD.BA', 'TGNO4.BA', 'GGAL.BA',
    'TXAR.BA', 'LOMA.BA', 'TRAN.BA', 'TGSU2.BA', 'PAMPD.BA', 'YPF',
    'YPFD.BA', 'BMA.BA', 'CRES.BA', 'CEPU.BA', 'COME.BA', 'MORI.BA',
    'PAMP.BA', 'AGRO.BA', 'IRSA.BA', 'AMZN.BA', 'BHIP.BA'
]

# Función para obtener los datos históricos de las acciones
def get_stock_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"No se pudo obtener datos para {ticker}: {e}")
        return None

# Definir fechas de inicio y fin (último año hasta hoy)
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

# Obtener los datos históricos para cada ticker
dfs = []
for ticker in tickers:
    df = get_stock_data(ticker, start_date, end_date)
    if df is not None and not df.empty:
        df['Symbol'] = ticker
        dfs.append(df)

# Verificar que haya al menos un DataFrame para continuar
if not dfs:
    print("No se obtuvieron datos para ningún ticker. Saliendo del programa.")
    exit()

# Concatenar todos los datos en un solo DataFrame
df_combined = pd.concat(dfs)

# Pivotar el DataFrame para tener una columna por cada ticker
df_pivot = df_combined.reset_index().pivot(index='Date', columns='Symbol', values='Adj Close')

# Calcular el precio actual para cada ticker
current_prices = df_pivot.iloc[-1]

# Dividir los tickers en tres grupos según el precio actual
tickers_mayor_3k = current_prices[current_prices > 3000].index.tolist()
tickers_entre_3k_1500 = current_prices[(current_prices >= 1500) & (current_prices <= 3000)].index.tolist()
tickers_menor_1500 = current_prices[current_prices < 1500].index.tolist()

# Filtrar el DataFrame pivoteado para cada grupo de tickers
df_pivot_mayor_3k = df_pivot[tickers_mayor_3k]
df_pivot_entre_3k_1500 = df_pivot[tickers_entre_3k_1500]
df_pivot_menor_1500 = df_pivot[tickers_menor_1500]

# Crear tres gráficos de la evolución de los precios de las acciones seleccionadas
plt.figure(figsize=(12, 10))

# Función para marcar el máximo valor en cada serie sin texto descriptivo
def annotate_max(df, ax):
    for column in df:
        max_value = df[column].max()
        max_date = df[column].idxmax()
        ax.annotate('', xy=(max_date, max_value), xytext=(max_date, max_value * 1.02),
                    arrowprops=dict(facecolor='black', arrowstyle='->'))

plt.subplot(3, 1, 1)
sns.lineplot(data=df_pivot_mayor_3k)
annotate_max(df_pivot_mayor_3k, plt.gca())
plt.title('Evolución de los precios de las acciones (Precio actual > 3000)')
plt.xlabel('Fecha')
plt.ylabel('Precio de cierre ajustado')
plt.legend(title='Symbol', loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)

plt.subplot(3, 1, 2)
sns.lineplot(data=df_pivot_entre_3k_1500)
annotate_max(df_pivot_entre_3k_1500, plt.gca())
plt.title('Evolución de los precios de las acciones (Precio actual entre 3000 y 1500)')
plt.xlabel('Fecha')
plt.ylabel('Precio de cierre ajustado')
plt.legend(title='Symbol', loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)

plt.subplot(3, 1, 3)
sns.lineplot(data=df_pivot_menor_1500)
annotate_max(df_pivot_menor_1500, plt.gca())
plt.title('Evolución de los precios de las acciones (Precio actual < 1500)')
plt.xlabel('Fecha')
plt.ylabel('Precio de cierre ajustado')
plt.legend(title='Symbol', loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)

plt.tight_layout()
plt.show()
