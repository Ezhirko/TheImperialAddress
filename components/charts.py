import streamlit as st
import plotly.express as px


def residents_chart(df):

    residents = df[df["OccupancyType"] == "Residents"]

    installed = residents["Installed"].sum()
    pending = len(residents) - installed

    fig = px.pie(
        names=["Installed", "Pending"],
        values=[installed, pending],
        title="Residents"
    )

    st.plotly_chart(fig, width="stretch")


def construction_chart(df):

    construction = df[df["OccupancyType"] == "Under Construction"]

    installed = construction["Installed"].sum()
    pending = len(construction) - installed

    fig = px.pie(
        names=["Installed", "Pending"],
        values=[installed, pending],
        title="Under Construction"
    )

    st.plotly_chart(fig, width="stretch")