import os
import pandas as pd
from datetime import datetime

from scoring import (
    calculate_lead_score,
    get_priority,
    get_recommendation
)


DATABASE_FILE = "leads.csv"


COLUMNS = [
    "id",
    "company_name",
    "website",
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
    "sales_notes",
    "score",
    "priority",
    "recommendation",
    "status",
    "created_at"
]


def initialize_database():
    """
    Create the database file if it does not already exist.
    """

    if not os.path.exists(DATABASE_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATABASE_FILE, index=False)


def get_all_leads():
    """
    Return all saved leads as a DataFrame.
    """

    initialize_database()

    try:
        df = pd.read_csv(DATABASE_FILE)

        if df.empty:
            return pd.DataFrame(columns=COLUMNS)

        return df

    except Exception:
        return pd.DataFrame(columns=COLUMNS)


def save_lead(lead):
    """
    Calculate score and save a new lead.
    """

    initialize_database()

    score = calculate_lead_score(
        lead.get("industry", ""),
        lead.get("company_size", ""),
        lead.get("annual_revenue", 0),
        lead.get("decision_maker", ""),
        lead.get("buying_timeline", ""),
        lead.get("requirement", ""),
        lead.get("existing_supplier", "")
    )

    priority = get_priority(score)
    recommendation = get_recommendation(score)

    existing_df = get_all_leads()

    if existing_df.empty:
        new_id = 1
    else:
        existing_df["id"] = pd.to_numeric(
            existing_df["id"],
            errors="coerce"
        )

        new_id = int(existing_df["id"].max()) + 1

    new_lead = {
        "id": new_id,
        "company_name": lead.get("company_name", ""),
        "website": lead.get("website", ""),
        "industry": lead.get("industry", ""),
        "company_size": lead.get("company_size", ""),
        "location": lead.get("location", ""),
        "annual_revenue": lead.get("annual_revenue", 0),
        "requirement": lead.get("requirement", ""),
        "buying_timeline": lead.get("buying_timeline", ""),
        "existing_supplier": lead.get("existing_supplier", ""),
        "decision_maker": lead.get("decision_maker", ""),
        "lead_source": lead.get("lead_source", ""),
        "relationship": lead.get("relationship", ""),
        "sales_notes": lead.get("sales_notes", ""),
        "score": score,
        "priority": priority,
        "recommendation": recommendation,
        "status": lead.get("status", "New"),
        "created_at": lead.get(
            "created_at",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    }

    df = pd.DataFrame([new_lead])

    df = pd.concat(
        [existing_df, df],
        ignore_index=True
    )

    df = df[COLUMNS]

    df.to_csv(
        DATABASE_FILE,
        index=False
    )

    return new_lead


def delete_lead(lead_id):
    """
    Delete a lead using its ID.
    """

    initialize_database()

    df = get_all_leads()

    if df.empty:
        return False

    df["id"] = pd.to_numeric(
        df["id"],
        errors="coerce"
    )

    original_count = len(df)

    df = df[df["id"] != int(lead_id)]

    if len(df) == original_count:
        return False

    df.to_csv(
        DATABASE_FILE,
        index=False
    )

    return True


def update_lead_status(lead_id, new_status):
    """
    Update the pipeline status of a lead.
    """

    initialize_database()

    df = get_all_leads()

    if df.empty:
        return False

    df["id"] = pd.to_numeric(
        df["id"],
        errors="coerce"
    )

    matching_rows = df["id"] == int(lead_id)

    if not matching_rows.any():
        return False

    df.loc[
        matching_rows,
        "status"
    ] = new_status

    df.to_csv(
        DATABASE_FILE,
        index=False
    )

    return True


def load_demo_leads():
    """
    Load realistic demonstration leads into the database.

    Existing companies are not duplicated.
    """

    from demo_data import DEMO_LEADS

    initialize_database()

    existing_df = get_all_leads()

    existing_companies = set()

    if not existing_df.empty:
        existing_companies = set(
            existing_df["company_name"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    added_leads = []

    for lead in DEMO_LEADS:

        company_name = str(
            lead.get("company_name", "")
        ).strip()

        if not company_name:
            continue

        if company_name.lower() in existing_companies:
            continue

        saved_lead = save_lead(lead)

        added_leads.append(saved_lead)

        existing_companies.add(
            company_name.lower()
        )

    return added_leads
