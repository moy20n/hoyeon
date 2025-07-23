streamlit run <(cat <<'EOF'
import streamlit as st
from datetime import date
import os
import json
import hashlib

# ─── 비밀번호 해시 함수 ─────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ─── 사용자 로그인 / 등록 ─────────────────────
if "username" not in st.session_state or "password" not in st.session_state:
    with st.form("login_form"):
        st.write("## 📖 일기장에 오신 걸 환영합니다!")
        name_input = st.text_input("당신의 이름을 입력해주세요:")
        password_input = st.text_input("비밀번호를 입력해주세요:", type="password")
        submitted = st.form_submit_button("입력 완료")
        if submitted:
            if name_input.strip() and password_input.strip():
                st.session_state.username = name_input.strip()
                st.session_state.password = password_input.strip()
                st.session_state.user_hash = (
                    f"{st.session_state.username}_{hash_password(st.session_state.password)}"
                )
            else:
                st.warning("이름과 비밀번호를 모두 입력해주세요.")

if "username" not in st.session_state or "password" not in st.session_state:
    st.stop()

USER_FOLDER = os.path.join("diary_data", st.session_state.user_hash)
os.makedirs(USER_FOLDER, exist_ok=True)

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

def get_diary_path(date_str: str) -> str:
    return os.path.join(USER_FOLDER, f"{date_str}.json")

def save_diary(date_str: str, text: str, emotion_code: str, weather_code: str):
    entry = {"text": text, "emotion": emotion_code, "weather": weather_code}
    with open(get_diary_path(date_str), "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)

def load_diary(date_str: str):
    path = get_diary_path(date_str)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def search_diaries(keyword: str):
    results = []
    for filename in os.listdir(USER_FOLDER):
        if filename.endswith(".json"):
            with open(os.path.join(USER_FOLDER, filename), "r", encoding="utf-8") as f:
                entry = json.load(f)
                if keyword in entry["text"]:
                    results.append((filename.replace(".json", ""), entry))
    return results

menu = st.sidebar.selectbox(
    "메뉴 선택",
    ["✍️ 일기 쓰기", "🔍 일기 검색", "📅 지난 일기 보기"]
)

if menu == "✍️ 일기 쓰기":
    st.header("✍️ 오늘의 일기 쓰기")
    selected_date = st.date_input("날짜 선택", date.today())
    date_str = selected_date.isoformat()
    emotion_category = st.selectbox("감정 카테고리를 선택하세요", list(EMOTION_CATEGORIES.keys()))
    emotion_options = EMOTION_CATEGORIES[emotion_category]
    emotion_label = st.selectbox("세부 감정을 선택하세요", list(emotion_options.keys()))
    emotion_code = emotion_options[emotion_label]
    weather_label = st.selectbox("오늘의 날씨는?", list(WEATHERS.keys()))
    weather_code = WEATHERS[weather_label]
    text = st.text_area("일기 내용 입력", height=300)
    if st.button("💾 저장하기"):
        save_diary(date_str, text, emotion_code, weather_code)
        st.success("✅ 일기가 저장되었습니다.")

elif menu == "📅 지난 일기 보기":
    st.header("📅 저장된 일기 보기")
    diary_files = sorted(os.listdir(USER_FOLDER))
    diary_dates = [f.replace(".json", "") for f in diary_files]
    if diary_dates:
        selected_date = st.selectbox("날짜 선택", diary_dates)
        entry = load_diary(selected_date)
        if entry:
            st.markdown(f"### 📅 {selected_date}")
            st.markdown(f"**감정:** {entry['emotion']} | **날씨:** {entry['weather']}")
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
                st.markdown(f"### 📅 {date_str} | 감정: {entry['emotion']} | 날씨: {entry['weather']}")
                st.markdown(entry["text"])
                st.markdown("---")
        else:
            st.warning("🔍 검색 결과가 없습니다.")
EOF
)
