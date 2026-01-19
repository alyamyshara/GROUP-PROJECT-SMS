import streamlit as st
import pandas as pd
import joblib

# Load model and data
model = joblib.load("course_model.pkl")
courses = pd.read_csv("data/coursea_data.csv")
courses = courses.loc[:, ~courses.columns.str.contains("^Unnamed")]

def get_real_course(course_type):
    if course_type == "Data":
        df = courses[courses["course_title"].str.contains("data|analytics", case=False)]
    elif course_type == "Programming":
        df = courses[courses["course_title"].str.contains("python|program|software", case=False)]
    else:
        df = courses[courses["course_title"].str.contains("business|management", case=False)]
    
    return df.iloc[0]["course_title"]

st.title("🎓 Course Recommendation System")

cgpa = st.slider("CGPA", 2.5, 4.0, 3.0, 0.1)

interest = st.selectbox(
    "Interest Area",
    ["Data Science", "Business", "Computer Science"]
)

career = st.selectbox(
    "Career Goal",
    ["Data Analyst", "Software Engineer", "Business Analyst"]
)

skill = st.selectbox(
    "Skill Level",
    ["Beginner", "Intermediate", "Advanced"]
)

if st.button("Recommend Course"):
    input_df = pd.DataFrame([{
        "cgpa": cgpa,
        "interest": interest,
        "career_goal": career,
        "skill_level": skill
    }])

    course_type = model.predict(input_df)[0]
    course_name = get_real_course(course_type)

    st.success(f"Recommended Course: {course_name}")
