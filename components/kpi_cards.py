import streamlit as st
from utils.analytics import Analytics


def draw_kpis(df):

    analytics = Analytics(df)
    summary = analytics.summary()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "🏡 Total Plots",
        summary["total"]
    )

    c2.metric(
        "👨 Residents",
        summary["residents"]
    )

    c3.metric(
        "🏗 Under Construction",
        summary["construction"]
    )

    c4.metric(
        "📱 MyGate Installed",
        summary["installed"]
    )

    c5.metric(
        "✅ Compliance",
        f'{summary["compliance"]}%'
    )