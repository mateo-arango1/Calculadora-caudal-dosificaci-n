import streamlit as st
import numpy as np

# --- Configuración de la Interfaz ---
st.set_page_config(
    page_title="Calculadora de Dosificación y Jar Test",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('🧪 Calculadora de Dosificación y Test de jarras')
st.markdown("---")

# --- Selector de Modo ---
modo = st.radio(
    "Seleccione el modo de cálculo:",
    ('Calcular Caudal de Dosificación (mL/min)', 'Calcular Dosis Actual (ppm)', 'Dosificación en Jarras (mL de producto)'),
    horizontal=False # Lo ponemos en vertical para que se vea mejor el tercer botón
)

st.markdown("---")

# Parámetros fijos
FACTOR_AJUSTE = 0.7
densidad = 1.0 # g/mL (Asumida)


# =====================================================================
## 🚀 MODO 1: CALCULAR CAUDAL DE DOSIFICACIÓN (mL/min)
# =====================================================================
if modo == 'Calcular Caudal de Dosificación (mL/min)':
    
    st.header('1. Caudal de Dosificación (mL/min)')

    # --- Solicitud de Datos (Widgets) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos de Caudal (m³/h)")
        # Valores de entrada sin decimales, como lo ajustaste
        Qe = st.number_input('Caudal de Entrada (Qe):', min_value=0, value=50, help="Caudal de agua fresca que entra a la planta.")
        Qr = st.number_input('Caudal de Recirculación (Qr):', min_value=0, value=60, help="Caudal de agua recirculada.")
        
        Q = Qe + Qr
        st.info(f"Caudal Total (Qe + Qr): **{Q:.2f} m³/h**")

    with col2:
        st.subheader("Datos de Dosificación")
        D = st.number_input('Dosis Requerida (ppm):', min_value=0, value=2, help="Cantidad de químico activo que se necesita por litro.")
        S = st.number_input('Concentración Producto (%):', min_value=0, max_value=100, value=40, help="Porcentaje de ingrediente activo en el producto químico.")
        
    st.write('---')

    if st.button('Calcular Caudal (mL/min)', type="primary"):
        if Q > 0 and D > 0 and S > 0:
            
            # 1. Masa activa requerida (g/h)
            masa_activa_g_h = Q * FACTOR_AJUSTE * D 

            # 2. Activo disponible por litro del producto (g/L)
            activo_por_litro = densidad * 1000 * (S / 100)

            if activo_por_litro == 0:
                st.error("Error: La concentración del producto (S) no puede ser 0 para el cálculo.")
            else:
                # 3. Caudal de químico (L/h)
                volumen_Lh = masa_activa_g_h / activo_por_litro

                # 4. Conversión a mL/min
                volumen_mLmin = volumen_Lh * 1000 / 60

                st.success("✅ Cálculo Exitoso")
                st.metric(label="Caudal de Dosificación Requerido", value=f"{volumen_mLmin:.3f} mL/min")
        else:
            st.warning("Por favor, asegúrese de que todos los valores sean mayores a cero.")


# =====================================================================
## 🌊 MODO 2: CALCULAR DOSIS ACTUAL (ppm)
# =====================================================================
elif modo == 'Calcular Dosis Actual (ppm)':
    
    st.header('2. Dosis Actual (ppm)')
    
    # --- Solicitud de Datos (Widgets) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos de Caudal (m³/h)")
        # Valores de entrada sin decimales, como lo ajustaste
        Qe = st.number_input('Caudal de Entrada (Qe):', min_value=0, value=50, key='Qe_dosis', help="Caudal de agua fresca que entra a la planta.")
        Qr = st.number_input('Caudal de Recirculación (Qr):', min_value=0, value=60, key='Qr_dosis', help="Caudal de agua recirculada.")
        
        Q = Qe + Qr
        st.info(f"Caudal Total (Qe + Qr): **{Q:.2f} m³/h**")

    with col2:
        st.subheader("Datos de Dosificación")
        S = st.number_input('Concentración Producto (%):', min_value=0, max_value=100, value=40, key='S_dosis', help="Porcentaje de ingrediente activo en el producto químico.")
        # Aquí se usa un valor inicial sin decimal, pero el campo permite decimales para mayor precisión en mL/min
        volumen_mLmin = st.number_input('Caudal de Dosificación (mL/min):', min_value=0, value=300, help="Caudal que la bomba está dosificando actualmente.")
        
    st.write('---')

    if st.button('Calcular Dosis (ppm)', type="primary"):
        if Q > 0 and S > 0 and volumen_mLmin > 0:
            
            # 1. Convertir el caudal dosificado a L/h
            volumen_Lh = volumen_mLmin * 60 / 1000 

            # 2. Activo disponible por litro del producto (g/L)
            activo_por_litro = densidad * 1000 * (S / 100)

            # 3. Calcular Masa Activa suministrada (g/h)
            masa_activa_g_h = volumen_Lh * activo_por_litro
            
            # 4. Calcular la Dosis (mg/L o ppm)
            denominador = Q * FACTOR_AJUSTE
            if denominador == 0:
                 st.error("Error: El Caudal Total no puede ser 0.")
            else:
                dosis_mg_l = masa_activa_g_h / denominador

                st.success("✅ Cálculo Exitoso")
                st.metric(label="Dosis Actual (ppm)", value=f"{dosis_mg_l:.2f} ppm")
        else:
            st.warning("Por favor, ingrese valores válidos mayores a cero.")


# =====================================================================
## 🧪 MODO 3: DOSIFICACIÓN EN JARRAS (mL de producto)
# =====================================================================
elif modo == 'Dosificación en Jarras (mL de producto)':
    
    st.header('3. Dosificación para Prueba de Jarras')
    
    st.markdown("Ingrese la dosis específica (en ppm) que desea probar en cada una de las jarras.")
    st.write('---')
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos del Producto")
        # Mantengo tu formato de decimales para el porcentaje
        S_jarra = st.number_input('Concentración Producto (%):', min_value=0.01, max_value=100.00, value=10.00, format="%.2f", key='S_jarra', help="Porcentaje de ingrediente activo en el producto químico.")
        
    with col2:
        st.subheader("Datos de la Prueba")
        # Mantengo tu formato de decimales para el volumen
        Vol_jarra_L = st.number_input('Volumen de la Jarra (L):', min_value=0.1, value=1.0, format="%.1f", key='Vol_jarra', help="Volumen de agua que contendrá cada jarra (típicamente 1 Litro).")
        
    st.subheader("Dosis (ppm) por Jarra")
    
    # ENTRADA MANUAL DE PPM PARA LAS 4 JARRAS EN COLUMNAS
    
    col_dosis = st.columns(4)
    
    # NOTA: Los valores iniciales (value) son solo sugerencias.
    ppm_jarra_1 = col_dosis[0].number_input('Jarra 1 (ppm):', min_value=0.0, value=1.0, format="%.1f", key='ppm_j1')
    ppm_jarra_2 = col_dosis[1].number_input('Jarra 2 (ppm):', min_value=0.0, value=1.2, format="%.1f", key='ppm_j2')
    ppm_jarra_3 = col_dosis[2].number_input('Jarra 3 (ppm):', min_value=0.0, value=1.4, format="%.1f", key='ppm_j3')
    ppm_jarra_4 = col_dosis[3].number_input('Jarra 4 (ppm):', min_value=0.0, value=1.6, format="%.1f", key='ppm_j4')
        
    dosis_ppm = [ppm_jarra_1, ppm_jarra_2, ppm_jarra_3, ppm_jarra_4]
    
    # Mostrar la dosis total seleccionada
    st.info(f"Se calculará la dosificación para las dosis (ppm): {dosis_ppm[0]:.1f}, {dosis_ppm[1]:.1f}, {dosis_ppm[2]:.1f}, {dosis_ppm[3]:.1f}")
        
    st.write('---')

    if st.button('Calcular mL para Jarras', type="primary"):
        
        # Validación de que al menos la concentración del producto y el volumen de jarra sean válidos.
        if S_jarra > 0 and Vol_jarra_L > 0:
            
            # FÓRMULA DE JAR TEST: mL_producto = (PPM_Deseada * Vol_Jarra_L) / (S_producto * 10)
            denominador = S_jarra * 10
            
            resultados = {}
            if denominador == 0:
                st.error("Error: La concentración del producto no puede ser cero.")
            else:
                
                st.success("✅ Cálculo Exitoso")
                st.markdown("##### Mililitros (mL) de producto a dosificar por jarra:")
                
                # Bucle para calcular los 4 resultados
                for i, D_ppm in enumerate(dosis_ppm):
                    
                    # Cálculo:
                    mL_producto = (D_ppm * Vol_jarra_L) / denominador
                    
                    # Guardar el resultado para mostrarlo, manteniendo tu formato de salida (.1f mL)
                    resultados[f"Jarra {i+1} ({D_ppm:.1f} ppm)"] = mL_producto
                
                # Mostrar los resultados en columnas
                cols = st.columns(4)
                for i, (label, ml) in enumerate(resultados.items()):
                    # Mantengo tu formato de salida (.1f mL)
                    cols[i].metric(label=label, value=f"{ml:.1f} mL")
        
        else:
            st.warning("Por favor, ingrese valores de concentración y volumen válidos (> 0).")
