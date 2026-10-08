import pandas as pd


def prepare_dataframe(leads):

    if leads is None:
        return pd.DataFrame()

    if isinstance(leads, pd.DataFrame):
        if leads.empty:
            return pd.DataFrame()

        df = leads.copy()

    else:
        if len(leads) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(leads)

    if "score" in df.columns:
        df["score"] = pd.to_numeric(
            df["score"],
            errors="coerce"
        ).fillna(0)

    if "annual_revenue" in df.columns:
        df["annual_revenue"] = pd.to_numeric(
            df["annual_revenue"],
            errors="coerce"
        ).fillna(0)

    return df


def get_priority_distribution(df):

    if df is None or df.empty:
        return pd.Series(dtype="int64")

    if "priority" not in df.columns:
        return pd.Series(dtype="int64")

    return df["priority"].value_counts()


def get_industry_distribution(df):

    if df is None or df.empty:
        return pd.Series(dtype="int64")

    if "industry" not in df.columns:
        return pd.Series(dtype="int64")

    return df["industry"].value_counts()


def get_average_score(df):

    if df is None or df.empty:
        return 0

    if "score" not in df.columns:
        return 0

    return round(df["score"].mean(), 1)


def get_total_revenue(df):

    if df is None or df.empty:
        return 0

    if "annual_revenue" not in df.columns:
        return 0

    return df["annual_revenue"].sum()


def get_revenue_by_industry(df):

    if df is None or df.empty:
        return pd.Series(dtype="float64")

    if (
        "industry" not in df.columns
        or "annual_revenue" not in df.columns
    ):
        return pd.Series(dtype="float64")

    return (
        df.groupby("industry")["annual_revenue"]
        .sum()
        .sort_values(ascending=False)
    )


def get_score_distribution(df):

    if df is None or df.empty:
        return pd.Series(
            dtype="float64"
        )

    if "score" not in df.columns:
        return pd.Series(
            dtype="float64"
        )

    return df["score"]


def get_status_distribution(df):

    if df is None or df.empty:
        return pd.Series(dtype="int64")

    if "status" not in df.columns:
        return pd.Series(dtype="int64")

    return df["status"].value_counts()


def get_top_leads(df, n=5):

    if df is None or df.empty:
        return pd.DataFrame()

    if "score" not in df.columns:
        return pd.DataFrame()

    return (
        df.sort_values(
            "score",
            ascending=False
        )
        .head(n)
        .copy()
    )


def get_attention_leads(df):

    if df is None or df.empty:
        return pd.DataFrame()

    if "score" not in df.columns:
        return pd.DataFrame()

    if "priority" not in df.columns:
        return pd.DataFrame()

    return (
        df[
            (df["score"] < 80)
            | (df["priority"] != "High Priority")
        ]
        .sort_values(
            "score",
            ascending=False
        )
        .copy()
    )