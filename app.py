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

# Heatmap: Average life expectancy by continent over time
st.subheader("Life Expectancy Trends by Continent")

heatmap_df = df.groupby(["continent", "year"])["lifeExp"].mean().reset_index()

fig_heatmap = px.imshow(
    heatmap_df.pivot(index="continent", columns="year", values="lifeExp"),
    labels=dict(x="Year", y="Continent", color="Life Expectancy"),
    title="Average Life Expectancy by Continent Over Time",
    aspect="auto",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig_heatmap, use_container_width=True)
