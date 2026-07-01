import streamlit as st
import requests

st.set_page_config(page_title="JDX AI", layout="wide")

st.markdown("""
<style>
.jd-box {
    background: #ffffff;
    padding: 25px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin-top: 20px;
    font-family: "Tahoma", sans-serif;
    line-height: 1.8;
    direction: rtl;
    text-align: right;
}

.jd-title {
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 15px;
}

@media print {
    .stButton, .stTextInput, .stTextArea, .stSubheader {
        display: none !important;
    }
    .jd-box {
        border: none;
        box-shadow: none;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("JDX AI — مولد الوصف الوظيفي")

if "jd_blocks" not in st.session_state:
    st.session_state["jd_blocks"] = [{}]

def generate_jd(title, tasks, skills):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": "Bearer ضع_مفتاحك_هنا",
        "Content-Type": "application/json"
    }

    prompt = f"""
    أنشئ وصف وظيفي احترافي للمسمى الوظيفي التالي:
    المسمى الوظيفي: {title}
    المهام الأساسية: {tasks}
    المهارات المطلوبة: {skills}

    أريد:
    - ملخص الوظيفة
    - المهام والمسؤوليات
    - المهارات المطلوبة
    - المؤهلات
    - الأدوات المستخدمة
    - خبرة العمل المطلوبة
    """

    data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]


for index, block in enumerate(st.session_state["jd_blocks"]):
    st.subheader(f"الوصف الوظيفي رقم {index + 1}")

    title = st.text_input(f"المسمى الوظيفي {index + 1}", key=f"title_{index}")
    tasks = st.text_area(f"المهام الأساسية {index + 1}", key=f"tasks_{index}")
    skills = st.text_area(f"المهارات المطلوبة {index + 1}", key=f"skills_{index}")

    if st.button(f"توليد الوصف الوظيفي {index + 1}"):
        jd_text = generate_jd(title, tasks, skills)
        st.session_state[f"jd_result_{index}"] = jd_text

    if f"jd_result_{index}" in st.session_state:
        st.markdown("### النتيجة:")

        st.markdown(
            f"""
            <div class="jd-box">
                <div class="jd-title">{title}</div>
                {st.session_state[f"jd_result_{index}"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info("لطباعة الوصف كـ PDF اضغط: Ctrl + P")

    st.markdown("---")

if st.button("+ إضافة وصف وظيفي جديد"):
    st.session_state["jd_blocks"].append({})
    st.experimental_rerun()
