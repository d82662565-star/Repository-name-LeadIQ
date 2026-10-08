import pandas as pd


def export_leads_to_csv(leads, filename="leadiq_leads.csv"):
    """Export leads to a CSV file."""

    if not leads:
        return None

    df = pd.DataFrame(leads)

    df.to_csv(
        filename,
        index=False,
        encoding="utf-8"
    )

    return filename


def export_leads_to_excel(leads, filename="leadiq_leads.xlsx"):
    """Export leads to an Excel file."""

    if not leads:
        return None

    df = pd.DataFrame(leads)

    df.to_excel(
        filename,
        index=False
    )

    return filename


def prepare_export_dataframe(leads):
    """Prepare lead data for downloading."""

    if not leads:
        return pd.DataFrame()

    df = pd.DataFrame(leads)

    preferred_columns = [
        "id",
        "company_name",
        "industry",
        "company_size",
        "location",
        "annual_revenue",
        "requirement",
        "buying_timeline",
        "existing_supplier",
        "decision_maker",
        "lead_source",
        "relationship",
        "score",
        "priority",
        "status",
        "recommendation",
        "created_at"
    ]

    available_columns = [
        column
        for column in preferred_columns
        if column in df.columns
    ]

    return df[available_columns]