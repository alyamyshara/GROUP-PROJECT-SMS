import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# ===============================
# Load model and dataset
# ===============================
model = joblib.load("course_model.pkl")
courses = pd.read_csv("data/coursea_data.csv")
courses = courses.loc[:, ~courses.columns.str.contains("^Unnamed")]

# ===============================
# Helper functions
# ===============================
def get_real_course(course_type):
    if course_type == "Data":
        df = courses[courses["course_title"].str.contains("data|analytics", case=False)]
    elif course_type == "Programming":
        df = courses[courses["course_title"].str.contains("python|program|software", case=False)]
    else:
        df = courses[courses["course_title"].str.contains("business|management", case=False)]
    return df.iloc[0]["course_title"]

def suggest_university(course_type):
    mapping = {
        "Data": "Google Data Analytics / Coursera (University of Michigan)",
        "Programming": "Harvard University (CS50) / Google",
        "Business": "Wharton School (University of Pennsylvania)"
    }
    return mapping.get(course_type, "Top Global University")

def career_advice(career):
    advice = {
        "Data Analyst": [
            "Statistics & probability fundamentals",
            "SQL and Python programming",
            "Dashboard and visualization tools"
        ],
        "Software Engineer": [
            "Data structures and algorithms",
            "Software architecture",
            "Version control (Git)"
        ],
        "Business Analyst": [
            "Business process modeling",
            "Data interpretation",
            "Stakeholder communication"
        ]
    }
    return advice.get(career, [])

def skill_gap_advice(career, difficulty):
    advice = {
        ("Data Analyst", "Beginner"):
            "Start with Excel, basic statistics, and simple data visualization.",
        ("Data Analyst", "Intermediate"):
            "Work on SQL, Python, and real datasets.",
        ("Data Analyst", "Advanced"):
            "Focus on machine learning and big data tools.",

        ("Software Engineer", "Beginner"):
            "Learn programming basics and problem-solving.",
        ("Software Engineer", "Intermediate"):
            "Build projects and practice algorithms.",
        ("Software Engineer", "Advanced"):
            "Study system design and scalable architectures.",

        ("Business Analyst", "Beginner"):
            "Understand business fundamentals and Excel.",
        ("Business Analyst", "Intermediate"):
            "Learn SQL, dashboards, and reporting.",
        ("Business Analyst", "Advanced"):
            "Focus on strategic analysis and decision modeling."
    }
    return advice.get((career, difficulty), "Keep improving consistently.")

# ===============================
# Page config
# ===============================
st.set_page_config(page_title="Course Recommendation System", layout="wide")

st.title("🎓 Smart Course Recommendation System")

# ===============================
# Tabs
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Course Recommendation",
    "🧭 Career Path Guidance",
    "📈 Skill Gap & Study Advice",
    "📊 Course Trends"
])

# ===============================
# TAB 1 — Recommendation
# ===============================
with tab1:
    st.subheader("Student Profile")

    col1, col2 = st.columns(2)

    with col1:
        cgpa = st.slider("CGPA", 2.5, 4.0, 3.0, 0.1)
        interest = st.selectbox(
            "Interest Area",
            ["Data Science", "Business", "Computer Science"]
        )

    with col2:
        career = st.selectbox(
            "Career Goal",
            ["Data Analyst", "Software Engineer", "Business Analyst"]
        )
        skill = st.selectbox(
            "Skill Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

    if st.button("🎯 Recommend Course"):
        input_df = pd.DataFrame([{
            "cgpa": cgpa,
            "interest": interest,
            "career_goal": career,
            "skill_level": skill
        }])

        course_type = model.predict(input_df)[0]
        course_name = get_real_course(course_type)
        university = suggest_university(course_type)

        st.success(f"✅ Recommended Course Category: **{course_type}**")
        st.info(f"📘 Suggested Course: **{course_name}**")
        st.warning(f"🏫 Suggested University / Organization: **{university}**")

# ===============================
# TAB 2 — Career Path Guidance
# ===============================
with tab2:
    st.subheader("Career Preparation Roadmap")

    selected_career = st.selectbox(
        "Select Your Career Goal",
        ["Data Analyst", "Software Engineer", "Business Analyst"]
    )

    advice_list = career_advice(selected_career)

    st.markdown(f"### 🧠 Key Skills for **{selected_career}**")
    for a in advice_list:
        st.write("✔", a)

    st.info("This guidance helps students align their course selection with long-term career planning.")

# ===============================
# TAB 3 — Skill Gap & Study Advice
# ===============================
with tab3:
    st.subheader("Personalized Study Plan")

    col1, col2 = st.columns(2)

    with col1:
        chosen_career = st.selectbox(
            "Select Career Goal",
            ["Data Analyst", "Software Engineer", "Business Analyst"]
        )

    with col2:
        difficulty = st.selectbox(
            "Select Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

    advice = skill_gap_advice(chosen_career, difficulty)

    st.success("📌 Recommended Learning Strategy")
    st.write(advice)

    st.markdown("""
    **Benefit to students:**
    - Helps plan learning progression  
    - Avoids choosing overly difficult courses  
    - Supports career readiness  
    """)

# ===============================
# TAB 4 — Interactive Chart
# ===============================
with tab4:
    st.subheader("Trending Course Categories")

    courses["category"] = courses["course_title"].str.extract(
        "(Data|Python|Business)", expand=False
    )

    category_counts = courses["category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Number of Courses"]

    fig = px.bar(
        category_counts,
        x="Category",
        y="Number of Courses",
        title="Course Category Availability",
        text="Number of Courses"
    )

    fig.update_layout(
        xaxis_title="Course Category",
        yaxis_title="Count",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
