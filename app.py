from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px                                           

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="InternTrack AI",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 InternTrack AI")

st.sidebar.info(
    """
    Features

    ✅ Internship Application Tracker

    ✅ Follow-Up Reminders

    ✅ Interview Preparation

    ✅ Application Analytics

    ✅ Resume Match Analyzer

    ✅ Career Insights
    """
)

st.title("🚀 InternTrack AI")

st.markdown("""
Your personal internship search dashboard.

Track applications, monitor interview progress,
manage follow-ups, analyze opportunities, and stay
organized throughout your internship journey.

Built to help students apply smarter, stay consistent,
and improve their chances of landing great opportunities.
""")

st.subheader(
    "Track • Analyze • Prepare • Succeed"
)

# -----------------------------
# LOAD DATA
# -----------------------------

try:
    df = pd.read_csv("applications.csv")

    if "Date Applied" in df.columns:
        df["Date Applied"] = df["Date Applied"].astype(str)

except:
    df = pd.DataFrame(
        columns=[
            "Company",
            "Role",
            "Date Applied",
            "Status",
            "Source",
            "Priority",
            "Application Link",
            "Notes"
        ]
    )

# -----------------------------
# ADD APPLICATION
# -----------------------------

st.header("➕ Add Application")

company = st.text_input("Company Name")

role = st.text_input("Role")

status = st.selectbox(
    "Status",
   [
    "Applied",
    "OA",
    "Interview Scheduled",
    "Interview Completed",
    "Rejected",
    "Offer"
]
)

source = st.selectbox(
    "Source",
   [
    "LinkedIn",
    "Referral",
    "Wellfound",
    "Company Website",
    "Internshala",
    "Campus Placement",
    "Other"
]
)

priority = st.selectbox(
    "Priority",
    [
        "High",
        "Medium",
        "Low"
    ]
)

application_link = st.text_input(
    "Application Link"
)

notes = st.text_area("Notes")

if st.button("Save Application"):

    if not company.strip() or not role.strip():
        st.error("Please enter Company Name and Role.")
        st.stop()

    new_row = pd.DataFrame(
        [[
            company,
            role,
            str(datetime.now().date()),
            status,
            source,
            priority,
            application_link,
            notes
        ]],
        columns=[
            "Company",
            "Role",
            "Date Applied",
            "Status",
            "Source",
            "Priority",
            "Application Link",
            "Notes"
        ]
    )

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_csv(
        "applications.csv",
        index=False
    )

    st.success(
        "Application Saved Successfully!"
    )

# -----------------------------
# DASHBOARD
# -----------------------------

st.header("📊 Dashboard")

total_apps = len(df)

interviews = len(
    df[
        df["Status"].isin(
            ["Interview Scheduled", "Interview Completed"]
        )
    ]
)

offers = len(
    df[df["Status"] == "Offer"]
)

rejections = len(
    df[df["Status"] == "Rejected"]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Applications",
    total_apps
)

col2.metric(
    "Interviews",
    interviews
)

col3.metric(
    "Offers",
    offers
)

col4.metric(
    "Rejections",
    rejections
)

# -----------------------------
# FOLLOW UPS
# -----------------------------

st.header("⏰ Follow-Up Reminders")

if not df.empty:

    today = datetime.now().date()

    reminders_found = False

    for index, row in df.iterrows():

        try:

            applied_date = pd.to_datetime(
                row["Date Applied"]
            ).date()

            days = (
                today - applied_date
            ).days

            if (
                days >= 5 and
                row["Status"] == "Applied"
            ):

                st.warning(
                    f"Follow up with {row['Company']} ({days} days ago)"
                )

                reminders_found = True

        except:
            pass

    if not reminders_found:

        st.success(
            "No pending follow-ups."
        )

# -----------------------------
# STATUS CHART
# -----------------------------

st.header(
    "📈 Application Status Distribution"
)

if not df.empty:

    status_count = (
        df["Status"]
        .value_counts()
        .reset_index()
    )

    status_count.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        status_count,
        names="Status",
        values="Count",
        title="Application Breakdown"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# SEARCH APPLICATIONS
# -----------------------------

st.header("🔍 Search Applications")

search_term = st.text_input(
    "Search by Company Name"
)

if search_term:

    filtered_df = df[
        df["Company"]
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        filtered_df.astype(str),
        use_container_width=True
    )

# -----------------------------
# UPDATE STATUS
# -----------------------------

st.header("✏️ Update Application Status")

if not df.empty:

    selected_company = st.selectbox(
        "Select Company",
        df["Company"]
    )

    updated_status = st.selectbox(
    "New Status",
    [
        "Applied",
        "OA",
        "Interview Scheduled",
        "Interview Completed",
        "Rejected",
        "Offer"
    ]
)

    if st.button("Update Status"):

        df.loc[
            df["Company"] == selected_company,
            "Status"
        ] = updated_status

        df.to_csv(
            "applications.csv",
            index=False
        )

        st.success(
            "Status Updated Successfully!"
        )

# -----------------------------
# DELETE APPLICATION
# -----------------------------

st.header("🗑 Delete Application")

if not df.empty:

    delete_company = st.selectbox(
        "Select Company To Delete",
        df["Company"],
        key="delete_company"
    )

    if st.button("Delete Application"):

        df = df[
            df["Company"] != delete_company
        ]

        df.to_csv(
            "applications.csv",
            index=False
        )

        st.success(
            "Application Deleted Successfully!"
        )

        st.rerun()

# -----------------------------
# INSIGHTS
# -----------------------------

st.header("💡 Insights")

if not df.empty:

    try:

        most_used_source = (
            df["Source"]
            .mode()[0]
        )

        st.info(
            f"Most Used Source: {most_used_source}"
        )

    except:
        pass

    high_priority_count = len(
        df[
            df["Priority"] == "High"
        ]
    )

    st.info(
        f"High Priority Applications: {high_priority_count}"
    )

    if total_apps > 0:

        interview_rate = (
            interviews / total_apps
        ) * 100

        offer_rate = (
            offers / total_apps
        ) * 100

        st.info(
            f"Interview Rate: {interview_rate:.1f}%"
        )

        st.info(
            f"Offer Rate: {offer_rate:.1f}%"
        )

# -----------------------------
# FOLLOW-UP EMAIL GENERATOR
# -----------------------------

st.header("✉️ AI Follow-Up Email Generator")

if not df.empty:

    selected_company = st.selectbox(
        "Choose Company",
        df["Company"],
        key="email_company"
    )

    selected_role = df[
        df["Company"] == selected_company
    ]["Role"].iloc[0]

    if st.button("Generate Email"):

        email = f"""
Subject: Follow-up on {selected_role} Application

Hi Team,

I hope you're doing well.

I recently applied for the {selected_role} position at {selected_company} and wanted to check if there are any updates regarding my application.

I remain very interested in the opportunity and would be excited to contribute to your team.

Thank you for your time and consideration.

Best regards,
Nimisha Sharma
"""

        st.text_area(
            "Generated Email",
            email,
            height=250
        )

# -----------------------------
# INTERVIEW QUESTION GENERATOR
# -----------------------------

st.header("🎯 Interview Question Generator")

if not df.empty:

    interview_company = st.selectbox(
        "Select Company",
        df["Company"],
        key="interview_company"
    )

    interview_role = df[
        df["Company"] == interview_company
    ]["Role"].iloc[0]

    if st.button("Generate Interview Questions"):

        questions = f"""
1. Tell me about yourself.

2. Why do you want to join {interview_company}?

3. Why are you interested in the {interview_role} role?

4. How would you improve a product offered by {interview_company}?

5. Describe a product you admire and why.

6. How do you prioritize features?

7. Tell me about a project you worked on.

8. How would you handle conflicting stakeholder requests?

9. What metrics would you track for a product?

10. Do you have any questions for us?
"""

        st.text_area(
            "Generated Questions",
            questions,
            height=300
        )

# -----------------------------
# APPLICATION HEALTH SCORE
# -----------------------------

st.header("📈 Application Health Score")

if not df.empty:

    total_apps = len(df)

    interviews = len(
        df[
            df["Status"].isin(
                ["Interview Scheduled", "Interview Completed"]
            )
        ]
    )

    offers = len(
        df[df["Status"] == "Offer"]
    )

    score = 0

    score += min(total_apps * 2, 40)

    score += interviews * 10

    score += offers * 20

    score = min(score, 100)

    st.metric(
        "Health Score",
        f"{score}/100"
    )

    if score >= 80:

        st.success(
            "Excellent Application Pipeline 🚀"
        )

    elif score >= 50:

        st.warning(
            "Good Progress - Keep Applying"
        )

    else:

        st.error(
            "Needs Attention - Increase Applications"
        )

# -----------------------------
# AI RESUME MATCH ANALYZER
# -----------------------------

st.header("🤖 AI Resume Match Analyzer")

skills = st.text_area(
    "Your Skills",
    placeholder="Python, SQL, Streamlit, Product Management"
)

job_description = st.text_area(
    "Paste Job Description"
)

if st.button("Analyze Match"):

    if skills and job_description:

        with st.spinner("Analyzing..."):

            vectorizer = TfidfVectorizer()

            vectors = vectorizer.fit_transform(
                [skills, job_description]
            )

            try:

                similarity = cosine_similarity(
                    vectors[0:1],
                    vectors[1:2]
                )[0][0]

            except:

                similarity = 0

            score = max(
                30,
                round(similarity * 100)
            )
        

            st.metric(
                "Resume Match Score",
                f"{score}%"
            )

            if score >= 75:

                st.success(
                    "Strong match for this role."
                )

            elif score >= 50:

                st.warning(
                    "Moderate match. Consider highlighting relevant skills."
                )

            else:

                st.error(
                    "Low match. Add more relevant keywords from the job description."
                )

    else:

        st.warning(
            "Please enter both fields."
        )


# -----------------------------
# APPLICATION TABLE
# -----------------------------
st.download_button(
    label="📥 Download Applications CSV",
    data=df.to_csv(index=False),
    file_name="applications.csv",
    mime="text/csv"
)

st.header("📋 All Applications")

display_df = df.copy()

display_df = display_df.astype(str)

st.dataframe(
    display_df,
    use_container_width=True
)
st.markdown("---")

st.caption(
    "Built by Nimisha Sharma | InternTrack AI"
)