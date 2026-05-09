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
    "This dashboard follows the same visual narrative as the report: identifying global health inequality, "
    "comparing economic inequality, exploring the relationship between wealth and health, examining regional "
    "and country-level differences, and showing how patterns change over time."
)

# -----------------------------
# Create story-based tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. Health Inequality",
    "2. Economic Inequality",
    "3. Wealth & Health",
    "4. Regional & Country Differences",
    "5. Change Over Time",
    "6. Explore & Export"
])

# ============================================================
# TAB 1: HEALTH INEQUALITY
# ============================================================
with tab1:

    st.header("1. Where are health inequalities visible globally?")

    year = st.select_slider(
        "Select year",
        options=sorted(df["year"].unique()),
        value=2007,
        key="health_year"
    )

    health_df = df[df["year"] == year].copy()

    fig_life_map = px.choropleth(
        health_df,
        locations="iso_alpha",
        color="lifeExp",
        hover_name="country",
        hover_data={
            "lifeExp": ":.1f",
            "gdpPercap": ":,.0f",
            "pop": ":,",
            "continent": True,
            "iso_alpha": False
        },
        color_continuous_scale="Viridis",
        title=f"Global Life Expectancy by Country in {year}",
        labels={
            "lifeExp": "Life Expectancy",
            "gdpPercap": "GDP per Capita",
            "pop": "Population"
        }
    )

    fig_life_map.update_layout(height=650, margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig_life_map, use_container_width=True)

    st.info(
        "This map highlights global differences in life expectancy, helping identify regions with poorer health outcomes."
    )

    st.subheader("Health Inequality Hotspots")

    def classify_health_hotspot(life_exp):
        if life_exp < 60:
            return "High priority: life expectancy < 60"
        elif life_exp < 70:
            return "Moderate priority: life expectancy 60–69"
        else:
            return "Lower priority: life expectancy 70+"

    health_df["Health Hotspot Category"] = health_df["lifeExp"].apply(classify_health_hotspot)

    fig_hotspot = px.choropleth(
        health_df,
        locations="iso_alpha",
        color="Health Hotspot Category",
        hover_name="country",
        hover_data={
            "lifeExp": ":.1f",
            "gdpPercap": ":,.0f",
            "pop": ":,",
            "continent": True,
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

    fig_hotspot.update_layout(height=650, margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig_hotspot, use_container_width=True)


# ============================================================
# TAB 2: ECONOMIC INEQUALITY
# ============================================================
with tab2:

    st.header("2. Are economic inequalities visible in the same places?")

    year = st.select_slider(
        "Select year",
        options=sorted(df["year"].unique()),
        value=2007,
        key="economic_year"
    )

    econ_df = df[df["year"] == year].copy()

    fig_gdp_map = px.choropleth(
        econ_df,
        locations="iso_alpha",
        color="gdpPercap",
        hover_name="country",
        hover_data={
            "lifeExp": ":.1f",
            "gdpPercap": ":,.0f",
            "pop": ":,",
            "continent": True,
            "iso_alpha": False
        },
        color_continuous_scale="Viridis",
        title=f"Global GDP per Capita by Country in {year}",
        labels={
            "gdpPercap": "GDP per Capita",
            "lifeExp": "Life Expectancy",
            "pop": "Population"
        }
    )

    fig_gdp_map.update_layout(height=650, margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig_gdp_map, use_container_width=True)

    st.info(
        "This map allows economic inequality to be compared with the life expectancy patterns shown in the previous tab."
    )


# ============================================================
# TAB 3: WEALTH AND HEALTH RELATIONSHIP
# ============================================================
with tab3:

    st.header("3. Is there a relationship between wealth and health?")

    relationship_year = st.select_slider(
        "Select year",
        options=sorted(df["year"].unique()),
        value=2007,
        key="relationship_year"
    )

    rel_df = df[df["year"] == relationship_year].copy()

    fig_scatter = px.scatter(
        rel_df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=120,
        trendline="ols",
        trendline_scope="overall",
        title=f"GDP per Capita vs Life Expectancy in {relationship_year}",
        labels={
            "gdpPercap": "GDP per Capita",
            "lifeExp": "Life Expectancy",
            "pop": "Population",
            "continent": "Continent"
        }
    )

    fig_scatter.update_xaxes(
        type="log",
        tickvals=[1000, 5000, 10000, 50000, 100000],
        ticktext=["1k", "5k", "10k", "50k", "100k"],
        title="GDP per Capita (log scale)"
    )

    fig_scatter.update_yaxes(title="Life Expectancy")
    fig_scatter.update_traces(opacity=0.7, marker=dict(sizemin=6))
    fig_scatter.update_layout(height=650, margin=dict(l=0, r=0, t=50, b=0))

    st.plotly_chart(fig_scatter, use_container_width=True)

    correlation = rel_df["gdpPercap"].corr(rel_df["lifeExp"])

    st.metric(
        "Correlation between GDP per capita and life expectancy",
        f"{correlation:.2f}"
    )

    st.info(
        "The scatter plot and correlation value show whether higher GDP per capita is associated with higher life expectancy."
    )


# ============================================================
# TAB 4: REGIONAL AND COUNTRY DIFFERENCES
# ============================================================
with tab4:

    st.header("4. Is the relationship the same across regions and countries?")

    region_year = st.select_slider(
        "Select year",
        options=sorted(df["year"].unique()),
        value=2007,
        key="region_year"
    )

    region_df = df[df["year"] == region_year].copy()
    region_df["log_gdpPercap"] = np.log(region_df["gdpPercap"])

    st.subheader("Regional Differences")

    fig_box_life = px.box(
        region_df,
        x="continent",
        y="lifeExp",
        color="continent",
        title=f"Life Expectancy by Continent in {region_year}",
        labels={"lifeExp": "Life Expectancy", "continent": "Continent"}
    )

    fig_box_life.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_box_life, use_container_width=True)

    fig_box_gdp = px.box(
        region_df,
        x="continent",
        y="log_gdpPercap",
        color="continent",
        title=f"Log GDP per Capita by Continent in {region_year}",
        labels={"log_gdpPercap": "Log GDP per Capita", "continent": "Continent"}
    )

    fig_box_gdp.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_box_gdp, use_container_width=True)

    st.subheader("Country-Level Rankings")

    ranking_variable = st.selectbox(
        "Select ranking variable",
        ["lifeExp", "gdpPercap", "pop"],
        key="ranking_variable_story"
    )

    top_10 = region_df.nlargest(10, ranking_variable)
    bottom_10 = region_df.nsmallest(10, ranking_variable)

    col1, col2 = st.columns(2)

    with col1:
        fig_top = px.bar(
            top_10.sort_values(ranking_variable),
            x=ranking_variable,
            y="country",
            orientation="h",
            title=f"Top 10 Countries by {ranking_variable} in {region_year}",
            hover_data=["continent", "lifeExp", "gdpPercap", "pop"]
        )
        fig_top.update_layout(height=500)
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        fig_bottom = px.bar(
            bottom_10.sort_values(ranking_variable, ascending=False),
            x=ranking_variable,
            y="country",
            orientation="h",
            title=f"Bottom 10 Countries by {ranking_variable} in {region_year}",
            hover_data=["continent", "lifeExp", "gdpPercap", "pop"]
        )
        fig_bottom.update_layout(height=500)
        st.plotly_chart(fig_bottom, use_container_width=True)


# ============================================================
# TAB 5: CHANGE OVER TIME
# ============================================================
with tab5:

    st.header("5. How have these patterns changed over time?")

    st.subheader("Animated Scatter Plot")

    fig_anim = px.scatter(
        df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        animation_frame="year",
        animation_group="country",
        size_max=120,
        title="GDP per Capita vs Life Expectancy Over Time",
        labels={
            "gdpPercap": "GDP per Capita",
            "lifeExp": "Life Expectancy",
            "pop": "Population",
            "continent": "Continent"
        }
    )

    fig_anim.update_traces(marker=dict(sizemin=6), opacity=0.7)
    fig_anim.update_yaxes(range=[20, 90])
    fig_anim.update_layout(height=650, margin=dict(l=0, r=0, t=50, b=0))

    st.plotly_chart(fig_anim, use_container_width=True)

    st.subheader("Average Life Expectancy by Continent Over Time")

    life_heatmap_df = df.groupby(["continent", "year"])["lifeExp"].mean().reset_index()

    fig_life_heatmap = px.imshow(
        life_heatmap_df.pivot(index="continent", columns="year", values="lifeExp"),
        labels=dict(x="Year", y="Continent", color="Life Expectancy"),
        title="Average Life Expectancy by Continent Over Time",
        aspect="auto",
        color_continuous_scale="Viridis",
        text_auto=True
    )

    fig_life_heatmap.update_layout(height=500)
    st.plotly_chart(fig_life_heatmap, use_container_width=True)

    st.subheader("Country Trends")

    selected_country = st.selectbox(
        "Select country to view trend",
        sorted(df["country"].unique()),
        key="country_trend_story"
    )

    country_df = df[df["country"] == selected_country].copy()

    col1, col2 = st.columns(2)

    with col1:
        fig_life_trend = px.line(
            country_df,
            x="year",
            y="lifeExp",
            markers=True,
            title=f"Life Expectancy Over Time: {selected_country}",
            labels={"lifeExp": "Life Expectancy", "year": "Year"}
        )
        st.plotly_chart(fig_life_trend, use_container_width=True)

    with col2:
        fig_gdp_trend = px.line(
            country_df,
            x="year",
            y="gdpPercap",
            markers=True,
            title=f"GDP per Capita Over Time: {selected_country}",
            labels={"gdpPercap": "GDP per Capita", "year": "Year"}
        )
        st.plotly_chart(fig_gdp_trend, use_container_width=True)


# ============================================================
# TAB 6: EXPLORE AND EXPORT
# ============================================================
with tab6:

    st.header("6. Explore and Export Data")

    st.write(
        "Use this section to explore the dataset directly and export selected rankings."
    )

    export_year = st.select_slider(
        "Select year",
        options=sorted(df["year"].unique()),
        value=2007,
        key="export_year"
    )

    export_variable = st.selectbox(
        "Select variable",
        ["lifeExp", "gdpPercap", "pop"],
        key="export_variable"
    )

    export_df = df[df["year"] == export_year].copy()

    ranking_table = export_df.sort_values(
        export_variable,
        ascending=False
    )[["country", "continent", "year", "lifeExp", "gdpPercap", "pop"]]

    ranking_table = ranking_table.reset_index(drop=True)
    ranking_table.index = ranking_table.index + 1

    st.dataframe(ranking_table, use_container_width=True)

    st.download_button(
        label="Download ranking table as CSV",
        data=ranking_table.to_csv(index=True),
        file_name=f"country_rankings_{export_variable}_{export_year}.csv",
        mime="text/csv"
    )
