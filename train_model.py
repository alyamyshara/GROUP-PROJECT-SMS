import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load real course data
courses = pd.read_csv("data/coursea_data.csv")
courses = courses.loc[:, ~courses.columns.str.contains("^Unnamed")]

# Synthetic student data
np.random.seed(42)
n = 400

students = pd.DataFrame({
    "cgpa": np.round(np.random.uniform(2.5, 4.0, n), 2),
    "interest": np.random.choice(["Data Science", "Business", "Computer Science"], n),
    "career_goal": np.random.choice(
        ["Data Analyst", "Software Engineer", "Business Analyst"], n
    ),
    "skill_level": np.random.choice(["Beginner", "Intermediate", "Advanced"], n)
})

# Target variable (CLEAR + DEFENSIBLE)
students["recommended_type"] = np.where(
    students["career_goal"] == "Data Analyst", "Data",
    np.where(students["career_goal"] == "Software Engineer", "Programming", "Business")
)

X = students[["cgpa", "interest", "career_goal", "skill_level"]]
y = students["recommended_type"]

# Preprocessing
preprocess = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["interest", "career_goal", "skill_level"]),
        ("num", "passthrough", ["cgpa"])
    ]
)

model = Pipeline([
    ("preprocess", preprocess),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X, y)

joblib.dump(model, "course_model.pkl")
