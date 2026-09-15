import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys
import sqlite3

# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR))

PROCESSED_DIR = BASE_DIR / "data" / "processed"
DATABASE_PATH = BASE_DIR / "data" / "crime_reports.db"

from src.single_report_analyzer import analyze_crime_report
from src.nlp_analysis import clean_text, extract_keywords


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Crime Report Analysis",
    layout="wide"
)

# ============================================================
# DASHBOARD HEADER
# ============================================================

st.title("AI-Powered Crime Report Analysis")
st.caption(
    "An intelligent system for analyzing cybercrime reports, "
    "detecting patterns, and generating AI-powered insights."
)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def load_database_records():

    if not DATABASE_PATH.exists():
        return pd.DataFrame()

    connection = sqlite3.connect(DATABASE_PATH)

    query = """
        SELECT
            report_id,
            category,
            sub_category,
            crime_type,
            summary,
            modus_operandi,
            platforms,
            entities,
            location,
            temporal_information,
            financial_loss,
            severity
        FROM crime_reports
        ORDER BY report_id
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


def get_database_record(report_id):

    if not DATABASE_PATH.exists():
        return None

    connection = sqlite3.connect(DATABASE_PATH)

    query = """
        SELECT
            report_id,
            category,
            sub_category,
            crime_type,
            summary,
            modus_operandi,
            platforms,
            entities,
            location,
            temporal_information,
            financial_loss,
            severity
        FROM crime_reports
        WHERE report_id = ?
    """

    result = pd.read_sql_query(
        query,
        connection,
        params=(int(report_id),)
    )

    connection.close()

    if result.empty:
        return None

    return result.iloc[0]


# ============================================================
# LOAD DATA
# ============================================================

category_df = pd.read_csv(
    PROCESSED_DIR / "crime_category_trends.csv"
)

subcategory_df = pd.read_csv(
    PROCESSED_DIR / "crime_subcategory_trends.csv"
)

length_df = pd.read_csv(
    PROCESSED_DIR / "crime_report_length_statistics.csv"
)

llm_severity_df = pd.read_csv(
    PROCESSED_DIR / "llm_severity_distribution.csv"
)

llm_crime_df = pd.read_csv(
    PROCESSED_DIR / "llm_crime_type_distribution.csv"
)

reports_df = pd.read_csv(
    PROCESSED_DIR / "cleaned_crime_reports.csv"
)


# ============================================================
# CALCULATE KEY VALUES
# ============================================================

total_records = int(
    category_df["count"].sum()
)

top_category = category_df.iloc[0]

top_subcategory = subcategory_df.iloc[0]

average_length = float(
    length_df.loc[
        length_df["metric"] == "Average Length",
        "value"
    ].iloc[0]
)

median_length = float(
    length_df.loc[
        length_df["metric"] == "Median Length",
        "value"
    ].iloc[0]
)

llm_total = int(
    llm_severity_df["count"].sum()
)

high_severity = llm_severity_df[
    llm_severity_df["severity"]
    .astype(str)
    .str.lower() == "high"
]

high_count = (
    int(high_severity["count"].iloc[0])
    if not high_severity.empty
    else 0
)

high_percentage = (
    high_count / llm_total * 100
    if llm_total > 0
    else 0
)


# ============================================================
# TITLE
# ============================================================

#st.title("AI-Powered Crime Report Analysis")

st.subheader(
    "Crime Trend Detection and Analysis Using Large Language Models"
)

st.write(
    "This dashboard presents statistical analysis of crime reports "
    "along with structured information extracted using Natural "
    "Language Processing and Large Language Models."
)


# ============================================================
# DATASET OVERVIEW
# ============================================================

st.header("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Crime Reports",
        f"{total_records:,}"
    )

with col2:

    st.metric(
        "Crime Categories",
        f"{len(category_df)}"
    )

with col3:

    st.metric(
        "Average Report Length",
        f"{average_length:.2f}"
    )

with col4:

    st.metric(
        "Median Report Length",
        f"{median_length:.0f}"
    )

st.caption(
    "Dataset statistics are calculated from the cleaned crime-report dataset."
)    


# ============================================================
# DATABASE RECORDS
# ============================================================

st.header("Database Records")

st.caption(
    "Structured crime analyses stored in the SQLite database."
)

database_df = load_database_records()

if not database_df.empty:

    st.write(
        f"Records currently stored in SQLite: "
        f"**{len(database_df)}**"
    )

    st.dataframe(
        database_df[
            [
                "report_id",
                "category",
                "sub_category",
                "crime_type",
                "severity"
            ]
        ],
        use_container_width=True
    )

else:

    st.warning(
        "No records found in the SQLite database."
    )


# ============================================================
# CRIME CATEGORY ANALYSIS
# ============================================================

st.header("Crime Category Distribution")

st.caption(
    "Pareto analysis showing report volume and cumulative contribution of each crime category."
)

pareto_df = category_df.copy()

pareto_df = pareto_df.sort_values(
    "count",
    ascending=False
).reset_index(drop=True)

pareto_df["cumulative_percentage"] = (
    pareto_df["count"].cumsum()
    / pareto_df["count"].sum()
    * 100
)

fig = px.bar(
    pareto_df,
    x="category",
    y="count",
    text="count",
    color="category",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig.update_traces(
    texttemplate="%{text:,}",
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Reports: %{y:,}<extra></extra>"
    ),
    showlegend=False,
    selector=dict(type="bar")
)

fig.add_scatter(
    x=pareto_df["category"],
    y=pareto_df["cumulative_percentage"],
    mode="lines+markers",
    name="Cumulative %",
    yaxis="y2",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Cumulative: %{y:.2f}%"
        "<extra></extra>"
    )
)

fig.update_layout(
    xaxis_title="Crime Category",
    yaxis_title="Number of Reports",
    yaxis2=dict(
        title="Cumulative Percentage",
        overlaying="y",
        side="right",
        range=[0, 100]
    ),
    height=650,
    margin=dict(l=20, r=30, t=30, b=150),
    xaxis_tickangle=-45
)

fig.add_hline(
    y=80,
    line_dash="dash",
    annotation_text="80% cumulative",
    annotation_position="top right",
    yref="y2"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.write(
    f"**Most common category:** "
    f"{top_category['category']} — "
    f"{int(top_category['count']):,} reports "
    f"({top_category['percentage']:.2f}%)."
)

# ============================================================
# SUBCATEGORY ANALYSIS
# ============================================================

st.header("Top Crime Subcategories")

st.caption(
    "Top 10 crime subcategories based on the number of reported cases."
)

top_subcategories = subcategory_df.head(10)

fig = px.bar(
    top_subcategories.sort_values("count"),
    x="count",
    y="sub_category",
    orientation="h",
    color="sub_category",
    text="count",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_traces(
    texttemplate="%{text:,}",
    textposition="outside",
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Reports: %{x:,}<extra></extra>"
    )
)

fig.update_layout(
    showlegend=False,
    xaxis_title="Number of Reports",
    yaxis_title="Crime Subcategory",
    height=500,
    margin=dict(l=20, r=80, t=30, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.write(
    f"**Most common subcategory:** "
    f"{top_subcategory['sub_category']} — "
    f"{int(top_subcategory['count']):,} reports "
    f"({top_subcategory['percentage']:.2f}%)."
)


# ============================================================
# LLM ANALYSIS
# ============================================================

st.header("LLM-Based Crime Analysis")

st.write(
    f"The initial LLM analysis successfully processed "
    f"**{llm_total} crime reports**."
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Severity Distribution")

    fig = px.pie(
        llm_severity_df,
        names="severity",
        values="count",
        hole=0.45,
        color="severity",
        color_discrete_map={
            "High": "#E74C3C",
            "Medium": "#F39C12",
            "Low": "#2ECC71"
        }
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Reports: %{value}<extra></extra>"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("Crime Types Extracted by LLM")

    fig = px.bar(
        llm_crime_df.sort_values("count"),
        x="count",
        y="crime_type",
        orientation="h",
        color="crime_type",
        text="count",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Reports: %{x:,}<extra></extra>"
        )
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Number of Reports",
        yaxis_title="Crime Type",
        height=450,
        margin=dict(l=20, r=80, t=30, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# ANALYTICAL INSIGHTS
# ============================================================

st.header("Analytical Insights")

insights_file = (
    PROCESSED_DIR / "crime_pattern_insights.csv"
)

if insights_file.exists():

    insights_df = pd.read_csv(insights_file)

    for _, row in insights_df.iterrows():

        st.subheader(
            row["insight_type"]
        )

        st.write(
            row["finding"]
        )

else:

    st.warning(
        "Analytical insights file not found."
    )


# ============================================================
# IMPORTANT NOTE
# ============================================================

st.header("Analytical Note")

st.warning(
    "The current dataset does not contain a dedicated date column. "
    "Therefore, the current analysis represents crime distributions "
    "and patterns rather than trends over time. LLM-based statistics "
    f"are based only on the initial {llm_total}-report sample and "
    "should not be generalized to the complete dataset."
)


# ============================================================
# REPORT EXPLORER
# ============================================================

st.header("Crime Report Explorer")

st.write(
    "Select an existing crime report from the cleaned dataset "
    "to view its original text and basic classification."
)

category_options = ["All Categories"] + sorted(
    reports_df["category"]
    .dropna()
    .unique()
    .tolist()
)

selected_category = st.selectbox(
    "Filter by Crime Category",
    category_options
)

if selected_category == "All Categories":

    filtered_reports = reports_df

else:

    filtered_reports = reports_df[
        reports_df["category"] == selected_category
    ]


st.caption(
    f"{len(filtered_reports):,} reports available in this selection."
)


selected_report_index = st.slider(
    "Select a Crime Report",
    min_value=0,
    max_value=len(filtered_reports) - 1,
    value=0,
    step=1
)

selected_report = filtered_reports.iloc[
    selected_report_index
]


st.caption(
    f"Showing report {selected_report_index + 1:,} "
    f"of {len(filtered_reports):,}"
)


st.subheader("Original Crime Report")

st.info(
    selected_report["crimeaditionalinfo"]
)


col1, col2 = st.columns(2)

with col1:

    st.write(
        f"**Category:** "
        f"{selected_report['category']}"
    )

with col2:

    st.write(
        f"**Subcategory:** "
        f"{selected_report['sub_category']}"
    )


# ============================================================
# SELECTED REPORT ANALYSIS
# ============================================================

if st.button("Analyze Selected Report"):

    report_id = int(selected_report.name)

    database_record = get_database_record(
        report_id
    )

    # --------------------------------------------------------
    # DATABASE RESULT
    # --------------------------------------------------------

    if database_record is not None:

        st.success(
            "Existing analysis found in database."
        )

        analysis = database_record.to_dict()

    # --------------------------------------------------------
    # LLM RESULT
    # --------------------------------------------------------

    else:

        st.info(
            "No stored analysis found. "
            "Analyzing this report using the LLM..."
        )

        with st.spinner(
            "Analyzing selected report using Gemini..."
        ):

            try:

                analysis = analyze_crime_report(
                    selected_report[
                        "crimeaditionalinfo"
                    ]
                )

            except Exception as e:

                st.error(
                    f"Unable to analyze the selected report: {e}"
                )

                analysis = None


    # --------------------------------------------------------
    # DISPLAY ANALYSIS
    # --------------------------------------------------------

    if analysis is not None:

        st.success(
            "Selected crime report analyzed successfully!"
        )

        st.subheader("LLM Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Crime Information")

            st.write(
                f"**Crime Type:** "
                f"{analysis.get('crime_type', 'Not specified')}"
            )

            severity = str(
                analysis.get(
                    "severity",
                    "Not specified"
                )
            ).strip()

            if severity.lower() == "high":

                st.error(
                    f"Severity: {severity}"
                )

            elif severity.lower() == "medium":

                st.warning(
                    f"Severity: {severity}"
                )

            elif severity.lower() == "low":

                st.success(
                    f"Severity: {severity}"
                )

            else:

                st.info(
                    f"Severity: {severity}"
                )

            st.write(
                f"**Location:** "
                f"{analysis.get('location', 'Not specified')}"
            )

            st.write(
                f"**Financial Loss:** "
                f"{analysis.get('financial_loss', 'Not specified')}"
            )

        with col2:

            st.subheader("Additional Information")

            st.write(
                f"**Platforms:** "
                f"{analysis.get('platforms', 'Not specified')}"
            )

            st.write(
                f"**Entities:** "
                f"{analysis.get('entities', 'Not specified')}"
            )

            st.write(
                f"**Temporal Information:** "
                f"{analysis.get('temporal_information', 'Not specified')}"
            )

        st.subheader("Summary")

        st.write(
            analysis.get(
                "summary",
                "No summary available."
            )
        )

        st.subheader("Modus Operandi")

        st.write(
            analysis.get(
                "modus_operandi",
                "Not specified"
            )
        )


# ============================================================
# SINGLE CRIME REPORT ANALYZER
# ============================================================

st.header("Analyze an Individual Crime Report")

st.write(
    "Enter a crime report below and use the Large Language Model "
    "to extract structured information from the report."
)

crime_report_input = st.text_area(
    "Enter Crime Report",
    placeholder=(
        "Example: I received a suspicious WhatsApp message asking "
        "me to transfer money to a UPI account."
    ),
    height=150
)


if st.button("Analyze Report"):

    if not crime_report_input.strip():

        st.warning(
            "Please enter a crime report before analyzing."
        )

    else:

        with st.spinner(
            "Analyzing crime report using Gemini..."
        ):

            try:

                # ------------------------------------------------
                # NLP ANALYSIS
                # ------------------------------------------------

                cleaned_report = clean_text(
                    crime_report_input
                )

                detected_keywords = extract_keywords(
                    cleaned_report
                )

                # ------------------------------------------------
                # LLM ANALYSIS
                # ------------------------------------------------

                analysis = analyze_crime_report(
                    crime_report_input
                )

                st.success(
                    "Crime report analyzed successfully!"
                )

                # ------------------------------------------------
                # DISPLAY STRUCTURED ANALYSIS
                # ------------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader(
                        "Crime Information"
                    )

                    st.write(
                        f"**Crime Type:** "
                        f"{analysis.get('crime_type', 'Not specified')}"
                    )

                    severity = str(
                        analysis.get(
                            "severity",
                            "Not specified"
                        )
                    ).strip()

                    if severity.lower() == "high":

                        st.error(
                            f"Severity: {severity}"
                        )

                    elif severity.lower() == "medium":

                        st.warning(
                            f"Severity: {severity}"
                        )

                    elif severity.lower() == "low":

                        st.success(
                            f"Severity: {severity}"
                        )

                    else:

                        st.info(
                            f"Severity: {severity}"
                        )

                    st.write(
                        f"**Location:** "
                        f"{analysis.get('location', 'Not specified')}"
                    )

                    st.write(
                        f"**Financial Loss:** "
                        f"{analysis.get('financial_loss', 'Not specified')}"
                    )

                with col2:

                    st.subheader(
                        "Additional Information"
                    )

                    st.write(
                        f"**Platforms:** "
                        f"{analysis.get('platforms', 'Not specified')}"
                    )

                    st.write(
                        f"**Entities:** "
                        f"{analysis.get('entities', 'Not specified')}"
                    )

                    st.write(
                        f"**Temporal Information:** "
                        f"{analysis.get('temporal_information', 'Not specified')}"
                    )

                st.subheader("Summary")

                st.write(
                    analysis.get(
                        "summary",
                        "No summary available."
                    )
                )

                st.subheader(
                    "Modus Operandi"
                )

                st.write(
                    analysis.get(
                        "modus_operandi",
                        "Not specified"
                    )
                )

                                # ------------------------------------------------
                # NLP KEYWORD ANALYSIS
                # ------------------------------------------------

                st.subheader("NLP Detected Keywords")

                if detected_keywords:

                    for keyword_category, keywords in detected_keywords.items():

                        st.write(
                            f"**{keyword_category.replace('_', ' ').title()}:** "
                            f"{', '.join(keywords)}"
                        )

                else:

                    st.info(
                        "No predefined crime-related keywords were detected."
                    )

            except Exception as e:

                st.error(
                    f"Unable to analyze the report: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Powered Crime Report Analysis and Trend Detection System "
    "Using Large Language Models"
)