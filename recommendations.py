def get_contact_strategy(lead):
    """Recommend how the sales team should approach the lead."""

    score = float(lead.get("score", 0))
    decision_maker = lead.get("decision_maker", "")
    buying_timeline = lead.get("buying_timeline", "")
    relationship = lead.get("relationship", "")
    existing_supplier = lead.get("existing_supplier", "")

    if score >= 80 and decision_maker == "Yes":
        return "Direct decision-maker outreach"

    if score >= 80:
        return "High-priority personalised outreach"

    if relationship == "Existing Customer":
        return "Relationship-led account expansion"

    if existing_supplier == "Yes":
        return "Competitive replacement approach"

    if buying_timeline in ["3–6 months", "More than 6 months"]:
        return "Nurture and scheduled follow-up"

    return "Qualification-first outreach"


def get_follow_up_frequency(lead):
    """Recommend how frequently the lead should be followed up."""

    score = float(lead.get("score", 0))
    buying_timeline = lead.get("buying_timeline", "")

    if score >= 80 and buying_timeline == "Immediate":
        return "Every 2–3 days"

    if score >= 80:
        return "Weekly"

    if score >= 50:
        return "Every 2 weeks"

    return "Monthly"


def get_information_to_collect(lead):
    """Identify important missing qualification information."""

    information = []

    if lead.get("decision_maker") == "No":
        information.append("Decision-maker details")

    if lead.get("requirement") in [
        "Partially Defined",
        "Not Defined"
    ]:
        information.append("Exact product/service requirement")

    if lead.get("existing_supplier") == "Unknown":
        information.append("Current supplier information")

    if lead.get("buying_timeline") in [
        "3–6 months",
        "More than 6 months"
    ]:
        information.append("Expected purchase date")

    if not lead.get("sales_notes"):
        information.append("Additional sales context")

    return information


def get_opportunity_type(lead):
    """Classify the commercial opportunity."""

    score = float(lead.get("score", 0))
    existing_supplier = lead.get(
        "existing_supplier",
        ""
    )
    relationship = lead.get(
        "relationship",
        ""
    )

    if relationship == "Existing Customer":
        return "Account Expansion"

    if existing_supplier == "No" and score >= 70:
        return "New Business Opportunity"

    if existing_supplier == "Yes" and score >= 60:
        return "Competitive Conversion"

    if score >= 50:
        return "Developing Opportunity"

    return "Early-Stage Prospect"


def generate_sales_plan(lead):
    """Generate a complete sales action plan."""

    return {
        "opportunity_type": get_opportunity_type(
            lead
        ),
        "contact_strategy": get_contact_strategy(
            lead
        ),
        "follow_up_frequency": get_follow_up_frequency(
            lead
        ),
        "information_to_collect": get_information_to_collect(
            lead
        )
    }