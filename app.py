import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

from scoring import (
    calculate_lead_score,
    get_priority,
    get_recommendation
)

from database import (
    get_all_leads,
    save_lead,
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
    get_top_leads
)

from insights import generate_lead_insights

from lead_utils import (
    validate_lead,
    prepare_lead
)

from pipeline import (
    get_pipeline_stages,
    calculate_pipeline_value,
    count_by_stage,
    calculate_conversion_rate,
    calculate_win_rate,
    get_stalled_leads
)

from recommendations import (
    generate_sales_plan
)

from export import (
    prepare_export_dataframe
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LeadIQ",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 30px;
        border-radius: 18px;
        background: linear-gradient(135deg, #0f4c81, #2563a6);
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 17px;
        opacity: 0.92;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🎯 LeadIQ"
    )

    st.caption(
        "Sales Intelligence Platform"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "➕ Add Lead",
            "📋 Lead Database",
            "📊 Analytics",
            "🤖 AI Insights",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )


# =========================================================
# LOAD DATA
# =========================================================

leads = get_all_leads()
df = prepare_dataframe(leads)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>LeadIQ</h1>
            <p>
                Identify high-value prospects,
                prioritise sales opportunities,
                and take smarter next actions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    total_leads = len(leads)

    high_priority = (
        len(df[df["priority"] == "High Priority"])
        if not df.empty else 0
    )

    medium_priority = (
        len(df[df["priority"] == "Medium Priority"])
        if not df.empty else 0
    )

    low_priority = (
        len(df[df["priority"] == "Low Priority"])
        if not df.empty else 0
    )

    average_score = get_average_score(df)

    conversion_rate = calculate_conversion_rate(leads)

    pipeline_value = calculate_pipeline_value(leads)

    # KPI ROW
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Leads", total_leads)

    with c2:
        st.metric("High Priority", high_priority)

    with c3:
        st.metric(
            "Average Score",
            f"{average_score:.1f}/100"
        )

    with c4:
        st.metric(
            "Pipeline Value",
            f"₹{pipeline_value:,.0f} Cr"
        )

    c5, c6, c7 = st.columns(3)

    with c5:
        st.metric(
            "Medium Priority",
            medium_priority
        )

    with c6:
        st.metric(
            "Low Priority",
            low_priority
        )

    with c7:
        st.metric(
            "Conversion Rate",
            f"{conversion_rate:.1f}%"
        )

    st.divider()

    if df.empty:

        st.info(
            "No leads have been added yet. "
            "Go to Add Lead to create your first opportunity."
        )

    else:

        # -------------------------------------------------
        # CHARTS
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Priority Distribution")

            priority_data = get_priority_distribution(df)

            fig = px.pie(
                values=priority_data.values,
                names=priority_data.index,
                hole=0.55
            )

            fig.update_layout(
                margin=dict(
                    l=10,
                    r=10,
                    t=30,
                    b=10
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        with col2:

            st.subheader("Leads by Industry")

            industry_data = get_industry_distribution(df)

            fig = px.bar(
                x=industry_data.index,
                y=industry_data.values,
                labels={
                    "x": "Industry",
                    "y": "Leads"
                }
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        col3, col4 = st.columns(2)

        with col3:

            st.subheader("Sales Pipeline")

            status_data = get_status_distribution(df)

            fig = px.bar(
                x=status_data.index,
                y=status_data.values,
                labels={
                    "x": "Status",
                    "y": "Leads"
                }
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        with col4:

            st.subheader("Revenue Potential by Industry")

            revenue_data = get_revenue_by_industry(df)

            fig = px.bar(
                x=revenue_data.index,
                y=revenue_data.values,
                labels={
                    "x": "Industry",
                    "y": "Revenue"
                }
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        # -------------------------------------------------
        # TOP OPPORTUNITIES
        # -------------------------------------------------

        st.subheader("🔥 Top Sales Opportunities")

        top_leads = get_top_leads(df, 5)

        for _, lead in top_leads.iterrows():

            with st.container(border=True):

                c1, c2, c3 = st.columns([2, 1, 1])

                with c1:

                    st.markdown(
                        f"### {lead['company_name']}"
                    )

                    st.caption(
                        f"{lead['industry']} • "
                        f"{lead['location']}"
                    )

                with c2:

                    st.metric(
                        "Score",
                        f"{lead['score']:.0f}/100"
                    )

                with c3:

                    st.metric(
                        "Priority",
                        lead["priority"]
                    )

                st.write(
                    f"**Next Action:** "
                    f"{lead['recommendation']}"
                )


# =========================================================
# ADD LEAD
# =========================================================

elif page == "➕ Add Lead":

    st.title("➕ Add New Lead")

    st.write(
        "Enter prospect information to generate "
        "a qualification score and sales intelligence."
    )

    with st.form("lead_form"):

        st.subheader("Company Information")

        c1, c2 = st.columns(2)

        with c1:

            company_name = st.text_input(
                "Company Name *"
            )

            website = st.text_input(
                "Website"
            )

            industry = st.selectbox(
                "Industry",
                [
                    "FMCG",
                    "Pharmaceuticals",
                    "Manufacturing",
                    "Chemicals",
                    "Logistics",
                    "Technology",
                    "Retail",
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

        with c2:

            location = st.text_input(
                "Location"
            )

            annual_revenue = st.number_input(
                "Annual Revenue (₹ Crore)",
                min_value=0.0,
                step=100.0
            )

            lead_source = st.selectbox(
                "Lead Source",
                [
                    "Website",
                    "LinkedIn",
                    "Referral",
                    "Cold Outreach",
                    "Existing Network",
                    "Event",
                    "Other"
                ]
            )

            relationship = st.selectbox(
                "Current Relationship",
                [
                    "New Prospect",
                    "Existing Customer",
                    "Former Customer",
                    "Partner",
                    "Other"
                ]
            )

        st.subheader("Qualification Information")

        c3, c4 = st.columns(2)

        with c3:

            requirement = st.selectbox(
                "Requirement Clarity",
                [
                    "Clearly Defined",
                    "Partially Defined",
                    "Not Defined"
                ]
            )

            buying_timeline = st.selectbox(
                "Buying Timeline",
                [
                    "Immediate",
                    "Within 3 months",
                    "3–6 months",
                    "More than 6 months"
                ]
            )

        with c4:

            existing_supplier = st.selectbox(
                "Existing Supplier",
                [
                    "No",
                    "Yes",
                    "Unknown"
                ]
            )

            decision_maker = st.selectbox(
                "Decision Maker Identified",
                [
                    "Yes",
                    "No"
                ]
            )

        sales_notes = st.text_area(
            "Sales Notes"
        )

        submitted = st.form_submit_button(
            "🚀 Evaluate & Save Lead",
            width="stretch"
        )

    if submitted:

        lead = {
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
            "sales_notes": sales_notes
        }

        errors = validate_lead(lead)

        if errors:

            for error in errors:
                st.error(error)

        else:

            lead = prepare_lead(lead)

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

            lead["score"] = score
            lead["priority"] = priority
            lead["recommendation"] = recommendation
            lead["status"] = "New"

            save_lead(lead)

            st.success(
                "Lead successfully evaluated and saved!"
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Lead Score",
                    f"{score}/100"
                )

            with c2:
                st.metric(
                    "Priority",
                    priority
                )

            with c3:
                st.metric(
                    "Opportunity",
                    generate_sales_plan(
                        lead
                    )["opportunity_type"]
                )

            st.info(recommendation)


# =========================================================
# LEAD DATABASE
# =========================================================

elif page == "📋 Lead Database":

    st.title("📋 Lead Database")

    leads = get_all_leads()

    if leads is None or leads.empty:

        st.info("No leads available.")

    else:

        df = prepare_dataframe(leads)

        c1, c2, c3 = st.columns(3)

        with c1:

            search = st.text_input(
                "🔎 Search Company"
            )

        with c2:

            priority_filter = st.selectbox(
                "Priority",
                [
                    "All",
                    "High Priority",
                    "Medium Priority",
                    "Low Priority"
                ]
            )

        with c3:

            status_filter = st.selectbox(
                "Status",
                ["All"] + get_pipeline_stages()
            )

        filtered_df = df.copy()

        if search:

            filtered_df = filtered_df[
                filtered_df["company_name"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if priority_filter != "All":

            filtered_df = filtered_df[
                filtered_df["priority"] == priority_filter
            ]

        if status_filter != "All":

            filtered_df = filtered_df[
                filtered_df["status"] == status_filter
            ]

        st.write(
            f"Showing {len(filtered_df)} lead(s)"
        )

        display_columns = [
            "id",
            "company_name",
            "industry",
            "annual_revenue",
            "score",
            "priority",
            "status",
            "buying_timeline"
        ]

        st.dataframe(
            filtered_df[display_columns],
            width="stretch",
            hide_index=True
        )

        st.divider()

        # STATUS

        st.subheader("Update Lead Status")

        lead_options = {
            f"{lead['id']} — {lead['company_name']}":
            lead["id"]
            for _, lead in leads.iterrows()
        }

        selected_lead = st.selectbox(
            "Select Lead",
            list(lead_options.keys())
        )

        selected_id = lead_options[selected_lead]

        new_status = st.selectbox(
            "New Status",
            get_pipeline_stages()
        )

        if st.button(
            "Update Status",
            width="stretch"
        ):

            update_lead_status(
                selected_id,
                new_status
            )

            st.success(
                "Lead status updated successfully."
            )

            st.rerun()

        # DELETE

        st.subheader("Delete Lead")

        delete_option = st.selectbox(
            "Select Lead to Delete",
            list(lead_options.keys()),
            key="delete_lead"
        )

        delete_id = lead_options[delete_option]

        if st.button(
            "🗑️ Delete Selected Lead",
            width="stretch"
        ):

            delete_lead(delete_id)

            st.success(
                "Lead deleted successfully."
            )

            st.rerun()

        # EXPORT

        st.subheader("Export Data")

        export_df = prepare_export_dataframe(
            filtered_df.to_dict("records")
        )

        csv_data = export_df.to_csv(index=False)

        st.download_button(
            "⬇️ Download CSV",
            csv_data,
            file_name="leadiq_leads.csv",
            mime="text/csv",
            width="stretch"
        )

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            export_df.to_excel(
                writer,
                index=False,
                sheet_name="LeadIQ Leads"
            )

        st.download_button(
            "⬇️ Download Excel",
            excel_buffer.getvalue(),
            file_name="leadiq_leads.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch"
        )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    st.title("📊 Sales Analytics")

    leads = get_all_leads()

    df = prepare_dataframe(leads)

    if df.empty:

        st.info(
            "Add leads to generate analytics."
        )

    else:

        conversion_rate = calculate_conversion_rate(leads)

        win_rate = calculate_win_rate(leads)

        pipeline_value = calculate_pipeline_value(leads)

        stalled = get_stalled_leads(leads)

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Average Score",
                f"{get_average_score(df):.1f}"
            )

        with c2:

            st.metric(
                "Pipeline Value",
                f"₹{pipeline_value:,.0f} Cr"
            )

        with c3:

            st.metric(
                "Conversion Rate",
                f"{conversion_rate:.1f}%"
            )

        with c4:

            st.metric(
                "Win Rate",
                f"{win_rate:.1f}%"
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "Lead Score Distribution"
            )

            scores = get_score_distribution(df)

            fig = px.histogram(
                scores,
                nbins=10
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        with col2:

            st.subheader(
                "Industry Revenue Potential"
            )

            revenue = get_revenue_by_industry(df)

            fig = px.bar(
                x=revenue.index,
                y=revenue.values
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        st.subheader(
            "Pipeline Stage Analysis"
        )

        stage_counts = count_by_stage(leads)

        pipeline_df = pd.DataFrame(
            {
                "Stage": list(stage_counts.keys()),
                "Leads": list(stage_counts.values())
            }
        )

        fig = px.funnel(
            pipeline_df,
            y="Stage",
            x="Leads"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.subheader(
            "⚠️ Leads Requiring Attention"
        )

        if stalled is not None and not stalled.empty:

            for _, lead in stalled.iterrows():

                st.write(
                    f"**{lead['company_name']}** — "
                    f"Score: {lead['score']} — "
                    f"Status: {lead['status']}"
                )

        else:

            st.success(
                "No high-value stalled leads identified."
            )


# =========================================================
# AI INSIGHTS
# =========================================================

elif page == "🤖 AI Insights":

    st.title("🤖 Lead Intelligence")

    st.write(
        "Turn lead information into actionable sales decisions."
    )

    leads = get_all_leads()

    if leads is None or leads.empty:

        st.info(
            "Add leads to generate intelligence."
        )

    else:

        lead_options = {
            f"{lead['company_name']} "
            f"(Score: {lead['score']})":
            lead
            for _, lead in leads.iterrows()
        }

        selected_label = st.selectbox(
            "Select a lead",
            list(lead_options.keys())
        )

        lead = lead_options[selected_label]

        intelligence = generate_lead_insights(lead)

        sales_plan = generate_sales_plan(lead)

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Lead Score",
                f"{float(lead['score']):.0f}/100"
            )

        with c2:

            st.metric(
                "Attractiveness",
                intelligence["attractiveness"]
            )

        with c3:

            st.metric(
                "Follow-up",
                intelligence["follow_up_priority"]
            )

        with c4:

            st.metric(
                "Opportunity Type",
                sales_plan["opportunity_type"]
            )

        st.subheader(
            "💪 Why This Lead Is Attractive"
        )

        if intelligence["strengths"]:

            for item in intelligence["strengths"]:
                st.success(f"✓ {item}")

        else:

            st.info(
                "No major strengths identified."
            )

        st.subheader(
            "🔎 Qualification Gaps"
        )

        if intelligence["gaps"]:

            for item in intelligence["gaps"]:
                st.warning(f"• {item}")

        else:

            st.success(
                "No major qualification gaps identified."
            )

        st.subheader(
            "⚠️ Potential Objections"
        )

        if intelligence["objections"]:

            for item in intelligence["objections"]:
                st.info(f"• {item}")

        else:

            st.success(
                "No major objections identified."
            )

        st.subheader(
            "🎯 Recommended Sales Plan"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write("**Contact Strategy**")

            st.info(
                sales_plan["contact_strategy"]
            )

            st.write("**Follow-up Frequency**")

            st.info(
                sales_plan["follow_up_frequency"]
            )

        with c2:

            st.write("**Recommended Action**")

            st.success(
                intelligence["recommended_action"]
            )

            st.write("**Next Best Action**")

            st.success(
                intelligence["next_action"]
            )

        st.subheader(
            "📌 Information to Collect"
        )

        information = sales_plan[
            "information_to_collect"
        ]

        if information:

            for item in information:
                st.write(f"• {item}")

        else:

            st.success(
                "Required qualification information is complete."
            )


# =========================================================
# SETTINGS
# =========================================================

elif page == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.subheader(
        "LeadIQ Configuration"
    )

    st.write(
        "Current scoring model"
    )

    st.info(
        "Rule-based lead qualification model using "
        "industry fit, company size, revenue, "
        "decision-maker availability, buying timeline, "
        "requirement clarity and supplier status."
    )

    st.subheader(
        "Pipeline Stages"
    )

    st.write(
        " → ".join(get_pipeline_stages())
    )

    st.subheader(
        "Project Information"
    )

    st.write(
        "LeadIQ is a sales intelligence prototype "
        "built using Python, Streamlit, Pandas and Plotly."
    )

    st.caption(
        "LeadIQ • Sales Intelligence Platform"
    )
