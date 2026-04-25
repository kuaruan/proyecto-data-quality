import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Validador de Datos", layout="wide")

st.title("Sistema de Validación de Datos")
st.markdown("""
Cargue su archivo de datos en formato csv para verificar las reglas de calidad 
antes de ser procesado.
""")

uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv") # componente para subir datos

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) # Lectura archivo
    
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    if st.button("Validar Calidad de Datos"): # Botón inicio validación
        errors = []
                
        expected_columns = ['fecha', 'producto', 'cantidad', 'precio'] # Comprobación de existencia
        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            errors.append(f"Faltan columnas: {missing_cols}")

        if df.isnull().values.any(): # Existencia de valores null
            errors.append("El archivo contiene valores vacíos (nulos).")

        if 'cantidad' in df.columns and (df['cantidad'] <= 0).any(): # Validar cantidades 
            errors.append("Hay registros con cantidad menor o igual a cero.")

        if 'precio' in df.columns and (df['precio'] < 0).any(): # Precio positivo
            errors.append("Hay precios negativos.")

        if not errors: 
            st.success("Los datos cumplen con todos los estándares de calidad.")
            
            if st.button("Cargar a la Base de Datos"): # Enviar a supabase para la carga
                st.info("Conectando con Supabase... (Próximo paso)")
        else:
            st.error("Se encontraron los siguientes problemas:")
            for error in errors:
                st.write(error)