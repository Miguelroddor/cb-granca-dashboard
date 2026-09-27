import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="CB Gran Canaria - Analytics", layout="wide")

# Estilos visuales corporativos
STYLING = """
    <style>
    .main { background-color: #F8F9FA; }
    h1 { color: #002B66; font-weight: 700; }
    .stMetric { background-color: #FFFFFF; padding: 12px; border-radius: 8px; border-left: 5px solid #002B66; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
"""
st.markdown(STYLING, unsafe_allow_html=True)

st.title("🏀 CB Gran Canaria — Departamento de Analítica Deportiva")
st.caption("Panel Ejecutivo de Rendimiento — Estrategia Primera FEB")

# ---------------------------------------------------------
# BASE DE DATOS 1: PLANTILLA ACTUAL
# ---------------------------------------------------------
data_informe = {
    'Jugador': [
        'Carlos Alocén', 'Jón Axel Guðmundsson', 'Christian Díaz', 'Marques Townes', 
        'Joe Cremo', 'Lucas Maniema', 'Nicolas Brussino', 'Miquel Salvó', 
        'Juan Rubio "Niñirola"', 'Pierre Pelos', 'Roberts Blumbergs', 'Eric Vila', 'Luis Chocho', 
        'Fran Guerra', 'Kur Kuath', 'Luke Fischer', 'Mike Tobey'
    ],
    'Posicion': [
        'Base', 'Base', 'Escolta', 'Escolta', 
        'Escolta', 'Escolta', 'Alero', 'Alero', 
        'Alero', 'Ala-Pivot', 'Ala-Pivot', 'Ala-Pivot', 'Ala-Pivot', 
        'Pivot', 'Pivot', 'Pivot', 'Pivot'
    ],
    'MIN/P': [25.5, 22.0, 16.5, 20.0, 18.0, 8.0, 26.5, 21.0, 15.0, 23.5, 18.0, 15.5, 10.0, 18.5, 19.0, 17.5, 12.0],
    'PTS/40M': [18.8, 16.4, 15.2, 17.5, 15.5, 11.5, 21.0, 13.2, 12.0, 17.0, 15.8, 13.5, 11.0, 23.8, 14.5, 16.2, 12.5],
    'eFG%': [51.2, 48.5, 49.0, 50.5, 56.0, 45.0, 55.5, 52.0, 51.0, 54.1, 52.5, 49.5, 48.0, 71.4, 62.0, 58.0, 54.0],
    'TS%': [55.4, 52.1, 52.5, 53.0, 58.2, 47.0, 58.0, 54.5, 53.0, 56.8, 55.0, 51.5, 50.0, 69.7, 63.5, 60.2, 55.5],
    'AST/TOV': [3.00, 1.33, 1.80, 1.60, 1.80, 0.90, 2.20, 1.50, 1.10, 1.20, 1.10, 1.00, 0.70, 0.50, 0.60, 0.80, 0.90],
    'Perfil Táctico': [
        'Generador principal, alto control de ritmo.',
        'Amenaza exterior en Catch & Shoot y P&R.',
        'Agresividad en penetración y cambio de ritmo.',
        'Potencia física y generación en 1v1.',
        'Especialista en espacio exterior (Spacing).',
        'Joven exterior, energía defensiva.',
        'Referente exterior, tiro lejano y generación.',
        'Intensidad física, rebote y trabajo defensivo.',
        'Especialista 3&D y solidez defensiva.',
        'Ala-Pivot tirador (Pick & Pop).',
        'Versatilidad interior/exterior y tiro tras bloqueo.',
        'Combo Forward polivalente.',
        'Rotación interior y trabajo en el rebote.',
        'Dominio absoluto en la pintura y continuación.',
        'Protector de aro, capacidad atlética e intimidación.',
        'Solidez en el bloqueo directo y juego en poste bajo.',
        'Veteranía, dureza y lectura del juego interior.'
    ]
}
df = pd.DataFrame(data_informe)

# ---------------------------------------------------------
# BASE DE DATOS 2: MERCADO DE SCOUTING (OPORTUNIDADES DE FICHAJE)
# ---------------------------------------------------------
data_scouting = {
    'Jugador': ['Marco V.', 'Kevon M.', 'David R.', 'Tariq K.', 'Luka P.', 'Samu T.'],
    'Liga Origen': ['Segunda FEB', 'Liga NBL / Europa', 'Primera FEB (Rotación)', 'Pro B Francia', 'ABA League 2', 'Segunda FEB'],
    'Posicion': ['Base', 'Escolta', 'Ala-Pivot', 'Pivot', 'Alero', 'Base'],
    'MIN/P': [19.5, 21.0, 16.0, 18.2, 22.0, 18.0],
    'PTS/40M': [17.2, 19.8, 14.5, 16.0, 18.0, 15.0],
    'eFG%': [54.0, 58.0, 55.0, 64.0, 53.5, 51.0],
    'TS%': [58.4, 61.2, 59.0, 66.5, 57.0, 55.0],
    'AST/TOV': [3.10, 1.90, 1.40, 0.80, 2.10, 2.80],
    'Caché Est. (€)': [32000, 45000, 38000, 42000, 40000, 28000],
    'Perfil Oportunidad': [
        'Generador joven con gran lectura de P&R e infravalorado por minutos.',
        'Tirador de Spacing de altísima eficiencia exterior.',
        'Stretch 4 reboteador con gran tiro tras bloqueo.',
        'Protector de aro atlético y contundente en continuaciones.',
        'Alero físico con capacidad de generar en 1v1 a bajo coste.',
        'Director de juego seguro con gran ratio asistencias/pérdidas.'
    ]
}
df_scouting = pd.DataFrame(data_scouting)

# Filtro lateral para la plantilla
st.sidebar.header("🎯 Filtros de Plantilla")
posiciones = list(df["Posicion"].unique())
posicion_filter = st.sidebar.multiselect("Filtrar por Posición:", options=posiciones, default=posiciones)

if posicion_filter:
    df_filtered = df[df["Posicion"].isin(posicion_filter)]
else:
    df_filtered = df

# Navegación por Pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Matriz Volumen vs Eficiencia", 
    "📊 Cuadro de Mando Táctico", 
    "🕸️ Ficha Táctica y Radar",
    "🔍 Scouting de Mercado (Fase 2)"
])

# ---------------------------------------------------------
# PESTAÑA 1: MATRIZ DE RENDIMIENTO
# ---------------------------------------------------------
with tab1:
    st.subheader("Matriz de Rol: Anotación Proyectada (PTS/40) vs Eficiencia Real (TS%)")
    avg_pts = df_filtered["PTS/40M"].mean()
    avg_ts = df_filtered["TS%"].mean()
    
    fig1 = px.scatter(
        df_filtered, x="PTS/40M", y="TS%", color="Posicion", text="Jugador",
        hover_data=["MIN/P", "eFG%", "AST/TOV"],
        color_discrete_map={'Base': '#002B66', 'Escolta': '#0055B8', 'Alero': '#3385E6', 'Ala-Pivot': '#E6B800', 'Pivot': '#FCD116'}
    )
    max_pts = df_filtered["PTS/40M"].max() + 2
    max_ts = df_filtered["TS%"].max() + 3

    fig1.add_shape(type="rect", x0=avg_pts, y0=avg_ts, x1=max_pts, y1=max_ts, fillcolor="rgba(252, 209, 22, 0.12)", line=dict(width=0))
    fig1.add_annotation(x=max_pts-2, y=max_ts-1, text="<b>ALTO VOLUMEN & EFICIENCIA</b>", showarrow=False, font=dict(size=10, color="#002B66"))
    fig1.add_vline(x=avg_pts, line_dash="dash", line_color="#888888", annotation_text=f"Media PTS/40 ({avg_pts:.1f})")
    fig1.add_hline(y=avg_ts, line_dash="dash", line_color="#888888", annotation_text=f"Media TS% ({avg_ts:.1f}%)")
    
    fig1.update_traces(textposition='top center', marker=dict(size=14, line=dict(width=1.5, color='DarkSlateGrey')))
    fig1.update_layout(xaxis_title="<b>Anotación Proyectada (PTS / 40 Minutos) →</b>", yaxis_title="<b>Eficiencia TS% →</b>", plot_bgcolor="#F8F9FA", paper_bgcolor="#F8F9FA", height=540)
    st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 2: CUADRO DE MANDO TÁCTICO
# ---------------------------------------------------------
with tab2:
    st.subheader("Cuadro de Mando: Análisis Comparativo de la Plantilla")
    col_left, col_right = st.columns(2)
    with col_left:
        fig_pts = px.bar(df_filtered.sort_values(by="PTS/40M"), x="PTS/40M", y="Jugador", orientation='h', color="Posicion", text="PTS/40M", title="Proyección Anotadora (PTS / 40M)", color_discrete_sequence=['#002B66', '#FCD116'])
        fig_pts.update_traces(texttemplate='%{text}', textposition='outside')
        fig_pts.update_layout(plot_bgcolor="#F8F9FA", height=500)
        st.plotly_chart(fig_pts, use_container_width=True)
    with col_right:
        fig_ast = px.bar(df_filtered.sort_values(by="AST/TOV"), x="AST/TOV", y="Jugador", orientation='h', color="Posicion", text="AST/TOV", title="Seguridad de Balón (Ratio AST / TOV)", color_discrete_sequence=['#002B66', '#FCD116'])
        fig_ast.update_traces(texttemplate='%{text}', textposition='outside')
        fig_ast.update_layout(plot_bgcolor="#F8F9FA", height=500)
        st.plotly_chart(fig_ast, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 3: FICHA TÁCTICA Y RADAR
# ---------------------------------------------------------
with tab3:
    st.subheader("Perfil Técnico de Rendimiento Individual")
    jugador_sel = st.selectbox("Seleccionar Jugador para Evaluación:", df["Jugador"].tolist())
    j = df[df["Jugador"] == jugador_sel].iloc[0]
    st.markdown(f"### **{j['Jugador']}** ({j['Posicion']})")
    st.info(f"**Perfil Táctico en Primera FEB:** {j['Perfil Táctico']}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Minutos / Partido", f"{j['MIN/P']} min")
    c2.metric("Puntos / 40 Min", f"{j['PTS/40M']}")
    c3.metric("True Shooting (TS%)", f"{j['TS%']}%")
    c4.metric("Ratio AST / TOV", f"{j['AST/TOV']}")

    categories = ['Puntos / 40M', 'eFG%', 'TS%', 'AST / TOV', 'Minutos / P']
    val_jugador = [j['PTS/40M'], j['eFG%'] / 2, j['TS%'] / 2, j['AST/TOV'] * 8, j['MIN/P']]
    val_media = [df['PTS/40M'].mean(), df['eFG%'].mean() / 2, df['TS%'].mean() / 2, df['AST/TOV'].mean() * 8, df['MIN/P'].mean()]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=val_jugador, theta=categories, fill='toself', name=j['Jugador'], fillcolor='rgba(0, 43, 102, 0.4)', line=dict(color='#002B66', width=2)))
    fig_radar.add_trace(go.Scatterpolar(r=val_media, theta=categories, fill='toself', name='Media de la Plantilla', fillcolor='rgba(252, 209, 22, 0.2)', line=dict(color='#FCD116', width=2, dash='dash')))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 35])), showlegend=True, height=480, paper_bgcolor="#F8F9FA")
    st.plotly_chart(fig_radar, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 4: SCOUTING DE MERCADO (FASE 2 - VISUAL ROI)
# ---------------------------------------------------------
with tab4:
    st.subheader("🎯 Módulo de Scouting Automatizado: Detección de Fichajes Eficientes")
    st.markdown("Algoritmo de identificación de **oportunidades de alto rendimiento y bajo coste presupuestario** en ligas FEB y europeas.")
    
    # Algoritmo de Score de Oportunidad
    df_scouting['Score Oportunidad'] = (
        (df_scouting['TS%'] * 0.5) + 
        (df_scouting['PTS/40M'] * 1.8) + 
        (df_scouting['AST/TOV'] * 4) - 
        (df_scouting['Caché Est. (€)'] / 2000)
    ).round(1)

    # Filtros interactivos
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pos_scout = st.selectbox("Buscar por Posición Necesaria:", ["Todas"] + list(df_scouting["Posicion"].unique()))
    with col_f2:
        max_precio = st.slider("Presupuesto Máximo de Fichaje (€):", 20000, 50000, 50000, step=5000)

    df_scout_filtered = df_scouting[df_scouting['Caché Est. (€)'] <= max_precio]
    if pos_scout != "Todas":
        df_scout_filtered = df_scout_filtered[df_scout_filtered['Posicion'] == pos_scout]

    # GRÁFICO 1: Matriz Caché vs Eficiencia Real
    fig_scout = px.scatter(
        df_scout_filtered,
        x="Caché Est. (€)",
        y="TS%",
        size="Score Oportunidad",
        color="Posicion",
        text="Jugador",
        hover_data=["Liga Origen", "PTS/40M", "AST/TOV"],
        title="<b>1. Matriz de Oportunidad: Caché (€) vs Eficiencia Real (TS%)</b>",
        color_discrete_sequence=['#002B66', '#FCD116', '#0055B8', '#E6B800']
    )
    fig_scout.update_traces(textposition='top center')
    fig_scout.update_layout(plot_bgcolor="#F8F9FA", paper_bgcolor="#F8F9FA", height=420)
    st.plotly_chart(fig_scout, use_container_width=True)

    # GRÁFICO 2: Comparativa de Rentabilidad
    st.markdown("---")
    st.subheader("📊 2. Comparativa de Rentabilidad y Eficiencia del Mercado")
    
    fig_bar_scout = px.bar(
        df_scout_filtered.sort_values(by="Score Oportunidad", ascending=True),
        x="Score Oportunidad",
        y="Jugador",
        orientation='h',
        color="Caché Est. (€)",
        text="Score Oportunidad",
        title="<b>Ranking de Oportunidades (Score de Rentabilidad vs Coste)</b>",
        color_continuous_scale="Blues"
    )
    fig_bar_scout.update_traces(texttemplate='%{text} pts', textposition='outside')
    fig_bar_scout.update_layout(plot_bgcolor="#F8F9FA", paper_bgcolor="#F8F9FA", height=380)
    st.plotly_chart(fig_bar_scout, use_container_width=True)

    # GRÁFICO 3: Radar de Impacto Individual vs Plantilla
    st.divider()
    st.subheader("📋 3. Radiografía Visual del Prospecto Seleccionado")
    scout_sel = st.selectbox("Seleccionar Prospecto para Comparación Visual:", df_scout_filtered["Jugador"].tolist())
    
    if scout_sel:
        s = df_scout_filtered[df_scout_filtered["Jugador"] == scout_sel].iloc[0]
        
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Liga de Origen", f"{s['Liga Origen']}")
        sc2.metric("Caché Estimado", f"{s['Caché Est. (€)']:,} €")
        sc3.metric("Eficiencia TS%", f"{s['TS%']}%")
        sc4.metric("Score Oportunidad", f"{s['Score Oportunidad']} / 100")

        st.success(f"**Análisis de Valor / ROI:** {s['Perfil Oportunidad']}")

        categories_scout = ['Puntos / 40M', 'TS%', 'AST / TOV', 'Eficiencia eFG%']
        val_prospecto = [s['PTS/40M'], s['TS%'] / 2, s['AST/TOV'] * 8, s['eFG%'] / 2]
        val_media_plantilla = [df['PTS/40M'].mean(), df['TS%'].mean() / 2, df['AST/TOV'].mean() * 8, df['eFG%'].mean() / 2]
        
        fig_radar_scout = go.Figure()
        fig_radar_scout.add_trace(go.Scatterpolar(
            r=val_prospecto, theta=categories_scout, fill='toself', 
            name=f"Fichaje Objetivo: {s['Jugador']}", 
            fillcolor='rgba(252, 209, 22, 0.4)', line=dict(color='#E6B800', width=3)
        ))
        fig_radar_scout.add_trace(go.Scatterpolar(
            r=val_media_plantilla, theta=categories_scout, fill='toself', 
            name='Media de la Plantilla Actual', 
            fillcolor='rgba(0, 43, 102, 0.2)', line=dict(color='#002B66', width=2, dash='dash')
        ))
        fig_radar_scout.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 35])), 
            showlegend=True, height=450, paper_bgcolor="#F8F9FA",
            title=f"<b>Impacto Esperado: {s['Jugador']} vs Media de Nuestra Plantilla Actual</b>"
        )
        st.plotly_chart(fig_radar_scout, use_container_width=True)

# Exportación de datos
st.divider()
csv_data = df_filtered.to_csv(index=False, sep=";", encoding="utf-8-sig")
st.download_button(label="Descargar Datos en CSV (Excel)", data=csv_data, file_name="informe_ejecutivo_cb_grancanaria.csv", mime="text/csv")