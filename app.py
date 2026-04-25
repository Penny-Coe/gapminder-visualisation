import streamlit as st
import plotly.express as px
import numpy as np

# -----------------------------
# Load data
# -----------------------------
df = px.data.gapminder()

# -----------------------------
# Page title
# -----------------------------
st.title("Global Health & Wealth Dashboard")

st.write(
    "This dashboard explores global inequalities in health and economic development "
    "using the Gapminder dataset."
)

# -----------------------------
# Sidebar controls
# -----------------------------
year = st.sidebar.select_slider(
    "Select Year",
    options=sorted(df["year"].unique()),
    value=2007
)

variable = st.sidebar.selectbox(
    "Select variable for map",
    ["lifeExp", "gdpPercap"]
)

filtered_df = df[df["year"] == year].copy()

# -----------------------------
# Main choropleth map
# -----------------------------
st.subheader("Global Map")

fig_map = px.choropleth(
    filtered_df,
    locations="iso_alpha",
    color=variable,
    hover_name="country",
    hover_data={
        "lifeExp": ":.1f",
        "gdpPercap": ":,.0f",
        "pop": ":,",
        "iso_alpha": False
    },
    color_continuous_scale="Viridis",
    title=f"{variable} by Country in {year}"
)

st.plotly_chart(fig_map, use_container_width=True)

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

# -----------------------------
# Health inequality hotspot map
# -----------------------------
st.subheader("Health Inequality Hotspot Map")

def classify_health_hotspot(life_exp):
    if life_exp < 60:
        return "High priority: life expectancy < 60"
    elif life_exp < 70:
        return "Moderate priority: life expectancy 60–69"
    else:
        return "Lower priority: life expectancy 70+"

filtered_df["Health Hotspot Category"] = filtered_df["lifeExp"].apply(classify_health_hotspot)

fig_hotspot = px.choropleth(
    filtered_df,
    locations="iso_alpha",
    color="Health Hotspot Category",
    hover_name="country",
    hover_data={
        "lifeExp": ":.1f",
        "gdpPercap": ":,.0f",
        "pop": ":,",
        "Health Hotspot Category": True,
        "iso_alpha": False
    },
    title=f"Health Inequality Hotspots in {year}",
    category_orders={
        "Health Hotspot Category": [
            "High priority: life expectancy < 60",
            "Moderate priority: life expectancy 60–69",
            "Lower priority: life expectancy 70+"
        ]
    }
)

st.plotly_chart(fig_hotspot, use_container_width=True)

st.write(
    "Countries are grouped into priority categories based on life expectancy. "
    "This visual helps identify areas where health outcomes may require greater attention."
)

# -----------------------------
# Animated scatter plot
# -----------------------------
st.subheader("GDP and Life Expectancy Over Time")

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
    title="GDP per Capita vs Life Expectancy Over Time",
    labels={
        "gdpPercap": "GDP per Capita",
        "lifeExp": "Life Expectancy",
        "pop": "Population",
        "continent": "Continent"
    }
)

fig_anim.update_yaxes(range=[20, 90])

st.plotly_chart(fig_anim, use_container_width=True)

# -----------------------------
# Heatmap
# -----------------------------
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

# -----------------------------
# Country trend section
# -----------------------------
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

# -----------------------------
# Simple projection
# -----------------------------
st.subheader("Projected Life Expectancy")

st.write(
    "This projection uses a simple linear trend based on historical life expectancy data. "
    "It is illustrative only and should not be interpreted as a precise forecast."
)

selected_projection_country = st.selectbox(
    "Select country for projection",
    sorted(df["country"].unique()),
    key="projection"
)

projection_df = df[df["country"] == selected_projection_country]

x = projection_df["year"]
y = projection_df["lifeExp"]

coeffs = np.polyfit(x, y, 1)
trend = np.poly1d(coeffs)

future_years = np.arange(x.min(), 2031, 1)
future_life = trend(future_years)

fig_pred = px.line(
    x=future_years,
    y=future_life,
    title=f"Projected Life Expectancy Trend: {selected_projection_country}",
    labels={"x": "Year", "y": "Life Expectancy"}
)

fig_pred.add_scatter(
    x=x,
    y=y,
    mode="markers",
    name="Actual Data"
)

st.plotly_chart(fig_pred, use_container_width=True)


