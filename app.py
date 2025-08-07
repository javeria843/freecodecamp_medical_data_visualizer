import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set Streamlit page config
st.set_page_config(page_title="Medical Data Visualizer", layout="wide")

# Title
st.title("🏥 Medical Data Visualizer")

# Load the data
df = pd.read_csv("medical_data.csv", delimiter=';')  # Use correct delimiter

# 🔧 Clean column names: strip spaces and convert to lowercase
df.columns = df.columns.str.strip().str.lower()

# ✅ Safe check: display columns (you can comment this later)
# st.write("Columns in dataset:", df.columns.tolist())

# Add overweight column
df['overweight'] = (df['Weight in kg'] / ((df['height'] / 100) ** 2)).apply(lambda x: 1 if x > 25 else 0)

# Normalize cholesterol and gluc (1 = good → 0, 2 or 3 = bad → 1)
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

# Sidebar
st.sidebar.header("Choose Visualization")
viz_type = st.sidebar.radio("Select one", ["Categorical Plot", "Correlation Heatmap"])

# 📊 Categorical Plot
if viz_type == "Categorical Plot":
    st.subheader("🧬 Categorical Feature Distribution by Cardio Status")

    # Melt the data
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )

    # Group and reformat
    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index(name="total")

    # Plot using seaborn catplot
    g = sns.catplot(
        x="variable", y="total", hue="value", col="cardio",
        kind="bar", data=df_cat, height=5, aspect=1
    )

    st.pyplot(g.fig)

# 🔥 Correlation Heatmap
elif viz_type == "Correlation Heatmap":
    st.subheader("📊 Correlation Heatmap of Medical Features")

    # Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['Weight in kg'] >= df['Weight in kg'].quantile(0.025)) &
        (df['Weight in kg'] <= df['Weight in kg'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Draw heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5}
    )
    st.pyplot(fig)
