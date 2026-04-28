import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Validador de calidad de datos", layout="wide")

st.title("Sistema de validación de calidad de datos")

uploaded_file = st.file_uploader(" Seleccione un archivo csv", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("Vista previa de los datos")
        st.dataframe(df.head(), use_container_width=True)

        if st.button("Iniciar Validación de Calidad"):
            errors = []
            
            expected_columns = ['fecha', 'producto', 'cantidad', 'precio'] # Verificación de columnas
            missing_cols = [col for col in expected_columns if col not in df.columns]
            
            if missing_cols:
                errors.append(f"Estructura incorrecta: Faltan las columnas {missing_cols}")

            if not missing_cols:
                
                if df.isnull().values.any(): # Valores nulos
                    num_nulos = df.isnull().sum().sum()
                    errors.append(f"Se encontraron {num_nulos} valores vacíos en el archivo.")

                if (df['cantidad'] <= 0).any():
                    errors.append("Existen registros con cantidades menores o iguales a cero.")

                if (df['precio'] < 0).any(): 
                    errors.append("Se detectaron precios negativos en la columna 'precio'.")

            if not errors:
                st.success("Validación Exitosa. Todos los datos cumplen con los estándares establecidos.")
                
                st.divider()
                if st.button("Cargar a Base de Datos"):
                    st.info("Conectando con el servidor de almacenamiento... (En desarrollo)")
            else:
                st.error("Se encontraron problemas de calidad:**")
                for error in errors:
                    st.warning(f"• {error}")

    except Exception as e:
        st.error("Error Crítico: No se pudo procesar el archivo. Asegúrese de que el CSV no esté dañado y tenga un formato estándar.")
        
        print(f"Log interno: {e}")

else:
    st.info("Por favor, cargue un archivo csv para comenzar el análisis.")