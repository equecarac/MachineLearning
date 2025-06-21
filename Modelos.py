import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#Paso 1: Datos desde Excel
ruta_archivo = "datos_bancarios.xlsx"
datos = pd.read_excel(ruta_archivo, sheet_name="Hoja1", engine='openpyxl')

#Paso 2: Variables
X = datos[["Sueldo (X)"]].values
y = datos["Préstamo Aprobado (y)"].values

#Paso 3: Crear y entrenar el modelo
modelo = LinearRegression()
modelo.fit(X, y)

#Paso 4: Predecir un nuevo valor
sueldo_nuevo = np.array([[5500]])
prestamo_predicho = modelo.predict(sueldo_nuevo)
print(f"Para un sueldo de ${sueldo_nuevo[0][0]}, el préstamo estimado es: ${prestamo_predicho[0]:.2f}")

#Paso 5: Calcular el error cuadrático (MSE)
predicciones = modelo.predict(X)
mse = mean_squared_error(y, predicciones)
print(f"Error Cuadrático Medio (MSE): {mse:.2f}")

#Paso 6: Graficar los resultados
plt.scatter(X, y, color='blue', label='Datos reales')
plt.plot(X, predicciones, color='red', label='Regresión lineal')
plt.xlabel('Sueldo Mensual ($)')
plt.ylabel('Préstamo Aprobado ($)')
plt.title('Predicción de Préstamos Bancarios (Regresión Lineal)')
plt.legend()
plt.grid(True)
plt.show()