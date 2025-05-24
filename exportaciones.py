import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
import matplotlib.pyplot as plt
import seaborn as sns
import json
import plotly.express as px
import io
import requests


# 🛠️ Configuración inicial obligatoria
st.set_page_config(page_title="Dashboard de Exportaciones", layout="wide")

# 📥 Cargar datos (desde archivo ya modificado con LATITUD y LONGITUD)

@st.cache_data
def cargar_datos():
    url = "https://drive.google.com/uc?id=1HxVhrT5bwke_2XkPtUDNmO8iPtCTDdLT"
    response = requests.get(url)
    return pd.read_excel(io.BytesIO(response.content))

df = cargar_datos()

# 🎛️ Menú de navegación lateral
st.sidebar.title("Panel de Navegación")
pestania = st.sidebar.radio("Selecciona una vista:", [
    "Resumen General",
    "Comparativo por País",
    "Mapa Interactivo",
    "Transporte y Régimen",
    " Logística y Modalidades de Exportación",
    "FOB por Departamento",
    "País y Régimen",
     "Mapa Mundial de KG"

])

# ======================
# 🧩 Pestaña 1 - Resumen
# ======================
if pestania == "Resumen General":
    st.markdown("## 🌿 Resumen General de Exportaciones")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Total registros", f"{len(df):,}")

    with col2:
        st.metric("💙 Países únicos", df["NOMBRE_PAIS"].nunique())

    with col3:
        # Extraer año directamente si está en la columna 'FECH'
        if df["FECH"].dtype == "int64" or df["FECH"].dtype == "float64":
            st.metric("📅 Año más reciente", int(df["FECH"].max()))
        else:
            st.metric("📅 Año más reciente", "No disponible")

    # 📊 Gráfico de barras con países top
    st.markdown("### Exportaciones por país")
    top_paises = df["NOMBRE_PAIS"].value_counts().head(10)
    top_paises_df = top_paises.reset_index()
    top_paises_df.columns = ["País", "Exportaciones"]

    fig = px.bar(
        top_paises_df,
        x="País",
        y="Exportaciones",
        labels={"Exportaciones": "Número de Exportaciones"},
        color_discrete_sequence=["#1f77b4"]
    )
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# 🧩 Pestaña 2 - Comparativo país
# ===============================
elif pestania == "Comparativo por País":
    st.markdown("## 🌍 Comparativo por País")

    paises = sorted(df["NOMBRE_PAIS"].dropna().unique())
    pais_seleccionado = st.selectbox("Selecciona un país", paises)

    df_pais = df[df["NOMBRE_PAIS"] == pais_seleccionado]
    if not df_pais.empty:
        df_agrupado = df_pais.groupby("FECH")["FOBDOL_MILLONES"].sum().reset_index()

        fig = px.line(
            df_agrupado,
            x="FECH",
            y="FOBDOL_MILLONES",
            markers=True,
            labels={"FOBDOL_MILLONES": "Millones FOB", "FECH": "Año"},
            title=f"Exportaciones de {pais_seleccionado} por Año"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos para este país.")

          # Segundo gráfico: FOB vs Peso Neto Exportado
    st.markdown("### 📦 Valor FOB vs Peso Neto de Exportaciones")
    df_pais_valid = df_pais[(df_pais["FOBDOL_MILLONES"] > 0) & (df_pais["PNK"] > 0)]

    if not df_pais_valid.empty:
        fig_scatter = px.scatter(
            df_pais_valid,
            x="PNK",
            y="FOBDOL_MILLONES",
            size="FOBDOL_MILLONES",
            color="FOBDOL_MILLONES",
            hover_data=["MES_NOMBRE"],
            labels={"PNK": "Peso Neto (KG)", "FOBDOL_MILLONES": "Valor FOB (Millones)"},
            color_continuous_scale=px.colors.sequential.Oranges,
            title=f"Relación entre Peso Neto y Valor FOB para {pais_seleccionado}"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No hay datos con peso neto y FOB positivo para este país.")




# =============================
# 🧩 Pestaña 3 - Mapa interactivo
# =============================


elif pestania == "Mapa Interactivo":
    st.markdown("## 🗺️ Volumen de exportaciones por país")
    st.markdown("### Exportaciones acumuladas por país (en millones FOB)")

    df_mapa = df.groupby(["NOMBRE_PAIS", "LATITUD", "LONGITUD"])["FOBDOL_MILLONES"].sum().reset_index()

    fig = px.scatter_geo(
        df_mapa,
        lat="LATITUD",
        lon="LONGITUD",
        size="FOBDOL_MILLONES",
        color="FOBDOL_MILLONES",
        projection="natural earth",
        hover_name="NOMBRE_PAIS",
        color_continuous_scale=[
            "#fff700",  # amarillo neón
            "#ffa500",  # naranja fuerte
            "#ff4500",  # naranja rojizo
            "#ff0000",  # rojo puro
            "#990000"   # rojo sangre
        ],
        title="Exportaciones en millones de dólares (FOB)"
    )

    fig.update_geos(
        landcolor="rgb(140, 255, 140)",   # verde chillón
        oceancolor="rgb(80, 180, 255)",   # azul fuerte
        showocean=True,
        showland=True,
        showcountries=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # 📆 Segundo gráfico animado
    # ==============================

    st.markdown("### 📆 Exportaciones mensuales por país (Animación)")

    orden_meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    df_animado = df.groupby(["MES_NOMBRE", "NOMBRE_PAIS", "LATITUD", "LONGITUD"])["FOBDOL_MILLONES"].sum().reset_index()
    df_animado["MES_NOMBRE"] = pd.Categorical(df_animado["MES_NOMBRE"], categories=orden_meses, ordered=True)
    df_animado = df_animado.sort_values("MES_NOMBRE")

    fig_animado = px.scatter_geo(
        df_animado,
        lat="LATITUD",
        lon="LONGITUD",
        size="FOBDOL_MILLONES",
        color="FOBDOL_MILLONES",
        animation_frame="MES_NOMBRE",
        projection="natural earth",
        hover_name="NOMBRE_PAIS",
        color_continuous_scale=px.colors.sequential.OrRd,
        title="Evolución mensual de exportaciones en millones de dólares (FOB)",
        height=600
    )

    fig_animado.update_geos(
        landcolor="rgb(140, 255, 140)",
        oceancolor="rgb(80, 180, 255)",
        showocean=True,
        showcountries=True,
        showland=True
    )

    st.plotly_chart(fig_animado, use_container_width=True)


# ================================
# 🧩 Pestaña 4 - Transporte y Régimen
# ================================

elif pestania == "Transporte y Régimen":
    st.markdown("## 🚢 Cantidad de exportaciones por tipo de transporte y régimen")
    st.markdown("Este análisis permite explorar cómo se distribuyen las exportaciones por medios de transporte y cómo varía su valor unitario.")

    # ====================
    # Gráfico 1: Barras interactivas por transporte y régimen
    # ====================
    vias_disponibles = sorted(df["VIA_TRANSPORTE"].dropna().unique())
    vias_seleccionadas = st.multiselect("Selecciona tipos de transporte", vias_disponibles, default=vias_disponibles)

    df_filtrado = df[df["VIA_TRANSPORTE"].isin(vias_seleccionadas)]
    df_regimen = df_filtrado.groupby(["VIA_TRANSPORTE", "REGIM"]).size().reset_index(name="Cantidad")

    fig_regimen = px.bar(
        df_regimen,
        x="VIA_TRANSPORTE",
        y="Cantidad",
        color="REGIM",
        labels={"VIA_TRANSPORTE": "Medio de Transporte", "REGIM": "Régimen"},
        title="📦 Cantidad de exportaciones por tipo de transporte y régimen",
        color_continuous_scale="Blues",
        barmode="stack"
    )
    st.plotly_chart(fig_regimen, use_container_width=True)

    st.markdown("---")

        # Gráfico 2: Boxplot de valor unitario por transporte (optimizando para no crashear)
    st.markdown("## 💰 Distribución de Valor Unitario por Medio de Transporte")

    df["VALOR_UNITARIO"] = pd.to_numeric(df["VALOR_UNITARIO"], errors="coerce")
    
    # ⚠️ Filtrar outliers extremos y limitar muestra
    df_box = df[df["VALOR_UNITARIO"].notna() & (df["VALOR_UNITARIO"] < 50000)]

    # ➕ Opción para seleccionar un subconjunto aleatorio (opcional)
    df_box_sample = df_box.sample(n=3000, random_state=42) if len(df_box) > 3000 else df_box

    fig_box = px.box(
        df_box_sample,
        x="VIA_TRANSPORTE",
        y="VALOR_UNITARIO",
        color="VIA_TRANSPORTE",
        labels={"VALOR_UNITARIO": "Valor Unitario (USD)", "VIA_TRANSPORTE": "Medio de Transporte"},
        title="💰 Distribución del Valor Unitario por Medio de Transporte (Muestra 3000)",
        points="outliers"  # menos carga visual que "all"
    )
    st.plotly_chart(fig_box, use_container_width=True)


# ================================
# ✨ Pestaña 5 - Visualizaciones Avanzadas
# ================================

elif pestania == " Logística y Modalidades de Exportación":
    st.markdown("## ✨ Análisis Avanzado de Exportaciones")

    # Asegurar tipos numéricos
    df["FOBDOL_MILLONES"] = pd.to_numeric(df["FOBDOL_MILLONES"], errors="coerce")
    df["PNK"] = pd.to_numeric(df["PNK"], errors="coerce")

    # ===============================
    # GRÁFICO 1: Bubble Chart Interactivo Mejorado
    # ===============================
    st.markdown("### 🌍 Relación entre Valor FOB y Peso Neto Exportado, por País")

    df_bubble = df[(df["FOBDOL_MILLONES"] > 0) & (df["PNK"] > 0)]

    # Normalizar tamaño para visualización adaptable
    size_maximo = df_bubble["FOBDOL_MILLONES"].max()
    df_bubble["FOB_SIZE"] = df_bubble["FOBDOL_MILLONES"] / size_maximo * 100  # Escala de 0 a 100

    fig_bubble = px.scatter(
        df_bubble,
        x="FOBDOL_MILLONES",
        y="PNK",
        size="FOB_SIZE",
        color="VIA_TRANSPORTE",
        hover_name="NOMBRE_PAIS",
        labels={
            "FOBDOL_MILLONES": "Valor FOB (Millones USD)",
            "PNK": "Peso Neto Exportado (KG)",
            "VIA_TRANSPORTE": "Medio de Transporte"
        },
        title="Relación entre Valor FOB y Peso Neto Exportado (por país y medio)",
        height=600,
        template="plotly_white"
    )

    fig_bubble.update_traces(
        marker=dict(opacity=0.6, line=dict(width=1, color='DarkSlateGrey')),
        selector=dict(mode='markers')
    )
    fig_bubble.update_layout(legend_title_text='Medio de Transporte')

    st.plotly_chart(fig_bubble, use_container_width=True)

    # ==============================
    # GRÁFICO 2: Radar Chart con Fondo Claro
    # ==============================
    st.markdown("### 📡 Perfil de Exportaciones por Régimen y Medio de Transporte")

    df_radar = df[df["FOBDOL_MILLONES"] > 0]
    df_radar = df_radar.groupby(["REGIM", "VIA_TRANSPORTE"])["FOBDOL_MILLONES"].mean().reset_index()

    regimenes = df_radar["REGIM"].unique()
    fig_radar = go.Figure()

    for regimen in regimenes:
        subset = df_radar[df_radar["REGIM"] == regimen]
        fig_radar.add_trace(go.Scatterpolar(
            r=subset["FOBDOL_MILLONES"],
            theta=subset["VIA_TRANSPORTE"],
            fill='toself',
            name=f"Régimen {regimen}"
        ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, linewidth=1, showline=True)
        ),
        showlegend=True,
        template="plotly_white",
        margin=dict(t=50, l=50, r=50, b=50),
        height=600
    )

    st.plotly_chart(fig_radar, use_container_width=True)


# ================================
# 🧩 Pestaña 6 - Exportaciones por Departamento y Régimen (Sunburst)
# ================================

elif pestania == "FOB por Departamento":
    st.markdown("## 🌞 Distribución Jerárquica de Exportaciones FOB")
    st.markdown("Este gráfico muestra cómo se reparten las exportaciones por departamento y régimen.")

    df["FOBDOL_MILLONES"] = pd.to_numeric(df["FOBDOL_MILLONES"], errors="coerce")

    df_sunburst = df.groupby(["ADUANA_NOMBRE", "REGIM"])["FOBDOL_MILLONES"].sum().reset_index()

    fig_sun = px.sunburst(
        df_sunburst,
        path=["ADUANA_NOMBRE", "REGIM"],
        values="FOBDOL_MILLONES",
        color="FOBDOL_MILLONES",
        color_continuous_scale="YlOrRd",
        title="🌍 Exportaciones FOB por Departamento y Régimen",
        height=700
    )

    fig_sun.update_traces(textinfo="label+percent entry+value")
    st.plotly_chart(fig_sun, use_container_width=True)

# ================================
    # Gráfico 2: Histograma interactivo por mes
    # ================================
    st.markdown("### 📊 Distribución Mensual de Exportaciones por Departamento")

    dpto_seleccionado = st.selectbox("Selecciona un departamento", sorted(df["ADUANA_NOMBRE"].dropna().unique()))

    df_filtrado = df[df["ADUANA_NOMBRE"] == dpto_seleccionado]
    orden_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                   "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

    df_mes = df_filtrado.groupby("MES_NOMBRE")["FOBDOL_MILLONES"].sum().reindex(orden_meses).reset_index()

    fig_bar = px.bar(
        df_mes,
        x="MES_NOMBRE",
        y="FOBDOL_MILLONES",
        labels={"MES_NOMBRE": "Mes", "FOBDOL_MILLONES": "Valor FOB (Millones USD)"},
        title=f"Exportaciones mensuales desde {dpto_seleccionado}",
        color="FOBDOL_MILLONES",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# ================================
# 🧩 Pestaña 7 - País y Régimen
# ================================
elif pestania == "País y Régimen":
    st.markdown("## 🌎 Análisis Interactivo de Exportaciones por País y Régimen")

    # ========================
    # 🧹 Conversión de columnas
    # ========================
    df["FOBDOL_MILLONES"] = pd.to_numeric(df["FOBDOL_MILLONES"], errors="coerce")
    df["PNK"] = pd.to_numeric(df["PNK"], errors="coerce")
    df["POSAR"] = df["POSAR"].astype(str)

    # ===============================
    # 📊 GRÁFICO 1: Treemap Interactivo (optimizado)
    # ===============================
    st.markdown("### 🌲 Treemap Interactivo (Top 30 países)")

    df_top_paises = df.groupby("NOMBRE_PAIS")["FOBDOL_MILLONES"].sum().nlargest(30).index
    df_filtrado = df[df["NOMBRE_PAIS"].isin(df_top_paises)]

    df_treemap = df_filtrado.groupby(["NOMBRE_PAIS", "REGIM", "POSAR"])["FOBDOL_MILLONES"].sum().reset_index()

    fig_treemap = px.treemap(
        df_treemap,
        path=["NOMBRE_PAIS", "REGIM", "POSAR"],
        values="FOBDOL_MILLONES",
        color="FOBDOL_MILLONES",
        color_continuous_scale="YlGnBu",
        title="🌍 Treemap de Exportaciones FOB por País, Régimen y Producto (Top 30 países)"
    )
    fig_treemap.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig_treemap, use_container_width=True)

    st.markdown("---")

    # ===============================
    # 📈 GRÁFICO 2: Animación por Mes
    # ===============================
    st.markdown("### 📆 Animación de Exportaciones por Mes")

    df_animado = df.groupby(["FECH", "NOMBRE_PAIS"]).agg({
        "FOBDOL_MILLONES": "sum",
        "PNK": "sum",
        "POSAR": "count"
    }).reset_index().rename(columns={"POSAR": "Cantidad_Productos"})

    fig_bubble = px.scatter(
        df_animado,
        x="PNK",
        y="FOBDOL_MILLONES",
        animation_frame="FECH",
        animation_group="NOMBRE_PAIS",
        size="Cantidad_Productos",
        color="NOMBRE_PAIS",
        hover_name="NOMBRE_PAIS",
        size_max=50,
        labels={
            "PNK": "Peso Neto Exportado (KG)",
            "FOBDOL_MILLONES": "Valor FOB (Millones USD)"
        },
        title="📦 Evolución Mensual de Exportaciones por País",
        height=600
    )

    fig_bubble.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig_bubble, use_container_width=True)

# =====================================
# 🧩 Pestaña 8 - Mapa Mundial por KG
# =====================================

elif pestania == "Mapa Mundial de KG":

    st.markdown("## 🌍 Mapa Mundial de Exportaciones en Kilogramos")
    st.markdown("Este mapa muestra los países a los que se exporta desde Colombia, según el total de kilogramos (PNK) exportados. Usa códigos ISO-3 para asegurar compatibilidad geográfica.")

    # Asegurarse que la columna esté en formato numérico
    df["PNK"] = pd.to_numeric(df["PNK"], errors="coerce")

    # Agrupar por código de país ISO-3
    df_pnk = df.groupby("COD_PAI4")["PNK"].sum().reset_index()

    # Crear choropleth map interactivo
    import plotly.express as px
    fig = px.choropleth(
        df_pnk,
        locations="COD_PAI4",
        color="PNK",
        locationmode="ISO-3",  # << Aquí es clave
        color_continuous_scale="YlOrRd",
        labels={"PNK": "Kilogramos Exportados"},
        title="🌎 Mapa Mundial de Exportaciones por Peso (KG)",
        height=650
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth"
        ),
        margin=dict(t=30, l=30, r=30, b=0)
    )

    # Mostrar el mapa
    st.plotly_chart(fig, use_container_width=True)
