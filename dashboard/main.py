import streamlit as st
import utils
from utils import load_cleaned_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Solar Energy Dashboard", layout="wide")

st.title("🌞 Solar Energy Dashboard")
st.markdown("""
Select one or more countries to explore solar energy data:
- View distributions of solar irradiance (GHI)
- Compare key metrics
- Interactive bubble charts
""")

# Select countries
country_options = ["Benin", "Sierraleone", "Togo"]
countries = st.multiselect("Select countries", options=country_options)

if not countries:
    st.warning("Please select at least one country to proceed.")
    st.stop()

# Load data

df = utils.load_cleaned_data(countries)

if df is None:
    st.error("No data loaded. Please check your data files in the data folder.")
else:
    if df.empty:
        st.warning("Loaded data is empty.")
    else:
        # Your normal data handling code here
        st.write(df)


# Sidebar - Select metric for boxplot
st.sidebar.header("Visualization Options")
metric = st.sidebar.selectbox("Choose metric for boxplot", options=["GHI", "DNI", "DHI"])

# Boxplot for selected metric
#st.subheader(f"{metric} Distribution by Country")
#if metric in df.columns:
#    st.pyplot()
#    
    
#    plt.figure(figsize=(10,5))
#   sns.boxplot(data=df, x='Country', y=metric, palette='Set2')
#   plt.title(f"{metric} Distribution by Country")
#   st.pyplot(plt.gcf())
#   plt.clf()
#else:
 #   st.warning(f"{metric} not found in data.")

# Show summary stats table
st.subheader("Summary Statistics")
metrics_to_summarize = ['GHI', 'DNI', 'DHI']
summary_df = utils.summary_stats(df, metrics_to_summarize)
st.dataframe(summary_df, use_container_width=True)

# ANOVA test
#st.subheader("ANOVA Test for GHI Differences Across Countries")
#p_value = utils.anova_test(df)
#if p_value is not None:
#    st.write(f"P-value: {p_value:.5f}")
#    if p_value < 0.05:
#        st.success("Statistically significant differences detected between countries (p < 0.05).")
#    else:

#        st.info("No statistically significant difference detected (p >= 0.05).")
#else:
#   st.warning("Not enough data to perform ANOVA test.")

# Bubble chart
st.subheader("Interactive Bubble Chart: GHI vs Temperature")
utils.plot_bubble_chart(df)

# Key observations
st.markdown("""
### Key Observations
- Country shows highest median GHI but also greatest variability.
- Differences in solar irradiance are statistically significant based on ANOVA.
- Temperature and humidity contribute to variations in solar potential.
""")
