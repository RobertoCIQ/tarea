import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("📈 Dashboard de Precios de Automóviles")

# --- 1. Carga y preprocesamiento de datos ---
# Cargamos el dataset original
df = pd.read_csv("car_price_prediction.csv")

# Limpieza de columnas específica
df["Engine volume"] = df["Engine volume"].astype(str).str.extract('(\\d+\\.?\\d*)', expand=False)
df["Engine volume"] = pd.to_numeric(df["Engine volume"], errors='coerce')

df["Doors"] = df["Doors"].astype(str).str.extract('(\\d+\\.?\\d*)', expand=False)
df["Doors"] = pd.to_numeric(df["Doors"], errors='coerce')

df["Mileage"] = df["Mileage"].astype(str).str.extract('(\\d+\\.?\\d*)', expand=False)
df["Mileage"] = pd.to_numeric(df["Mileage"], errors='coerce')

# Limpiar columna Levy: reemplazar '-' con 0 y convertir a entero
df['Levy'] = df['Levy'].replace('-', 0).astype(int)

# Eliminar outliers principales (como se hizo en el notebook)
max_price_index = df['Price'].idxmax()
df = df.drop(max_price_index).reset_index(drop=True)

# El outlier de Engine volume fue un valor maximo que probablemente era un error.
# Para el dashboard, simplemente nos aseguraremos de que no haya nulos y los trataremos si fuera necesario.
# En este caso, ya están tratados por pd.to_numeric(errors='coerce')

# Eliminación de outliers de 'Price' usando 3 desviaciones estándar (como se hizo en el notebook)
mean_price = df['Price'].mean()
std_price = df['Price'].std()
upper_bound = mean_price + (3 * std_price)
df = df[df['Price'] < upper_bound]

# --- 2. KPIs ---
col1, col2, col3 = st.columns(3)
col1.metric("Total de Vehículos", f"{df.shape[0]:,}")
col2.metric("Precio Promedio", f"${df['Price'].mean():,.0f}")
col3.metric("Fabricantes Únicos", f"{df['Manufacturer'].nunique()}")

# --- 3. Gráficas ---
# Gráfica de distribución de precios
fig_price_dist = px.histogram(df, x="Price", nbins=50, title="Distribución de Precios de Vehículos")
st.plotly_chart(fig_price_dist)

# Gráfica de precio promedio por categoría
avg_price_by_category = df.groupby('Category')['Price'].mean().reset_index()
fig_avg_price_category = px.bar(
    avg_price_by_category,
    x="Category",
    y="Price",
    title="Precio Promedio por Categoría",
    labels={"Price": "Precio Promedio", "Category": "Categoría"},
    template="plotly_white"
)
st.plotly_chart(fig_avg_price_category)

# Gráfica de precio promedio por fabricante (top 10)
avg_price_by_manufacturer = df.groupby('Manufacturer')['Price'].mean().sort_values(ascending=False).head(10).reset_index()
fig_avg_price_manufacturer = px.bar(
    avg_price_by_manufacturer,
    x="Manufacturer",
    y="Price",
    title="Top 10 Fabricantes por Precio Promedio",
    labels={"Price": "Precio Promedio", "Manufacturer": "Fabricante"},
    template="plotly_white"
)
st.plotly_chart(fig_avg_price_manufacturer)
