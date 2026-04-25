import streamlit as st
import plotly.express as px

# Load dataset
df = px.data.gapminder()

st.title("Global Health & Wealth Dashboard")

# Sidebar
year = st.sidebar.select_slider(
    "Select Year",
    options=sorted(df["year"].unique()),
    value=2007
)

variable = st.sidebar.selectbox(
    "Select Variable",
    ["lifeExp", "gdpPercap"]
)

filtered_df = df[df.year == year]

# Map
fig_map = px.choropleth(
    filtered_df,
    locations="iso_alpha",
    color=variable,
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"{variable} by Country in {year}"
)

st.plotly_chart(fig_map)

# Scatter
fig_scatter = px.scatter(
    filtered_df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    title="GDP vs Life Expectancy"
)

st.plotly_chart(fig_scatter)
