import os
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Estudio de la natalidad de US en 1967 - 1988")

@st.cache_data
def load_data(file_path):
  try:
    df = pd.read_csv(file_path)
    df.drop(columns=['date', 'rownames'], inplace=True)
    return df
  except FileNotFoundError:
    st.error("El archivo no no ha sido encontrado")

df = load_data(os.curdir + '/Birthdays.csv')

st.title("Estudio de la natalidad de US en 1967 - 1988")

with st.sidebar:
    st.header("Opciones de visualización")

    filtered_state = st.multiselect("Estados a incluir:", options=df['state'].unique(
    ), key='selected_states', placeholder="Seleccione un estado")
    if filtered_state:
        filtered_df = df.query("@filtered_state in state")
    else:
        filtered_df = df

    # Año
    filtered_year_start, filtered_year_end = st.slider(
        "Años a incluir",
        value=(min(df['year'].unique()), max(df['year'].unique())),
        min_value=min(df['year'].unique()),
        max_value=max(df['year'].unique())
    )
    filtered_df = filtered_df.query(
        "@filtered_year_start <= year and @filtered_year_end >= year")
    enable_date_filter = st.checkbox("Habilitar busqueda por fecha")
    if enable_date_filter:

        # Mes
        filtered_month_start, filtered_month_end = st.slider(
            "Mes a incluir",
            value=(min(df['month'].unique()), max(df['month'].unique())),
            min_value=min(df['month'].unique()),
            max_value=max(df['month'].unique())
        )
        filtered_df = filtered_df.query(
            "@filtered_month_start <= month and @filtered_month_end >= month")
        # Dia
        filtered_day_start, filtered_year_end = st.slider(
            "Dias a incluir",
            value=(min(df['day'].unique()), max(df['day'].unique())),
            min_value=min(df['day'].unique()),
            max_value=max(df['day'].unique())
        )
        filtered_df = filtered_df.query(
            "@filtered_day_start <= day and @filtered_year_end >= day")

        # Dia semana
        filtered_weekday = st.multiselect(
            "Seleccione el dia de la semana", options=df['wday'].unique())
        if filtered_weekday:
            filtered_df = filtered_df.query(
                "@filtered_weekday in wday"
            )


tab1, tab2 = st.tabs(["Resumen general", "Tabla de datos"])
with tab1:
    st.markdown("### Número total de nacimientos por estado")
    mean_birth = round(filtered_df['births'].mean(), 2)
    total_state = len(filtered_df['state'].unique())

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total de estados", total_state)

    with col2:
        st.metric("Media de nacimientos", mean_birth)

    birth_over_year = filtered_df.groupby(
        "year")["births"].mean().reset_index()
    fig, ax = plt.subplots()
    ax.plot(birth_over_year['year'], birth_over_year['births'], marker='o')
    ax.set_title("Tendencia de natalidad")
    ax.set_xlabel("Año")
    ax.set_ylabel("Media de nacimientos")
    ax.grid()

    st.pyplot(fig)

    # st.line_chart(data=birth_over_year, x='year', y='births')


with tab2:
    st.markdown("### Tabla")
    st.dataframe(filtered_df)
