import streamlit as st
import pandas as pd

from scoring import (
    calculate_lead_score,
    get_priority,
    get_recommendation
)

from database import (
    initialize_database,
    save_lead,
    get_all_leads,
    delete_lead,
    update_lead_status
)

from analytics import (
    prepare_dataframe,
    get_priority_distribution,
    get_industry_distribution,
    get_average_score,
    get_total_revenue,
    get_revenue_by_industry,
    get_score_distribution,
    get_status_distribution,
    get_top_leads,
    get_attention_leads
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LeadIQ",
    page_icon="🎯",
    layout="wide"
)

initialize_database()


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 1.5rem 2rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #172554, #2563eb);
    color: white;
    margin-bottom: 2rem;
}

.hero h1 {
    margin-bottom: 0.3rem;
    font-size: 2.5rem;
}

.hero p {
    font-size: 1.05rem;
    margin-bottom: 0;
    opacity: 0.9;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}

.recommendation {
    padding: 1rem;
    border-radius: 12px;
    background-color: #eff6ff;
    border-left: 5px solid #2563eb;
    margin-top: 1rem;
}

.insight-card {
    padding: 1.2rem;
    border-radius: 14px;
    background-color: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>🎯 LeadIQ</h1>
    <p>Lead Intelligence & Sales Prioritisation Platform</p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("LeadIQ")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "➕ Add Lead",
            "📋 Lead Database",
            "📊 Analytics",
            "🤖 AI Insights"
        ]
    )

    st.divider()

    st.caption("LeadIQ v1.0")
    st.caption("Sales intelligence prototype")


# ==================================================
# DASHBOARD
# ==================================================

if page == "🏠 Dashboard":

    st.header("Sales Intelligence Dashboard")

    leads = get_all_leads()

    df = prepare_dataframe(leads)

    total_leads = len(df)

    if not df.empty:

        high_priority = (
            df["priority"] == "High Priority"
        ).sum()

        medium_priority = (
            df["priority"] == "Medium Priority"
        ).sum()

        low_priority = (
            df["priority"] == "Low Priority"
        ).sum()

        average_score = get_average_score(df)

        potential_revenue = get_total_revenue(df)

    else:

        high_priority = 0
        medium_priority = 0
        low_priority = 0
        average_score = 0
        potential_revenue = 0


    # --------------------------------------------------
    # MAIN METRICS
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Leads",
        total_leads
    )

    col2.metric(
        "High Priority",
        high_priority
    )

    col3.metric(
        "Average Score",
        f"{average_score:.1f}"
    )

    col4.metric(
        "Potential Revenue",
        f"₹{potential_revenue:,.0f} Cr"
    )


    st.divider()


    # --------------------------------------------------
    # SECONDARY METRICS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Medium Priority",
        medium_priority
    )

    col2.metric(
        "Low Priority",
        low_priority
    )

    if total_leads > 0:

        high_percentage = (
            high_priority / total_leads
        ) * 100

    else:

        high_percentage = 0

    col3.metric(
        "High Priority %",
        f"{high_percentage:.0f}%"
    )


    st.divider()


    # --------------------------------------------------
    # DASHBOARD CHARTS
    # --------------------------------------------------

    if not df.empty:

        st.subheader("Lead Overview")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Priority Distribution")

            priority_data = get_priority_distribution(df)

            st.bar_chart(
                priority_data
            )

        with col2:

            st.markdown("#### Leads by Industry")

            industry_data = get_industry_distribution(df)

            st.bar_chart(
                industry_data
            )


        st.divider()


        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Sales Pipeline")

            status_data = get_status_distribution(df)

            st.bar_chart(
                status_data
            )

        with col2:

            st.markdown("#### Revenue Potential by Industry")

            revenue_data = get_revenue_by_industry(df)

            st.bar_chart(
                revenue_data
            )


        st.divider()


        # --------------------------------------------------
        # TOP OPPORTUNITIES
        # --------------------------------------------------

        st.subheader("🔥 Top Sales Opportunities")

        top_leads = get_top_leads(
            df,
            5
        )

        for _, lead in top_leads.iterrows():

            with st.container(border=True):

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"**{lead['company_name']}**"
                    )

                    st.caption(
                        lead["industry"]
                    )

                with col2:

                    st.metric(
                        "Score",
                        f"{lead['score']:.0f}/100"
                    )

                with col3:

                    st.metric(
                        "Priority",
                        lead["priority"]
                    )


    else:

        st.info(
            "No leads have been added yet. "
            "Go to 'Add Lead' to create your first lead."
        )


# ==================================================
# ADD LEAD
# ==================================================

elif page == "➕ Add Lead":

    st.header("Add New Lead")

    st.write(
        "Enter information about the prospect to generate "
        "a qualification assessment."
    )

    st.divider()


    # --------------------------------------------------
    # COMPANY INFORMATION
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">🏢 Company Information</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        company_name = st.text_input(
            "Company Name",
            placeholder="e.g. ITC Limited"
        )

        industry = st.selectbox(
            "Industry",
            [
                "FMCG",
                "Chemicals",
                "Logistics",
                "Manufacturing",
                "Pharmaceuticals",
                "Technology",
                "Other"
            ]
        )

        company_size = st.selectbox(
            "Company Size",
            [
                "Small",
                "Medium",
                "Large",
                "Enterprise"
            ]
        )

    with col2:

        website = st.text_input(
            "Company Website",
            placeholder="https://example.com"
        )

        location = st.text_input(
            "Company Location",
            placeholder="e.g. Delhi, Mumbai, Bengaluru"
        )

        annual_revenue = st.number_input(
            "Estimated Annual Revenue (₹ Crore)",
            min_value=0.0,
            step=100.0
        )


    st.divider()


    # --------------------------------------------------
    # BUYING INFORMATION
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">🛒 Buying Information</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        requirement = st.selectbox(
            "Requirement Clarity",
            [
                "Clearly Defined",
                "Partially Defined",
                "Not Defined"
            ]
        )

        buying_timeline = st.selectbox(
            "Expected Buying Timeline",
            [
                "Immediate",
                "Within 3 months",
                "3–6 months",
                "More than 6 months"
            ]
        )

    with col2:

        existing_supplier = st.selectbox(
            "Existing Supplier",
            [
                "Yes",
                "No",
                "Unknown"
            ]
        )

        decision_maker = st.selectbox(
            "Decision Maker Identified?",
            [
                "Yes",
                "No"
            ]
        )


    st.divider()


    # --------------------------------------------------
    # SALES INFORMATION
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">🤝 Sales Information</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        lead_source = st.selectbox(
            "Lead Source",
            [
                "Website",
                "LinkedIn",
                "Referral",
                "Cold Outreach",
                "Trade Show",
                "Database",
                "Other"
            ]
        )

    with col2:

        relationship = st.selectbox(
            "Current Relationship",
            [
                "New Prospect",
                "Initial Contact",
                "Engaged",
                "Existing Customer"
            ]
        )


    notes = st.text_area(
        "Sales Notes",
        placeholder="Add useful information about this prospect..."
    )


    st.divider()


    # --------------------------------------------------
    # EVALUATE AND SAVE
    # --------------------------------------------------

    if st.button(
        "🎯 Evaluate & Save Lead",
        use_container_width=True
    ):

        if not company_name.strip():

            st.warning(
                "Please enter a company name."
            )

        else:

            score = calculate_lead_score(
                industry,
                company_size,
                annual_revenue,
                decision_maker,
                buying_timeline,
                requirement,
                existing_supplier
            )

            priority = get_priority(score)

            recommendation = get_recommendation(score)


            lead_data = {

                "company_name": company_name,
                "website": website,
                "industry": industry,
                "company_size": company_size,
                "location": location,
                "annual_revenue": annual_revenue,
                "requirement": requirement,
                "buying_timeline": buying_timeline,
                "existing_supplier": existing_supplier,
                "decision_maker": decision_maker,
                "lead_source": lead_source,
                "relationship": relationship,
                "sales_notes": notes,
                "score": score,
                "priority": priority,
                "recommendation": recommendation,
                "status": "New"

            }


            save_lead(
                lead_data
            )


            st.success(
                f"Lead saved successfully! "
                f"{company_name} received a score of {score}/100."
            )


            st.divider()


            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Lead Score",
                f"{score}/100"
            )

            col2.metric(
                "Priority",
                priority
            )


            if score >= 80:

                potential = "High"

            elif score >= 50:

                potential = "Medium"

            else:

                potential = "Low"


            col3.metric(
                "Sales Potential",
                potential
            )


            st.markdown(
                f"""
                <div class="recommendation">
                    <strong>Recommended Action</strong><br><br>
                    {recommendation}
                </div>
                """,
                unsafe_allow_html=True
            )


# ==================================================
# LEAD DATABASE
# ==================================================

elif page == "📋 Lead Database":

    st.header("Lead Database")

    leads = get_all_leads()

    if not leads:

        st.info(
            "No leads available yet."
        )

    else:

        df = prepare_dataframe(
            leads
        )


        # SEARCH

        search = st.text_input(
            "🔎 Search Company",
            placeholder="Type company name..."
        )


        if search:

            df = df[
                df["company_name"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]


        # FILTERS

        col1, col2, col3 = st.columns(3)

        with col1:

            priority_filter = st.selectbox(
                "Priority",
                [
                    "All",
                    "High Priority",
                    "Medium Priority",
                    "Low Priority"
                ]
            )

        with col2:

            industry_filter = st.selectbox(
                "Industry",
                ["All"] +
                sorted(
                    df["industry"].unique().tolist()
                )
            )

        with col3:

            status_filter = st.selectbox(
                "Status",
                [
                    "All",
                    "New",
                    "Contacted",
                    "Qualified",
                    "Proposal",
                    "Won",
                    "Lost"
                ]
            )


        if priority_filter != "All":

            df = df[
                df["priority"] ==
                priority_filter
            ]


        if industry_filter != "All":

            df = df[
                df["industry"] ==
                industry_filter
            ]


        if status_filter != "All":

            df = df[
                df["status"] ==
                status_filter
            ]


        # SORTING

        sort_option = st.selectbox(
            "Sort Leads",
            [
                "Highest Score",
                "Lowest Score",
                "Newest First",
                "Oldest First"
            ]
        )


        if sort_option == "Highest Score":

            df = df.sort_values(
                "score",
                ascending=False
            )

        elif sort_option == "Lowest Score":

            df = df.sort_values(
                "score",
                ascending=True
            )

        elif sort_option == "Newest First":

            df = df.sort_values(
                "created_at",
                ascending=False
            )

        elif sort_option == "Oldest First":

            df = df.sort_values(
                "created_at",
                ascending=True
            )


        st.divider()


        st.subheader(
            f"{len(df)} lead(s) found"
        )


        display_df = df[
            [
                "id",
                "company_name",
                "industry",
                "location",
                "score",
                "priority",
                "status"
            ]
        ].copy()


        display_df.columns = [
            "ID",
            "Company",
            "Industry",
            "Location",
            "Score",
            "Priority",
            "Status"
        ]


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        # MANAGE LEAD

        st.subheader("Manage Lead")


        selected_id = st.number_input(
            "Enter Lead ID",
            min_value=1,
            step=1
        )


        col1, col2 = st.columns(2)


        with col1:

            new_status = st.selectbox(
                "Update Status",
                [
                    "New",
                    "Contacted",
                    "Qualified",
                    "Proposal",
                    "Won",
                    "Lost"
                ]
            )


            if st.button(
                "📌 Update Status",
                use_container_width=True
            ):

                update_lead_status(
                    selected_id,
                    new_status
                )

                st.success(
                    "Lead status updated."
                )

                st.rerun()


        with col2:

            if st.button(
                "🗑️ Delete Lead",
                use_container_width=True
            ):

                delete_lead(
                    selected_id
                )

                st.success(
                    "Lead deleted successfully."
                )

                st.rerun()


# ==================================================
# ANALYTICS
# ==================================================

elif page == "📊 Analytics":

    st.header("Lead Analytics")

    leads = get_all_leads()

    df = prepare_dataframe(
        leads
    )


    if df.empty:

        st.info(
            "Add leads to generate analytics."
        )

    else:

        st.subheader(
            "📊 Portfolio Overview"
        )


        col1, col2, col3, col4 = st.columns(4)


        col1.metric(
            "Total Leads",
            len(df)
        )

        col2.metric(
            "Average Score",
            f"{get_average_score(df):.1f}"
        )

        col3.metric(
            "Potential Revenue",
            f"₹{get_total_revenue(df):,.0f} Cr"
        )

        col4.metric(
            "High Priority",
            int(
                (
                    df["priority"] ==
                    "High Priority"
                ).sum()
            )
        )


        st.divider()


        # PRIORITY

        st.subheader(
            "Priority Distribution"
        )

        priority_data = get_priority_distribution(
            df
        )

        st.bar_chart(
            priority_data
        )


        st.divider()


        # INDUSTRY

        st.subheader(
            "Industry Distribution"
        )

        industry_data = get_industry_distribution(
            df
        )

        st.bar_chart(
            industry_data
        )


        st.divider()


        # REVENUE

        st.subheader(
            "Revenue Potential by Industry"
        )

        revenue_data = get_revenue_by_industry(
            df
        )

        st.bar_chart(
            revenue_data
        )


        st.divider()


        # STATUS

        st.subheader(
            "Sales Pipeline"
        )

        status_data = get_status_distribution(
            df
        )

        st.bar_chart(
            status_data
        )


        st.divider()


        # SCORES

        st.subheader(
            "Lead Score Distribution"
        )

        score_data = get_score_distribution(
            df
        )

        st.line_chart(
            score_data
        )


# ==================================================
# AI INSIGHTS
# ==================================================

elif page == "🤖 AI Insights":

    st.header("🤖 Lead Intelligence")

    leads = get_all_leads()

    df = prepare_dataframe(
        leads
    )


    if df.empty:

        st.info(
            "Add leads to generate intelligence."
        )

    else:

        st.subheader(
            "🔥 Top Sales Opportunities"
        )


        top_leads = get_top_leads(
            df,
            5
        )


        for _, lead in top_leads.iterrows():

            with st.container(border=True):

                col1, col2, col3 = st.columns(3)


                with col1:

                    st.write(
                        f"### {lead['company_name']}"
                    )

                    st.caption(
                        lead["industry"]
                    )


                with col2:

                    st.metric(
                        "Score",
                        f"{lead['score']:.0f}/100"
                    )


                with col3:

                    st.metric(
                        "Priority",
                        lead["priority"]
                    )


                st.write(
                    f"**Buying Timeline:** "
                    f"{lead['buying_timeline']}"
                )

                st.write(
                    f"**Requirement:** "
                    f"{lead['requirement']}"
                )

                st.write(
                    f"**Recommendation:** "
                    f"{lead['recommendation']}"
                )


        st.divider()


        st.subheader(
            "⚠️ Leads Requiring Attention"
        )


        attention_leads = get_attention_leads(
            df,
            5
        )


        for _, lead in attention_leads.iterrows():

            st.write(
                f"**{lead['company_name']}** — "
                f"Score: {lead['score']:.0f}/100 — "
                f"{lead['priority']}"
            )