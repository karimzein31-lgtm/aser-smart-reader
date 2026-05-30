import streamlit as st
from google import genai
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة والهوية البصرية الاحترافية ---
st.set_page_config(
    page_title="منصة آسر التعليمية",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }
    .main-title {
        color: #1E293B;
        font-family: 'Segoe UI', system-ui, sans-serif;
        text-align: center;
        font-weight: 700;
        font-size: 32px;
        margin-top: 20px;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .subtitle {
        color: #64748B;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        margin-bottom: 30px;
    }
    div[data-baseweb="input"] {
        border-radius: 12px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. إعداد مفتاح ومكتبة Google GenAI ---
API_KEY = "AIzaSyAOBg67pMTj2gYrc7PCs2MmRzQGhfedGmI"

@st.cache_resource
def get_ai_client():
    if API_KEY and "ضـع" not in API_KEY:
        return genai.Client(api_key=API_KEY)
    return None

client = get_ai_client()

# --- 3. الهيكل الخارجي للواجهة ---
st.markdown("<div class='main-title'>منصة آسِر الذكية للتفاعل الصوتي</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>بيئة تعليمية متطورة لتحليل نبرة الحماس أثناء القراءة مباشرة</div>", unsafe_allow_html=True)

if "ai_reply" not in st.session_state:
    st.session_state.ai_reply = "مرحباً بك يا صديقي! أنا جاهز للاستماع إليك ومشاركتك رحلة القراءة. ✨📚"
if "last_text" not in st.session_state:
    st.session_state.last_text = ""

# --- 4. محرك البث اللحظي المطور بالتنعيم والتهدئة البرمجية ---
professional_ui_html = """
<div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); font-family: 'Segoe UI', system-ui, sans-serif; direction: rtl;">
    
    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 25px;">
        <div id="emoji" style="font-size: 55px; background: #F8FAFC; padding: 10px 20px; border-radius: 50%; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); transition: all 0.4deg cubic-bezier(0.4, 0, 0.2, 1);">😴</div>
        <div style="text-align: right;">
            <div style="color: #94A3B8; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 2px;">حالة المساعد الذكي</div>
            <div id="status-text" style="color: #334155; font-size: 15px; font-weight: 600; transition: color 0.3s;">آسر في انتظار بدء القراءة المستمرة...</div>
        </div>
    </div>

    <div style="margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 6px;">
            <span>📊 مؤشر التفاعل الصوتي اللحظي</span>
            <span id="percentage-txt">0%</span>
        </div>
        <div style="background-color: #F1F5F9; border-radius: 9999px; height: 8px; width: 100%; overflow: hidden;">
            <div id="progress-bar" style="background-color: #2563EB; height: 100%; width: 0%; transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.4s;"></div>
        </div>
    </div>

    <div style="text-align: center;">
        <button id="micBtn" style="background-color: #2563EB; color: #FFFFFF; border: none; padding: 14px 40px; border-radius: 10px; font-size: 15px; cursor: pointer; font-weight: 600; box-shadow: 0 4px 12px rgba(37,99,235,0.2); transition: all 0.2s ease; width: 100%; max-width: 400px;">
            🎙️ اضغط لتفعيل الاتصال الصوتي المباشر
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

// متغيرات الذاكرة لتهدئة ومنع القفزات السريعة
let currentLevel = 0;
let stableState = "sleep"; // sleep, normal, high
let stateTimer = null;

micBtn.onclick = async function() {
    if (isListening) return;
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
        isListening = true;
        micBtn.innerText = "🟢 النظام متصل ويحلل صوتك الآن...";
        micBtn.style.backgroundColor = "#10B981";
        micBtn.style.boxShadow = "0 4px 12px rgba(16,185,129,0.2)";
        
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const analyser = audioContext.createAnalyser();
        const microphone = audioContext.createMediaStreamSource(stream);
        const javascriptNode = audioContext.createScriptProcessor(2048, 1, 1);
        
        // رفع التنعيم لأعلى درجة (0.85) لجعل حركة المؤشر انسيابية جداً وليست عصبية
        analyser.smoothingTimeConstant = 0.85;
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
            
            if (average < 6) average = 0; 
            let targetPercentage = Math.min(Math.round((average / 55) * 100), 100);
            
            // تحديث النسبة المئوية وشريط التقدم تدريجياً وبنعومة
            progressBar.style.width = targetPercentage + "%";
            percentageTxt.innerText = targetPercentage + "%";
            
            // تحديد الحالة المستهدفة بناءً على نبرة الصوت الحالية
            let targetState = "sleep";
            if (targetPercentage >= 65) {
                targetState = "high";
            } else if (targetPercentage >= 20) {
                targetState = "normal";
            }
            
            // آلية التهدئة (Debounce): لا نغير الإيموجي والنص فوراً، بل ننتظر نصف ثانية (500ms) للتأكد من استقرار النبرة
            if (targetState !== stableState) {
                if (!stateTimer) {
                    stateTimer = setTimeout(() => {
                        stableState = targetState;
                        updateVisuals(stableState, targetPercentage);
                        stateTimer = null;
                    }, 500); // 500 مللي ثانية للثبات والاتزان
                }
            } else {
                if (stateTimer) {
                    clearTimeout(stateTimer);
                    stateTimer = null;
                }
                // تحديث طفيف للون الشريط حتى لو كانت الحالة ثابتة
                if (stableState === "high") progressBar.style.backgroundColor = "#10B981";
                else if (stableState === "normal") progressBar.style.backgroundColor = "#3B82F6";
                else progressBar.style.backgroundColor = "#94A3B8";
            }
        }
    } catch (err) {
        alert("يرجى تفعيل صلاحية المايكروفون.");
    }
};

// دالة تحديث الواجهات الهادئة والموزونة
function updateVisuals(state, percentage) {
    if (state === "high") {
        emojiDiv.innerText = "🤩";
        statusTxt.innerText = "أداء مذهل! نبرة مليئة بالحماس والطاقة العالية";
    } else if (state === "normal") {
        emojiDiv.innerText = "😊";
        statusTxt.innerText = "قراءة ممتازة ونبرة صوتية واضحة ومستقرة";
    } else {
        emojiDiv.innerText = "🥱";
        statusTxt.innerText = "في استماع دائم.. بانتظار بدء التحدث أو رفع الصوت قليلاً";
    }
}
</script>
"""

components.html(professional_ui_html, height=250)

st.write("") 

# --- 5. حقل مدخلات النص وصندوق رد آسر الذكي ---
teacher_text = st.text_input(
    label="نص القراءة الحالي:",
    placeholder="اكتب هنا النص المراد التدرب على قراءته لتلقي التغذية الراجعة من آسر...",
    value=""
)

if teacher_text and teacher_text != st.session_state.last_text:
    st.session_state.last_text = teacher_text
    if client:
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"أنت طالب ذكي ومشجع اسمه آسر. رد باختصار شديد جداً (سطر واحد) وبأسلوب تعليمي لطيف على جملة معلمك أو صديقك التي كتبها لك الآن وهي: {teacher_text}."
            )
            st.session_state.ai_reply = response.text
        except:
            st.session_state.ai_reply = "أهلاً بك! أنا أستمع إليك الآن بدقة."

st.markdown("<p style='font-weight: 600; color: #475569; font-size: 14px; margin-bottom: 5px; text-align: right;'>🧠 رد المساعد الذكي (آسِر):</p>", unsafe_allow_html=True)
st.info(st.session_state.ai_reply)