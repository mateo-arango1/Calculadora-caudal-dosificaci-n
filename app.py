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
    ('Calcular Caudal de Dosificación (mL/min)', 'Calcular Dosis Actual (ppm)', 'Dosificación en Jarras (mL de producto)'),
    horizontal=False # Lo ponemos en vertical para que se vea mejor el tercer botón

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

# =====================================================================
## 🧪 MODO 3: DOSIFICACIÓN EN JARRAS (mL de producto)
# =====================================================================
elif modo == 'Dosificación en Jarras (mL de producto)':
    
    st.header('3. Dosificación para Prueba de Jarras')
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos de Producto")
        S_jarra = st.number_input('Concentración Producto (%):', min_value=0.0, max_value=100.0, value=40.0, key='S_jarra', help="Porcentaje de ingrediente activo en el producto químico.")
        D_base = st.number_input('Dosis Inicial (ppm):', min_value=0.0, value=1.0, key='D_jarra', help="Dosis inicial para la primera jarra.")
        
    with col2:
        st.subheader("Datos de la Prueba")
        Vol_jarra_L = st.number_input('Volumen de la Jarra (L):', min_value=0.01, value=1.0, key='Vol_jarra', help="Volumen de agua que contendrá cada jarra (típicamente 1 Litro).")
        
        # Las dosis que quieres probar (4 resultados)
        ppm_jarra_1 = D_base
        ppm_jarra_2 = D_base * 1.5  # Ejemplo: 50% más
        ppm_jarra_3 = D_base * 2.0  # Ejemplo: el doble
        ppm_jarra_4 = D_base * 2.5  # Ejemplo: 2.5 veces
        
        dosis_ppm = [ppm_jarra_1, ppm_jarra_2, ppm_jarra_3, ppm_jarra_4]
        
        st.info(f"Se calculará la dosificación para las siguientes dosis (ppm): {dosis_ppm}")
        
    st.write('---')

    if st.button('Calcular mL para Jarras', type="primary"):
        if S_jarra > 0 and Vol_jarra_L > 0:
            
            # Cálculo de la constante para un Jar Test (factor de conversión)
            # Objetivo: obtener mL de producto necesarios para una dosis D (en ppm)
            # Fórmula general: mL_producto = (Dosis_ppm * Vol_jarra_L) / (S_producto * 10)
            
            # Denominador: Concentración del producto en una forma conveniente
            # Asumiendo 1 g/mL de densidad, el factor es (S * 10)
            denominador = S_jarra * 10
            
            resultados = {}
            if denominador == 0:
                st.error("Error: La concentración del producto no puede ser cero.")
            else:
                
                st.success("✅ Cálculo Exitoso")
                st.markdown("##### Mililitros (mL) de producto a dosificar por jarra:")
                
                # Bucle para calcular los 4 resultados
                for i, D_ppm in enumerate(dosis_ppm):
                    
                    # mL_producto = (Dosis_ppm * Vol_jarra_L) / denominador
                    mL_producto = (D_ppm * Vol_jarra_L) / denominador
                    
                    # Guardar el resultado para mostrarlo
                    resultados[f"Jarra {i+1} ({D_ppm} ppm)"] = mL_producto
                
                # Mostrar los resultados en una tabla o columnas
                cols = st.columns(4)
                for i, (label, ml) in enumerate(resultados.items()):
                    cols[i].metric(label=label, value=f"{ml:.3f} mL")
        
        else:
            st.warning("Por favor, ingrese valores de concentración y volumen válidos.")
