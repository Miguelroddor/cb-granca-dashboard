import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="CB Gran Canaria - Analytics", layout="wide")

STYLING = """
<style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #002B49; font-weight: 700; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 5px solid #FFC72C; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
</style>
"""
st.markdown(STYLING, unsafe_allow_html=True)

st.title("🏀 CB Gran Canaria — Departamento de Analítica Deportiva")
st.caption("Panel Ejecutivo de Rendimiento — Estrategia Primera FEB")

# ==========================================
# BASE DE DATOS 1: PLANTILLA ACTUAL
# ==========================================
data_informe = {
    "Jugador": [
        "Carlos Alocén", "Jón Axel Guðmundsson", "Christian Díaz", "Marques Townes",
        "Joe Cremo", "Tomas Pavelka", "Miquel Salvó", "Miguel Sazo",
        "Juan Rubio", "Massamba Diop", "Pierre Pelos", "Roberts Blumbergs", "Eric Vila", "Luis Chocho",
        "Lucas Marí", "Ken Kuric", "Luka Fischer", "Mike Tobey"
    ],
    "Posicion": [
        "Base", "Base", "Base", "Escolta", "Escolta",
        "Pívot", "Alero", "Alero", "Alero", "Pívot",
        "Ala-Pívot", "Ala-Pívot", "Ala-Pívot", "Ala-Pívot",
        "Escolta", "Escolta", "Pívot", "Pívot"
    ],
    "Minutos / Partido": [25.5, 22.0, 15.0, 20.0, 18.0, 21.0, 22.5, 12.0, 14.0, 10.0, 23.5, 18.0, 16.5, 8.0, 10.0, 19.5, 12.0, 22.0],
    "PTS/40": [18.8, 16.4, 15.2, 17.5, 16.0, 21.0, 15.0, 13.5, 11.0, 18.0, 16.5, 15.0, 12.0, 10.0, 11.5, 20.0, 14.0, 19.5],
    "eFG%": [52.0, 50.0, 48.0, 51.0, 53.0, 62.0, 54.0, 47.0, 45.0, 58.0, 55.0, 52.0, 46.0, 42.0, 46.0, 56.0, 53.0, 57.0],
    "TS%": [55.4, 53.2, 51.0, 53.0, 56.5, 64.0, 57.0, 50.0, 48.0, 60.0, 58.0, 54.5, 49.0, 44.0, 49.0, 59.0, 55.0, 60.5],
    "AST/40": [8.5, 6.2, 7.0, 4.2, 3.5, 1.2, 3.0, 2.0, 1.8, 0.8, 2.2, 1.5, 2.5, 1.0, 3.2, 2.0, 1.1, 2.0],
    "AST / TOV": [3.0, 2.1, 2.3, 1.6, 1.8, 0.7, 1.5, 1.1, 1.0, 0.5, 1.3, 1.1, 1.4, 0.6, 1.5, 1.7, 0.8, 1.2],
    "Perfil Táctico": [
        "Generador principal, alto control de ritmo.",
        "Amenaza exterior en Catch & Shoot y P&R.",
        "Base organizador de perfil tradicional.",
        "Potencia física y generación en 1v1.",
        "Especialista en tiro tras pantalla.",
        "Joven exterior, energía defensiva.",
        "Alero todoterreno de gran versatilidad.",
        "Intensidad física, rebote y trabajo defensivo.",
        "Especialista defensivo de perímetro.",
        "Interior físico en desarrollo.",
        "Versatilidad interior/exterior y tiro tras bloqueo.",
        "Ala-Pívot tirador (Pick & Pop).",
        "Combo Forward polivalente.",
        "Presencia física y trabajo en el rebote.",
        "Dominio absoluto en la pintura y continuación.",
        "Anotación interior y trabajo en el rebote.",
        "Protector de aro, capacidad atlética e intimidación.",
        "Veteranía, dureza y lectura del juego interior."
    ]
}

df = pd.DataFrame(data_informe)

# ==========================================
# BASE DE DATOS 2: MERCADO DE SCOUTING
# ==========================================
data_scouting = {
    "Jugador": ["Marco S.", "Nemanja V.", "Devon M.", "David R.", "Tariq K.", "Luka P.", "Samu L."],
    "Liga Origen": ["Segunda FEB", "Segunda FEB", "Liga LEB Oro / Primera FEB", "Pro B Francia", "ABA League 2", "Segunda FEB", "Segunda FEB"],
    "Posicion": ["Base", "Escolta", "Ala-Pívot", "Pívot", "Alero", "Base", "Pívot"],
    "MIN/P": [19.5, 21.0, 16.0, 18.2, 22.0, 18.0, 15.0],
    "PTS/40": [18.2, 21.5, 14.8, 19.0, 16.5, 15.0, 13.5],
    "eFG%": [54.0, 58.0, 49.0, 61.0, 52.0, 50.0, 55.0],
    "TS%": [58.4, 61.2, 52.0, 63.5, 55.8, 53.0, 57.5],
    "AST/40": [7.8, 3.5, 2.1, 1.2, 4.0, 6.5, 1.0],
    "AST / TOV": [2.5, 1.4, 1.1, 0.8, 1.8, 2.2, 0.6],
    "Caché Est. (€)": [22000, 28000, 35000, 42000, 30000, 20000, 18000],
    "Perfil Oportunidad": [
        "Generador joven con gran lectura de P&R e infravalorado por minutos.",
        "Tirador de spacing de altísima eficiencia exterior.",
        "Stretch 4 reboteador con gran tiro tras bloqueo.",
        "Pívot físico de gran impacto defensivo y continuaciones.",
        "Alero físico con capacidad de generación en 1v1 a bajo coste.",
        "Director de juego seguro con gran ratio asistencias/pérdidas.",
        "Pívot joven con margen de desarrollo en pintura."
    ]
}

df_scouting = pd.DataFrame(data_scouting)

# Filtro lateral para la plantilla
st.sidebar.header("🔍 Filtros de Plantilla")
default_posiciones = ["Base", "Escolta", "Ala-Pívot", "Pívot"]
position_filter = st.sidebar.multiselect("Filtrar por Posición", options=default_posiciones, default=default_posiciones)

if position_filter:
    df_filtered = df[df["Posicion"].isin(position_filter)]
else:
    df_filtered = df

# ==========================================
# NAVEGACIÓN POR PESTAÑAS (5 VISTAS)
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Matriz Volumen vs Eficiencia", 
    "📋 Cuadro de Mando Táctico", 
    "🎯 Ficha Táctica y Radar", 
    "🔍 Scouting de Mercado", 
    "🏀 LEB Oro: vs Oviedo (108-69)"
])

# ------------------------------------------
# PESTAÑA 1: MATRIZ DE RENDIMIENTO
# ------------------------------------------
with tab1:
    st.markdown("### Matriz de Rol: Anotación Proyectada (PTS/40) vs Eficiencia Real (TS%)")
    
    avg_pts = df_filtered["PTS/40"].mean()
    avg_ts = df_filtered["TS%"].mean()

    fig1 = px.scatter(
        df_filtered, x="PTS/40", y="TS%", color="Posicion", text="Jugador",
        hover_data=["Minutos / Partido", "eFG%", "AST / TOV"],
        color_discrete_map={"Base": "#FFC72C", "Escolta": "#002B49", "Alero": "#338566", "Ala-Pívot": "#E68000", "Pívot": "#D13636"}
    )
    
    min_pts = df_filtered["PTS/40"].min() - 2
    max_pts = df_filtered["PTS/40"].max() + 2

    fig1.add_shape(type="rect", x0=avg_pts, y0=avg_ts, x1=max_pts, y1=max(df_filtered["TS%"]) + 3, fillcolor="rgba(252, 209, 22, 0.12)", line=dict(width=0))
    fig1.add_hline(y=avg_ts, line_dash="dash", line_color="#888888", annotation_text=f"Media TS% ({avg_ts:.1f}%)")
    fig1.add_vline(x=avg_pts, line_dash="dash", line_color="#888888", annotation_text=f"Media PTS/40 ({avg_pts:.1f})")

    fig1.update_traces(textposition="top center", marker=dict(size=14, line=dict(width=1, color="DarkSlateGrey")))
    fig1.update_layout(xaxis_title="Anotación Proyectada (PTS / 40 Minutos)", yaxis_title="Eficiencia TS% (%)", template="plotly_white", height=540)
    st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------
# PESTAÑA 2: CUADRO DE MANDO TÁCTICO
# ------------------------------------------
with tab2:
    st.subheader("Cuadro de Mando: Análisis Comparativo de la Plantilla")
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig_bar1 = px.bar(
            df_filtered.sort_values(by="PTS/40", ascending=True), 
            x="PTS/40", y="Jugador", orientation="h", color="Posicion", 
            title="Proyección Anotadora (PTS / 40M)", color_discrete_sequence=["#002B49", "#FFC72C"]
        )
        fig_bar1.update_traces(texttemplate="%{x:.1f}", textposition="outside")
        fig_bar1.update_layout(template="plotly_white", height=500)
        st.plotly_chart(fig_bar1, use_container_width=True)

    with col_right:
        fig_bar2 = px.bar(
            df_filtered.sort_values(by="AST / TOV", ascending=True), 
            x="AST / TOV", y="Jugador", orientation="h", color="Posicion", 
            title="Seguridad de Balón (Ratio AST / TOV)", color_discrete_sequence=["#002B49", "#FFC72C"]
        )
        fig_bar2.update_traces(texttemplate="%{x:.1f}", textposition="outside")
        fig_bar2.update_layout(template="plotly_white", height=500)
        st.plotly_chart(fig_bar2, use_container_width=True)

# ------------------------------------------
# PESTAÑA 3: FICHA TÁCTICA Y RADAR
# ------------------------------------------
with tab3:
    st.subheader("Perfil Técnico de Rendimiento Individual")
    scout_sel = st.selectbox("Seleccionar jugador para evaluación:", df["Jugador"].tolist())
    
    if scout_sel:
        row = df[df["Jugador"] == scout_sel].iloc[0]
        st.markdown(f"### {row['Jugador']} ({row['Posicion']})")
        st.info(f"**Perfil Técnico en Primero FEB:** {row['Perfil Táctico']}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Minutos / Partido", f"{row['Minutos / Partido']} min")
        c2.metric("Puntos / 40 Min", f"{row['PTS/40']}")
        c3.metric("Tiro Real (TS%)", f"{row['TS%']}%")
        c4.metric("Ratio AST / TOV", f"{row['AST / TOV']}")

        categories = ["Puntos / 40M", "TS%", "AST / TOV", "Minutos / P"]
        val_jugador = [row["PTS/40"], row["TS%"], row["AST / TOV"] * 10, row["Minutos / Partido"]]
        val_media = [df["PTS/40"].mean(), df["TS%"].mean(), df["AST / TOV"].mean() * 10, df["Minutos / Partido"].mean()]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=val_jugador, theta=categories, fill='toself', name=row['Jugador'], fillcolor="rgba(0, 43, 73, 0.4)", line=dict(color="#002B49", width=3)))
        fig_radar.add_trace(go.Scatterpolar(r=val_media, theta=categories, fill='toself', name="Media de la Plantilla", fillcolor="rgba(255, 199, 44, 0.3)", line=dict(color="#FFC72C", width=2, dash="dash")))

        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 70])), showlegend=True, height=450)
        st.plotly_chart(fig_radar, use_container_width=True)

# ------------------------------------------
# PESTAÑA 4: SCOUTING DE MERCADO
# ------------------------------------------
with tab4:
    st.subheader("Módulo de Scouting Automatizado: Detección de Fichajes Eficientes")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pos_scout = st.selectbox("Buscar por Posición Necesaria:", ["Todas"] + list(df_scouting["Posicion"].unique()))
    with col_f2:
        max_precio = st.slider("Presupuesto máximo de Fichaje (€):", 15000, 50000, 50000, step=1000)

    df_scout_filtered = df_scouting[df_scouting["Caché Est. (€)"] <= max_precio]
    if pos_scout != "Todas":
        df_scout_filtered = df_scout_filtered[df_scout_filtered["Posicion"] == pos_scout]

    fig_scout = px.scatter(
        df_scout_filtered, x="Caché Est. (€)", y="TS%", color="Posicion", text="Jugador",
        title="Matriz de Oportunidad: Caché (€) vs Eficiencia Real (TS%)",
        color_discrete_sequence=["#FFC72C", "#002B49", "#338566", "#E68000"]
    )
    fig_scout.update_traces(textposition="top center")
    fig_scout.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_scout, use_container_width=True)

# ------------------------------------------
# PESTAÑA 5: INFORME PARTIDO VS OVIEDO
# ------------------------------------------
with tab5:
    st.title("🏀 CB GRAN CANARIA vs ALIMERKA OVIEDO")
    st.subheader("Jornada 1 - Liga LEB Oro | Marcador Final: 108 - 69 (+39)")

    st.divider()

    # KPIs Directos
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Puntos Totales", value="108", delta="+39 vs Rival")
    with col2:
        st.metric(label="% Tiro de Campo (TC)", value="55.0%", delta="44/80 aciertos")
    with col3:
        st.metric(label="Rebotes Totales", value="41", delta="16 Ofensivos")
    with col4:
        st.metric(label="Puntos tras Pérdida", value="28 pts", delta="Provocadas al rival")

    st.divider()

    # Evolución por Cuartos
    st.markdown("### 📈 Evolución del Marcador por Cuartos")
    df_cuartos = pd.DataFrame({
        'Cuarto': ['Q1', 'Q2', 'Q3', 'Q4'],
        'CB Gran Canaria': [23, 32, 23, 30],
        'Alimerka Oviedo': [27, 16, 14, 12]
    })

    fig_cuartos = go.Figure()
    fig_cuartos.add_trace(go.Bar(
        x=df_cuartos['Cuarto'], 
        y=df_cuartos['CB Gran Canaria'],
        name='CB Gran Canaria',
        marker_color="#FFC72C",
        text=df_cuartos['CB Gran Canaria'],
        textposition='auto'
    ))
    fig_cuartos.add_trace(go.Bar(
        x=df_cuartos['Cuarto'], 
        y=df_cuartos['Alimerka Oviedo'],
        name='Alimerka Oviedo',
        marker_color="#002B49",
        text=df_cuartos['Alimerka Oviedo'],
        textposition='auto'
    ))

    fig_cuartos.update_layout(
        barmode='group',
        xaxis_title="Cuartos",
        yaxis_title="Puntos Anotados",
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_cuartos, use_container_width=True)

    st.divider()

    # NUEVO GRÁFICO 1 Y 2: COMPARATIVA DE ESTADÍSTICAS Y ORIGEN DEL PUNTUAJE
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("### 📊 Métrica Comparativa Colectiva")
        df_stats = pd.DataFrame({
            'Métrica': ['Rebotes', 'Asistencias', 'Robos', 'Puntos en Pintura', 'Puntos Banquillo'],
            'CB Gran Canaria': [41, 26, 14, 52, 44],
            'Alimerka Oviedo': [28, 14, 6, 30, 22]
        })

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            y=df_stats['Métrica'], x=df_stats['CB Gran Canaria'],
            name='CB Gran Canaria', orientation='h', marker_color='#FFC72C',
            text=df_stats['CB Gran Canaria'], textposition='inside'
        ))
        fig_comp.add_trace(go.Bar(
            y=df_stats['Métrica'], x=df_stats['Alimerka Oviedo'],
            name='Alimerka Oviedo', orientation='h', marker_color='#002B49',
            text=df_stats['Alimerka Oviedo'], textposition='inside'
        ))
        fig_comp.update_layout(
            barmode='group',
            template="plotly_white",
            height=340,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_g2:
        st.markdown("### 🎯 Origen de la Anotación (Puntos por Tipo)")
        df_origen = pd.DataFrame({
            'Equipo': ['CB Gran Canaria', 'Alimerka Oviedo'],
            'Tiros de 2 (Pintura/Media)': [62, 38],
            'Triples (T3)': [39, 21],
            'Tiros Libres (TL)': [7, 10]
        })

        fig_origen = go.Figure()
        fig_origen.add_trace(go.Bar(name='T2 (Pintura/Media)', x=df_origen['Equipo'], y=df_origen['Tiros de 2 (Pintura/Media)'], marker_color='#002B49'))
        fig_origen.add_trace(go.Bar(name='Triples (T3)', x=df_origen['Equipo'], y=df_origen['Triples (T3)'], marker_color='#FFC72C'))
        fig_origen.add_trace(go.Bar(name='Tiros Libres (TL)', x=df_origen['Equipo'], y=df_origen['Tiros Libres (TL)'], marker_color='#338566'))

        fig_origen.update_layout(
            barmode='stack',
            template="plotly_white",
            height=340,
            yaxis_title="Puntos Totales",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_origen, use_container_width=True)

    st.divider()

    # Efectividad de Tiro
    st.markdown("### 🎯 Eficiencia en Tiros de Campo (Porcentajes)")
    col_left, col_right = st.columns(2)

    with col_left:
        fig_t2 = go.Figure(data=[go.Pie(
            labels=['Aciertos T2', 'Fallos T2'], 
            values=[31, 21], 
            hole=.6,
            marker_colors=["#FFC72C", '#E0E0E0']
        )])
        fig_t2.update_layout(
            title_text="Efectividad en Tiros de 2 (59.6%)",
            annotations=[dict(text='59.6%', x=0.5, y=0.5, font_size=22, showarrow=False)],
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig_t2, use_container_width=True)

    with col_right:
        fig_t3 = go.Figure(data=[go.Pie(
            labels=['Aciertos T3', 'Fallos T3'], 
            values=[13, 15], 
            hole=.6,
            marker_colors=["#002B49", '#E0E0E0']
        )])
        fig_t3.update_layout(
            title_text="Efectividad en Triples (46.4%)",
            annotations=[dict(text='46.4%', x=0.5, y=0.5, font_size=22, showarrow=False)],
            height=280,
            showlegend=False
        )
        st.plotly_chart(fig_t3, use_container_width=True)

# Exportación de datos
st.divider()
csv_data = df_filtered.to_csv(index=False, sep=";", encoding="utf-8-sig")
st.download_button(label="Descargar Datos en CSV (Excel)", data=csv_data, file_name="informe_ejecutivo_cb_grancanaria.csv", mime="text/csv")
