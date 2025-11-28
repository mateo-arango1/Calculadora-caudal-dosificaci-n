import streamlit as st

# --- Configuración de la Interfaz ---
st.set_page_config(
    page_title="Calculadora de Dosificación",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('🧪 Caudal de Dosificación de Químico')
st.write('---')
st.markdown("##### Ingrese los valores de la planta y del producto:")

# --- Solicitud de Datos (Widgets de Streamlit) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Datos de Caudal (m³/h)")
    Qe = st.number_input('Caudal de Entrada (Qe):', min_value=0.0, value=100.0, format="%.2f", help="Caudal de agua fresca que entra a la planta.")
    Qr = st.number_input('Caudal de Recirculación (Qr):', min_value=0.0, value=50.0, format="%.2f", help="Caudal de agua recirculada.")

    Q = Qe + Qr
    st.info(f"Caudal Total (Qe + Qr): **{Q:.2f} m³/h**")

with col2:
    st.subheader("Datos de Dosificación")
    D = st.number_input('Dosis Requerida (mg/L):', min_value=0.0, value=2.0, format="%.2f", help="Cantidad de químico activo que se necesita por litro.")
    S = st.number_input('Concentración Producto (%):', min_value=0.0, max_value=100.0, value=40.0, format="%.2f", help="Porcentaje de ingrediente activo en el producto químico.")

# Parámetros fijos según tu lógica
FACTOR_AJUSTE = 0.7
densidad = 1.0 # g/mL (Asumida)

st.write('---')

# --- Lógica de Cálculo ---
if st.button('Calcular Caudal de Dosificación', type="primary"):
    if Q > 0 and D > 0 and S > 0:

        # Paso 1: masa activa requerida (g/h)
        masa_activa_g_h = Q * FACTOR_AJUSTE * D 

        # Paso 2: activo disponible por litro del producto (g/L)
        activo_por_litro = densidad * 1000 * (S / 100)

        # Evitar división por cero
        if activo_por_litro == 0:
            st.error("Error: La concentración del producto (S) no puede ser 0 para el cálculo.")
        else:
            # Paso 3: caudal de químico (L/h)
            volumen_Lh = masa_activa_g_h / activo_por_litro

            # Paso 4: Conversión a la unidad de dosificación (mL/min)
            volumen_mLmin = volumen_Lh * 1000 / 60

            # --- Resultados ---
            st.success("✅ Cálculo Exitoso")

            st.metric(
                label="Caudal de Dosificación Requerido",
                value=f"{volumen_mLmin:.3f} mL/min"
            )

            st.markdown(f"""
            <details><summary>Detalles del Cálculo</summary>

            * Caudal Total utilizado: **{Q:.2f} m³/h**
            * Masa Activa Requerida: **{masa_activa_g_h:.2f} g/h** (Aplicando factor 0.7)
            * Activo en Producto: **{activo_por_litro:.2f} g/L** (Densidad 1 g/mL)

            </details>
            """, unsafe_allow_html=True)

    else:
        st.warning("Por favor, asegúrese de que todos los valores de entrada sean mayores a cero.")
