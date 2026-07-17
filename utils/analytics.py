import pandas as pd


class Analytics:

    def __init__(self, df):
        self.df = df

    # -------------------------
    # KPIs
    # -------------------------
    def summary(self):

        total = len(self.df)

        residents = (
            self.df["OccupancyType"] == "Residents"
        ).sum()

        construction = (
            self.df["OccupancyType"] == "Under Construction"
        ).sum()

        installed = self.df["Installed"].sum()

        pending = total - installed

        compliance = round(installed / total * 100, 1)

        return {
            "total": total,
            "residents": residents,
            "construction": construction,
            "installed": installed,
            "pending": pending,
            "compliance": compliance
        }

    # -------------------------
    # Pie Chart
    # -------------------------
    def installation_status(self):

        return (
            self.df["Installed"]
            .map({
                True: "Installed",
                False: "Pending"
            })
            .value_counts()
            .reset_index()
            .rename(columns={
                "index": "Status",
                "count": "Count"
            })
        )

    # -------------------------
    # Occupancy
    # -------------------------
    def occupancy(self):

        return (
            self.df["OccupancyType"]
            .value_counts()
            .reset_index()
            .rename(columns={
                "index": "Type",
                "count": "Count"
            })
        )

    # -------------------------
    # Phase-wise
    # -------------------------
    def phase_summary(self):

        phase = (
            self.df
            .groupby(["Phase", "Installed"])
            .size()
            .reset_index(name="Count")
        )

        phase["Status"] = phase["Installed"].map({
            True: "Installed",
            False: "Pending"
        })

        return phase