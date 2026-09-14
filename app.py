import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Student Performance Dashboard",
    layout="wide"
)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("student-mat-clean (1).csv")


df = load_data()


# ============================================================
# TITLE
# ============================================================

st.title(" Student Performance Dashboard")

st.write(
    "Interactive dashboard for analysing student academic performance."
)

st.divider()


# ============================================================
# TASK 1: BASIC DATASET INFORMATION
# ============================================================

st.header("1. Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Students",
        value=df.shape[0]
    )

with col2:
    st.metric(
        label="Total Columns",
        value=df.shape[1]
    )

with col3:
    st.metric(
        label="Missing Values",
        value=int(df.isnull().sum().sum())
    )


# Dataset information inside expandable section

with st.expander("View Dataset Information"):

    st.subheader("First 5 Rows")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.subheader("Column Names")

    st.write(
        df.columns.tolist()
    )

    st.subheader("Data Types")

    datatype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(
        datatype_df,
        use_container_width=True
    )

    st.subheader("Missing Values")

    missing_df = (
        df.isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Column",
        "Missing Values"
    ]

    st.dataframe(
        missing_df,
        use_container_width=True
    )


st.divider()


# ============================================================
# TASK 2: INTERACTIVE FILTERS
# ============================================================

st.sidebar.title("Dashboard Filters")


# ------------------------------
# FILTER 1: SCHOOL
# ------------------------------

school_options = sorted(
    df["school"].unique()
)

selected_school = st.sidebar.multiselect(
    "Select School",
    options=school_options,
    default=school_options
)


# ------------------------------
# FILTER 2: GENDER
# ------------------------------

gender_options = sorted(
    df["gender"].unique()
)

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=gender_options,
    default=gender_options
)


# ------------------------------
# FILTER 3: AGE
# ------------------------------

min_age = int(df["age"].min())
max_age = int(df["age"].max())

selected_age = st.sidebar.slider(
    "Select Age Range",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)


# ------------------------------
# FILTER 4: STUDY TIME
# ------------------------------

studytime_options = sorted(
    df["studytime"].unique()
)

studytime_names = {
    1: "< 2 Hours",
    2: "2 - 5 Hours",
    3: "5 - 10 Hours",
    4: "> 10 Hours"
}

selected_studytime = st.sidebar.multiselect(
    "Select Study Time",
    options=studytime_options,
    default=studytime_options,
    format_func=lambda x: studytime_names.get(
        x,
        str(x)
    )
)


# ============================================================
# FILTER DATASET
# ============================================================

filtered_df = df[
    (df["school"].isin(selected_school))
    &
    (df["gender"].isin(selected_gender))
    &
    (
        df["age"].between(
            selected_age[0],
            selected_age[1]
        )
    )
    &
    (
        df["studytime"].isin(
            selected_studytime
        )
    )
]


# ============================================================
# DISPLAY ACTIVE FILTER INFORMATION
# ============================================================

st.subheader("2. Filtered Dataset Summary")

st.write(
    f"Showing **{len(filtered_df)}** students "
    f"out of **{len(df)}** total students."
)


# ============================================================
# TASK 3: DYNAMIC KPIs
# ============================================================

st.header("3. Key Performance Indicators")


if len(filtered_df) > 0:

    total_students = len(filtered_df)

    average_grade = (
        filtered_df["G3"].mean()
    )

    average_absences = (
        filtered_df["absences"].mean()
    )

    pass_percentage = (
        (
            filtered_df["G3"] >= 10
        ).mean()
        * 100
    )

else:

    total_students = 0
    average_grade = 0
    average_absences = 0
    pass_percentage = 0


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        label="Total Students",
        value=total_students
    )


with kpi2:

    st.metric(
        label="Average Final Grade",
        value=f"{average_grade:.2f} / 20"
    )


with kpi3:

    st.metric(
        label="Average Absences",
        value=f"{average_absences:.2f}"
    )


with kpi4:

    st.metric(
        label="Pass Percentage",
        value=f"{pass_percentage:.2f}%"
    )


st.divider()


# ============================================================
# TASK 4: INTERACTIVE VISUALIZATIONS
# ============================================================

st.header("4. Interactive Visualizations")


if len(filtered_df) == 0:

    st.warning(
        "No data matches the selected filters."
    )

else:

    chart1_col, chart2_col = st.columns(2)


    # ========================================================
    # CHART 1
    # ========================================================

    with chart1_col:

        st.subheader(
            "Average Final Grade by Study Time"
        )


        study_grade = (
            filtered_df
            .groupby(
                "studytime",
                as_index=False
            )["G3"]
            .mean()
        )


        study_grade[
            "Study Time"
        ] = study_grade[
            "studytime"
        ].map(
            studytime_names
        )


        fig1 = px.bar(
            study_grade,
            x="Study Time",
            y="G3",
            text_auto=".2f",
            labels={
                "G3":
                "Average Final Grade"
            }
        )


        fig1.update_layout(
            xaxis_title="Study Time",
            yaxis_title="Average Final Grade"
        )


        st.plotly_chart(
            fig1,
            use_container_width=True
        )


    # ========================================================
    # CHART 2
    # ========================================================

    with chart2_col:

        st.subheader(
            "Absences vs Final Grade"
        )


        fig2 = px.scatter(
            filtered_df,
            x="absences",
            y="G3",
            color="gender",
            size="studytime",

            hover_data=[
                "school",
                "age",
                "studytime",
                "G1",
                "G2",
                "G3"
            ],

            labels={
                "absences":
                "Number of Absences",

                "G3":
                "Final Grade",

                "gender":
                "Gender"
            }
        )


        st.plotly_chart(
            fig2,
            use_container_width=True
        )


    # ========================================================
    # EXTRA VISUALIZATIONS
    # ========================================================

    chart3_col, chart4_col = st.columns(2)


    # ========================================================
    # CHART 3
    # ========================================================

    with chart3_col:

        st.subheader(
            "Final Grade Distribution"
        )


        fig3 = px.histogram(
            filtered_df,
            x="G3",
            nbins=20,

            labels={
                "G3":
                "Final Grade"
            }
        )


        st.plotly_chart(
            fig3,
            use_container_width=True
        )


    # ========================================================
    # CHART 4
    # ========================================================

    with chart4_col:

        st.subheader(
            "Average Final Grade by Gender"
        )


        gender_grade = (
            filtered_df
            .groupby(
                "gender",
                as_index=False
            )["G3"]
            .mean()
        )


        fig4 = px.bar(
            gender_grade,
            x="gender",
            y="G3",
            text_auto=".2f",

            labels={
                "gender":
                "Gender",

                "G3":
                "Average Final Grade"
            }
        )


        st.plotly_chart(
            fig4,
            use_container_width=True
        )


st.divider()


# ============================================================
# TASK 5: FILTERED TABLE
# ============================================================

st.header("5. Filtered Student Dataset")


columns_to_show = [
    "school",
    "gender",
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",
    "G3"
]


st.dataframe(
    filtered_df[
        columns_to_show
    ],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

csv_data = (
    filtered_df
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Student Performance Dashboard | "
    "Built using Streamlit, Pandas and Plotly"
)