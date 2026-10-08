import pandas as pd


PIPELINE_STAGES = [
    "New",
    "Contacted",
    "Qualified",
    "Proposal",
    "Negotiation",
    "Won",
    "Lost"
]


def get_pipeline_stages():
    return PIPELINE_STAGES


def get_stage_index(stage):
    if stage in PIPELINE_STAGES:
        return PIPELINE_STAGES.index(stage)

    return -1


def get_next_stage(stage):
    index = get_stage_index(stage)

    if index == -1 or index >= len(PIPELINE_STAGES) - 1:
        return None

    return PIPELINE_STAGES[index + 1]


def is_active_lead(lead):
    if isinstance(lead, dict):
        return lead.get("status") not in ["Won", "Lost"]

    if isinstance(lead, pd.Series):
        return lead.get("status") not in ["Won", "Lost"]

    return False


def calculate_pipeline_value(leads):

    if leads is None:
        return 0

    if isinstance(leads, pd.DataFrame):

        if leads.empty:
            return 0

        df = leads.copy()

        if "annual_revenue" not in df.columns:
            return 0

        if "status" in df.columns:
            df = df[
                ~df["status"].isin(["Won", "Lost"])
            ]

        df["annual_revenue"] = pd.to_numeric(
            df["annual_revenue"],
            errors="coerce"
        ).fillna(0)

        return df["annual_revenue"].sum()

    if len(leads) == 0:
        return 0

    total = 0

    for lead in leads:

        if not is_active_lead(lead):
            continue

        try:
            total += float(
                lead.get("annual_revenue", 0)
            )
        except (TypeError, ValueError):
            pass

    return total


def count_by_stage(leads):

    result = {
        stage: 0
        for stage in PIPELINE_STAGES
    }

    if leads is None:
        return result

    if isinstance(leads, pd.DataFrame):

        if leads.empty or "status" not in leads.columns:
            return result

        counts = leads["status"].value_counts()

        for stage in PIPELINE_STAGES:
            result[stage] = int(
                counts.get(stage, 0)
            )

        return result

    for lead in leads:

        if isinstance(lead, dict):
            stage = lead.get("status")

            if stage in result:
                result[stage] += 1

    return result


def get_active_leads(leads):

    if leads is None:
        return pd.DataFrame()

    if isinstance(leads, pd.DataFrame):

        if leads.empty:
            return leads.copy()

        if "status" not in leads.columns:
            return leads.copy()

        return leads[
            ~leads["status"].isin(
                ["Won", "Lost"]
            )
        ].copy()

    return [
        lead
        for lead in leads
        if is_active_lead(lead)
    ]


def get_won_leads(leads):

    if leads is None:
        return pd.DataFrame()

    if isinstance(leads, pd.DataFrame):

        if leads.empty or "status" not in leads.columns:
            return leads.copy()

        return leads[
            leads["status"] == "Won"
        ].copy()

    return [
        lead
        for lead in leads
        if (
            isinstance(lead, dict)
            and lead.get("status") == "Won"
        )
    ]


def get_lost_leads(leads):

    if leads is None:
        return pd.DataFrame()

    if isinstance(leads, pd.DataFrame):

        if leads.empty or "status" not in leads.columns:
            return leads.copy()

        return leads[
            leads["status"] == "Lost"
        ].copy()

    return [
        lead
        for lead in leads
        if (
            isinstance(lead, dict)
            and lead.get("status") == "Lost"
        )
    ]


def calculate_conversion_rate(leads):

    if leads is None:
        return 0

    if isinstance(leads, pd.DataFrame):

        if leads.empty or "status" not in leads.columns:
            return 0

        total = len(leads)

        if total == 0:
            return 0

        converted = (
            leads["status"] == "Won"
        ).sum()

        return round(
            (converted / total) * 100,
            1
        )

    if len(leads) == 0:
        return 0

    converted = sum(
        1
        for lead in leads
        if (
            isinstance(lead, dict)
            and lead.get("status") == "Won"
        )
    )

    return round(
        (converted / len(leads)) * 100,
        1
    )


def calculate_win_rate(leads):

    if leads is None:
        return 0

    if isinstance(leads, pd.DataFrame):

        if leads.empty or "status" not in leads.columns:
            return 0

        won = (
            leads["status"] == "Won"
        ).sum()

        lost = (
            leads["status"] == "Lost"
        ).sum()

        total_decided = won + lost

        if total_decided == 0:
            return 0

        return round(
            (won / total_decided) * 100,
            1
        )

    if len(leads) == 0:
        return 0

    won = 0
    lost = 0

    for lead in leads:

        if not isinstance(lead, dict):
            continue

        status = lead.get("status")

        if status == "Won":
            won += 1

        elif status == "Lost":
            lost += 1

    total_decided = won + lost

    if total_decided == 0:
        return 0

    return round(
        (won / total_decided) * 100,
        1
    )


def get_stalled_leads(leads):

    if leads is None:
        return pd.DataFrame()

    if isinstance(leads, pd.DataFrame):

        if leads.empty:
            return leads.copy()

        if "status" not in leads.columns:
            return pd.DataFrame()

        stalled_stages = [
            "Contacted",
            "Qualified"
        ]

        return leads[
            leads["status"].isin(
                stalled_stages
            )
        ].copy()

    return [
        lead
        for lead in leads
        if (
            isinstance(lead, dict)
            and lead.get("status")
            in ["Contacted", "Qualified"]
        )
    ]