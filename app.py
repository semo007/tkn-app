import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ---------------------------------------------------------
# 1. إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(page_title="TKN Studio", layout="wide")

# تخصيص الألوان
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #00d26a; color: black; border-radius: 4px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. التأكد من المفتاح (المحاولة من Secrets أو إدخال يدوي للطوارئ)
# ---------------------------------------------------------
api_key = None

# محاولة جلب المفتاح من Secrets
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# لو المفتاح مش موجود في Secrets، اطلب من المستخدم يدخله (حل مؤقت عشان يشتغل)
if not api_key:
    st.sidebar.warning("⚠️ لم يتم العثور على مفتاح في Secrets")
    api_key = st.sidebar.text_input("أدخل API Key هنا للتشغيل الفوري:", type="password")

if not api_key:
    st.warning("⬅️ من فضلك أدخل مفتاح API في القائمة الجانبية أو تأكد من إعدادات Secrets لتشغيل التطبيق.")
    st.stop()

# إعداد Gemini
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring API: {e}")

# ---------------------------------------------------------
# 3. واجهة TKN
# ---------------------------------------------------------
st.title("TKN – Product Imaging System")
st.markdown("`Protocol: V25.7 | Status: ONLINE`")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Upload Product Image", type=['png', 'jpg', 'jpeg', 'webp'])
    if uploaded_file:
        st.image(uploaded_file, caption="Source Image", use_column_width=True)

with col2:
    angle = st.selectbox("Target Angle", [
        "Front View", "Right Profile", "Three-Quarter", 
        "Top-Down", "High Hero", "Back Spine", "Macro Texture"
    ])
    
    bg_color = st.text_input("Background", value="Pure White #FFFFFF")
    
    if st.button("EXECUTE PRODUCTION"):
        if not uploaded_file:
            st.error("Please upload an image first.")
        else:
            with st.spinner("Processing TKN Protocol..."):
                try:
                    # فتح الصورة
                    image = Image.open(uploaded_file)
                    
                    # الموديل والبرومبت
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Act as a professional product photographer. Transform this product image to have a {bg_color} background. View angle: {angle}. Keep strict fidelity to the original product details. Output a high-quality photorealistic image."
                    
                    # التنفيذ
                    response = model.generate_content([prompt, image])
                    
                    # عرض النتيجة
                    st.success("Generation Complete!")
                    st.write(response.text) # في حالة لو الموديل رجع وصف
                    
                    # لو الموديل رجع صورة (حسب التحديثات)
                    if hasattr(response, 'parts'):
                         for part in response.parts:
                            if hasattr(part, "inline_data"): # images
                                st.image(part.inline_data, caption="Generated Image")
                            elif hasattr(part, "text"):
                                st.write(part.text)
                                
                except Exception as e:
                    st.error(f"Error
