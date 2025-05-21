import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
import plotly.express as px

# Function to load dataset
def load_data(file_path):
    """Loads the dataset from a given path."""
    return pd.read_csv(file_path)

# Function for summary statistics and missing value report
def summary_and_missing(df):
    """Displays summary statistics and missing values."""
    print("Summary Statistics:\n", df.describe())
    print("\nMissing Value Count:\n", df.isna().sum())
    high_nulls = df.columns[df.isna().mean() > 0.05]
    if len(high_nulls) > 0:
        print("\nColumns with >5% missing values:", list(high_nulls))
        print(df.describe())
        print(df.isna().sum())

# Function to detect and handle outliers, impute missing values
import pandas as pd
import numpy as np
from scipy.stats import zscore

import pandas as pd
import numpy as np
from scipy.stats import zscore

import pandas as pd
import numpy as np
from scipy.stats import zscore

def clean_data(df):
    """
    Clean the dataset by:
    - Imputing missing values in key columns with the median.
    - Detecting outliers using Z-score and removing rows with |Z| > 3 in key columns.
    
    Args:
        df (pd.DataFrame): Original dataframe
    
    Returns:
        pd.DataFrame: Cleaned dataframe without outliers and missing values imputed
    """
    key_columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']

    # Make a copy so original df is not changed (avoid SettingWithCopyWarning)
    df_clean = df.copy()

    # Impute missing values with median for key columns
    for col in key_columns:
        if col in df_clean.columns:
            median_val = df_clean[col].median()
            df_clean.loc[:, col] = df_clean[col].fillna(median_val)

    # Calculate Z-scores for key columns
    z_scores = df_clean[key_columns].apply(zscore)

    # Identify rows where any Z-score > 3 (outliers)
    outlier_mask = (np.abs(z_scores) > 3).any(axis=1)

    # Drop those outlier rows
    df_clean = df_clean.loc[~outlier_mask].reset_index(drop=True)

    return df_clean


# Function to export cleaned data
def export_cleaned_data(df, country):
    """Exports cleaned dataset to data/<country>_clean.csv."""
    df.to_csv(f"data/{country}_clean.csv", index=False)

# Function for time series visualization
def time_series_analysis(df):
    """Creates time series plots for solar parameters."""
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        df[["GHI", "DNI", "DHI", "Tamb"]].plot(subplots=True, figsize=(12, 10), title="Time Series Analysis")
        plt.tight_layout()
        plt.show()

# Function to analyze impact of cleaning flag
def cleaning_impact(df):
    """Plots average ModA and ModB values grouped by Cleaning flag."""
    if "Cleaning" in df.columns:
        df.groupby("Cleaning")[["ModA", "ModB"]].mean().plot(kind="bar", title="Cleaning Impact on ModA & ModB")
        plt.ylabel("Average Value")
        plt.tight_layout()
        plt.show()

# Function for correlation and scatter plots
def correlation_analysis(df):
    """Displays correlation heatmap and scatter plots."""
    corr_cols = [col for col in ["GHI", "DNI", "DHI", "TModA", "TModB"] if col in df.columns]
    sns.heatmap(df[corr_cols].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()
    
    scatter_pairs = [("WS", "GHI"), ("WSgust", "GHI"), ("WD", "GHI"), ("RH", "Tamb"), ("RH", "GHI")]
    for x, y in scatter_pairs:
        if x in df.columns and y in df.columns:
            sns.scatterplot(data=df, x=x, y=y)
            plt.title(f"{x} vs {y}")
            plt.show()

# Function for wind rose and distribution analysis
def wind_distribution(df):
    """Creates histograms and wind rose plots."""
    if "WS" in df.columns:
        df['WS'].hist(bins=30)
        plt.title("Wind Speed Distribution")
        plt.xlabel("WS")
        plt.show()
    if "WD" in df.columns and "WS" in df.columns:
        fig = px.bar_polar(df, r="WS", theta="WD", title="Wind Rose")
        fig.show()

# Function to analyze relative humidity impact
def temperature_analysis(df):
    """Plots RH vs Tamb and RH vs GHI."""
    if "RH" in df.columns:
        if "Tamb" in df.columns:
            sns.scatterplot(data=df, x="RH", y="Tamb")
            plt.title("RH vs Tamb")
            plt.show()
        if "GHI" in df.columns:
            sns.scatterplot(data=df, x="RH", y="GHI")
            plt.title("RH vs GHI")
            plt.show()

# Function to plot bubble chart
def bubble_chart(df):
    """Plots bubble chart of GHI vs Tamb with RH or BP as size."""
    if "GHI" in df.columns and "Tamb" in df.columns:
        size_col = "RH" if "RH" in df.columns else "BP" if "BP" in df.columns else None
        if size_col:
            fig = px.scatter(df, x="Tamb", y="GHI", size=size_col, title="GHI vs Tamb Bubble Chart")
            fig.show()

# Example usage:
# df = load_data("data/benin.csv")
# summary_and_missing(df)
# df = clean_data(df)
# export_cleaned_data(df, "benin")
# time_series_analysis(df)
# cleaning_impact(df)
# correlation_analysis(df)
# wind_distribution(df)
# temperature_analysis(df)
# bubble_chart(df)
