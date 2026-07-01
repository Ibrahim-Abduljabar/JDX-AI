import streamlit as st
import requests
import os

st.set_page_config(page_title="JDX AI", layout="wide")

st.markdown("<h1 style='text-align: center;'>مولد الوصف الوظيفي — JDX AI</h1>", unsafe_allow_html=True)

def generate_jd(title, tasks, skills):
    api_key = os.getenv("GROQ_API_KEY")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    اكتب وصفًا وظيفيًا احترافيًا للمسمى الوظيفي: {title}
    المهام الأساسية:
    {tasks}

    المهارات المطلوبة:
    {skills}

    اكتب الوصف بشكل منسق وواضح.
    """

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" not in result:
        return "⚠ حدث خطأ أثناء الاتصال بالنموذج. تأكد من صحة المفتاح أو أعد المحاولة."

    return result["choices"][0]["message"]["content"]


st.markdown("### الوصف الوظيفي رقم 1")

title = st.text_input("المسمى الوظيفي", "")
tasks = st.text_area("المهام الأساسية", "")
skills = st.text_area("المهارات المطلوبة", "")

if st.button("توليد الوصف الوظيفي"):
    if title.strip() == "" or tasks.strip() == "" or skills.strip() == "":
        st.error("رجاءً عبّئ جميع الحقول قبل التوليد.")
    else:
        jd_text = generate_jd(title, tasks, skills)

        st.markdown("### النتيجة:")
        st.markdown(
            f"""
            <div style="
                padding: 15px;
                background: #f7f7f7;
                border-radius: 10px;
                border: 1px solid #ddd;
                line-height: 1.8;
            ">
                {jd_text}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info("إذا تبغى تحفظ الوصف كـ PDF اضغط Ctrl + P")

if st.button("➕ إضافة وصف وظيفي جديد"):
    st.rerun()
