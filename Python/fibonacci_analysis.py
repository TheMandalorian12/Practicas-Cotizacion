import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime, timedelta

# Obtener la fecha actual
current_date = datetime.now()

# Calcular la fecha hace 6 meses
start_date = current_date - timedelta(days=6*30)  # Asumiendo que un mes tiene 30 días

# Convertir las fechas a strings con el formato necesario para la consulta
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = current_date.strftime('%Y-%m-%d')

# Obtener datos históricos de precios de cierre para $BHIP.BA desde Yahoo Finance
data = yf.download('BHIP.BA', start=start_date_str, end=end_date_str)

# Calcular los niveles de retroceso de Fibonacci
high = data['High'].max()
low = data['Low'].min()
diff = high - low

# Niveles de retroceso de Fibonacci
levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]

fib_levels = []
for level in levels:
    fib_levels.append(low + level * diff)

# Graficar los datos de precios con los niveles de retroceso de Fibonacci
mpf.plot(data, type='candle', style='charles', title='$BHIP.BA Fibonacci Retracement',
         ylabel='Precio', ylabel_lower='Volumen', volume=True,
         hlines=dict(hlines=fib_levels, colors='r', linestyle='--'))

plt.show()


