import streamlit as st
import pandas as pd
import joblib

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

def career_advice(career):
    advice = {
        "Data Analyst": [
            "Strong foundation in statistics",
            "Learn Python & SQL",
            "Practice data visualization"
        ],
        "Software Engineer": [
            "Master programming fundamentals",
            "Learn system design",
            "Practice coding interviews"
        ],
        "Business Analyst": [
            "Understand business processes",
            "Develop analytical thinking",
            "Improve communication skills"
        ]
    }
    return advice.get(career, [])

def skill_gap_advice(skill):
    if skill == "Beginner":
        return "Focus on fundamentals and introductory courses."
    elif skill == "Intermediate":
        return "Start applying knowledge through projects."
    else:
        return "Advance with specialization and real-world case studies."

# ===============================
# Page config
# ===============================
st.set_page_config(page_title="Course Recommendation System", layout="wide")

st.title("🎓 Smart Course Recommendation System")

# ===============================
# Tabs (NEW STRUCTURE)
# ===============================
tab1, tab2, tab3 = st.tabs([
    "🎯 Course Recommendation",
    "🧭 Career Path Guidance",
    "📈 Skill Gap & Study Advice"
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

        st.success(f"✅ Recommended Course Category: **{course_type}**")
        st.info(f"📘 Suggested Course: **{course_name}**")

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
    st.subheader("Personalized Study Advice")

    skill_level = st.radio(
        "Your Current Skill Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    advice = skill_gap_advice(skill_level)

    st.success("📌 Recommended Learning Strategy")
    st.write(advice)

    st.markdown("""
    **Why this matters:**
    - Helps students prepare before taking advanced courses  
    - Reduces failure risk  
    - Encourages continuous learning  
    """)

