import yfinance as yf
import tkinter as tk
from tkinter import ttk
import pandas as pd

def actualizar_cotizaciones():
    acciones = [
        'AGRO.BA', 'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 
        'COME.BA', 'CRES.BA', 'CVH.BA', 'EDN.BA', 'GGAL.BA', 'HARG.BA', 
        'MIRG.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGSU2.BA', 'TRAN.BA', 
        'TXAR.BA', 'VALO.BA', 'YPFD.BA', 'IRSA.BA', 'AUSO.BA', 'BHIP.BA',
        'TGNO4.BA', 'LOMA.BA'
    ]  # Lista de símbolos de acciones argentinas
    
    datos = {}
    
    for accion in acciones:
        ticker = yf.Ticker(accion)
        historial = ticker.history(period='1d')
        if not historial.empty:
            datos[accion] = historial['Close'].iloc[-1]
        else:
            datos[accion] = 'N/D'  # No disponible
    
        for accion, precio in datos.items():
         if precio != 'N/D':
            precio = f"${precio:.2f}"  # Agregar signo de pesos
        treeview.item(accion, values=(accion, precio))
    
    root.after(60000, actualizar_cotizaciones)  # Actualizar cada 60 segundos

root = tk.Tk()
root.title("Cotizaciones en Tiempo Real")

treeview = ttk.Treeview(root)
treeview['columns'] = ('Accion', 'Precio')
treeview.column('#0', width=0, stretch=tk.NO)
treeview.column('Accion', anchor=tk.W, width=120)
treeview.column('Precio', anchor=tk.W, width=120)

treeview.heading('#0', text='', anchor=tk.W)
treeview.heading('Accion', text='Acción', anchor=tk.W)
treeview.heading('Precio', text='Precio', anchor=tk.W)

acciones = [
    'AGRO.BA', 'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 
    'COME.BA', 'CRES.BA', 'CVH.BA', 'EDN.BA', 'GGAL.BA', 'HARG.BA', 
    'MIRG.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGSU2.BA', 'TRAN.BA', 
    'TXAR.BA', 'VALO.BA', 'YPFD.BA', 'IRSA.BA', 'AUSO.BA', 'BHIP.BA',
    'TGNO4.BA', 'LOMA.BA'
]  # Lista de símbolos de acciones argentinas

for accion in acciones:
    treeview.insert(parent='', index='end', iid=accion, text='', values=(accion, ''))

treeview.pack(pady=20)

# Llamar a la función de actualización por primera vez
actualizar_cotizaciones()

root.mainloop()
