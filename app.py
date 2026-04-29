# -----------------------------
# Import libraries
# -----------------------------
import streamlit as st
import plotly.express as px
import numpy as np

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Global Health & Wealth Dashboard",
    layout="wide"
)

# -----------------------------
# Load data
# -----------------------------
df = px.data.gapminder()

# -----------------------------
# Dashboard title and introduction
# -----------------------------
st.title("Global Health & Wealth Dashboard")

st.write(
    "This dashboard explores global inequalities in health and economic development "
    "using the Gapminder dataset. It allows users to compare life expectancy, GDP per capita, "
    "population patterns and projected health trends across countries and continents."
)

# -----------------------------
# Create dashboard tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Global Maps",
    "Trends Over Time",
    "Projection",
     "Country Rankings"
])

# ============================================================
# TAB 1: GLOBAL MAPS
# ============================================================
with tab1:

    st.header("Global Overview")

    st.write(
        "Use the controls below to explore global patterns in life expectancy and GDP per capita."
    )

    # -----------------------------
    # Controls for global maps
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        year = st.select_slider(
            "Select year",
            options=sorted(df["year"].unique()),
            value=2007
        )

    with col2:
        variable = st.selectbox(
            "Select variable for map",
            ["lifeExp", "gdpPercap"]
        )

    with col3:
        selected_country = st.selectbox(
            "Search/select a country",
            ["All countries"] + sorted(df["country"].unique())
        )

    # -----------------------------
    # Filter data
    # -----------------------------
    filtered_df = df[df["year"] == year].copy()

    if selected_country != "All countries":
        filtered_df = filtered_df[filtered_df["country"] == selected_country]

    # -----------------------------
    # KPI summary cards
    # -----------------------------
    avg_life = filtered_df["lifeExp"].mean()
    avg_gdp = filtered_df["gdpPercap"].mean()
    total_pop = filtered_df["pop"].sum()

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric("Average Life Expectancy", f"{avg_life:.1f} years")
    kpi2.metric("Average GDP per Capita", f"${avg_gdp:,.0f}")
    kpi3.metric("Total Population", f"{total_pop:,.0f}")

    # -----------------------------
    # Main choropleth map
    # -----------------------------
    st.subheader("Global Overview Map")

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

    fig_map.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig_map, use_container_width=True)

    # -----------------------------
    # Health inequality hotspot map
    # -----------------------------
    st.subheader("Health Inequality Hotspot Map")

    st.write(
        "This map groups countries into priority categories based on life expectancy. "
        "It helps identify countries where health outcomes may require greater attention."
    )

    def classify_health_hotspot(life_exp):
        if life_exp < 60:
            return "High priority: life expectancy < 60"
        elif life_exp < 70:
            return "Moderate priority: life expectancy 60–69"
        else:
            return "Lower priority: life expectancy 70+"

    filtered_df["Health Hotspot Category"] = filtered_df["lifeExp"].apply(
        classify_health_hotspot
    )

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

    fig_hotspot.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig_hotspot, use_container_width=True)


# ============================================================
# TAB 2: TRENDS OVER TIME
# ============================================================
with tab2:

    st.header("Trends Over Time")

    st.write(
        "This section explores how GDP per capita and life expectancy have changed over time."
    )

    # -----------------------------
    # Animated scatter plot
    # -----------------------------
    st.subheader("GDP per Capita and Life Expectancy Over Time")

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

    fig_anim.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig_anim, use_container_width=True)

    # -----------------------------
    # Heatmap
    # -----------------------------
    st.subheader("Average Life Expectancy by Continent")

    heatmap_df = df.groupby(["continent", "year"])["lifeExp"].mean().reset_index()

    fig_heatmap = px.imshow(
        heatmap_df.pivot(
            index="continent",
            columns="year",
            values="lifeExp"
        ),
        labels=dict(
            x="Year",
            y="Continent",
            color="Life Expectancy"
        ),
        title="Average Life Expectancy by Continent Over Time",
        aspect="auto",
        color_continuous_scale="Viridis"
    )

    fig_heatmap.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # -----------------------------
    # Country trend section
    # -----------------------------
    st.subheader("Country Trend Over Time")

    selected_trend_country = st.selectbox(
        "Select a country to view its trend",
        sorted(df["country"].unique()),
        key="trend_country"
    )

    country_df = df[df["country"] == selected_trend_country]

    col1, col2 = st.columns(2)

    with col1:
        fig_life = px.line(
            country_df,
            x="year",
            y="lifeExp",
            markers=True,
            title=f"Life Expectancy Over Time: {selected_trend_country}",
            labels={
                "lifeExp": "Life Expectancy",
                "year": "Year"
            }
        )

        fig_life.update_layout(height=450)
        st.plotly_chart(fig_life, use_container_width=True)

    with col2:
        fig_gdp = px.line(
            country_df,
            x="year",
            y="gdpPercap",
            markers=True,
            title=f"GDP per Capita Over Time: {selected_trend_country}",
            labels={
                "gdpPercap": "GDP per Capita",
                "year": "Year"
            }
        )

        fig_gdp.update_layout(height=450)
        st.plotly_chart(fig_gdp, use_container_width=True)


# ============================================================
# TAB 3: PROJECTION
# ============================================================
with tab3:

    st.header("Projected Life Expectancy")

    st.write(
        "This section uses a simple linear trend based on historical life expectancy data. "
        "The projection is illustrative only and should not be interpreted as a precise forecast."
    )

    selected_projection_country = st.selectbox(
        "Select country for projection",
        sorted(df["country"].unique()),
        key="projection_country"
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
        labels={
            "x": "Year",
            "y": "Life Expectancy"
        }
    )

    fig_pred.add_scatter(
        x=x,
        y=y,
        mode="markers",
        name="Actual Data"
    )

    fig_pred.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    st.plotly_chart(fig_pred, use_container_width=True)

    projected_2030 = trend(2030)

    st.metric(
        label=f"Projected life expectancy in 2030 for {selected_projection_country}",
        value=f"{projected_2030:.1f} years"
    )

# ============================================================
# TAB 4: COUNTRY RANKINGS
# ============================================================
with tab4:

    st.header("Country Rankings")

    st.write(
        "This section ranks countries by life expectancy, GDP per capita or population. "
        "Use the year slider to see how the rankings change over time."
    )

    # -----------------------------
    # Ranking controls
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        ranking_year = st.select_slider(
            "Select year for ranking",
            options=sorted(df["year"].unique()),
            value=2007,
            key="ranking_year"
        )

    with col2:
        ranking_variable = st.selectbox(
            "Select variable for ranking",
            ["lifeExp", "gdpPercap", "pop"],
            key="ranking_variable"
        )

    # -----------------------------
    # Filter data for selected year
    # -----------------------------
    ranking_df = df[df["year"] == ranking_year].copy()

    # -----------------------------
    # Create top and bottom 10 datasets
    # -----------------------------
    top_10 = ranking_df.nlargest(10, ranking_variable)
    bottom_10 = ranking_df.nsmallest(10, ranking_variable)

    # -----------------------------
    # Display top and bottom 10 side by side
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        fig_top = px.bar(
            top_10.sort_values(ranking_variable),
            x=ranking_variable,
            y="country",
            orientation="h",
            title=f"Top 10 Countries by {ranking_variable} in {ranking_year}",
            hover_data={
                "lifeExp": ":.1f",
                "gdpPercap": ":,.0f",
                "pop": ":,",
                "continent": True
            },
            labels={
                "country": "Country",
                "lifeExp": "Life Expectancy",
                "gdpPercap": "GDP per Capita",
                "pop": "Population"
            }
        )

        fig_top.update_layout(height=550)
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        fig_bottom = px.bar(
            bottom_10.sort_values(ranking_variable, ascending=False),
            x=ranking_variable,
            y="country",
            orientation="h",
            title=f"Bottom 10 Countries by {ranking_variable} in {ranking_year}",
            hover_data={
                "lifeExp": ":.1f",
                "gdpPercap": ":,.0f",
                "pop": ":,",
                "continent": True
            },
            labels={
                "country": "Country",
                "lifeExp": "Life Expectancy",
                "gdpPercap": "GDP per Capita",
                "pop": "Population"
            }
        )

        fig_bottom.update_layout(height=550)
        st.plotly_chart(fig_bottom, use_container_width=True)

    # -----------------------------
    # Ranking table
    # -----------------------------
    st.subheader("Full Ranking Table")

    ranking_table = ranking_df.sort_values(
        ranking_variable,
        ascending=False
    )[["country", "continent", "year", "lifeExp", "gdpPercap", "pop"]]

    ranking_table = ranking_table.reset_index(drop=True)
    ranking_table.index = ranking_table.index + 1

    st.dataframe(
        ranking_table,
        use_container_width=True
    )
