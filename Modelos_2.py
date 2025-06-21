import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

#Paso 1: Datos desde Excel
ruta_archivo = "datos_bancarios.xlsx"
datos = pd.read_excel(ruta_archivo, sheet_name="Hoja2", engine='openpyxl')

# Paso 1: variables
X = datos[["Sueldo (X1)", "Score Crediticio (X2)"]].values
y = datos["Incumplió (y)"].values

# Paso 2: dividir datos de entrenamiento y prueba (70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Paso 3: Predecir un nuevo valor
modelo = LogisticRegression()
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

precision = accuracy_score(y_test, y_pred)
matriz_confusion = confusion_matrix(y_test, y_pred)

print(f"Precisión del modelo: {precision * 100:.2f}%")
print("Matriz de confusión:")
print(matriz_confusion)

# Paso 4: Predecir
nuevo_cliente = np.array([[2500, 550]])
prediccion = modelo.predict(nuevo_cliente)
print(f"\nPredicción para nuevo cliente (1=Incumplió, 0=Pagó): {prediccion[0]}")

# Paso 5: Para el taxi
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', alpha=0.7)
plt.xlabel('Sueldo ($)')
plt.ylabel('Score Crediticio')
plt.title('Clasificación de Préstamos (Regresión Logística)')
plt.colorbar(label='Incumplió (1) / Pagó (0)')
plt.grid(True)
plt.show()