import streamlit as st
from groq import Groq

# --- إعدادات الصفحة ---
st.set_page_config(page_title="X Assistant PRO", page_icon="🤖", layout="centered")

# --- استدعاء مفتاح الأمان (API Key) من Streamlit Secrets ---
# تأكد إنك ضفت GROQ_API_KEY في إعدادات Secrets في موقع Streamlit
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except Exception:
    st.error("يا حريف، لازم تضيف الـ API Key في الـ Secrets بتاعة Streamlit عشان البوت يشتغل.")
    st.stop()

# --- عنوان التطبيق ---
st.title("🤖 X Assistant PRO")
st.markdown(f"---")
st.caption("Developed by: **Ahmed El-Hareef** | المبرمج: أحمد الحريف")

# --- تهيئة الذاكرة (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "أنت مساعد ذكي ومرح اسمك 'X Assistant'. اللي صنعك ومبرمجك هو 'أحمد الحريف'. اتكلم دايماً بالعامية المصرية، وردودك تكون ذكية وخفيفة الظل. لو حد سألك عن هويتك قول إنك نسخة مطورة من برمجة الحريف."
        }
    ]

# --- عرض الرسائل السابقة في الواجهة ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- استقبال سؤال المستخدم ---
if prompt := st.chat_input("قول يا حريف، محتاج مساعدة في إيه؟"):
    # إضافة سؤال المستخدم للذاكرة وللواجهة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- توليد الرد من الذكاء الاصطناعي ---
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # استخدام موديل Llama 3 (سريع جداً ومستقر)
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            # عرض الرد بشكل تدريجي (Streaming)
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # إضافة رد البوت للذاكرة
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error("حصلت مشكلة في الاتصال بالسيرفر، جرب تاني يا بطل.")
          
