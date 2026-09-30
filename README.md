# 🇨🇴 Dashboard Interactivo de Exportaciones de Colombia

Proyecto de análisis y visualización de datos desarrollado en **Python y Streamlit**
para explorar el comportamiento de las exportaciones colombianas mediante un
dashboard interactivo.

La aplicación permite analizar información relacionada con **países de destino,
valor FOB, peso neto exportado, medios de transporte, régimen de exportación,
aduanas, productos y evolución temporal**, utilizando diferentes técnicas de
análisis y visualización de datos.

---

## 🛠️ Tecnologías utilizadas

- Python
- Pandas
- Streamlit
- Plotly
- Matplotlib
- Seaborn
- OpenPyXL
- Requests

---

## 🎯 Objetivo del proyecto

El objetivo principal fue desarrollar una herramienta de **Business Intelligence
y análisis exploratorio de datos** que permitiera transformar información de
exportaciones colombianas en visualizaciones interactivas y métricas fáciles de
interpretar.

El dashboard permite explorar los datos desde diferentes perspectivas,
facilitando la identificación de tendencias, patrones geográficos, comportamiento
por país y diferencias según los medios de transporte y regímenes de exportación.

---

## 📥 Carga y procesamiento de datos

Los datos son cargados dinámicamente desde una fuente externa mediante Python.

Durante el procesamiento se realizan tareas como:

- Carga de archivos Excel mediante Pandas.
- Conversión y validación de variables numéricas.
- Filtrado de observaciones.
- Agrupación y agregación de información.
- Tratamiento de valores utilizados en las visualizaciones.
- Preparación de variables geográficas.
- Organización temporal de los datos.
- Optimización de muestras para visualizaciones de gran volumen.

---

## 📊 Dashboard interactivo

La aplicación fue desarrollada en **Streamlit** y está organizada mediante un
panel de navegación que permite acceder a diferentes módulos de análisis.

### 1. 📈 Resumen General

Presenta indicadores principales del conjunto de datos:

- Número total de registros.
- Número de países de destino.
- Año más reciente disponible.
- Ranking de los principales países según número de exportaciones.

---

### 2. 🌍 Comparativo por País

Permite seleccionar dinámicamente un país y analizar:

- Evolución del valor FOB a través del tiempo.
- Exportaciones por año.
- Relación entre peso neto exportado y valor FOB.
- Comparación mediante gráficos interactivos.

---

### 3. 🗺️ Análisis Geográfico

Se desarrollaron mapas interactivos para representar la distribución internacional
de las exportaciones colombianas.

Incluye:

- Mapa mundial según valor FOB.
- Ubicación geográfica mediante latitud y longitud.
- Evolución mensual animada de las exportaciones.
- Comparación entre países de destino.

---

### 4. 🚢 Transporte y Régimen

Análisis de las exportaciones según los diferentes medios de transporte y
regímenes utilizados.

Incluye:

- Selección interactiva de medios de transporte.
- Cantidad de exportaciones por transporte y régimen.
- Distribución del valor unitario mediante boxplots.
- Tratamiento de valores extremos para mejorar la interpretación.

---

### 5. ✨ Logística y Modalidades de Exportación

Análisis avanzado de la relación entre:

- Valor FOB.
- Peso neto exportado.
- País de destino.
- Medio de transporte.
- Régimen de exportación.

Se utilizaron **Bubble Charts y Radar Charts interactivos** para representar
diferentes dimensiones de los datos.

---

### 6. ☀️ Exportaciones FOB por Departamento

Análisis jerárquico de las exportaciones mediante:

- Diagramas Sunburst.
- Valor FOB por aduana/departamento.
- Régimen de exportación.
- Evolución mensual.
- Comparaciones mediante filtros interactivos.

---

### 7. 🌲 País, Régimen y Producto

Se desarrolló un **Treemap interactivo** para analizar conjuntamente:

- País de destino.
- Régimen.
- Producto.
- Valor FOB.

Además, se construyó una visualización animada para estudiar la evolución de las
exportaciones según peso neto, valor FOB y cantidad de productos.

---

### 8. 🌎 Mapa Mundial por Peso Exportado

Se desarrolló un mapa mundial tipo **choropleth** utilizando códigos ISO-3 para
representar los países de destino según el total de kilogramos exportados desde
Colombia.

---

## 📈 Visualizaciones desarrolladas

Durante el proyecto se implementaron diferentes técnicas de visualización:

- Gráficos de barras.
- Gráficos de líneas.
- Scatter plots.
- Bubble charts.
- Boxplots.
- Radar charts.
- Sunburst charts.
- Treemaps.
- Mapas geográficos interactivos.
- Choropleth maps.
- Visualizaciones animadas.

Todas las visualizaciones principales fueron desarrolladas de forma interactiva
mediante **Plotly y Streamlit**.

---

## 💡 Habilidades aplicadas

Este proyecto demuestra experiencia práctica en:

- Análisis de datos con Python.
- Manipulación de datos con Pandas.
- Análisis exploratorio de datos (EDA).
- Transformación y preparación de datos.
- Agrupación y agregación de información.
- Desarrollo de dashboards.
- Business Intelligence.
- Visualización interactiva de datos.
- Análisis geográfico.
- Análisis temporal.
- Desarrollo de aplicaciones analíticas con Streamlit.
- Interpretación y comunicación de resultados.

---

## 📁 Estructura del proyecto

### `exportaciones.py`

Archivo principal de la aplicación. Contiene la carga y procesamiento de los datos,
la navegación del dashboard y las diferentes visualizaciones interactivas.

### `exportaciones/`

Carpeta que contiene recursos utilizados durante el desarrollo del proyecto.

### `requirements.txt`

Contiene las dependencias necesarias para ejecutar la aplicación.

---

## 🚀 Cómo ejecutar el proyecto

Clonar el repositorio:

    git clone https://github.com/willercanonarvaez/Exportaciones-Colombia.git

Instalar las dependencias:

    pip install -r requirements.txt

Ejecutar la aplicación:

    streamlit run exportaciones.py

---

## 👨‍💻 Autor

**Willer Cano Narváez**

Profesional en Estadística y estudiante del Máster en Análisis de Datos e
Inteligencia de Negocios en la Universidad Complutense de Madrid.

Proyecto desarrollado como parte de mi portafolio profesional en **Data Analytics,
Business Intelligence y visualización de datos**.
