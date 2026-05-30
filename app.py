import streamlit as st
from google import genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="منصة آسر التعليمية | Aser Platform",
    page_icon="🤖",
    layout="centered"
)

# --- 2. نظام إدارة اللغات والترجمات ---
if "lang" not in st.session_state:
    st.session_state.lang = "العربية"

# زر تبديل اللغة في أعلى الصفحة بشكل أنيق
col_space, col_lang = st.columns([4, 1])
with col_lang:
    current_lang = st.selectbox("🌐 Language / اللغة", ["العربية", "English"], index=0 if st.session_state.lang == "العربية" else 1)
    if current_lang != st.session_state.lang:
        st.session_state.lang = current_lang
        st.rerun()

# قاموس النصوص والترجمات لواجهة المستخدم
translations = {
    "العربية": {
        "direction": "rtl",
        "align": "right",
        "title": "منصة آسِر الذكية للتفاعل الصوتي",
        "subtitle": "بيئة تعليمية متطورة لتحليل نبرة الحماس أثناء القراءة مباشرة",
        "input_label": "📖 اختر نصاً للقراءة أو اكتب نصك الخاص:",
        "placeholder": "اختر من القائمة أعلاه أو اكتب هنا النص المراد التدرب عليه...",
        "ai_label": "🧠 رد المساعد الذكي (آسِر):",
        "ai_default": "مرحباً بك يا صديقي! أنا جاهز للاستماع إليك ومشاركتك رحلة القراءة. ✨📚",
        "custom_text": "✍️ نص مخصص (اكتب نصك هنا)",
        "passages": [
            "✍️ نص مخصص (اكتب نصك هنا)",
            "الحرية شمس يجب أن تشرق في كل نفس، فمن عاش محرومًا منها عاش في ظلمة حالكة.",
            "النجاح ليس مفتاح السعادة، بل السعادة هي مفتاح النجاح. إذا كنت تحب ما تفعل، فستنجح بالتأكيد.",
            "القراءة تغذي العقل، وتفتح أبواب المعرفة، وتأخذنا في رحلات ساحرة عبر الزمن دون أن نتحرك من مكاننا."
        ],
        "mic_btn_idle": "🎙️ اضغط لتفعيل الاتصال الصوتي المباشر",
        "mic_btn_active": "🟢 النظام متصل ويحلل صوتك الآن...",
        "status_idle": "آسر في انتظار بدء القراءة المستمرة...",
        "status_normal": "قراءة ممتازة ونبرة صوتية واضحة ومستقرة",
        "status_high": "أداء مذهل! نبرة مليئة بالحماس والطاقة العالية",
        "indicator_title": "📊 مؤشر التفاعل الصوتي اللحظي",
        "status_title": "حالة المساعد الذكي"
    },
    "English": {
        "direction": "ltr",
        "align": "left",
        "title": "Aser Smart Audio Interactive Platform",
        "subtitle": "An advanced educational environment to analyze reading enthusiasm in real-time",
        "input_label": "📖 Choose a reading passage or write your own:",
        "placeholder": "Select from the list above or type your own text here...",
        "ai_label": "🧠 Smart Assistant Reply (Aser):",
        "ai_default": "Hello my friend! I am ready to listen to you and share your reading journey. ✨📚",
        "custom_text": "✍️ Custom Text (Type your own)",
        "passages": [
            "✍️ Custom Text (Type your own)",
            "The early bird catches the worm. Success comes to those who prepare well and work hard.",
            "Reading is to the mind what exercise is to the body. It expands our horizons and inspires our souls.",
            "Believe you can and you're halfway there. Confidence and enthusiasm are the keys to achievements."
        ],
        "mic_btn_idle": "🎙️ Click to activate live voice connection",
        "mic_btn_active": "🟢 System is connected and analyzing your voice...",
        "status_idle": "Aser is waiting for you to start reading continuously...",
        "status_normal": "Excellent reading with a clear and stable tone",
        "status_high": "Amazing performance! Full of enthusiasm and high energy",
        "indicator_title": "📊 Real-time Voice Engagement Indicator",
        "status_title": "Assistant Status"
    }
}

t = translations[st.session_state.lang]

# --- 3. تصميم الـ CSS المتجاوب مع الاتجاهين ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }}
    .main-title {{
        color: #1E293B;
        font-family: 'Segoe UI', system-ui, sans-serif;
        text-align: center;
        font-weight: 700;
        font-size: 32px;
        margin-top: 10px;
        margin-bottom: 5px;
    }}
    .subtitle {{
        color: #64748B;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        margin-bottom: 25px;
    }}
    div[data-baseweb="input"], div[data-baseweb="select"] {{
        border-radius: 12px !important;
    }}
    div[data-testid="stMarkdownContainer"] {{
        text-align: {t['align']};
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. إعداد مفتاح ومكتبة Google GenAI ---
API_KEY = "AIzaSyAOBg67pMTj2gYrc7PCs2MmRzQGhfedGmI"

@st.cache_resource
def get_ai_client():
    if API_KEY and "ضـع" not in API_KEY:
        return genai.Client(api_key=API_KEY)
    return None

client = get_ai_client()

st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='subtitle'>{t['subtitle']}</div>", unsafe_allow_html=True)

if "ai_reply" not in st.session_state:
    st.session_state.ai_reply = t["ai_default"]
if "last_text" not in st.session_state:
    st.session_state.last_text = ""

# --- 5. محرك البث اللحظي الآمن والمفصول برمجياً عن تعارض الأقواس ---
raw_html_template = """
<div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); font-family: 'Segoe UI', system-ui, sans-serif; direction: DIRECTION_HOLDER;">
    
    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <div id="emoji" style="font-size: 55px; background: #F8FAFC; padding: 10px 20px; border-radius: 50%; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); transition: all 0.4s ease;">😴</div>
        <div style="text-align: ALIGN_HOLDER;">
            <div style="color: #94A3B8; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 2px;">STATUS_TITLE_HOLDER</div>
            <div id="status-text" style="color: #334155; font-size: 15px; font-weight: 600;">STATUS_IDLE_HOLDER</div>
        </div>
    </div>

    <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 6px;">
            <span>INDICATOR_TITLE_HOLDER</span>
            <span id="percentage-txt">0%</span>
        </div>
        <div style="background-color: #F1F5F9; border-radius: 9999px; height: 8px; width: 100%; overflow: hidden;">
            <div id="progress-bar" style="background-color: #2563EB; height: 100%; width: 0%; transition: width 0.3s ease, background-color 0.4s;"></div>
        </div>
    </div>

    <div style="text-align: center;">
        <button id="micBtn" style="background-color: #2563EB; color: #FFFFFF; border: none; padding: 14px 40px; border-radius: 10px; font-size: 15px; cursor: pointer; font-weight: 600; box-shadow: 0 4px 12px rgba(37,99,235,0.2); transition: all 0.2s ease; width: 100%; max-width: 400px;">
            MIC_BTN_IDLE_HOLDER
        </button>
    </div>
</div>

<script>
const micBtn = document.getElementById('micBtn');
const emojiDiv = document.getElementById('emoji');
const statusTxt = document.getElementById('status-text');
const progressBar = document.getElementById('progress-bar');
const percentageTxt = document.getElementById('percentage-txt');
let isListening = false;
let stableState = "sleep"; 
let stateTimer = null;

micBtn.onclick = async function() {
    if (isListening) return;
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true }, 
            video: false 
        });
        isListening = true;
        micBtn.innerText = "MIC_BTN_ACTIVE_HOLDER";
        micBtn.style.backgroundColor = "#10B981";
        
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const analyser = audioContext.createAnalyser();
        const microphone = audioContext.createMediaStreamSource(stream);
        const javascriptNode = audioContext.createScriptProcessor(2048, 1, 1);
        
        analyser.smoothingTimeConstant = 0.8;
        analyser.fftSize = 256;
        
        microphone.connect(analyser);
        analyser.connect(javascriptNode);
        javascriptNode.connect(audioContext.destination);
        
        javascriptNode.onaudioprocess = function() {
            let array = new Uint8Array(analyser.frequencyBinCount);
            analyser.getByteFrequencyData(array);
            let values = 0;
            for (let i = 0; i < array.length; i++) { values += array[i]; }
            let average = values / array.length;
            
            if (average < 5) average = 0; 
            let targetPercentage = Math.min(Math.round((average / 45) * 100), 100);
            
            progressBar.style.width = targetPercentage + "%";
            percentageTxt.innerText = targetPercentage + "%";
            
            let targetState = "sleep";
            if (targetPercentage >= 70) {
                targetState = "high";
            } else if (targetPercentage >= 20) {
                targetState = "normal";
            }
            
            if (targetState !== stableState) {
                if (!stateTimer) {
                    stateTimer = setTimeout(() => {
                        stableState = targetState;
                        updateVisuals(stableState);
                        stateTimer = null;
                    }, 350);
                }
            } else {
                if (stateTimer) { clearTimeout(stateTimer); stateTimer = null; }
                if (stableState === "high") progressBar.style.backgroundColor = "#10B981";
                else if (stableState === "normal") progressBar.style.backgroundColor = "#3B82F6";
                else progressBar.style.
