# Gapminder Visualisation Dashboard
This project explores global health and wealth inequalities using the Gapminder dataset. It investigates the relationship between GDP per capita, life expectancy, population size, continent and time using interactive data visualisation techniques.

## Project Aim
The aim of this project is to use data visualisation to identify global patterns of inequality and explore whether economic development is associated with health outcomes.

## Dataset
The project uses the Gapminder dataset, accessed through the Plotly library. The dataset contains country-level data for:

- Country
- Continent
- Year
- Life expectancy
- GDP per capita
- Population

## Tools and Libraries
The analysis was completed using:
- Python
- Google Colab
- pandas
- NumPy
- Plotly
- Streamlit

## Visualisations Included
The project includes:
- Choropleth maps of life expectancy and GDP per capita
- Scatter plots showing the relationship between GDP per capita and life expectancy
- Correlation matrix
- Boxplots comparing continents
- Ranking charts
- Time-series line charts
- Heatmaps
- Animated scatter plot
- Interactive Streamlit dashboard

## How to Run the Project

#### Option 1: Open Google Colab using link from the report or below. Run the cells from top to bottom. The notebook contains the full data loading, preprocessing, visualisation code and output results.
https://colab.research.google.com/drive/1YOQ6Z9rLcg7TZl1LBVRGw63IzWdq6WuF

#### Option 2: Streamlit Dashboard
The interactive dashboard can be accessed using the Streamlit link provided in the report (also below).
https://gapminder-visualisation-2026.streamlit.app/

#### Option 3: Run Locally
Clone this repository:

```bash
git clone https://github.com/Penny-Coe/gapminder-visualisation.git
cd gapminder-visualisation
```

### Install the required packages:

```bash
pip install pandas numpy plotly streamlit
```

### Run the dashboard:

```bash
streamlit run app.py
```

```text
gapminder-visualisation/
│
├── app.py                 # Streamlit dashboard
├── README.md              # Project documentation
├── requirements.txt       # Package dependencies
└── notebooks/
    └── gapminder_analysis.ipynb
```

## Reproducibility

The Google Colab notebook included in this repository contains the full executed code, preprocessing steps, visualisation generation and output results. The Streamlit dashboard provides an interactive version of the main visualisations presented in the report.

## Author

Penny Coe
DSC6002M Data Visualisation
