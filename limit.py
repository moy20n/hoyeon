import streamlit as st
from datetime import date
import os
import json
import hashlib

# --- 1. 상태 분기 세팅 ---
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- 2. 로그아웃 안내 페이지 (항상 최상단 분기!) ---
if st.session_state.page == "logout":
    st.success("로그아웃 되었습니다. 🌊📝")
    if st.button("로그인 화면으로 돌아가기"):
        st.session_state.page = "login"
    st.stop()

# --- 3. 로그아웃 함수 (rerun/st.stop 없이 상태만 변경) ---
def logout():
    for k in ["username", "password", "user_hash", "temp_user_hash"]:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state.page = "logout"

# --- 4. 로그인/회원가입 화면 (파랑파랑 디자인!) ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_hint_path(user_hash):
    return os.path.join("diary_data", user_hash, ".hint")

def save_hint(user_hash, hint_text):
    path = get_hint_path(user_hash)
    if hint_text.strip():
        with open(path, "w", encoding="utf-8") as f:
            f.write(hint_text.strip())

def load_hint(user_hash):
    path = get_hint_path(user_hash)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

if (
    "username" not in st.session_state
    or "password" not in st.session_state
    or "user_hash" not in st.session_state
) or st.session_state.page == "login":
    if "temp_user_hash" not in st.session_state:
        st.session_state.temp_user_hash = ""

    # 🟦💙📝 파랑파랑하게 상단 꾸미기
    st.markdown("""
    <div style='
        background: linear-gradient(120deg, #b3d8ff 0%, #84a9ff 100%);
        border-radius: 20px;
        padding: 2.5rem 1.2rem 1.7rem 1.2rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 2px 24px #1976d230;
        text-align: center;
    '>
        <div style='font-size: 2.9rem; margin-bottom: 0.5rem;'>🌊 💙 📝</div>
        <div style='font-size: 2.1rem; font-weight: 900; color:#176be6; margin-bottom:0.5rem; letter-spacing:-1px'>
            파랑파랑 감정 일기장
        </div>
        <div style='font-size: 1.14rem; color:#1b3047; margin-bottom:0.4rem;'>
            오늘의 감정과 하루를<br>
            <span style='color:#2278fd; font-weight:600;'>파랗게</span> 기록해보세요!<br>
            <span style='font-size:1.4em;'>🖊️✨</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        name_input = st.text_input("당신의 이름을 입력해주세요:")
        password_input = st.text_input("비밀번호를 입력해주세요:", type="password")
        if name_input.strip() and password_input.strip():
            user_hash = f"{name_input.strip()}_{hash_password(password_input.strip())}"
            st.session_state.temp_user_hash = user_hash
        else:
            user_hash = ""
            st.session_state.temp_user_hash = ""
        hint = None
        if st.session_state.temp_user_hash:
            hint = load_hint(st.session_state.temp_user_hash)
        if hint:
            st.info(f"🔑 비밀번호 힌트: {hint}")
        submitted = st.form_submit_button("입력 완료")
        if submitted:
            if name_input.strip() and password_input.strip():
                st.session_state.username = name_input.strip()
                st.session_state.password = password_input.strip()
                st.session_state.user_hash = f"{name_input.strip()}_{hash_password(password_input.strip())}"
                st.session_state.page = "main"
            else:
                st.warning("이름과 비밀번호를 모두 입력해주세요.")
    if (
        st.session_state.temp_user_hash
        and not os.path.exists(
            os.path.join("diary_data", st.session_state.temp_user_hash)
        )
    ):
        with st.form("hint_form"):
            hint_input = st.text_input("비밀번호 힌트(선택):")
            submitted_hint = st.form_submit_button("힌트 저장")
            if submitted_hint:
                os.makedirs(
                    os.path.join("diary_data", st.session_state.temp_user_hash),
                    exist_ok=True,
                )
                save_hint(st.session_state.temp_user_hash, hint_input)
                st.success("힌트가 저장되었습니다. 이제 이름/비밀번호를 다시 입력해 로그인하세요.")
    st.stop()

# --- 5. 일기장 본 기능 ---
USER_FOLDER = os.path.join("diary_data", st.session_state.user_hash)
os.makedirs(USER_FOLDER, exist_ok=True)

with st.sidebar:
    st.markdown("---")
    if st.button("로그아웃"):
        logout()

st.title(f"📔 {st.session_state.username}의 일기장 🔐")

EMOTION_CATEGORIES = {
    "긍정적인 감정": {
        "😊 행복": "happy",
        "😍 사랑스러움": "loving",
        "🤩 신남": "excited",
        "😌 평온함": "calm"
    },
    "부정적인 감정": {
        "😢 슬픔": "sad",
        "😡 화남": "angry",
        "😭 울고싶음": "crying",
        "😖 짜증남": "frustrated",
        "😟 걱정": "worried",
        "😨 불안": "anxious"
    },
    "중립/혼합 감정": {
        "😐 무덤덤": "neutral",
        "🤔 고민됨": "thoughtful",
        "😶 말문이 막힘": "speechless"
    },
    "신체 상태": {
        "😴 피곤함": "tired",
        "😫 지침": "exhausted"
    }
}

WEATHERS = {
    "☀️ 맑음": "sunny",
    "⛅ 구름": "cloudy",
    "🌧️ 비": "rainy",
    "🌨️ 눈": "snowy",
    "🌫️ 안개": "foggy",
    "🌩️ 천둥번개": "stormy"
}

def get_diary_path(date_str):
    return os.path.join(USER_FOLDER, f"{date_str}.json")

def save_diary(date_str, text, emotion_code, weather_code):
    entry = {"text": text, "emotion": emotion_code, "weather": weather_code}
    with open(get_diary_path(date_str), "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)

def load_diary(date_str):
    path = get_diary_path(date_str)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def search_diaries(keyword):
    results = []
    for filename in os.listdir(USER_FOLDER):
        if filename.endswith(".json"):
            with open(os.path.join(USER_FOLDER, filename), "r", encoding="utf-8") as f:
                entry = json.load(f)
                if keyword in entry["text"]:
                    results.append((filename.replace(".json", ""), entry))
    return results

menu = st.sidebar.selectbox("메뉴 선택", ["✍️ 일기 쓰기", "🔍 일기 검색", "📅 지난 일기 보기"])

if menu == "✍️ 일기 쓰기":
    st.header("오늘의 일기 쓰기")
    selected_date = st.date_input("날짜 선택", date.today())
    date_str = selected_date.isoformat()

    existing_entry = load_diary(date_str)
    if existing_entry:
        default_emotion_category = None
        default_emotion_label = None
        for category, emotions in EMOTION_CATEGORIES.items():
            for label, code in emotions.items():
                if code == existing_entry['emotion']:
                    default_emotion_category = category
                    default_emotion_label = label
                    break
            if default_emotion_category:
                break
        default_weather_label = None
        for label, code in WEATHERS.items():
            if code == existing_entry['weather']:
                default_weather_label = label
                break
        default_text = existing_entry["text"]
    else:
        default_emotion_category = list(EMOTION_CATEGORIES.keys())[0]
        default_emotion_label = list(EMOTION_CATEGORIES[default_emotion_category].keys())[0]
        default_weather_label = list(WEATHERS.keys())[0]
        default_text = ""

    emotion_category = st.selectbox(
        "감정 카테고리를 선택하세요",
        list(EMOTION_CATEGORIES.keys()),
        index=list(EMOTION_CATEGORIES.keys()).index(default_emotion_category) if default_emotion_category else 0
    )
    emotion_options = EMOTION_CATEGORIES[emotion_category]
    emotion_label = st.selectbox(
        "세부 감정을 선택하세요",
        list(emotion_options.keys()),
        index=list(emotion_options.keys()).index(default_emotion_label) if default_emotion_label and default_emotion_label in emotion_options else 0
    )
    emotion_code = emotion_options[emotion_label]

    weather_label = st.selectbox(
        "오늘의 날씨는?",
        list(WEATHERS.keys()),
        index=list(WEATHERS.keys()).index(default_weather_label) if default_weather_label else 0
    )
    weather_code = WEATHERS[weather_label]

    text = st.text_area("일기 내용 입력", value=default_text, height=300)

    if st.button("💾 저장하기"):
        save_diary(date_str, text, emotion_code, weather_code)
        st.success("일기가 저장되었습니다.")

    if existing_entry:
        st.info("이 날짜의 일기가 이미 저장되어 있습니다. 내용을 수정하면 덮어씌워집니다.")

elif menu == "📅 지난 일기 보기":
    st.header("저장된 일기 보기")
    diary_files = sorted(os.listdir(USER_FOLDER))
    diary_dates = [f.replace(".json", "") for f in diary_files]
    
    if diary_dates:
        selected_date = st.selectbox("날짜 선택", diary_dates)
        entry = load_diary(selected_date)
        if entry:
            st.markdown(f"### 📅 {selected_date}")
            st.markdown(f"**감정:** {entry['emotion']}  |  **날씨:** {entry['weather']}")
            st.text_area("내용", entry["text"], height=300, disabled=True)
    else:
        st.info("아직 저장된 일기가 없습니다.")

elif menu == "🔍 일기 검색":
    st.header("🔍 키워드로 일기 검색")
    keyword = st.text_input("검색할 키워드 입력")

    if st.button("검색"):
        results = search_diaries(keyword)
        if results:
            for date_str, entry in results:
                st.markdown(f"### 📅 {date_str} | 감정: {entry['emotion']} | 날씨: {entry['weather']}")
                st.markdown(entry["text"])
                st.markdown("---")
        else:
            st.warning("검색 결과가 없습니다.")
