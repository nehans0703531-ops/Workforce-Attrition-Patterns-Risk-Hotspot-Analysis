import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #F8FAFC;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

h1 {
    color: #0F172A;
    font-weight: 700;
}

h2 {
    color: #1E293B;
}

h3 {
    color: #334155;
}

[data-testid="stMetric"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.12);
    border: 1px solid #E2E8F0;
}

[data-testid="stSidebar"] {
    background-color: #F1F5F9;
}

.stButton > button {
    border-radius: 8px;
}

div[data-testid="stTabs"] button {
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FILE PATHS
# =========================================================

DATASET_PATH = "employee_attrition.csv"
LOGO_PATH = "assets/logo.png"
BANNER_PATH = "assets/banner.png"


# =========================================================
# LOAD DATASET
# =========================================================

if not os.path.exists(DATASET_PATH):

    st.error(
        "❌ employee_attrition.csv was not found."
    )

    st.info(
        "Please place employee_attrition.csv in the same folder as app.py."
    )

    st.stop()


df = pd.read_csv(DATASET_PATH)


# =========================================================
# BASIC DATA CLEANING
# =========================================================

df = df.drop_duplicates().reset_index(drop=True)


# =========================================================
# HEADER
# =========================================================

if os.path.exists(BANNER_PATH):
    st.image(
        BANNER_PATH,
        use_container_width=True
    )


col1, col2 = st.columns([1, 6])

with col1:

    if os.path.exists(LOGO_PATH):
        st.image(
            LOGO_PATH,
            width=110
        )

with col2:

    st.markdown("""
    <h1 style="margin-bottom:0px;">
        Employee Attrition Dashboard
    </h1>

    <h4 style="
        color:#64748B;
        margin-top:5px;
        font-weight:400;
    ">
        Workforce Attrition Patterns & Risk Hotspot Analysis
    </h4>
    """, unsafe_allow_html=True)


st.markdown("---")


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to analyze employee attrition."
)


# Department
if "Department" in df.columns:

    department_filter = st.sidebar.multiselect(
        "🏢 Department",
        options=sorted(df["Department"].dropna().unique()),
        default=sorted(df["Department"].dropna().unique())
    )

else:

    department_filter = []


# Gender
if "Gender" in df.columns:

    gender_filter = st.sidebar.multiselect(
        "👥 Gender",
        options=sorted(df["Gender"].dropna().unique()),
        default=sorted(df["Gender"].dropna().unique())
    )

else:

    gender_filter = []


# Job Role
if "JobRole" in df.columns:

    jobrole_filter = st.sidebar.multiselect(
        "💼 Job Role",
        options=sorted(df["JobRole"].dropna().unique()),
        default=sorted(df["JobRole"].dropna().unique())
    )

else:

    jobrole_filter = []


# Overtime
if "OverTime" in df.columns:

    overtime_filter = st.sidebar.multiselect(
        "⏰ Overtime",
        options=sorted(df["OverTime"].dropna().unique()),
        default=sorted(df["OverTime"].dropna().unique())
    )

else:

    overtime_filter = []


# Business Travel
if "BusinessTravel" in df.columns:

    travel_filter = st.sidebar.multiselect(
        "✈️ Business Travel",
        options=sorted(df["BusinessTravel"].dropna().unique()),
        default=sorted(df["BusinessTravel"].dropna().unique())
    )

else:

    travel_filter = []


# Years at Company
if "YearsAtCompany" in df.columns:

    min_years = int(df["YearsAtCompany"].min())
    max_years = int(df["YearsAtCompany"].max())

    years_filter = st.sidebar.slider(
        "📅 Years at Company",
        min_value=min_years,
        max_value=max_years,
        value=(min_years, max_years)
    )

else:

    years_filter = None


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if "Department" in df.columns and department_filter:

    filtered_df = filtered_df[
        filtered_df["Department"].isin(department_filter)
    ]


if "Gender" in df.columns and gender_filter:

    filtered_df = filtered_df[
        filtered_df["Gender"].isin(gender_filter)
    ]


if "JobRole" in df.columns and jobrole_filter:

    filtered_df = filtered_df[
        filtered_df["JobRole"].isin(jobrole_filter)
    ]


if "OverTime" in df.columns and overtime_filter:

    filtered_df = filtered_df[
        filtered_df["OverTime"].isin(overtime_filter)
    ]


if "BusinessTravel" in df.columns and travel_filter:

    filtered_df = filtered_df[
        filtered_df["BusinessTravel"].isin(travel_filter)
    ]


if "YearsAtCompany" in df.columns and years_filter:

    filtered_df = filtered_df[
        filtered_df["YearsAtCompany"].between(
            years_filter[0],
            years_filter[1]
        )
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_employees = len(filtered_df)


if "Attrition" in filtered_df.columns:

    employees_left = int(
        filtered_df["Attrition"].sum()
    )

else:

    employees_left = 0


retained = total_employees - employees_left


if total_employees > 0:

    attrition_rate = (
        employees_left / total_employees
    ) * 100

else:

    attrition_rate = 0


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👨‍💼 Total Employees",
        f"{total_employees:,}"
    )


with col2:

    st.metric(
        "🚪 Employees Left",
        f"{employees_left:,}"
    )


with col3:

    st.metric(
        "✅ Retained Employees",
        f"{retained:,}"
    )


with col4:

    st.metric(
        "📉 Attrition Rate",
        f"{attrition_rate:.2f}%"
    )


st.markdown("---")


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([

    "📈 Overview",

    "🏢 Department Analysis",

    "👥 Employee Demographics",

    "⚙️ Workload Analysis",

    "🔥 Correlation Heatmap",

    "💡 Insights & Recommendations",

    "📋 Complete Dataset"

])


# =========================================================
# TAB 1 - OVERVIEW
# =========================================================

with tab1:

    st.subheader("📈 Attrition Overview")

    col1, col2 = st.columns(2)


    # Attrition Distribution
    with col1:

        if "Attrition" in filtered_df.columns:

            attrition_counts = (
                filtered_df["Attrition"]
                .value_counts()
                .reset_index()
            )

            attrition_counts.columns = [
                "Attrition",
                "Count"
            ]

            attrition_counts["Status"] = (
                attrition_counts["Attrition"]
                .map({
                    0: "Retained",
                    1: "Left"
                })
            )

            fig = px.pie(
                attrition_counts,
                names="Status",
                values="Count",
                hole=0.45,
                title="Employee Attrition Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Department Attrition
    with col2:

        if (
            "Department" in filtered_df.columns
            and "Attrition" in filtered_df.columns
        ):

            dept = (
                filtered_df
                .groupby("Department")["Attrition"]
                .mean()
                .reset_index()
            )

            dept["Attrition"] *= 100

            fig = px.bar(
                dept,
                x="Department",
                y="Attrition",
                color="Department",
                title="Department-wise Attrition (%)",
                text_auto=".1f"
            )

            fig.update_layout(
                yaxis_title="Attrition (%)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# =========================================================
# TAB 2 - DEPARTMENT ANALYSIS
# =========================================================

with tab2:

    st.subheader("🏢 Department & Job Role Analysis")


    if (
        "JobRole" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        jobrole = (
            filtered_df
            .groupby("JobRole")["Attrition"]
            .mean()
            .reset_index()
        )

        jobrole["Attrition"] *= 100

        fig = px.bar(
            jobrole,
            x="JobRole",
            y="Attrition",
            color="JobRole",
            title="Job Role-wise Attrition (%)",
            text_auto=".1f"
        )

        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_title="Attrition (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 3 - DEMOGRAPHICS
# =========================================================

with tab3:

    st.subheader("👥 Employee Demographics")


    # Gender
    if (
        "Gender" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        gender = (
            filtered_df
            .groupby("Gender")["Attrition"]
            .mean()
            .reset_index()
        )

        gender["Attrition"] *= 100

        fig = px.bar(
            gender,
            x="Gender",
            y="Attrition",
            color="Gender",
            title="Gender-wise Attrition (%)",
            text_auto=".1f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Age
    if "Age" in filtered_df.columns:

        fig = px.histogram(
            filtered_df,
            x="Age",
            nbins=20,
            title="Age Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Monthly Income
    if "MonthlyIncome" in filtered_df.columns:

        st.subheader("💰 Monthly Income Distribution")

        fig = px.histogram(
            filtered_df,
            x="MonthlyIncome",
            nbins=30,
            title="Monthly Income Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.subheader("💰 Monthly Income by Department")

        if "Department" in filtered_df.columns:

            fig = px.box(
                filtered_df,
                x="Department",
                y="MonthlyIncome",
                color="Department",
                title="Monthly Income across Departments"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Age Groups
    if (
        "Age" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        st.subheader("📊 Attrition by Age Group")

        age_group = pd.cut(
            filtered_df["Age"],
            bins=[
                18,
                25,
                35,
                45,
                55,
                65
            ],
            labels=[
                "18-25",
                "26-35",
                "36-45",
                "46-55",
                "56-65"
            ]
        )

        age_df = filtered_df.copy()

        age_df["AgeGroup"] = age_group

        age_attrition = (
            age_df
            .groupby(
                "AgeGroup",
                observed=False
            )["Attrition"]
            .mean()
            .reset_index()
        )

        age_attrition["Attrition"] *= 100

        fig = px.bar(
            age_attrition,
            x="AgeGroup",
            y="Attrition",
            color="AgeGroup",
            title="Age Group vs Attrition (%)",
            text_auto=".1f"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 4 - WORKLOAD ANALYSIS
# =========================================================

with tab4:

    st.subheader("⚙️ Workload & Employee Satisfaction")


    col1, col2 = st.columns(2)


    # Overtime
    with col1:

        if (
            "OverTime" in filtered_df.columns
            and "Attrition" in filtered_df.columns
        ):

            overtime = (
                filtered_df
                .groupby("OverTime")["Attrition"]
                .mean()
                .reset_index()
            )

            overtime["Attrition"] *= 100

            fig = px.bar(
                overtime,
                x="OverTime",
                y="Attrition",
                color="OverTime",
                title="Overtime vs Attrition (%)",
                text_auto=".1f"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Business Travel
    with col2:

        if (
            "BusinessTravel" in filtered_df.columns
            and "Attrition" in filtered_df.columns
        ):

            travel = (
                filtered_df
                .groupby("BusinessTravel")["Attrition"]
                .mean()
                .reset_index()
            )

            travel["Attrition"] *= 100

            fig = px.bar(
                travel,
                x="BusinessTravel",
                y="Attrition",
                color="BusinessTravel",
                title="Business Travel vs Attrition (%)",
                text_auto=".1f"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # Work Life Balance
    if (
        "WorkLifeBalance" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        st.subheader("⚖️ Work-Life Balance")

        wlb = (
            filtered_df
            .groupby("WorkLifeBalance")["Attrition"]
            .mean()
            .reset_index()
        )

        wlb["Attrition"] *= 100

        fig = px.line(
            wlb,
            x="WorkLifeBalance",
            y="Attrition",
            markers=True,
            title="Work-Life Balance vs Attrition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Years at Company
    if (
        "YearsAtCompany" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        st.subheader("📅 Years at Company")

        years = (
            filtered_df
            .groupby("YearsAtCompany")["Attrition"]
            .mean()
            .reset_index()
        )

        years["Attrition"] *= 100

        fig = px.line(
            years,
            x="YearsAtCompany",
            y="Attrition",
            markers=True,
            title="Years at Company vs Attrition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Job Satisfaction
    if (
        "JobSatisfaction" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        st.subheader("😊 Job Satisfaction")

        job_sat = (
            filtered_df
            .groupby("JobSatisfaction")["Attrition"]
            .mean()
            .reset_index()
        )

        job_sat["Attrition"] *= 100

        fig = px.bar(
            job_sat,
            x="JobSatisfaction",
            y="Attrition",
            color="JobSatisfaction",
            title="Job Satisfaction vs Attrition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Environment Satisfaction
    if (
        "EnvironmentSatisfaction" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        st.subheader("🏢 Environment Satisfaction")

        env = (
            filtered_df
            .groupby("EnvironmentSatisfaction")["Attrition"]
            .mean()
            .reset_index()
        )

        env["Attrition"] *= 100

        fig = px.bar(
            env,
            x="EnvironmentSatisfaction",
            y="Attrition",
            color="EnvironmentSatisfaction",
            title="Environment Satisfaction vs Attrition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Education
    if (
        "Education" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        st.subheader("🎓 Education Level")

        edu = (
            filtered_df
            .groupby("Education")["Attrition"]
            .mean()
            .reset_index()
        )

        edu["Attrition"] *= 100

        fig = px.bar(
            edu,
            x="Education",
            y="Attrition",
            color="Education",
            title="Education Level vs Attrition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Distance vs Income
    if (
        "DistanceFromHome" in filtered_df.columns
        and "MonthlyIncome" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        st.subheader("🏠 Distance from Home vs Monthly Income")

        fig = px.scatter(
            filtered_df,
            x="DistanceFromHome",
            y="MonthlyIncome",
            color="Attrition",
            title="Distance from Home vs Monthly Income"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Promotion
    if (
        "YearsSinceLastPromotion" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        st.subheader("📈 Years Since Last Promotion")

        promotion = (
            filtered_df
            .groupby(
                "YearsSinceLastPromotion"
            )["Attrition"]
            .mean()
            .reset_index()
        )

        promotion["Attrition"] *= 100

        fig = px.line(
            promotion,
            x="YearsSinceLastPromotion",
            y="Attrition",
            markers=True,
            title="Years Since Last Promotion vs Attrition"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# TAB 5 - CORRELATION HEATMAP
# =========================================================

with tab5:

    st.subheader("🔥 Correlation Heatmap")

    numeric_df = filtered_df.select_dtypes(
        include="number"
    )

    if numeric_df.shape[1] >= 2:

        corr = numeric_df.corr()

        fig, ax = plt.subplots(
            figsize=(15, 9)
        )

        sns.heatmap(
            corr,
            annot=False,
            cmap="coolwarm",
            linewidths=0.5,
            ax=ax
        )

        ax.set_title(
            "Employee Attrition Correlation Heatmap"
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

    else:

        st.warning(
            "Not enough numerical columns to create a correlation heatmap."
        )


# =========================================================
# TAB 6 - INSIGHTS
# =========================================================

with tab6:

    st.subheader("💡 Key Insights & Recommendations")


    # Department insight
    if (
        "Department" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        dept = (
            filtered_df
            .groupby("Department")["Attrition"]
            .mean()
            .reset_index()
        )

        dept["Attrition"] *= 100

        if not dept.empty:

            highest_dept = (
                dept
                .sort_values(
                    "Attrition",
                    ascending=False
                )
                .iloc[0]
            )

            st.success(
                f"🏢 Highest Attrition Department: "
                f"{highest_dept['Department']} "
                f"({highest_dept['Attrition']:.2f}%)"
            )


    # Job role insight
    if (
        "JobRole" in filtered_df.columns
        and "Attrition" in filtered_df.columns
    ):

        jobrole = (
            filtered_df
            .groupby("JobRole")["Attrition"]
            .mean()
            .reset_index()
        )

        jobrole["Attrition"] *= 100

        if not jobrole.empty:

            highest_role = (
                jobrole
                .sort_values(
                    "Attrition",
                    ascending=False
                )
                .iloc[0]
            )

            st.success(
                f"💼 Highest Attrition Job Role: "
                f"{highest_role['JobRole']} "
                f"({highest_role['Attrition']:.2f}%)"
            )


    st.markdown("---")

    st.markdown("### 🎯 Recommendations")

    st.markdown("""
    **1. Reduce excessive overtime**

    Employees working overtime should be monitored because
    excessive workload can contribute to employee turnover.

    **2. Review business travel**

    Frequently traveling employees may require additional
    support and work-life balance initiatives.

    **3. Improve career growth**

    Create clearer promotion paths and professional development
    opportunities.

    **4. Improve employee engagement**

    Employee satisfaction and workplace environment should be
    regularly monitored.

    **5. Focus on high-risk departments**

    Departments and job roles with higher attrition rates
    should receive targeted retention strategies.
    """)


# =========================================================
# TAB 7 - COMPLETE DATASET
# =========================================================

with tab7:

    st.subheader("📋 Complete Employee Dataset")

    st.markdown(
        """
        Explore the complete employee dataset below.
        You can search the dataset, inspect columns,
        view statistics and download the data.
        """
    )


    # Dataset KPI cards
    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📊 Total Records",
            f"{len(df):,}"
        )


    with col2:

        st.metric(
            "📑 Total Columns",
            f"{len(df.columns):,}"
        )


    with col3:

        missing_values = int(
            df.isnull().sum().sum()
        )

        st.metric(
            "⚠️ Missing Values",
            f"{missing_values:,}"
        )


    with col4:

        duplicate_rows = int(
            df.duplicated().sum()
        )

        st.metric(
            "♻️ Duplicate Rows",
            f"{duplicate_rows:,}"
        )


    st.markdown("---")


    # =====================================================
    # SEARCH DATASET
    # =====================================================

    st.subheader("🔍 Search Dataset")

    search_text = st.text_input(
        "Search across all columns",
        placeholder="Example: Sales, Male, Manager, Yes..."
    )


    display_df = df.copy()


    if search_text:

        mask = (
            display_df
            .astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search_text,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        )

        display_df = display_df[mask]


    st.info(
        f"Showing {len(display_df):,} "
        f"of {len(df):,} records"
    )


    # =====================================================
    # DATA TABLE
    # =====================================================

    st.dataframe(
        display_df,
        use_container_width=True,
        height=600,
        hide_index=True
    )


    st.markdown("---")


    # =====================================================
    # COLUMN INFORMATION
    # =====================================================

    st.subheader("📑 Dataset Column Information")


    column_info = pd.DataFrame({

        "Column Name": df.columns,

        "Data Type":
            df.dtypes.astype(str).values,

        "Missing Values":
            df.isnull().sum().values,

        "Unique Values":
            [
                df[column].nunique()
                for column in df.columns
            ]

    })


    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True
    )


    st.markdown("---")


    # =====================================================
    # STATISTICS
    # =====================================================

    st.subheader("📊 Numerical Dataset Statistics")


    numeric_columns = df.select_dtypes(
        include="number"
    ).columns


    if len(numeric_columns) > 0:

        statistics = (
            df[numeric_columns]
            .describe()
            .T
            .reset_index()
        )

        statistics = statistics.rename(
            columns={
                "index": "Column"
            }
        )

        st.dataframe(
            statistics,
            use_container_width=True,
            hide_index=True
        )


    st.markdown("---")


    # =====================================================
    # DOWNLOAD COMPLETE DATASET
    # =====================================================

    st.subheader("⬇️ Download Dataset")


    complete_csv = (
        df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(

        label="⬇️ Download Complete Dataset",

        data=complete_csv,

        file_name="Employee_Attrition_Complete_Dataset.csv",

        mime="text/csv",

        use_container_width=True

    )


    # Filtered dataset
    filtered_csv = (
        filtered_df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(

        label="⬇️ Download Current Filtered Dataset",

        data=filtered_csv,

        file_name="Filtered_Employees.csv",

        mime="text/csv",

        use_container_width=True

    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;">

        <h4>📊 Employee Attrition Dashboard</h4>

        <p style="color:#64748B;">
            Developed using Python • Streamlit • Pandas • Plotly
        </p>

        <p style="color:#94A3B8;">
            © 2026 DATAVANE
        </p>

    </div>
    """,
    unsafe_allow_html=True
)