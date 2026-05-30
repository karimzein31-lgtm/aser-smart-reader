import streamlit as st
from google import genai
import streamlit.components.v1 as components
import os

# --- 1. إعدادات الصفحة واللغة ---
st.set_page_config(page_title="منصة آسر التعليمية", page_icon="🤖", layout="centered")

if "lang" not in st.session_state:
    st.session_state.lang = "العربية"

col_space, col_lang = st.columns([4, 1])
with col_lang:
    current_lang = st.selectbox("🌐 Language / اللغة", ["العربية", "English"], index=0 if st.session_state.lang == "العربية" else 1)
    if current_lang != st.session_state.lang:
        st.session_state.lang = current_lang
        st.rerun()

# --- 2. قاموس البيانات والنصوص المطولة ---
translations = {
    "العربية": {
        "direction": "rtl", "align": "right",
        "title": "منصة آسِر الذكية ✏️",
        "subtitle": "بيئة تعليمية تفاعلية ممتعة لتحليل نبرة الحماس أثناء القراءة مباشرة!",
        "input_label": "📖 اختر نصاً كاملاً للقراءة أو اكتب نصك الخاص:",
        "placeholder": "اختر من القائمة أعلاه أو اكتب هنا النص المراد التدرب عليه...",
        "ai_label": "🧠 رد المساعد الذكي (آسِر):",
        "ai_default": "مرحباً بك يا صديقي! أنا جاهز للاستماع إليك ومشاركتك رحلة القراءة. ✨📚",
        "custom_text": "✍️ نص مخصص (اكتب نصك هنا)",
        "passages": [
            "✍️ نص مخصص (اكتب نصك هنا)",
            "الحرية شمس يجب أن تشرق في كل نفس، فمن عاش محرومًا منها عاش في ظلمة حالكة لا يرى فيها نوراً الشروق. إن القيمة الحقيقية للإنسان تكمن في قدرته على اتخاذ قراراته بنفسه وبناء مستقبله بكل ثقة وإصرار، فالأمم لا تنهض ولا ترتقي إلا عندما يتنفس أفرادها عبير الحرية والكرامة.",
            "النجاح ليس مفتاح السعادة، بل إن السعادة الحقيقية والرضا الداخلي هما المفتاح الأساسي للنجاح. إذا كنت تحب ما تفعله، وتمتلك الشغف اليومي للاستمرار والتعلم من الأخطاء دون استسلام، فستصل بالتأكيد إلى أهدافك وتصنع لنفسك مساراً متميزاً يلهم الآخرين من حولك.",
            "القراءة هي الغذاء الحقيقي للعقل، وهي النافذة السحرية التي تفتح لنا أبواب المعرفة الواسعة وتأخذنا في رحلات مذهلة عبر الزمن والبلدان دون أن نتحرك من مكاننا. من يعشق القراءة لا يشعر بالوحدة أبداً، لأن الكتب تصبح أعز أصدقائه وتمنحه الحكمة والخبرة لمواجهة الحياة."
        ],
        "mic_idle": "🎙️ اضغط لتفعيل الاتصال الصوتي المباشر", "mic_active": "🟢 النظام متصل ويحلل صوتك الآن...",
        "status_idle": "آسر في انتظار بدء القراءة المستمرة...", "status_normal": "قراءة ممتازة ونبرة صوتية واضحة ومستقرة", "status_high": "أداء مذهل! نبرة مليئة بالحماس والطاقة العالية",
        "indicator_title": "📊 مؤشر التفاعل الصوتي اللحظي", "status_title": "حالة المساعد الذكي"
    },
    "English": {
        "direction": "ltr", "align": "left",
        "title": "Aser Smart Platform ✏️",
        "subtitle": "A fun interactive learning environment to analyze reading enthusiasm in real-time!",
        "input_label": "📖 Choose a full passage or write your own:",
        "placeholder": "Select from the list above or type your own text here...",
        "ai_label": "🧠 Smart Assistant Reply (Aser):",
        "ai_default": "Hello my friend! I am ready to listen to you and share your reading journey. ✨📚",
        "custom_text": "✍️ Custom Text (Type your own)",
        "passages": [
            "✍️ Custom Text (Type your own)",
            "The early bird catches the worm, which means that success and outstanding achievement come to those who prepare well, wake up with determination, and work hard while others are still resting. True dedication is the golden key that opens doors to incredible opportunities and shapes a bright and prosperous future.",
            "Reading is to the mind what physical exercise is to the human body. It continuously expands our horizons, enhances our critical thinking, and inspires our souls to reach greatness. When you open a book, you explore new ideas and travel through unique worlds and times without moving an inch from your comfortable seat.",
            "Believe you can and you are already halfway there. Confidence, combined with passion and unyielding enthusiasm, is the ultimate driver of human achievements. No matter how many challenges you face on your journey, maintaining a positive mindset and a strong voice will always guide you directly to victory."
        ],
        "mic_idle": "🎙️ Click to activate live voice connection", "mic_active": "🟢 System is connected and analyzing your voice...",
        "status_idle": "Aser is waiting for you to start reading continuously...", "status_normal": "Excellent reading with a clear and stable tone", "status_high": "Amazing performance! Full of enthusiasm and high energy",
        "indicator_title": "📊 Real-time Voice Engagement Indicator", "status_title": "Assistant Status"
    }
}

t = translations[st.session_state.lang]

# --- 3. تصميم الـ CSS الكرتوني العصري (Neo-Brutalist) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFDF0 !important; }}
    .main-title {{ color: #000000; font-family: 'Segoe UI', sans-serif; text-align: center; font-weight: 900; font-size: 34px; margin-top: 5px; }}
    .subtitle {{ color: #333333; text-align: center; font-family: 'Segoe UI', sans-serif; font-size: 15px; margin-bottom: 20px; font-weight: 500; }}
    
    /* حقول الإدخال والقوائم الكرتونية حادة الحواف */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox, .stTextArea {{ 
        border: 3px solid #000000 !important; border-radius: 12px !important;
        box-shadow: 4px 4px 0px #000000 !important; background-color: #FFFFFF !important;
    }}
    div[data-testid="stMarkdownContainer"] {{ text-align: {t['align']}; }}
    
    /* حجم خط نصوص القراءة المطور لـ 18px */
    textarea {{ font-size: 18px !important; font-family: 'Segoe UI', sans-serif !important; line-height: 1.6 !important; color: #000000 !important; }}
    
    .stAlert {{ border: 3px solid #000000 !important; border-radius: 16px !important; box-shadow: 5px 5px 0px #000000 !important; background-color: #FFFAF0 !important; }}
    
    /* تصميم خاص مخصص لإبراز حواف البانر المرفوع من كانفا */
    .canva-banner {{
        border: 3px solid #000000;
        border-radius: 16px;
        box-shadow: 6px 6px 0px #000000;
        margin-bottom: 25px;
        overflow: hidden;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. إدراج تصميم كانفا في أعلى الصفحة ---
# يبحث الكود عن الصورة المرفوعة؛ إذا وجدها يعرضها بستايل كرتوني محاط بإطار أسود، وإذا لم يجدها يعرض العنوان النصي العادي.
if os.path.exists("header.png"):
    st.markdown('<div class="canva-banner">', unsafe_allow_html=True)
    st.image("header.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(f"<div class='main-title'>{t['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{t['subtitle']}</div>", unsafe_allow_html=True)

# --- 5. إعداد الـ API ---
API_KEY = "AIzaSyAOBg67pMTj2gYrc7PCs2MmRzQGhfedGmI"
@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=API_KEY) if (API_KEY and "ضـع" not in API_KEY) else None
client = get_ai_client()

if "ai_reply" not in st.session_state: st.session_state.ai_reply = t["ai_default"]
if "last_text" not in st.session_state: st.session_state.last_text = ""

# --- 6. كود الـ HTML والمؤشر الصوتي التفاعلي اللحظي ---
html_code = """
<div id="box" style="background:#FFFFFF; border: 3px solid #000000; border-radius: 16px; padding: 25px; box-shadow: 6px 6px 0px #000000; font-family:'Segoe UI', sans-serif; margin-bottom: 10px;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <div id="emoji" style="font-size: 55px; background: #FFFDF0; border: 3px solid #000000; padding: 10px 20px; border-radius: 50%; box-shadow: 3px 3px 0px #000000;">😴</div>
        <div id="stBlock">
            <div id="lblTitle" style="color:#555555; font-size:13px; font-weight:700; text-transform: uppercase;"></div>
            <div id="lblStatus" style="color:#000000; font-size:16px; font-weight:900; margin-top:3px;"></div>
        </div>
    </div>
    <div style="margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 800; color: #000000; margin-bottom: 8px;">
            <span id="lblInd"></span> <span id="txtPerc" style="background:#FFDE4D; border:2px solid #000000; padding:2px 8px; border-radius:6px;">0%</span>
        </div>
        <div style="background:#FFFFFF; border:3px solid #000000; border-radius: 9999px; height: 18px; overflow: hidden; padding:2px;">
            <div id="bar" style="background:#10B981; border-radius:9999px; height: 100%; width: 0%; transition: width 0.2s ease;"></div>
        </div>
    </div>
    <div style="text-align:center;">
        <button id="btn" style="background:#2563EB; color:#FFFFFF; border: 3px solid #000000; padding: 15px 40px; border-radius: 12px; font-size: 16px; font-weight: 900; width: 100%; max-width: 400px; cursor: pointer; box-shadow: 4px 4px 0px #000000; transition: transform 0.1s;"></button>
    </div>
</div>
<script>
const cfg = { dir: "D_V", align: "A_V", title: "T_V", idle: "I_V", norm: "N_V", high: "H_V", ind: "IND_V", act: "ACT_V", bIdle: "B_I_V" };
document.getElementById('box').style.direction = cfg.dir;
document.getElementById('stBlock').style.textAlign = cfg.align;
document.getElementById('lblTitle').innerText = cfg.title;
document.getElementById('lblStatus').innerText = cfg.idle;
document.getElementById('lblInd').innerText = cfg.ind;
document.getElementById('btn').innerText = cfg.bIdle;

const btn = document.getElementById('btn'); const emoji = document.getElementById('emoji');
const lblStatus = document.getElementById('lblStatus'); const bar = document.getElementById('bar'); const txtPerc = document.getElementById('txtPerc');
let isList = false; let stable = "sleep"; let timer = null;

btn.onmousedown = function() { btn.style.transform = "translate(2px, 2px)"; btn.style.boxShadow = "2px 2px 0px #000000"; }
btn.onmouseup = function() { btn.style.transform = "none"; btn.style.boxShadow = "4px 4px 0px #000000"; }

btn.onclick = async function() {
    if (isList) return;
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation:true, noiseSuppression:true, autoGainControl:true }, video:false });
        isList = true; btn.innerText = cfg.act; btn.style.backgroundColor = "#E11D48";
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const ans = ctx.createAnalyser(); ctx.createMediaStreamSource(stream).connect(ans);
        const node = ctx.createScriptProcessor(2048, 1, 1); ans.connect(node); node.connect(ctx.destination);
        ans.smoothingTimeConstant = 0.8; ans.fftSize = 256;
        node.onaudioprocess = function() {
            let arr = new Uint8Array(ans.frequencyBinCount); ans.getByteFrequencyData(arr);
            let v = 0; for(let i=0; i<arr.length; i++) { v += arr[i]; }
            let avg = v / arr.length; if (avg < 5) avg = 0;
            let pct = Math.min(Math.round((avg / 45) * 100), 100);
            bar.style.width = pct + "%"; txtPerc.innerText = pct + "%";
            let tState = pct >= 70 ? "high" : (pct >= 20 ? "normal" : "sleep");
            if (tState !== stable) {
                if (!timer) {
                    timer = setTimeout(() => {
                        stable = tState;
                        if (stable === "high") { emoji.innerText = "🤩"; lblStatus.innerText = cfg.high; }
                        else if (stable === "normal") { emoji.innerText = "😊"; lblStatus.innerText = cfg.norm; }
                        else { emoji.innerText = "🥱"; lblStatus.innerText = cfg.idle; }
                        timer = null;
                    }, 350);
                }
            } else {
                if(timer) { clearTimeout(timer); timer = null; }
                bar.style.backgroundColor = stable === "high" ? "#10B981" : (stable === "normal" ? "#3B82F6" : "#94A3B8");
            }
        }
    } catch(e) { alert("Microphone error"); }
};
</script>
"""

configured_html = html_code\
    .replace("D_V", t["direction"]).replace("A_V", t["align"])\
    .replace("T_V", t["status_title"]).replace("I_V", t["status_idle"])\
    .replace("N_V", t["status_normal"]).replace("H_V", t["status_high"])\
    .replace("IND_V", t["indicator_title"]).replace("B_I_V", t["mic_idle"]).replace("ACT_V", t["mic_active"])

components.html(configured_html, height=260)
st.write("")

# --- 7. حقل المدخلات ونصوص المعلم ---
st.markdown(f"<p style='font-weight: 800; color: #000000; font-size: 15px; margin-bottom: 5px;'>{t['input_label']}</p>", unsafe_allow_html=True)

selected_passage = st.selectbox(label="Passage Selector", options=t["passages"], label_visibility="collapsed")
default_text_val = "" if selected_passage == t["custom_text"] else selected_passage

teacher_text = st.text_area(label="Text Area", placeholder=t["placeholder"], value=default_text_val, height=180, label_visibility="collapsed")

if teacher_text and teacher_text != st.session_state.last_text:
    st.session_state.last_text = teacher_text
    if client:
        try:
            prompt = f"أنت طالب ذكي ومشجع اسمه آسر. رد باختصار شديد جداً (سطر واحد) وبأسلوب تعليمي لطيف ومشجع بنفس لغة النص التالية: {teacher_text}."
            if st.session_state.lang == "English":
                prompt = f"You are a smart and encouraging student named Aser. Reply very briefly (one short line) in English to this sentence: {teacher_text}."
            st.session_state.ai_reply = client.models.generate_content(model="gemini-1.5-flash", contents=prompt).text
        except:
            st.session_state.ai_reply = t["ai_default"]

st.markdown(f"<p style='font-weight: 800; color: #000000; font-size: 15px; margin-bottom: 5px;'>{t['ai_label']}</p>", unsafe_allow_html=True)
st.info(st.session_state.ai_reply)
