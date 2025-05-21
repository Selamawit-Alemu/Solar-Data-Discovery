import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import streamlit as st

def load_cleaned_data(countries):
    data_frames = []
    for country in countries:
        file_path = f"../notebooks/data/{country.lower()}_clean.csv"
        print(f"Trying to load: {file_path}")  # Debug print
        if not os.path.exists(file_path):
            print(f"Missing file: {file_path}")
            continue
        try:
            df = pd.read_csv(file_path)
            df["Country"] = country
            data_frames.append(df)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue

    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        print("No data loaded. Please check your data files in the data folder.")
        return None


def plot_ghi_boxplot(df):
    """
    Display a Seaborn boxplot for GHI by Country inside Streamlit.
    """
    if df.empty:
        return
    
    # Create the figure and axes
    fig, ax = plt.subplots()

    # Draw your plot on this axis
    sns.boxplot(data=df, x='Country', y='GHI', ax=ax)

    # Display the plot in Streamlit safely
    st.pyplot(fig)


def plot_bubble_chart(df):
    """
    Plot an interactive bubble chart of GHI vs Tamb with size by RH or BP using Plotly.
    """
    size_col = None
    if 'RH' in df.columns:
        size_col = 'RH'
    elif 'BP' in df.columns:
        size_col = 'BP'

    if 'GHI' in df.columns and 'Tamb' in df.columns and size_col:
        fig = px.scatter(df, x='Tamb', y='GHI', size=size_col,
                         color='Country' if 'Country' in df.columns else None,
                         title='GHI vs Temperature Bubble Chart',
                         labels={'Tamb':'Ambient Temperature (°C)', 'GHI':'Global Horizontal Irradiance (W/m²)'},
                         size_max=30)
        st.plotly_chart(fig)

def summary_stats(df, metrics):
    """
    Create a summary DataFrame showing mean, median, std for specified metrics grouped by Country.
    """
    if df.empty:
        return pd.DataFrame()
    summary = df.groupby('Country')[metrics].agg(['mean', 'median', 'std']).round(2)
    summary.columns = ['_'.join(col) for col in summary.columns]
    return summary.reset_index()

def anova_test(df):
    """
    Perform one-way ANOVA test on GHI across countries and return p-value.
    """
    from scipy.stats import f_oneway

    groups = [group['GHI'].dropna().values for name, group in df.groupby('Country')]
    if len(groups) < 2:
        return None
    stat, pval = f_oneway(*groups)
    return pval
