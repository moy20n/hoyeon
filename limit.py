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

# --- 3. 로그아웃 함수 ---
def logout():
    for k in ["username", "password", "user_hash", "temp_user_hash"]:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state.page = "logout"

# --- 4. 비밀번호 해시 함수 ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- 5. 로그인/회원가입 화면 ---
if (
    "username" not in st.session_state
    or "password" not in st.session_state
    or "user_hash" not in st.session_state
    or st.session_state.page == "login"
):
    if "temp_user_hash" not in st.session_state:
        st.session_state.temp_user_hash = ""
    if "pw_fail_count" not in st.session_state:
        st.session_state.pw_fail_count = 0

    # 파랑 안내 영역
    st.markdown("""
    <div style='
        background: linear-gradient(120deg, #b3d8ff 0%, #84a9ff 100%);
        border-radius: 18px;
        padding: 1.3rem 1rem 1.1rem 1rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 24px #1976d230;
        text-align: center;
    '>
        <span style='font-size:2.1rem; margin-bottom:0.4rem;'>🌊💙📝</span>
        <div style='font-size: 1.09rem; color:#114485; margin-top:0.4rem;'>
            <b>기분과 하루를 파란 하늘처럼 기록해 보세요!</b>
        </div>
        <div style='font-size: 1.2em; margin-top:0.2em;'>오늘도 좋은 하루 보내세요! 🫧</div>
    </div>
    """, unsafe_allow_html=True)

    st.title("☁𝓓𝓲𝓪𝓻𝔂☁")

    with st.form("login_form"):
        name_input = st.text_input("당신의 이름을 입력해주세요:")
        password_input = st.text_input("비밀번호를 입력해주세요:", type="password")
        submitted = st.form_submit_button("입력 완료")

        if name_input.strip() and password_input.strip():
            user_hash = f"{name_input.strip()}_{hash_password(password_input.strip())}"
            st.session_state.temp_user_hash = user_hash
        else:
            user_hash = ""
            st.session_state.temp_user_hash = ""

        if submitted:
            if name_input.strip() and password_input.strip():
                user_dir = os.path.join("diary_data", f"{name_input.strip()}_{hash_password(password_input.strip())}")
                # 기존 유저: 비밀번호 체크
                if os.path.exists(user_dir):
                    expected_hash = f"{name_input.strip()}_{hash_password(password_input.strip())}"
                    if expected_hash == st.session_state.temp_user_hash:
                        st.session_state.username = name_input.strip()
                        st.session_state.password = password_input.strip()
                        st.session_state.user_hash = expected_hash
                        st.session_state.page = "main"
                        st.session_state.pw_fail_count = 0
                    else:
                        st.session_state.pw_fail_count += 1
                        st.warning("비밀번호가 틀렸습니다.")
                else:
                    # 신규 회원가입: 바로 진입
                    st.session_state.username = name_input.strip()
                    st.session_state.password = password_input.strip()
                    st.session_state.user_hash = f"{name_input.strip()}_{hash_password(password_input.strip())}"
                    st.session_state.page = "main"
                    st.session_state.pw_fail_count = 0
            else:
                st.warning("이름과 비밀번호를 모두 입력해주세요.")
    st.stop()

# --- 6. 일기장 본 기능 (로그인 성공 후에만!) ---
if (
    "username" in st.session_state
    and "password" in st.session_state
    and "user_hash" in st.session_state
    and st.session_state.page == "main"
):
    USER_FOLDER = os.path.join("diary_data", st.session_state.user_hash)
    os.makedirs(USER_FOLDER, exist_ok=True)

    with st.sidebar:
        st.markdown("---")
        if st.button("로그아웃"):
            logout()

    st.title("☁𝓓𝓲𝓪𝓻𝔂☁")

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

    EMOJI_EMOTION = {
        "happy": "😊",
        "loving": "😍",
        "excited": "🤩",
        "calm": "😌",
        "sad": "😢",
        "angry": "😡",
        "crying": "😭",
        "frustrated": "😖",
        "worried": "😟",
        "anxious": "😨",
        "neutral": "😐",
        "thoughtful": "🤔",
        "speechless": "😶",
        "tired": "😴",
        "exhausted": "😫"
    }

    EMOJI_WEATHER = {
        "sunny": "☀️",
        "cloudy": "⛅",
        "rainy": "🌧️",
        "snowy": "🌨️",
        "foggy": "🌫️",
        "stormy": "🌩️"
    }

    def get_diary_path(date_str):
        return os.path.join(USER_FOLDER, f"{date_str}.json")

    def save_diary(date_str, text, emotion_code, weather_code, song_artist, song_title):
        entry = {
            "text": text,
            "emotion": emotion_code,
            "weather": weather_code,
            "song_artist": song_artist,
            "song_title": song_title
        }
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
                    if keyword in entry.get("text", ""):
                        results.append((filename.replace(".json", ""), entry))
        return results

    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["✍️ 일기 쓰기", "🔍 일기 검색", "📅 지난 일기 보기", "🎵 추천곡 리스트"]
    )

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
            default_text = existing_entry.get("text", "")
            default_song_artist = existing_entry.get("song_artist", "")
            default_song_title = existing_entry.get("song_title", "")
        else:
            default_emotion_category = list(EMOTION_CATEGORIES.keys())[0]
            default_emotion_label = list(EMOTION_CATEGORIES[default_emotion_category].keys())[0]
            default_weather_label = list(WEATHERS.keys())[0]
            default_text = ""
            default_song_artist = ""
            default_song_title = ""

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

        st.markdown("#### 오늘의 추천곡")
        song_artist = st.text_input("가수 이름", value=default_song_artist)
        song_title = st.text_input("곡 제목", value=default_song_title)

        if st.button("💾 저장하기"):
            save_diary(date_str, text, emotion_code, weather_code, song_artist, song_title)
            st.success("일기가 저장되었습니다.")

        if existing_entry:
            st.info("이 날짜의 일기가 이미 저장되어 있습니다. 내용을 수정하면 덮어씌워집니다.")

    elif menu == "📅 지난 일기 보기":
        st.header("저장된 일기 보기")

        diary_files = sorted(os.listdir(USER_FOLDER))
        diary_dates = [f.replace(".json", "") for f in diary_files]

        if diary_dates:
            selected_date = st.date_input(
                "날짜 선택",
                value=date.fromisoformat(diary_dates[-1]),  # 최근 저장된 날짜로 기본값
                min_value=date.fromisoformat(min(diary_dates)),
                max_value=date.fromisoformat(max(diary_dates))
            )
            date_str = selected_date.isoformat()
            if date_str in diary_dates:
                entry = load_diary(date_str)
                if entry:
                    emotion_icon = EMOJI_EMOTION.get(entry['emotion'], "")
                    weather_icon = EMOJI_WEATHER.get(entry['weather'], "")
                    st.markdown(f"### {date_str}  {weather_icon} {emotion_icon}")
                    st.text_area("내용", entry["text"], height=300, disabled=True)
                    if entry.get("song_artist") or entry.get("song_title"):
                        st.markdown(
                            f"#### 🎵 오늘의 추천곡\n- 가수: {entry.get('song_artist','')}\n- 제목: {entry.get('song_title','')}"
                        )
            else:
                st.info("이 날짜에는 저장된 일기가 없습니다.")
        else:
            st.info("아직 저장된 일기가 없습니다.")

    elif menu == "🔍 일기 검색":
        st.header("🔍 키워드로 일기 검색")
        keyword = st.text_input("검색할 키워드 입력")

        if st.button("검색"):
            results = search_diaries(keyword)
            if results:
                for date_str, entry in results:
                    emotion_icon = EMOJI_EMOTION.get(entry['emotion'], "")
                    weather_icon = EMOJI_WEATHER.get(entry['weather'], "")
                    st.markdown(f"### 📅 {date_str} | 감정: {emotion_icon} | 날씨: {weather_icon}")
                    st.markdown(entry["text"])
                    if entry.get("song_artist") or entry.get("song_title"):
                        st.markdown(
                            f"🎵 <b>{entry.get('song_artist','')}</b> - {entry.get('song_title','')}",
                            unsafe_allow_html=True
                        )
                    st.markdown("---")
            else:
                st.warning("검색 결과가 없습니다.")

    elif menu == "🎵 추천곡 리스트":
        st.header("🎵 추천곡 리스트 (날짜별 정리)")
        diary_files = sorted(os.listdir(USER_FOLDER))
        diary_dates = [f.replace(".json", "") for f in diary_files]

        found = False
        for date_str in diary_dates:
            entry = load_diary(date_str)
            if entry and (entry.get("song_artist") or entry.get("song_title")):
                found = True
                st.markdown(f"**{date_str}**<br>가수: <b>{entry.get('song_artist','')}</b> | 곡명: <b>{entry.get('song_title','')}</b>", unsafe_allow_html=True)
        if not found:
            st.info("아직 등록된 추천곡이 없습니다.")
