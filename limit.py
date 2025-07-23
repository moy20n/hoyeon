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

    st.title("나만의 감정 일기장")

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
        "exhausted": "�
