# Librerias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Datos
df = pd.read_csv(r"D:\101010 Revisiones\Sprint-7-Proyecto\clean_vehicles_df.csv")
df["type"] = df["type"].astype(str)

## creacion de la aplicacion
# Titulo
st.header('Análisis de Anuncios de Venta de Vehículos', divider = "blue")
st.write("Bienvenido al panel de análisis exploratorio de datos (EDA) para el conjunto de datos de vehículos.")

# Boton Descargar
st.download_button(
    label = "Descargar Stock de Vehículos", 
    data = df.to_csv(index=False), 
    file_name = "vehicles_tock.csv"
)

st.divider()


# --- Visor de datos con casilla de verificación ---
if st.checkbox('Mostrar dataframe con fabricantes con menos de 1000 anuncios'):
    st.write('Mostrando los fabricantes con menos de 1000 anuncios:')
    # Contar la frecuencia de cada modelo
    model_counts = df['manufacturer'].value_counts()
    # Filtrar los modelos con menos de 1000 anuncios
    manufacturers_less_than_1000 = model_counts[model_counts < 1000].index
    # Crear un nuevo DataFrame con solo esos fabricantes
    filtered_df = df[df['manufacturer'].isin(manufacturers_less_than_1000)]
    st.dataframe(filtered_df)

st.divider()

# --- Visor de datos por fabricante y modelo ---
if st.checkbox('Mostrar dataframe por fabricante y modelo'):
    st.write('Mostrando el dataframe por fabricante y modelo:')
    # Seleccionador de fabricante
    opciones = list(df["manufacturer"].unique())
    opcion = st.selectbox(
        label = "Seleccione un fabricante:",
        options = opciones
    )
    # Filtrar el DataFrame por el fabricante seleccionado
    filtered_df = df[df['manufacturer'] == opcion]
    st.dataframe(filtered_df)                                                   

# --- Grafica de distribucion de vehiculos por fabricante ---
st.header('Vehiculos por Fabricante', divider= "orange")
st.write("Comparación de vehiculos por Fabricante.")

if st.checkbox('Mostrar Distribución de Vehículos por Fabricante'):
    manufacturer_dist = px.histogram(df, x = 'manufacturer', color = "type")
    st.plotly_chart(manufacturer_dist, use_container_width=True)
    # sleccionador de fabricante para ver la media del precio
    opcion_0 = st.selectbox(
        label = "Seleccione el fabricante para ver la media del precio:",
        options = df["manufacturer"].unique()
    )
    # Calcular medias agrupadas por fabricante
    medias_por_fabricante = df.groupby('manufacturer')['price'].mean()
    man_media = medias_por_fabricante.loc[opcion_0]
    st.metric(label=f"Media de {opcion_0}, (precios en dolares)", value=f"{round(man_media, 2)}")

st.divider()


# --- Hisograma de Condicion vs Año del Vehiculo ---
st.header('Histograma de Condición vs Año del Vehículo', divider= "red")
st.write("Comparación de la condición del vehículo por año.")

if st.checkbox('Mostrar Histograma de Condición por Año del Vehículo'):
    condition_hist = px.histogram(df, x = 'model_year', color = "condition", title="Distribución de Condición por Año del Vehículo") 
    st.plotly_chart(condition_hist, use_container_width=True)

st.divider()


# --- Comparación de la Distribución de Vehículos por Fabricante ---
st.header('Distribución de precios por Fabricante', divider= "green")
st.write("Comparación de distribución de precios por Fabricante.")

# Seleccionador de Fabricante 1
opciones_1 = list(df["manufacturer"].unique())
opciones_2 = list(df["manufacturer"].unique())

filtro_1 = st.selectbox(
    label = "Seleccione el primer fabricante:",
    options = opciones_1
)

# Seleccionador de Fabricante 2
filtro_2 = st.selectbox(
    label = "Seleccione el segundo fabricante:",
    options = opciones_2
)

manufacturer_comp = px.histogram(df[df['manufacturer'].isin([filtro_1, filtro_2])], 
    x = 'manufacturer', 
    y = 'price', 
    color = "manufacturer", 
    title = f"Distribución de precios: {filtro_1} vs {filtro_2}",
)
st.plotly_chart(manufacturer_comp, use_container_width=True)

#Mostrar el total de unidades y la media de precios
col_filtro_1, col_filtro_2 = st.columns(2)

with col_filtro_1:
    total_filtro_1 = df[df['manufacturer'] == filtro_1].shape[0]
    media_filtro_1 = df[df['manufacturer'] == filtro_1]['price'].mean()
    st.metric(label=f"Total de vehículos {filtro_1}", value=f"{total_filtro_1}")
    st.metric(label=f"Media de {filtro_1} (precios en dolares)", value=f"{round(media_filtro_1, 2)}")
with col_filtro_2:
    total_filtro_2 = df[df['manufacturer'] == filtro_2].shape[0]
    media_filtro_2 = df[df['manufacturer'] == filtro_2]['price'].mean()
    st.metric(label=f"Total de vehículos {filtro_2}", value=f"{total_filtro_2}")
    st.metric(label=f"Media de {filtro_2} (precios en dolares)", value=f"{round(media_filtro_2, 2)}")

st.divider()


# --- Relación Precio vs Millas Recorridads y Gráfica de Dispersión ---
st.header('Relación Precio vs Millas Recorridas', divider= "violet")
st.write("Análisis de la relación entre el precio y las millas recorridas de los vehículos.")

# Seleccionador de Fabricante
opciones_3 = list(df["manufacturer"].unique())
filtro_3 = st.selectbox(
    label = "Seleccione el fabricante para analizar Precio vs Millas Recorridas:",
    options = opciones_3
)
disp_plot = px.scatter(df[df['manufacturer'].isin([filtro_3])], 
    x = 'odometer',
    y = 'price', 
    title=f"Dispersión Precio vs Millas Recorridas: {filtro_3}"
)
st.plotly_chart(disp_plot, use_container_width=True)

corr_price_miles = df[df['manufacturer'] == filtro_3][['price', 'odometer']].corr().iloc[0, 1]
st.metric(label="Correlación entre Precio y Millas Recorridas", value=f"{round(corr_price_miles, 2)}")

st.divider()


# --- Otros Análisis ---
st.header('Otros Análisis', divider= "rainbow")
st.write("Realiza un análisis exploratorio de datos seleccionando dos variables.")
# Seleccionador de variables
opciones = list(df.columns)[0:14]

v = st.multiselect(
    label = "Seleccione máximo 2 variables:",
    options = opciones,
    max_selections = 2
)

# Boton de ejecutar
analisis_b = st.button(
    label = "Analizar"
)

st.divider()

# Analisis
if analisis_b:
    try:

        col1, col2 = st.columns(2)
        
        # Histograma de variable 1
        with col1:
    
            hist_plot01 = px.histogram(df, x = v[0], title = f"Distribución {v[0]}", color = "condition")
            st.plotly_chart(hist_plot01, use_container_width=True)

            c1, c2, c3 = st.columns(3)

            with c1: 
                prom1 = np.mean(df[v[0]])
                st.metric(
                    label = "Media",
                    value = "{}".format(round(prom1,1))
                )
            with c2:
                med1 = np.median(df[v[0]])
                st.metric(
                    label = "Mediana",
                    value = "{}".format(round(med1,1))
                )
            with c3:
                desv1 = np.std(df[v[0]])
                st.metric(
                    label = "Desviación",
                    value = "{}".format(round(desv1,1))
                )


# Histograma de variable 2
        with col2:
            
            hist_plot02 = px.histogram(df, x = v[1], title = f"Distribución {v[1]}", color = "condition")
            st.plotly_chart(hist_plot02, use_container_width=True)

            c4, c5, c6 = st.columns(3)

            with c4: 
                prom2 = np.mean(df[v[1]])
                st.metric(
                    label = "Media",
                    value = "{}".format(round(prom2,1))
                )
            with c5:
                med2 = np.median(df[v[1]])
                st.metric(
                    label = "Mediana",
                    value = "{}".format(round(med2,1))
                )
            with c6:
                desv2 = np.std(df[v[1]])
                st.metric(
                    label = "Desviación",
                    value = "{}".format(round(desv2,1))
                )
            
        #Grafica de dispersion
        disp_plot = px.scatter(df, x = v[0], y = v[1], color = "condition", title = f"Dispersión {v[1]} vs. {v[0]}")
        st.plotly_chart(disp_plot, use_container_width=True)

        correl = np.corrcoef(df[v[0]],df[v[1]])
        st.metric(
            label = "Correlación de Pearson",
            value = "{}%".format(round(correl[0,1]*100,1))
        )

    except:
        
        st.write("Faltan variables por seleccionar")
