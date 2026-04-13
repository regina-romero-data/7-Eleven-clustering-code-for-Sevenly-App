"""
=============================================================================
7-Eleven Customer Segmentation — K-Means Clustering
=============================================================================
Project:    ICONN / Petro Seven · Academic Consulting Project
Author:     Regina Romero de León
Year:       2025

Description:
    End-to-end customer segmentation pipeline on real transactional data
    from ICONN/7-Eleven México. Identifies behavioral customer profiles
    based on product preference, coupon type, temperature patterns, and
    soccer match correlation to optimize the Petro Seven mobile coupon
    strategy.

Methodology:
    - Data Wrangling & Normalization
    - Feature Engineering (numerical + categorical)
    - Scikit-learn Preprocessing Pipeline (StandardScaler + OneHotEncoder)
    - K-Means Clustering (k=4)
    - Geographic Filtering (Nuevo León)
    - Cluster Summary & Export to Excel

Tools: Python · Pandas · NumPy · Scikit-learn · KPrototypes · OpenPyXL
=============================================================================
"""

# =============================================================================
# 1. IMPORTS & BASIC CONFIGURATION
# =============================================================================

import pandas as pd
import numpy as np
import unicodedata
from IPython.display import display

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans

# =============================================================================
# 2. LOAD DATA
# =============================================================================

FILE_PATH = "/content/Data-Proyecto-TEC-_2_ (7).xlsx"  # Update path if needed
SHEET = "Worksheet"

# Read only necessary columns to speed up processing
USECOLS = [
    "ID Cliente", "Tipo Transacción", "Cupón", "Tipo Cupón", "Fecha",
    "Producto", "Plaza", "Temp_prom", "Partido"
]

df = pd.read_excel(FILE_PATH, sheet_name=SHEET, usecols=USECOLS, engine="openpyxl")

# Filter out rows where 'Tipo Transacción' is 'transacción'
df = df[df["Tipo Transacción"] != "transacción"].copy()

# =============================================================================
# 3. DATE PROCESSING
# =============================================================================

# Convert the column to datetime format (this fixes the .dt error)
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

# Filter records for year 2025 only
df_2025 = df[df["Fecha"].dt.year == 2025]

# =============================================================================
# 4. COLUMN NORMALIZATION
# =============================================================================

# Normalize column names: remove spaces, convert to lowercase
# and replace accented characters
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("ó", "o")
    .str.replace("ú", "u")
    .str.replace("í", "i")
    .str.replace("é", "e")
    .str.replace("á", "a")
)

# Verify columns were renamed correctly
print("Columns:", df.columns.tolist())

# Ensure datetime format
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

# Select columns (already normalized)
columnas = ["id_cliente", "producto", "partido", "temp_prom", "fecha", "tipo_cupon", "cupon"]
df_filtrado = df[columnas].copy()

# =============================================================================
# 5. DATA CLEANING — REMOVE FUEL PRODUCTS
# =============================================================================

# Text cleaning and normalization for the 'producto' column
df["producto"] = df["producto"].astype(str).str.strip().str.upper()

# Robust filter: removes all possible variants of fuel products
productos_excluir = ["MAGNA", "PREMIUM", "DIESEL"]
df = df[~df["producto"].isin(productos_excluir)]

# Verification
print("Unique products after filter:", df["producto"].unique())

# =============================================================================
# 6. PREPROCESSING PIPELINE
# =============================================================================

# Preprocessing: separate numerical and categorical features
num_features = ["temp_prom"]
cat_features = ["producto", "partido", "tipo_cupon", "cupon"]

# Convert categorical features to string type to handle mixed types (e.g., NaNs)
for col in cat_features:
    df[col] = df[col].astype(str)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features)
    ]
)

# =============================================================================
# 7. K-MEANS CLUSTERING (k=4)
# =============================================================================

# Build clustering pipeline
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("cluster", KMeans(n_clusters=4, random_state=42))
])

# Fit the model
pipeline.fit(df)

# Add cluster labels to the DataFrame
df["cluster"] = pipeline.named_steps["cluster"].labels_

# Analyze results
cluster_summary = df.groupby("cluster").agg({
    "id_cliente": "nunique",
    "temp_prom": "mean",
}).rename(columns={"id_cliente": "unique_customers", "temp_prom": "avg_temperature"})

print("\nInitial Cluster Summary:")
print(cluster_summary)

# =============================================================================
# 8. COMPREHENSIVE CLUSTER SUMMARY
# =============================================================================

# Display size of each cluster
print("\nObservations per cluster:")
print(df["cluster"].value_counts().sort_index())

# Comprehensive summary by cluster
resumen = df.groupby("cluster").agg({
    "id_cliente": "nunique",
    "producto": lambda x: x.value_counts().index[0],
    "partido": lambda x: x.value_counts().index[0],
    "tipo_cupon": lambda x: x.value_counts().index[0] if x.notna().any() else "No coupon",
    "fecha": ["min", "max"],
    "temp_prom": "mean"
})

# Clean column names
resumen.columns = [
    "unique_customers", "most_common_product", "most_common_match_day",
    "most_common_coupon_type", "date_min", "date_max", "avg_temperature"
]

print("\nCluster Summary:")
print(resumen)

# =============================================================================
# 9. GEOGRAPHIC FILTER — NUEVO LEÓN ONLY
# =============================================================================

def clean_text(x):
    """Normalize text to remove accents and corrupted characters."""
    if pd.isna(x):
        return ""
    x = str(x).lower()
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8")
    return x

# Apply cleaning to location column
df["plaza_limpia"] = df["plaza"].apply(clean_text)

# Robust filter: detects 'nuevo le3', 'nuevo le' or 'nuevo leon'
df_nl = df[df["plaza_limpia"].str.contains("nuevo le", na=False)]

print(f"\nRows found for Nuevo León: {len(df_nl)}")

# =============================================================================
# 10. CLUSTER SUMMARY FOR NUEVO LEÓN
# =============================================================================

if not df_nl.empty:
    resumen_clusters = df_nl.groupby("cluster").agg({
        "id_cliente": "nunique",
        "producto": lambda x: x.value_counts().index[0],
        "partido": lambda x: x.value_counts().index[0],
        "tipo_cupon": lambda x: x.value_counts().index[0],
        "temp_prom": "mean",
        "fecha": ["min", "max", "count"]
    })

    resumen_clusters.columns = [
        "unique_customers",
        "most_common_product",
        "most_common_match_day",
        "most_common_coupon_type",
        "avg_temperature",
        "date_min",
        "date_max",
        "total_transactions"
    ]

    print("\nCluster Summary — Nuevo León:")
    display(resumen_clusters)

    # (Optional) Export results to Excel
    resumen_clusters.to_excel("cluster_summary_nuevo_leon.xlsx", index=True)
    print("\nResults saved to: cluster_summary_nuevo_leon.xlsx")

else:
    print("No rows found for Nuevo León.")

# =============================================================================
# 11. SAVE FULL DATAFRAME WITH CLUSTER ASSIGNMENTS
# =============================================================================

# Save the DataFrame with cluster assignments to an Excel file
output_file_path = "data_with_clusters.xlsx"
df.to_excel(output_file_path, index=False)
print(f"DataFrame with clusters saved to: {output_file_path}")
