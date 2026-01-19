import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# =====================================================
# Page configuration (MUST be first Streamlit command)
# =====================================================
st.set_page_config(
    page_title="Smart Course Recommendation System",
    layout="wide"
)

# =====================================================
# Load model and dataset
# =====================================================
model = joblib.load("course_model.pkl")

courses = pd.read_csv("data/coursea_data.csv")
courses = courses.loc[:, ~courses.columns.str.contains("^Unnamed")]

# =====================================================
# Global Options
# =====================================================
career_options = [
    "Data Analyst",
    "Data Scientist",
    "Software Engineer",
    "AI / ML Engineer",
    "Business Analyst",
    "Cybersecurity Analyst",
    "Product Manager"
]

skill_levels = ["Beginner", "Intermediate", "Advanced"]

interest_areas = ["Data Science", "Business", "Computer Science"]

# =====================================================
# Helper Functions
# =====================================================
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
        "Data": "University of Michigan / Google / IBM",
        "Programming": "Harvard University (CS50) / MIT",
        "Business": "Wharton School / INSEAD"
    }
    return mapping.get(course_type, "Top Global University")

# -------------------------------
# Career Path Guidance (Detailed)
# -------------------------------
def career_guidance(career):
    return {
        "Data Analyst": {
            "Overview": "Analyze structured data to support operational and strategic decisions.",
            "Core Skills": [
                "Statistics and probability",
                "SQL and Python",
                "Data visualization"
            ],
            "Tools": ["Excel", "SQL", "Python", "Power BI"],
            "Career Path": [
                "Junior Data Analyst",
                "Senior Data Analyst",
                "Data Scientist"
            ]
        },
        "Data Scientist": {
            "Overview": "Develop predictive models and advanced analytics solutions.",
            "Core Skills": [
                "Machine learning",
                "Advanced statistics",
                "Big data processing"
            ],
            "Tools": ["Python", "R", "TensorFlow", "Spark"],
            "Career Path": [
                "Data Scientist",
                "Senior Data Scientist",
                "AI Engineer"
            ]
        },
        "Software Engineer": {
            "Overview": "Design, build, and maintain scalable software systems.",
            "Core Skills": [
                "Algorithms and data structures",
                "System design",
                "Software testing"
            ],
            "Tools": ["Python", "Java", "Git", "Docker"],
            "Career Path": [
                "Junior Software Engineer",
                "Senior Software Engineer",
                "Technical Lead"
            ]
        },
        "AI / ML Engineer": {
            "Overview": "Deploy and optimize AI and machine learning systems.",
            "Core Skills": [
                "Deep learning",
                "Model optimization",
                "MLOps"
            ],
            "Tools": ["PyTorch", "TensorFlow", "MLflow"],
            "Career Path": [
                "ML Engineer",
                "AI Engineer",
                "AI Architect"
            ]
        },
        "Business Analyst": {
            "Overview": "Translate business problems into data-driven solutions.",
            "Core Skills": [
                "Business analysis",
                "Decision modeling",
                "Communication"
            ],
            "Tools": ["Excel", "SQL", "Power BI"],
            "Career Path": [
                "Business Analyst",
                "Senior BA",
                "Product Manager"
            ]
        },
        "Cybersecurity Analyst": {
            "Overview": "Protect systems and data from cyber threats.",
            "Core Skills": [
                "Network security",
                "Risk assessment",
                "Incident response"
            ],
            "Tools": ["Wireshark", "Metasploit", "SIEM tools"],
            "Career Path": [
                "Security Analyst",
                "Security Engineer",
                "Security Architect"
            ]
        },
        "Product Manager": {
            "Overview": "Define product vision and coordinate cross-functional teams.",
            "Core Skills": [
                "Product strategy",
                "User research",
                "Stakeholder management"
            ],
            "Tools": ["JIRA", "Figma", "Analytics tools"],
            "Career Path": [
                "Associate PM",
                "Product Manager",
                "Senior PM"
            ]
        }
    }[career]

# -------------------------------
# Skill Gap & Study Advice
# -------------------------------
def skill_gap_advice(career, level):
    general = {
        "Beginner": {
            "Focus": "Build strong fundamentals",
            "Actions": [
                "Take introductory courses",
                "Practice basic exercises",
                "Learn core tools"
            ]
        },
        "Intermediate": {
            "Focus": "Apply knowledge practically",
            "Actions": [
                "Complete hands-on projects",
                "Work with real datasets",
                "Participate in internships"
            ]
        },
        "Advanced": {
            "Focus": "Specialize and master skills",
            "Actions": [
                "Advanced coursework",
                "Research papers",
                "Capstone projects"
            ]
        }
    }

    career_specific = {
        "Data Analyst": "Focus on dashboards and business reporting.",
        "Data Scientist": "Improve model tuning and feature engineering.",
        "Software Engineer": "Practice system design and scalability.",
        "AI / ML Engineer": "Deploy and optimize ML pipelines.",
        "Business Analyst": "Strengthen decision analysis and communication.",
        "Cybersecurity Analyst": "Practice penetration testing and monitoring.",
        "Product Manager": "Work on product case studies and roadmaps."
    }

    return general[level], career_specific[career]

# =====================================================
# App Title
# =====================================================
st.title("🎓 Smart Course Recommendation System")

# =====================================================
# Tabs
# =====================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Course Recommendation",
    "🧭 Career Path Guidance",
    "📈 Skill Gap & Study Advice",
    "📊 Course Trends"
])

# =====================================================
# TAB 1 — Course Recommendation
# =====================================================
with tab1:
    st.subheader("Student Profile")

    col1, col2 = st.columns(2)

    with col1:
        cgpa = st.slider("CGPA", 2.5, 4.0, 3.0, 0.1, key="cgpa")
        interest = st.selectbox("Interest Area", interest_areas, key="interest")

    with col2:
        career = st.selectbox("Career Goal", career_options, key="career_tab1")
        skill = st.selectbox("Skill Level", skill_levels, key="skill_tab1")

    if st.button("🎯 Recommend Course", key="recommend_btn"):
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

# =====================================================
# TAB 2 — Career Path Guidance
# =====================================================
with tab2:
    st.subheader("Career Roadmap")

    selected_career = st.selectbox(
        "Select Career",
        career_options,
        key="career_tab2"
    )

    guide = career_guidance(selected_career)

    st.markdown(f"### 🔍 Role Overview")
    st.write(guide["Overview"])

    st.markdown("### 🧠 Core Skills Required")
    for s in guide["Core Skills"]:
        st.write("✔", s)

    st.markdown("### 🛠️ Recommended Tools & Technologies")
    for t in guide["Tools"]:
        st.write("🔧", t)

    st.markdown("### 📈 Typical Career Progression")
    for p in guide["Career Path"]:
        st.write("➡️", p)

# =====================================================
# TAB 3 — Skill Gap & Study Advice
# =====================================================
with tab3:
    st.subheader("Personalized Learning Plan")

    col1, col2 = st.columns(2)

    with col1:
        chosen_career = st.selectbox(
            "Career Goal",
            career_options,
            key="career_tab3"
        )

    with col2:
        difficulty = st.selectbox(
            "Current Skill Level",
            skill_levels,
            key="difficulty_tab3"
        )

    general, career_specific = skill_gap_advice(chosen_career, difficulty)

    st.markdown(f"### 🎯 Learning Focus: {general['Focus']}")

    st.markdown("### 📘 Recommended Learning Actions")
    for a in general["Actions"]:
        st.write("•", a)

    st.info(f"💡 Career-Specific Advice: {career_specific}")

# =====================================================
# TAB 4 — Course Trends (Interactive Chart)
# =====================================================
with tab4:
    st.subheader("Course Category Trends")

    courses["category"] = courses["course_title"].str.extract(
        "(Data|Python|Business)", expand=False
    )

    category_counts = courses["category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Number of Courses"]

    fig = px.bar(
        category_counts,
        x="Category",
        y="Number of Courses",
        text="Number of Courses",
        title="Distribution of Available Courses"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)
