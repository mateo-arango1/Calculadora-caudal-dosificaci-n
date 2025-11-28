import streamlit as st
import numpy as np

# --- Configuración de la Interfaz ---
st.set_page_config(
    page_title="Calculadora de Dosificación - Doble Función",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('🧪 Calculadora de Dosificación de Químico')
st.markdown("---")

# --- Selector de Modo ---
modo = st.radio(
    "Seleccione el modo de cálculo:",
    ('Calcular Caudal de Dosificación (mL/min)', 'Calcular Dosis Actual (ppm)'),
    horizontal=True
)

st.markdown("---")

# Parámetros fijos
FACTOR_AJUSTE = 0.7
densidad = 1.0 # g/mL (Asumida)


## 🚀 MODO 1: CALCULAR CAUDAL DE DOSIFICACIÓN (mL/min)
if modo == 'Calcular Caudal de Dosificación (mL/min)':
    
    st.header('1. Caudal de Dosificación (mL/min)')

    # --- Solicitud de Datos (Widgets) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos de Caudal (m³/h)")
        # USAMOS X.0 PARA EVITAR EL ERROR
        Qe = st.number_input('Caudal de Entrada (Qe):', min_value=0, value=50, help="Caudal de agua fresca que entra a la planta.")
        Qr = st.number_input('Caudal de Recirculación (Qr):', min_value=0, value=60, help="Caudal de agua recirculada.")
        
        Q = Qe + Qr
        st.info(f"Caudal Total (Qe + Qr): **{Q:.2f} m³/h**")

    with col2:
        st.subheader("Datos de Dosificación")
        D = st.number_input('Dosis Requerida (ppm):', min_value=0, value=100, help="Cantidad de químico activo que se necesita por litro.")
        # USAMOS X.0 PARA EVITAR EL ERROR
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
                st.metric(label="Caudal de Dosificación Requerido", value=f"{volumen_mLmin:.2f} mL/min")
        else:
            st.warning("Por favor, asegúrese de que todos los valores sean mayores a cero.")


## 🌊 MODO 2: CALCULAR DOSIS ACTUAL (ppm)
elif modo == 'Calcular Dosis Actual (ppm)':
    
    st.header('2. Dosis Actual (ppm)')
    
    # --- Solicitud de Datos (Widgets) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos de Caudal (m³/h)")
        # USAMOS X.0 PARA EVITAR EL ERROR
        Qe = st.number_input('Caudal de Entrada (Qe):', min_value=0, value=50, key='Qe_dosis', help="Caudal de agua fresca que entra a la planta.")
        Qr = st.number_input('Caudal de Recirculación (Qr):', min_value=0, value=60, key='Qr_dosis', help="Caudal de agua recirculada.")
        
        Q = Qe + Qr
        st.info(f"Caudal Total (Qe + Qr): **{Q:.2f} m³/h**")

    with col2:
        st.subheader("Datos de Dosificación")
        # USAMOS X.0 PARA EVITAR EL ERROR
        S = st.number_input('Concentración Producto (%):', min_value=0, max_value=100, value=40, key='S_dosis', help="Porcentaje de ingrediente activo en el producto químico.")
        # ESTE YA TENÍA DECIMAL:
        volumen_mLmin = st.number_input('Caudal de Dosificación (mL/min):', min_value=0, value=300, help="Caudal que la bomba está dosificando actualmente.")
        
    st.write('---')

    if st.button('Calcular Dosis (ppm)', type="primary"):
        if Q > 0 and S > 0 and volumen_mLmin > 0:
            
            # Reordenamos la fórmula original para despejar D (Dosis)
            
            # 1. Convertir el caudal dosificado a L/h
            volumen_Lh = volumen_mLmin * 60 / 1000 

            # 2. Activo disponible por litro del producto (g/L)
            activo_por_litro = densidad * 1000 * (S / 100)

            # 3. Calcular Masa Activa suministrada (g/h)
            masa_activa_g_h = volumen_Lh * activo_por_litro
            
            # 4. Calcular la Dosis (mg/L)
            denominador = Q * FACTOR_AJUSTE
            if denominador == 0:
                 st.error("Error: El Caudal Total no puede ser 0.")
            else:
                # El resultado está en g/m^3, que es equivalente a mg/L (ppm)
                dosis_mg_l = masa_activa_g_h / denominador

                st.success("✅ Cálculo Exitoso")
                st.metric(label="Dosis Actual (ppm)", value=f"{dosis_mg_l:.2f} ppm")
        else:
            st.warning("Por favor, ingrese valores válidos mayores a cero.")
