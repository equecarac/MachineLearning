import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# PAso 1: Leer datos desde Excel
ruta_archivo = "datos_bancarios.xlsx"
datos = pd.read_excel(ruta_archivo, sheet_name="Hoja4", engine='openpyxl')

# Paso 2: Preprocesamiento
le = LabelEncoder()
datos['Historial'] = le.fit_transform(datos['Historial'])  # <= Bueno = 0, Malo = 1. Regular = 2
datos['Riesgo'] = le.fit_transform(datos['Riesgo'])

# Definimos variables
X = datos[['Ingresos', 'Deuda', 'Score', 'Historial']]
y = datos['Riesgo']

# Paso 4: Dividr
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Pago 5: Crear y entrenar
modelo_rf = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
modelo_rf.fit(X_train, y_train)

# Paso 6: Evaluarlo
y_pred = modelo_rf.predict(X_test)
precision = accuracy_score(y_test, y_pred)
reporte = classification_report(y_test, y_pred, target_names=['Bajo', 'Alto', 'Medio'])

print(f"Precisión del modelo: {precision * 100:.2f}%")
print("\nReporte de Clasificación:")
print(reporte)

# Paso 7: Visualizar un árbol del bosque
plt.figure(figsize=(12, 8))
plot_tree(modelo_rf.estimators_[0], feature_names=X.columns, class_names=['Bajo', 'Alto', 'Medio'], filled=True)
plt.title("Árbol Individual del Random Forest")
plt.show()

# 8. Predecir un nuevo cliente
nuevo_cliente = pd.DataFrame({
    'Ingresos': [4000],
    'Deuda': [3500],
    'Score': [650],
    'Historial': ['Malo']  # Debe ser el valor codificado (Malo=1)
})
nuevo_cliente['Historial'] = le.transform(nuevo_cliente['Historial'])
prediccion = modelo_rf.predict(nuevo_cliente)
print(f"\nPredicción de Riesgo: {le.inverse_transform(prediccion)[0]}")