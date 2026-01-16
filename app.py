import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="TKN Studio", layout="wide")

# التصميم والألوان
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #00d26a; color: black; border-radius: 4px; font-weight: bold; width: 100%; }
</style>
""", unsafe_allow_html=True)

# التأكد من المفتاح
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

if not api_key:
    st.sidebar.warning("⚠️ لم يتم العثور على مفتاح في Secrets")
    api_key = st.sidebar.text_input("أدخل API Key هنا للتشغيل:", type="password")

if not api_key:
    st.warning("⚠️ من فضلك أدخل مفتاح API للبدء.")
    st.stop()

# تشغيل Gemini
genai.configure(api_key=api_key)

# واجهة البرنامج
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
        "Top-Down", "High Hero", "Back Spine"
    ])
    
    bg_color = st.text_input("Background", value="Pure White #FFFFFF")
    
    if st.button("EXECUTE PRODUCTION"):
        if not uploaded_file:
            st.error("Please upload an image first.")
        else:
            with st.spinner("Processing TKN Protocol..."):
                try:
                    image = Image.open(uploaded_file)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Professional product photography. Transform background to {bg_color}. Angle: {angle}. High quality, photorealistic."
                    
                    response = model.generate_content([prompt, image])
                    
                    st.success("Generation Complete!")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Error: {e}")
