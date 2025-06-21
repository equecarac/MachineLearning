import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

# 1. Leer datos desde Excel
ruta_archivo = "datos_bancarios.xlsx"
datos = pd.read_excel(ruta_archivo, sheet_name="Hoja3", engine='openpyxl')

# 2. Praparar las variables
X = datos[["Sueldo", "Score Crediticio", "Deudas"]]
y = datos["Aprueba Préstamo"]

# 3. Dividir
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. Crear y entrenar el modelo
modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo.fit(X_train, y_train)

# 5. Predececir y evaluar
y_pred = modelo.predict(X_test)
precision = accuracy_score(y_test, y_pred)
matriz_confusion = confusion_matrix(y_test, y_pred)

print(f"Precisión del modelo: {precision * 100:.2f}%")
print("Matriz de Confusión:")
print(matriz_confusion)

# 6. Visualizar el árbol
plt.figure(figsize=(12, 8))
plot_tree(modelo,
          feature_names=X.columns,
          class_names=modelo.classes_,
          filled=True,
          rounded=True)
plt.title("Árbol de Decisión - Clasificación de Préstamos Bancarios")
plt.show()

nuevo_cliente = pd.DataFrame({
    "Sueldo": [4000],
    "Score Crediticio": [650],
    "Deudas": [3500]
})
prediccion = modelo.predict(nuevo_cliente)
print(f"\nPredicción para nuevo cliente: {prediccion[0]}")