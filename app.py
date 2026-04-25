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

fig_anim = px.scatter(
    df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
    animation_frame="year",
    animation_group="country",
    title="GDP vs Life Expectancy Over Time"
)

fig_anim.update_yaxes(range=[20, 90])  # <-- FIX HERE

st.plotly_chart(fig_anim, use_container_width=True)

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

st.subheader("Country Trend Over Time")

selected_country = st.selectbox(
    "Select a country",
    sorted(df["country"].unique())
)

country_df = df[df["country"] == selected_country]

fig_life = px.line(
    country_df,
    x="year",
    y="lifeExp",
    markers=True,
    title=f"Life Expectancy Over Time: {selected_country}",
    labels={"lifeExp": "Life Expectancy", "year": "Year"}
)

st.plotly_chart(fig_life, use_container_width=True)

fig_gdp = px.line(
    country_df,
    x="year",
    y="gdpPercap",
    markers=True,
    title=f"GDP per Capita Over Time: {selected_country}",
    labels={"gdpPercap": "GDP per Capita", "year": "Year"}
)

st.plotly_chart(fig_gdp, use_container_width=True)

st.subheader("Global Development Over Time (Animated)")


