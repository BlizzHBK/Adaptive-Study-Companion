import streamlit as st
import json

# ---------- LOAD DATA ----------
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------- QUIZ QUESTIONS ----------
quiz = [
    {"q": "2 + 2 = ?", "a": "4", "topic": "Arithmetic"},
    {"q": "5 * 6 = ?", "a": "30", "topic": "Multiplication"},
    {"q": "10 - 3 = ?", "a": "7", "topic": "Subtraction"}
]

# ---------- UI ----------
st.title("📚 AI Study Companion")

menu = st.sidebar.selectbox("Menu", ["Quiz", "Progress", "Study Plan"])

# ---------- QUIZ ----------
if menu == "Quiz":
    st.header("📝 Quiz")

    answers = []

    # FRONTEND
    for i, q in enumerate(quiz):
        ans = st.text_input(q["q"], key=i)
        answers.append(ans)

    if st.button("Submit Quiz"):
        score = 0
        mistakes = []

        # BACKEND
        for i, q in enumerate(quiz):
            if answers[i].strip() == q["a"]:
                score += 1
            else:
                mistakes.append(q["topic"])

        # SAVE DATA
        subject = "Math"
        if subject not in data:
            data[subject] = {"mistakes": []}

        data[subject]["mistakes"].extend(mistakes)
        save_data(data)

        # FRONTEND OUTPUT
        st.success(f"Score: {score}/{len(quiz)}")

        if mistakes:
            st.warning("Weak Topics:")
            st.write(set(mistakes))

            # AI Insight
            st.info(f"🤖 AI Insight: Focus on {mistakes[-1]}")

        # Metrics UI
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Score", score)
        with col2:
            st.metric("Mistakes", len(mistakes))

# ---------- PROGRESS ----------
elif menu == "Progress":
    st.header("📊 Progress")

    if not data:
        st.info("No data yet")
    else:
        for subject, info in data.items():
            st.subheader(subject)

            if info["mistakes"]:
                st.write("Weak Topics:", set(info["mistakes"]))
            else:
                st.write("No mistakes 🎉")

# ---------- STUDY PLAN ----------
elif menu == "Study Plan":
    st.header("🧠 AI Study Plan")

    if not data:
        st.info("No data available")
    else:
        for subject, info in data.items():
            st.subheader(subject)

            count = len(info["mistakes"])

            # BACKEND LOGIC
            if count >= 5:
                st.error("🚨 High priority! Revise immediately")
            elif count >= 2:
                st.warning("⚠️ Needs revision")
            else:
                st.success("✅ You are doing well")

            # AI Suggestion
            if info["mistakes"]:
                st.write("👉 Focus Topic:", info["mistakes"][-1])