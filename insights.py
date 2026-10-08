def generate_lead_insights(lead):
    """
    Generate rule-based sales intelligence for a lead.
    """

    score = float(lead.get("score", 0))

    industry = lead.get("industry", "")
    company_size = lead.get("company_size", "")
    revenue = float(lead.get("annual_revenue", 0))
    decision_maker = lead.get("decision_maker", "")
    buying_timeline = lead.get("buying_timeline", "")
    requirement = lead.get("requirement", "")
    existing_supplier = lead.get("existing_supplier", "")
    relationship = lead.get("relationship", "")
    status = lead.get("status", "")

    strengths = []
    gaps = []
    objections = []

    # ---------------------------------------------
    # STRENGTHS
    # ---------------------------------------------

    if industry in [
        "FMCG",
        "Pharmaceuticals",
        "Manufacturing",
        "Chemicals"
    ]:
        strengths.append(
            "Strong industry alignment with the target market."
        )

    if company_size in [
        "Large",
        "Enterprise"
    ]:
        strengths.append(
            "Large company size indicates higher potential business value."
        )

    if revenue >= 10000:
        strengths.append(
            "High estimated revenue indicates strong commercial potential."
        )

    if decision_maker == "Yes":
        strengths.append(
            "Decision maker has been identified."
        )

    if buying_timeline == "Immediate":
        strengths.append(
            "Immediate buying timeline indicates strong purchase readiness."
        )

    if requirement == "Clearly Defined":
        strengths.append(
            "Requirement is clearly defined, reducing qualification uncertainty."
        )

    if existing_supplier == "No":
        strengths.append(
            "No existing supplier relationship may create an opportunity for entry."
        )


    # ---------------------------------------------
    # QUALIFICATION GAPS
    # ---------------------------------------------

    if decision_maker == "No":
        gaps.append(
            "Decision maker has not been identified."
        )

    if buying_timeline in [
        "3–6 months",
        "More than 6 months"
    ]:
        gaps.append(
            "Purchase decision may take longer to materialise."
        )

    if requirement == "Partially Defined":
        gaps.append(
            "Customer requirement needs further clarification."
        )

    if requirement == "Not Defined":
        gaps.append(
            "Customer requirement is currently unclear."
        )

    if existing_supplier == "Yes":
        gaps.append(
            "Existing supplier may create switching barriers."
        )

    if existing_supplier == "Unknown":
        gaps.append(
            "Current supplier situation is unknown."
        )


    # ---------------------------------------------
    # POTENTIAL OBJECTIONS
    # ---------------------------------------------

    if existing_supplier == "Yes":
        objections.append(
            "Customer may prefer the existing supplier due to established relationships."
        )

    if company_size in [
        "Large",
        "Enterprise"
    ]:
        objections.append(
            "Large organisations may have longer procurement and approval processes."
        )

    if requirement != "Clearly Defined":
        objections.append(
            "Customer may not yet have a clearly defined business requirement."
        )

    if buying_timeline == "More than 6 months":
        objections.append(
            "Customer may not have sufficient urgency to move forward."
        )


    # ---------------------------------------------
    # FOLLOW-UP PRIORITY
    # ---------------------------------------------

    if score >= 80:

        follow_up_priority = "Immediate"

    elif score >= 50:

        follow_up_priority = "Within 1 week"

    else:

        follow_up_priority = "Nurture"


    # ---------------------------------------------
    # RECOMMENDED ACTION
    # ---------------------------------------------

    if score >= 80:

        recommended_action = (
            "Initiate direct sales outreach and schedule a qualification "
            "conversation with the relevant decision maker."
        )

    elif score >= 50:

        recommended_action = (
            "Nurture the lead, clarify the requirement and identify "
            "the decision-making process."
        )

    else:

        recommended_action = (
            "Continue qualification before allocating significant "
            "sales resources."
        )


    # ---------------------------------------------
    # NEXT BEST ACTION
    # ---------------------------------------------

    if decision_maker == "No":

        next_action = (
            "Identify and connect with the relevant decision maker."
        )

    elif requirement != "Clearly Defined":

        next_action = (
            "Conduct a discovery conversation to understand the exact requirement."
        )

    elif existing_supplier == "Yes":

        next_action = (
            "Understand the current supplier relationship and identify "
            "a potential switching opportunity."
        )

    elif buying_timeline in [
        "3–6 months",
        "More than 6 months"
    ]:

        next_action = (
            "Establish a follow-up timeline and nurture the opportunity."
        )

    else:

        next_action = (
            "Proceed with direct sales engagement and move toward conversion."
        )


    # ---------------------------------------------
    # LEAD ATTRACTIVENESS
    # ---------------------------------------------

    if score >= 80:

        attractiveness = "Highly Attractive"

    elif score >= 50:

        attractiveness = "Moderately Attractive"

    else:

        attractiveness = "Low Attractiveness"


    return {
        "attractiveness": attractiveness,
        "strengths": strengths,
        "gaps": gaps,
        "objections": objections,
        "follow_up_priority": follow_up_priority,
        "recommended_action": recommended_action,
        "next_action": next_action
    }