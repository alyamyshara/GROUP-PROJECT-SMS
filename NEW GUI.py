import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# ===============================
# Load model and dataset
# ===============================
model = joblib.load("course_model.pkl")
courses = pd.read_csv("data/coursea_data.csv")
courses = courses.loc[:, ~courses.columns.str.contains("^Unnamed")]

# ===============================
# Helper function
# ===============================
def get_real_course(course_type):
    if course_type == "Data":
        df = courses[courses["course_title"].str.contains("data|analytics", case=False)]
    elif course_type == "Programming":
        df = courses[courses["course_title"].str.contains("python|program|software", case=False)]
    else:
        df = courses[courses["course_title"].str.contains("business|management", case=False)]
    return df.iloc[0]["course_title"]

# ===============================
# Page config
# ===============================
st.set_page_config(page_title="Course Recommendation System", layout="wide")

st.title("🎓 Smart Course Recommendation System")

# ===============================
# Tabs
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Recommendation",
    "📊 Data Insights",
    "🧠 Model Explanation",
    "📁 Dataset Preview"
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

        st.success(f"✅ Recommended Course Type: **{course_type}**")
        st.info(f"📘 Suggested Course: **{course_name}**")

# ===============================
# TAB 2 — Data Insights
# ===============================
with tab2:
    st.subheader("Course Category Distribution")

    category_counts = courses["course_title"].str.extract(
        "(data|python|business)", expand=False
    ).value_counts()

    fig, ax = plt.subplots()
    category_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Courses")
    ax.set_title("Available Course Categories")

    st.pyplot(fig)

# ===============================
# TAB 3 — Model Explanation
# ===============================
with tab3:
    st.subheader("How the Model Works")

    st.markdown("""
    **Model Used:** Logistic Regression  

    **Input Variables:**
    - CGPA
    - Interest Area
    - Career Goal
    - Skill Level

    **Process:**
    1. Categorical variables are converted using One-Hot Encoding  
    2. Model predicts the most suitable course category  
    3. A real course is selected from the dataset  

    **Why Logistic Regression?**
    - Easy to interpret
    - Suitable for categorical outcomes
    - Reliable for decision support systems
    """)

# ===============================
# TAB 4 — Dataset Preview
# ===============================
with tab4:
    st.subheader("Coursera Dataset Preview")
    st.dataframe(courses.head(20))
