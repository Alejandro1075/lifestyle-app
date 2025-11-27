import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carga del CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# 1. Cargar dataset
st.title("Lifestyle Analytics Dashboard")
st.write("Dashboard de análisis de estilo de vida, salud y actividad física.")

uploaded_file = "Final_data.csv"
try:
    data = pd.read_csv(uploaded_file)
except FileNotFoundError:
    st.error("❌ No se encontró 'Final_data.csv'. Coloca el archivo junto a app.py.")
    st.stop()


# 2. Filtros
st.subheader("🎚 Filtros")
f1, f2, f3 = st.columns(3)

with f1:
    gender_filter = st.multiselect(
        "Género:",
        options=data["Gender"].dropna().unique(),
        default=data["Gender"].dropna().unique()
    )

with f2:
    difficulty_filter = st.multiselect(
        "Dificultad:",
        options=data["Difficulty Level"].dropna().unique(),
        default=data["Difficulty Level"].dropna().unique()
    )

with f3:
    bodypart_filter = st.multiselect(
        "Parte del cuerpo:",
        options=data["Body Part"].dropna().unique(),
        default=data["Body Part"].dropna().unique()
    )

filtered = data[
    (data["Gender"].isin(gender_filter)) &
    (data["Difficulty Level"].isin(difficulty_filter)) &
    (data["Body Part"].isin(bodypart_filter))
]


# 3. Vista previa
st.subheader("📄 Vista Previa del Dataset")
st.dataframe(data.head())

st.subheader("📊 Resumen estadístico")
st.write(data.describe(include='all'))


# 4. KPI's
st.subheader("🏅 Indicadores Principales del Estilo de Vida")
col1, col2, col3, col4 = st.columns(4)

if "Calories_Burned" in data.columns:
    col1.metric("🔥 Calorías Promedio", f"{data['Calories_Burned'].mean():.1f}")

if "BMI_calc" in data.columns:
    col2.metric("⚖️ IMC Promedio", f"{data['BMI_calc'].mean():.1f}")

if "Avg_BPM" in data.columns:
    col3.metric("❤️ BPM Promedio", f"{data['Avg_BPM'].mean():.1f}")

if "Session_Duration (hours)" in data.columns:
    col4.metric("⏱ Duración Promedio (hrs)", f"{data['Session_Duration (hours)'].mean():.2f}")


# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Histograma BMI",
    "📙 Boxplot Calories",
    "📗 Tiempo Cocción",
    "📕 Top 10 Ejercicios"
])

# Tab 1
with tab1:
    st.markdown('<div class="tab-bg">', unsafe_allow_html=True)
    st.write("### Histograma de BMI")

    if "BMI_calc" in filtered.columns:
        fig, ax = plt.subplots()
        fig.patch.set_facecolor("#E8E2DB")
        ax.set_facecolor("#E8E2DB")

        ax.hist(
            filtered["BMI_calc"].dropna(),
            bins=20,
            edgecolor="black",
            color="#E25439"
        )

        ax.set_xlabel("BMI")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)


# Tab 2
with tab2:
    st.markdown('<div class="tab-bg">', unsafe_allow_html=True)
    st.write("### Boxplot de Calorías por Tipo de Ejercicio")

    if "Workout_Type" in filtered.columns and "Calories_Burned" in filtered.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor("#E8E2DB")
        ax.set_facecolor("#E8E2DB")

        filtered.boxplot(
            column="Calories_Burned",
            by="Workout_Type",
            ax=ax,
            boxprops=dict(color="#E25439"),
            medianprops=dict(color="black"),
            whiskerprops=dict(color="#E25439"),
            capprops=dict(color="#E25439")
        )

        ax.set_xlabel("Workout Type")
        ax.set_ylabel("Calories Burned")
        plt.suptitle("")
        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)


# Tab 3
with tab3:
    st.markdown('<div class="tab-bg">', unsafe_allow_html=True)
    st.write("### Tiempo Promedio por Método de Cocción")

    if "cooking_method" in filtered.columns and "cook_time_min" in filtered.columns:
        prep_avg = filtered.groupby("cooking_method")["cook_time_min"].mean().sort_values()

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor("#E8E2DB")
        ax.set_facecolor("#E8E2DB")

        ax.bar(prep_avg.index, prep_avg.values, color="#E25439", edgecolor="black")
        plt.xticks(rotation=45)

        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)


# Tab 4
with tab4:
    st.markdown('<div class="tab-bg">', unsafe_allow_html=True)
    st.write("### 🔥 Top 10 Ejercicios")

    if "Name of Exercise" in filtered.columns and "Calories_Burned" in filtered.columns:
        top10 = (
            filtered.groupby("Name of Exercise")["Calories_Burned"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )

        st.table(top10.reset_index().rename(columns={"Calories_Burned": "Avg Calories"}))

    st.markdown("</div>", unsafe_allow_html=True)


# 6. Descargar datos filtrados
st.markdown('<div class="download-box">', unsafe_allow_html=True)
st.download_button(
    "⬇️ Descargar datos filtrados",
    data=filtered.to_csv(index=False).encode('utf-8'),
    file_name="filtered_lifestyle_data.csv",
    mime="text/csv"
)
st.markdown("</div>", unsafe_allow_html=True)
