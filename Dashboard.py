# Dashboard 1
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Bancario",
    page_icon="🏦",
    layout="wide"
)

# Título del dashboard
st.title("📊 Dashboard Bancario Interactivo")
st.markdown("""
**Panel** de un dashboard para análisis de productos bancarios:
- Streamlit para la interfaz
- Plotly y Altair para gráficos interactivos
""")


# Datos de ejemplo (simulando datos bancarios)
@st.cache_data
def cargar_datos():
    fecha_actual = datetime.now().date()
    datos = pd.DataFrame({
        'Producto': ['Hipotecario', 'Consumo', 'Tarjeta Crédito', 'Ahorros', 'Inversiones'],
        'Clientes': [1500, 8500, 12000, 25000, 3000],
        'Saldo_Total': [450000000, 125000000, 85000000, 320000000, 280000000],
        'Tasa_Interes': [7.5, 15.2, 18.0, 2.3, 5.8],
        'Mora': [4.2, 8.7, 12.5, 0.5, 1.2],  # Porcentaje
        'Fecha_Actualizacion': [fecha_actual] * 5
    })
    return datos


df = cargar_datos()

# Sidebar con filtros
st.sidebar.header("Filtros")
productos_seleccionados = st.sidebar.multiselect(
    "Seleccione productos:",
    options=df['Producto'].unique(),
    default=df['Producto'].unique()
)

# Filtrar datos según selección
df_filtrado = df[df['Producto'].isin(productos_seleccionados)]

# Métricas clave
st.subheader("Métricas Clave")
col1, col2, col3 = st.columns(3)
col1.metric("Total Productos", len(df_filtrado))
col2.metric("Clientes Totales", f"{df_filtrado['Clientes'].sum():,}")
col3.metric("Saldo Total", f"${df_filtrado['Saldo_Total'].sum() / 1e6:,.1f} M")

# Pestañas para diferentes visualizaciones
tab1, tab2, tab3 = st.tabs(["Gráficos Plotly", "Gráficos Altair", "Datos"])

with tab1:
    st.header("Visualizaciones con Plotly")
    colores = ['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728', '#9467bd']
    # Gráfico de barras interactivo
    fig1 = px.bar(
        df_filtrado,
        x='Producto',
        y='Saldo_Total',
        color='Producto',
        title='Saldo Total por Producto',
        labels={'Saldo_Total': 'Saldo Total (USD)'},
        hover_data=['Tasa_Interes', 'Mora'],
        color_discrete_sequence=colores,
        text='Saldo_Total'
    )

    #etiquetas

    fig1.update_traces(
        texttemplate='%{text:$,.0f}',
        textposition='outside'
    )


    fig1.add_scatter(
        x=df_filtrado['Producto'],
        y=df_filtrado['Saldo_Total'],
        mode='lines+markers',
        line=dict(color='gray',width=2 , dash='dot'),
        marker=dict(color='black',size=10),
        name='Tendencia'
    )
    st.plotly_chart(fig1, use_container_width=True)



    # Gráfico de dispersión
    fig2 = px.scatter(
        df_filtrado,
        x='Tasa_Interes',
        y='Mora',
        size='Clientes',
        color='Producto',
        title='Relación entre Tasa de Interés y Mora',
        labels={'Tasa_Interes': 'Tasa de Interés (%)', 'Mora': 'Mora (%)'}
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("Visualizaciones con Altair")

    # Gráfico de barras
    chart1 = alt.Chart(df_filtrado).mark_bar().encode(
        x='Producto:N',
        y='Saldo_Total:Q',
        color='Producto:N',
        tooltip=['Producto', 'Saldo_Total', 'Tasa_Interes']
    ).properties(
        title='Saldo por Producto (Altair)',
        width=600,
        height=400
    )
    st.altair_chart(chart1, use_container_width=True)

    # Gráfico de burbujas
    chart2 = alt.Chart(df_filtrado).mark_circle(size=100).encode(
        x='Tasa_Interes:Q',
        y='Mora:Q',
        size='Clientes:Q',
        color='Producto:N',
        tooltip=['Producto', 'Clientes', 'Tasa_Interes', 'Mora']
    ).properties(
        title='Relación Tasa de Interés vs Mora',
        width=600,
        height=400
    )
    st.altair_chart(chart2, use_container_width=True)

with tab3:
    st.header("Datos Detallados")

    # Mostrar dataframe con formato
    st.dataframe(
        df_filtrado.style.format({
            'Saldo_Total': '${:,.0f}',
            'Tasa_Interes': '{:.1f}%',
            'Mora': '{:.1f}%'
        }),
        column_config={
            "Fecha_Actualizacion": st.column_config.DateColumn(
                "Última Actualización",
                format="DD/MM/YYYY"
            )
        }
    )

    # Opción para descargar datos
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar datos como CSV",
        data=csv,
        file_name='datos_bancarios.csv',
        mime='text/csv'
    )

# Notas finales
st.markdown("---")
st.caption("Dashboard creado con Streamlit")