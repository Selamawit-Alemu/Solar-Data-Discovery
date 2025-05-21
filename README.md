# Solar-Data-Discovery
Week 0 Challenge
# ☀️ Solar Data Discovery - Main Branch

This repository contains data exploration and preprocessing scripts for analyzing solar farm data from Benin, Sierra Leone, and Togo as part of the AI Mastery Program by Kifiya & Mastercard. The project aims to build insights from the data and lay the foundation for a Streamlit-based interactive dashboard.

---

## 📁 Folder Structure

├── dashboard/ # Streamlit dashboard (dashboard-dev branch)
├── data/ # Cleaned and processed datasets
│ ├── eda_benin.csv
│ └── ...
├── notebooks/ # EDA notebooks (per country, in respective branches)
├── scripts/ # Python scripts and utilities
│ └── eda_utils.py
├── README.md # Project documentation (you are here)


> ⚠️ Note: The `dashboard/` directory contains the Streamlit dashboard and is under development in the `dashboard-dev` branch. Cleaned datasets live in the `main` branch under `data/`.

---

## 📊 Project Scope

The project is divided into 3 phases:

### ✅ Task 1: Data Profiling and Cleaning

- Raw data for each country cleaned and saved to CSV.
- Common issues like missing values and inconsistent formats were handled.
- Output files: `eda_benin.csv`, `eda_sierraleone.csv`, etc.

### ✅ Task 2: Cross-Country Comparison

- Performed in Jupyter Notebooks (stored per-branch).
- Explored similarities and differences in solar metrics.
- Generated visualizations for Global Horizontal Irradiance (GHI), daily solar potential, etc.

### 🚧 Task 3 (In Progress): Streamlit Dashboard

- Interactive dashboard to explore cleaned solar data.
- In development on `dashboard-dev` branch.
- Uses Streamlit widgets, boxplots, and top region insights.

---

## 📌 How to Run the Project (Locally)

1. Clone the repository:

```bash
git clone https://github.com/your-username/Solar-Data-Discovery.git
cd Solar-Data-Discovery

    (Optional) Create a virtual environment:

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

    Install requirements:

pip install -r requirements.txt

    Open Jupyter for exploring notebooks (EDA):

jupyter notebook

🔀 Branches

    main: Cleaned data, utilities, and project documentation.

    benin-dev: EDA for Benin.

    sierraleone-dev: EDA for Sierra Leone.

    togo-dev: EDA for Togo.

    dashboard-dev: Streamlit dashboard code.


📂 Data Files
Country	File Name	Description
Benin	eda_benin.csv	Cleaned and ready for plotting
Sierra Leone	eda_sierraleone.csv	Coming soon
Togo	eda_togo.csv	Coming soon
