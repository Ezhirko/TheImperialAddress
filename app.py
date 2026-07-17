import streamlit as st

from utils.data_loader import DataLoader
from utils.preprocessing import DataProcessor

from components.charts import (
    residents_chart,
    construction_chart,
)

st.set_page_config(
    page_title="Imperial Address",
    layout="wide"
)

# ----------------------------
# Load Data
# ----------------------------

loader = DataLoader()

internal, owners, mygate = loader.load()

processor = DataProcessor(
    internal,
    owners,
    mygate
)

df = processor.merge()

owner_installation = (
    df.groupby("Owner")["Installed"]
      .any()
      .rename("OwnerInstalled")
)

df = df.join(owner_installation, on="Owner")

df["Installed"] = df["OwnerInstalled"]

df.drop(columns=["OwnerInstalled"], inplace=True)

# ------------------------------------------------------------
# If an owner has installed MyGate for ANY one of their plots,
# mark all plots owned by that owner as Installed.
# ------------------------------------------------------------

# Create a normalized owner name to avoid duplicates due to
# MR., MRS., extra spaces, etc.
df["OwnerKey"] = (
    df["Owner"]
      .fillna("")
      .str.upper()
      .str.replace(r"MR\.?|MRS\.?|MS\.?", "", regex=True)
      .str.replace("&", " ", regex=False)
      .str.replace(r"\s+", " ", regex=True)
      .str.strip()
)

# Determine whether each owner has at least one MyGate installation
owner_status = (
    df.groupby("OwnerKey")["Installed"]
      .any()
      .reset_index()
      .rename(columns={"Installed": "OwnerInstalled"})
)

# Merge back to all plots
df = df.merge(owner_status, on="OwnerKey", how="left")

# Replace plot-level installation with owner-level installation
df["Installed"] = df["OwnerInstalled"]

# Clean up helper columns
df.drop(columns=["OwnerInstalled"], inplace=True)

# ----------------------------
# Split Data
# ----------------------------

residents = df[df["OccupancyType"] == "Residents"]

construction = df[df["OccupancyType"] == "Under Construction"]

# ----------------------------
# Counts
# ----------------------------

resident_installed = residents["Installed"].sum()
resident_pending = len(residents) - resident_installed

construction_installed = construction["Installed"].sum()
construction_pending = len(construction) - construction_installed

# ----------------------------
# Compliance
# ----------------------------

total_installed = resident_installed + construction_installed
total_pending = resident_pending + construction_pending
total_plots = total_installed + total_pending

compliance = (
    round((total_installed / total_plots) * 100, 1)
    if total_plots > 0 else 0
)

# ----------------------------
# Title
# ----------------------------

st.title("🏡 Imperial Address - MyGate Compliance Dashboard")

# ----------------------------
# KPI Cards
# ----------------------------

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Residents Installed", resident_installed)

c2.metric("Residents Pending", resident_pending)

c3.metric("Construction Installed", construction_installed)

c4.metric("Construction Pending", construction_pending)

c5.metric("Overall Compliance", f"{compliance}%")

st.subheader("Overall MyGate Compliance")

st.progress(compliance / 100)

st.write(f"**{compliance}%** of eligible plots have MyGate installed.")

# ----------------------------
# Pie Charts
# ----------------------------

col1, col2 = st.columns(2)

with col1:
    residents_chart(df)

with col2:
    construction_chart(df)

# ----------------------------
# Pending Residents
# ----------------------------

st.subheader("Residents without MyGate")

pending_residents = residents[
    residents["Installed"] == False
]

st.dataframe(
    pending_residents[
        [
            "Phase",
            "PlotNo",
            "Owner",
            "Phone"
        ]
    ],
    width="stretch"
)

# ----------------------------
# Pending Construction
# ----------------------------

st.subheader("Construction without MyGate")

pending_construction = construction[
    construction["Installed"] == False
]

st.dataframe(
    pending_construction[
        [
            "Phase",
            "PlotNo",
            "Owner",
            "Phone"
        ]
    ],
    width="stretch"
)