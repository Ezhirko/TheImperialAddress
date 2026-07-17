import pandas as pd
import re


class DataProcessor:

    def __init__(self, internal, owners, mygate):

        self.internal = internal.copy()
        self.owners = owners.copy()
        self.mygate = mygate.copy()

    # ----------------------------------------------------
    # Normalize Column Names
    # ----------------------------------------------------
    @staticmethod
    def normalize_columns(df):

        df.columns = (
            df.columns
            .str.strip()
            .str.replace("'", "", regex=False)
            .str.replace(" ", "_")
            .str.replace("-", "_")
            .str.lower()
        )

        return df

    # ----------------------------------------------------
    # Internal Population
    # ----------------------------------------------------
    def process_internal(self):

        self.internal = self.normalize_columns(self.internal)

        self.internal = self.internal.rename(columns={
            "phase": "Phase",
            "plotno": "PlotNo",
            "occupancytype": "OccupancyType"
        })

        self.internal["Phase"] = (
            self.internal["Phase"]
            .astype(int)
            .astype(str)
        )

        self.internal["PlotNo"] = self.internal["PlotNo"].astype(int)

        return self.internal

    # ----------------------------------------------------
    # Owners
    # ----------------------------------------------------
    def process_owners(self):

        self.owners = self.normalize_columns(self.owners)

        print(self.owners.columns.tolist())   # <-- Keep this temporarily

        self.owners = self.owners.rename(columns={
            "plot_nos": "PlotNo",
            "applicant_names": "Owner",
            "contact": "Phone",
            "email_id": "Email",
            "phase": "Phase"
        })

        self.owners["Phase"] = (
            self.owners["Phase"]
            .astype(int)
            .astype(str)
        )

        self.owners["PlotNo"] = self.owners["PlotNo"].astype(int)

        return self.owners

    # ----------------------------------------------------
    # MyGate
    # ----------------------------------------------------
    def process_mygate(self):

        flat = self.mygate["Flat"].astype(str).str.upper()

        self.mygate["Phase"] = (
            flat.str.extract(r"PHASE\s*([0-9]+)", expand=False)
        )

        self.mygate["PlotNo"] = (
            flat.str.extract(r"(\d+)$", expand=False)
        )

        self.mygate = self.mygate.dropna(subset=["Phase", "PlotNo"])

        self.mygate["Phase"] = self.mygate["Phase"].astype(str)

        self.mygate["PlotNo"] = self.mygate["PlotNo"].astype(int)

        users = (
            self.mygate
            .groupby(["Phase", "PlotNo"])
            .size()
            .reset_index(name="MygateUsers")
        )

        return users

    # ----------------------------------------------------
    # Merge Everything
    # ----------------------------------------------------
    def merge(self):

        internal = self.process_internal()

        owners = self.process_owners()

        users = self.process_mygate()

        df = (
            internal
            .merge(
                owners,
                on=["Phase", "PlotNo"],
                how="left"
            )
            .merge(
                users,
                on=["Phase", "PlotNo"],
                how="left"
            )
        )

        df["MygateUsers"] = df["MygateUsers"].fillna(0).astype(int)

        df["Installed"] = df["MygateUsers"] > 0

        df["PlotID"] = (
            "P"
            + df["Phase"]
            + "-"
            + df["PlotNo"].astype(str)
        )

        return df