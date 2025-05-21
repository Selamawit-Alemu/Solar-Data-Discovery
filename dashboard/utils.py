import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import streamlit as st
from scipy.stats import f_oneway
from typing import List, Optional, Union

def load_cleaned_data(countries):
    data_frames = []
    data_folder = "../data"  # Make this explicit
    
    # Debug: Print current working directory
    st.write(f"Current working directory: {os.getcwd()}")
    st.write(f"Looking for data in: {os.path.abspath(data_folder)}")
    
    for country in countries:
        file_name = f"{country.lower()}_clean.csv"
        file_path = os.path.join(data_folder, file_name)
        
        # Debug output for each file
        st.write(f"Attempting to load: {file_path}")
        st.write(f"File exists: {os.path.exists(file_path)}")
        
        if not os.path.exists(file_path):
            st.error(f"⚠️ Missing file: {file_path}")
            continue
            
        try:
            df = pd.read_csv(file_path)
            df["Country"] = country
            data_frames.append(df)
            st.success(f"✅ Successfully loaded {country} data")
        except Exception as e:
            st.error(f"❌ Error loading {file_path}: {str(e)}")
            continue

    if not data_frames:
        st.error("No data loaded. Please check:")
        st.error(f"- Data folder exists at {os.path.abspath(data_folder)}")
        st.error("- Files follow naming convention: 'countryname_clean.csv'")
        return None
        
    return pd.concat(data_frames, ignore_index=True)


def plot_ghi_boxplot(df: pd.DataFrame) -> None:
    """
    Display a Seaborn boxplot for GHI by Country inside Streamlit.
    
    Args:
        df: DataFrame containing 'Country' and 'GHI' columns
    """
    if df.empty or 'GHI' not in df.columns or 'Country' not in df.columns:
        st.warning("Insufficient data to plot GHI boxplot")
        return
    
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(data=df, x='Country', y='GHI', palette='viridis')
    ax.set_title('GHI Distribution by Country')
    ax.set_ylabel('Global Horizontal Irradiance (W/m²)')
    ax.set_xlabel('')
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.close()


def plot_bubble_chart(df: pd.DataFrame) -> None:
    """
    Plot an interactive bubble chart of GHI vs Temperature with size by RH or BP.
    
    Args:
        df: DataFrame containing required metrics
    """
    required_cols = ['GHI', 'Tamb']
    size_options = ['RH', 'BP']
    
    if not all(col in df.columns for col in required_cols):
        st.warning("Missing required columns for bubble chart")
        return
        
    size_col = next((col for col in size_options if col in df.columns), None)
    
    fig = px.scatter(
        df, 
        x='Tamb', 
        y='GHI', 
        size=size_col,
        color='Country' if 'Country' in df.columns else None,
        title='GHI vs Temperature Bubble Chart',
        labels={
            'Tamb': 'Ambient Temperature (°C)', 
            'GHI': 'Global Horizontal Irradiance (W/m²)',
            'RH': 'Relative Humidity (%)',
            'BP': 'Atmospheric Pressure (hPa)'
        },
        size_max=30,
        hover_data=df.columns
    )
    
    fig.update_layout(
        hovermode='closest',
        xaxis_title='Ambient Temperature (°C)',
        yaxis_title='Global Horizontal Irradiance (W/m²)'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def summary_stats(df: pd.DataFrame, metrics: List[str]) -> pd.DataFrame:
    """
    Create summary statistics for specified metrics grouped by Country.
    
    Args:
        df: Input DataFrame
        metrics: List of metric columns to summarize
        
    Returns:
        DataFrame with summary statistics
    """
    if df.empty or not metrics:
        return pd.DataFrame()
        
    # Filter for existing metrics only
    valid_metrics = [m for m in metrics if m in df.columns]
    
    if not valid_metrics:
        return pd.DataFrame()
    
    summary = df.groupby('Country')[valid_metrics].agg(['mean', 'median', 'std', 'min', 'max'])
    summary.columns = [' '.join(col).strip() for col in summary.columns.values]
    return summary.reset_index().round(2)


def anova_test(df: pd.DataFrame, target_col: str = 'GHI') -> Optional[float]:
    """
    Perform one-way ANOVA test on specified column across countries.
    
    Args:
        df: Input DataFrame
        target_col: Column name to analyze
        
    Returns:
        p-value or None if test cannot be performed
    """
    if df.empty or target_col not in df.columns:
        return None
        
    country_groups = df.groupby('Country')[target_col]
    
    # Need at least 2 groups with data
    if len(country_groups) < 2:
        return None
        
    # Extract data for each group (filtering out NaN values)
    samples = [group.dropna().values for _, group in country_groups]
    
    # Check we have at least 2 samples with data
    if sum(len(s) > 0 for s in samples) < 2:
        return None
        
    _, p_value = f_oneway(*samples)
    return p_value
