import streamlit as st
import pandas as pd
import plotly.express as px


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="Paragraph Diagnostic Analyzer",
    layout="wide"
)

st.title("📘 Paragraph Diagnostic Analyzer")
st.write(
    "AI-supported rubric-based analysis of students' paragraph writing performance."
)


# ---------------------------------
# Performance Categories
# ---------------------------------

levels = [
    (0, 20, "Minimal"),
    (21, 40, "Needs Improvement"),
    (41, 60, "Developing"),
    (61, 80, "Proficient"),
    (81, 100, "Exemplary")
]


colors = {
    "Minimal": "red",
    "Needs Improvement": "orange",
    "Developing": "#FFD84F",
    "Proficient": "blue",
    "Exemplary": "green"
}


# ---------------------------------
# Performance Legend
# ---------------------------------

st.subheader("Performance Criteria")

legend = st.columns(5)

for col, item in zip(legend, levels):

    start, end, label = item

    with col:

        st.markdown(
            f"""
            <div style="
            background-color:{colors[label]};
            color:white;
            padding:10px;
            border-radius:8px;
            text-align:center">

            <b>{label}</b><br>
            {start}-{end}%

            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------
# Rubric Information
# ---------------------------------

rubric = {

"Topic Sentence":
{
"max":3,
"description":
"Clear topic and controlling idea."
},

"Supporting Details":
{
"max":3,
"description":
"Relevant major and minor supporting details."
},

"Conclusion":
{
"max":3,
"description":
"Conclusion supports the main idea and details."
},

"Mechanics":
{
"max":2,
"description":
"Grammar, spelling, sentence structure and coherence."
},

"Word Count":
{
"max":2,
"description":
"Writing follows required length."
},

"Vocabulary":
{
"max":2,
"description":
"Appropriate and varied vocabulary."
}

}


components = list(rubric.keys())


# ---------------------------------
# Activities Database
# ---------------------------------

activities = {


"Topic Sentence":
[
"Identify topic and controlling idea from sample sentences.",
"Rewrite weak topic sentences with clearer controlling ideas."
],


"Supporting Details":
[
"Add supporting examples to a given topic sentence.",
"Expand major ideas with relevant minor details."
],


"Conclusion":
[
"Match conclusions with suitable paragraphs.",
"Rewrite weak conclusions to connect with the main idea."
],


"Mechanics":
[
"Correct grammar, spelling and punctuation errors.",
"Combine simple sentences into compound and complex structures."
],


"Word Count":
[
"Expand short paragraphs by adding supporting information.",
"Practice writing paragraphs within a specific word limit."
],


"Vocabulary":
[
"Replace common words with academic alternatives.",
"Create a topic-based vocabulary improvement list."
]

}



# ---------------------------------
# Upload File
# ---------------------------------

uploaded = st.file_uploader(
    "Upload Student Rubric Result Excel File",
    type=["xlsx"]
)



def assign_level(score):

    for low, high, label in levels:

        if low <= score <= high:
            return label

    return "Unknown"



# ---------------------------------
# Main Analysis
# ---------------------------------

if uploaded:


    df = pd.read_excel(uploaded)


    st.success("File uploaded successfully")


    required_columns = [
        "Student ID",
        "Student Name",
        "Topic Sentence",
        "Supporting Details",
        "Conclusion",
        "Mechanics",
        "Word Count",
        "Vocabulary",
        "Total /15"
    ]


    missing = set(required_columns) - set(df.columns)


    if missing:

        st.error(
            f"Missing columns: {missing}"
        )


    else:


        st.metric(
            "Number of Students",
            len(df)
        )


        # -------------------------
        # Convert scores to %
        # -------------------------

        percentage_df = pd.DataFrame()


        for component in components:

            percentage_df[component] = (
                df[component]
                /
                rubric[component]["max"]
                *
                100
            )


        overall_scores = (
            percentage_df
            .stack()
        )


        st.metric(
            "Average Writing Performance",
            f"{overall_scores.mean():.1f}%"
        )


        # -------------------------
        # Overall Distribution
        # -------------------------

        st.subheader(
            "Overall Performance Distribution"
        )


        distribution = (
            overall_scores
            .apply(assign_level)
            .value_counts()
            .reindex(
                [
                "Minimal",
                "Needs Improvement",
                "Developing",
                "Proficient",
                "Exemplary"
                ],
                fill_value=0
            )
        )


        pie = px.pie(
            values=distribution.values,
            names=distribution.index,
            color=distribution.index,
            color_discrete_map=colors
        )


        st.plotly_chart(
            pie,
            use_container_width=True
        )


        # -------------------------
        # Component Analysis
        # -------------------------

        st.subheader(
            "Rubric Component Analysis"
        )


        component_average = (
            percentage_df
            .mean()
            .sort_values()
        )


        bar = px.bar(
            component_average,
            labels={
                "value":"Average Percentage",
                "index":"Component"
            }
        )


        st.plotly_chart(
            bar,
            use_container_width=True
        )


        # -------------------------
        # Strong / Weak Area
        # -------------------------

        weakest = component_average.index[0]
        strongest = component_average.index[-1]


        c1, c2 = st.columns(2)


        with c1:

            st.success(
                f"""
                ⭐ Strongest Component

                {strongest}

                Score:
                {component_average[strongest]:.1f}%

                {rubric[strongest]['description']}
                """
            )


        with c2:

            st.warning(
                f"""
                ⚠️ Area Needing Improvement

                {weakest}

                Score:
                {component_average[weakest]:.1f}%

                {rubric[weakest]['description']}
                """
            )


        # -------------------------
        # Student Level Output
        # -------------------------

        st.subheader(
            "Student Performance Report"
        )


        output = df.copy()


        output["Percentage"] = (
            output["Total /15"]
            /
            15
            *
            100
        )


        output["Performance Level"] = (
            output["Percentage"]
            .apply(assign_level)
        )


        st.dataframe(
            output,
            use_container_width=True
        )


        # -------------------------
        # Suggested Activities
        # -------------------------

        st.subheader(
            "🎯 Targeted Improvement Activities"
        )


        st.write(
            f"Recommended activities for improving **{weakest}**:"
        )


        for activity in activities[weakest]:

            st.info(activity)



        # -------------------------
        # Mini Practice Task
        # -------------------------

        st.subheader(
            "📝 Quick Classroom Practice Activity"
        )


        practice_tasks = {


        "Topic Sentence":
        "Write a topic sentence with a clear topic and controlling idea for: 'The role of technology in education'.",


        "Supporting Details":
        "Add two major supporting details and one example for: 'Reading improves academic success'.",


        "Conclusion":
        "Write a concluding sentence that connects with the main idea of a paragraph about healthy lifestyles.",


        "Mechanics":
        "Correct this sentence: 'Students who studies regularly improves their writing skills.'",


        "Word Count":
        "Expand this idea into a complete paragraph: 'AI is changing education.'",


        "Vocabulary":
        "Replace simple words with academic alternatives: 'Good teachers help students learn new things.'"

        }


        st.write(
            practice_tasks[weakest]
        )
