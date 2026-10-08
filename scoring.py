def calculate_lead_score(
    industry,
    company_size,
    annual_revenue,
    decision_maker,
    buying_timeline,
    requirement,
    existing_supplier
):
    score = 0

    # Industry fit
    if industry in ["FMCG", "Pharmaceuticals", "Manufacturing", "Chemicals"]:
        score += 20
    elif industry in ["Logistics", "Technology"]:
        score += 15
    else:
        score += 8

    # Company size
    if company_size == "Enterprise":
        score += 20
    elif company_size == "Large":
        score += 16
    elif company_size == "Medium":
        score += 10
    else:
        score += 5

    # Revenue potential
    if annual_revenue >= 10000:
        score += 20
    elif annual_revenue >= 5000:
        score += 16
    elif annual_revenue >= 1000:
        score += 12
    elif annual_revenue > 0:
        score += 6

    # Decision-maker availability
    if decision_maker == "Yes":
        score += 15
    else:
        score += 5

    # Buying timeline
    if buying_timeline == "Immediate":
        score += 15
    elif buying_timeline == "Within 3 months":
        score += 12
    elif buying_timeline == "3–6 months":
        score += 8
    else:
        score += 4

    # Requirement clarity
    if requirement == "Clearly Defined":
        score += 5
    elif requirement == "Partially Defined":
        score += 3

    # Existing supplier
    if existing_supplier == "No":
        score += 5

    return min(score, 100)


def get_priority(score):
    if score >= 80:
        return "High Priority"
    elif score >= 50:
        return "Medium Priority"
    else:
        return "Low Priority"


def get_recommendation(score):
    if score >= 80:
        return "Prioritise immediately and initiate direct sales outreach."
    elif score >= 50:
        return "Nurture the lead and gather additional qualification information."
    else:
        return "Keep under observation and qualify further before investing significant sales effort."