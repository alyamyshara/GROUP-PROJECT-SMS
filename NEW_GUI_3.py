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
# Career Options
# ===============================
career_options = [
    "Data Analyst",
    "Data Scientist",
    "Software Engineer",
    "AI / ML Engineer",
    "Business Analyst",
    "Cybersecurity Analyst",
    "Product Manager"
]

# ===============================
# Helper Functions
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
        "Data": "University of Michigan / Google / IBM",
        "Programming": "Harvard University (CS50) / MIT",
        "Business": "Wharton School / INSEAD"
    }
    return mapping.get(course_type, "Top Global University")

# -------------------------------
# Career Path Guidance (DETAILED)
# -------------------------------
def career_guidance(career):
    guidance = {
        "Data Analyst": {
            "Role Overview": "Analyze data to support business decision-making.",
            "Core Skills": [
                "Statistics and probability",
                "SQL and Python",
                "Data visualization (Tableau, Power BI)"
            ],
            "Recommended Tools": [
                "Excel", "Python", "SQL", "Power BI"
            ],
            "Career Progression": [
                "Junior Data Analyst",
                "Senior Data Analyst",
                "Data Scientist"
            ]
        },
        "Data Scientist": {
            "Role Overview": "Build predictive models and extract insights from data.",
            "Core Skills": [
                "Machine learning",
                "Advanced statistics",
                "Big data processing"
            ],
            "Recommended Tools": [
                "Python", "R", "TensorFlow", "Spark"
            ],
            "Career Progression": [
                "Data Scientist",
                "Senior Data Scientist",
                "AI Engineer"
            ]
        },
        "Software Engineer": {
            "Role Overview": "Design and develop software systems.",
            "Core Skills": [
                "Data structures & algorithms",
                "System design",
                "Software testing"
            ],
            "Recommended Tools": [
                "Python", "Java", "Git", "Docker"
            ],
            "Career Progression": [
                "Junior Software Engineer",
                "Senior Software Engineer",
                "Technical Lead"
            ]
        },
        "AI / ML Engineer": {
            "Role Overview": "Develop AI models and deploy intelligent systems.",
            "Core Skills": [
                "Deep learning",
                "Model optimization",
                "AI deployment"
            ],
            "Recommended Tools": [
                "PyTorch", "TensorFlow", "MLOps tools"
            ],
            "Career Progression": [
                "ML Engineer",
                "AI Engineer",
                "AI Architect"
            ]
        },
        "Business Analyst": {
            "Role Overview": "Bridge business needs and data-driven solutions.",
            "Core Skills": [
                "Business analysis",
                "Decision modeling",
                "Communication"
            ],
            "Recommended Tools": [
                "Excel", "Power BI", "SQL"
            ],
            "Career Progression": [
                "Business Analyst",
                "Senior BA",
                "Product Manager"
            ]
        },
        "Cybersecurity Analyst": {
            "Role Overview": "Protect systems and data from cyber threats.",
            "Core Skills": [
                "Network security",
                "Risk assessment",
                "Ethical hacking"
            ],
            "Recommended Tools": [
                "Wireshark", "Metasploit", "SIEM tools"
            ],
            "Career Progression": [
                "Security Analyst",
                "Security Engineer",
                "Security Architect"
            ]
        },
        "Product Manager": {
            "Role Overview": "Define product vision and coordinate teams.",
            "Core Skills": [
                "Product strategy",
                "User research",
                "Stakeholder management"
            ],
            "Recommended Tools": [
                "JIRA", "Figma", "Analytics tools"
            ],
            "Career Progression": [
                "Associate PM",
                "Product Manager",
                "Senior PM"
            ]
        }
    }
    return guidance.get(career, {})

# -------------------------------
# Skill Gap & Study Advice (DETAILED)
# -------------------------------
def skill_gap_advice(career, difficulty):
    advice = {
        "Beginner": {
            "Focus": "Build strong fundamentals.",
            "Learning Strategy": [
                "Take introductory courses",
                "Practice with small exercises",
                "Learn basic tools"
            ]
        },
        "Intermediate": {
            "Focus": "Apply knowledge in real scenarios.",
            "Learning Strategy": [
                "Work on projects",
                "Analyze real datasets",
                "Participate in internships"
            ]
        },
        "Advanced": {
            "Focus": "Specialize and master the domain.",
            "Learning Strategy": [
                "Advanced coursework",
                "Research papers",
                "Capstone projects"
            ]
        }
    }

    career_specific = {
        "Data Scientist": "Focus on ML models and real-world datasets.",
        "Software Engineer": "Practice system design and large projects.",
        "AI / ML Engineer": "Deploy models and optimize performance.",
        "Cybersecurity Analyst": "Practice penetration testing and monitoring.",
        "Product Manager": "Work on product case studies.",
        "Business Analyst": "Improve decision-making and reporting."
    }

    return advice[difficulty], career_specific.get(career, "")

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
        career = st.selectbox("Career Goal", career_options)
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
    st.subheader("Career Roadmap")

    selected_career = st.selectbox("Select Career", career_options)
    guidance = career_guidance(selected_career)

    st.markdown(f"### 🧠 {guidance['Role Overview']}")
    
    st.markdown("**Core Skills Required:**")
    for s in guidance["Core Skills"]:
        st.write("✔", s)

    st.markdown("**Recommended Tools & Technologies:**")
    for t in guidance["Recommended Tools"]:
        st.write("🛠️", t)

    st.markdown("**Typical Career Progression:**")
    for p in guidance["Career Progression"]:
        st.write("➡️", p)

# ===============================
# TAB 3 — Skill Gap & Study Advice
# ===============================
with tab3:
    st.subheader("Personalized Learning Plan")

    col1, col2 = st.columns(2)

    with col1:
        chosen_career = st.selectbox("Career Goal", career_options)

    with col2:
        difficulty = st.selectbox(
            "Current Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

    general, career_specific = skill_gap_advice(chosen_career, difficulty)

    st.markdown(f"### 🎯 Focus Area: {general['Focus']}")

    st.markdown("**Recommended Learning Strategy:**")
    for l in general["Learning Strategy"]:
        st.write("📘", l)

    st.info(f"💡 Career-Specific Advice: {career_specific}")

# ===============================
# TAB 4 — Interactive Chart
# ===============================
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
