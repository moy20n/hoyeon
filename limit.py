import streamlit as st
from datetime import date
import os
import json
import hashlib

# ───── 로그아웃 즉시 앱 완전 정지(에러 예방) ─────
if "logout" in st.session_state and st.session_state["logout"]:
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.stop()

# ───── 비밀번호 해시 함수 ─────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ───── 비밀번호 힌트 저장 및 로드 ─────
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

# ───── 완전 안전한 로그아웃 함수 ─────
def logout():
    st.session_state["logout"] = True
    st.experimental_rerun()

# ───── 사용자 인증 및 폴더 관리 ─────
if "username" not in st.session_state or "password" not in st.session_state or "user_hash" not in st.session_state:
    # 임시적으로 hint 확인용 user_hash 입력값 유지
    if "temp_user_hash" not in st.session_state:
        st.session_state.temp_user_hash = ""
    with st.form("login_form"):
        name_input = st.text_input("당신의 이름을 입력해주세요:")
        password_input = st.text_input("비밀번호를 입력해주세요:", type="password")
        # 이름, 비밀번호 입력 시 hash 생성
        if name_input.strip() and password_input.strip():
            user_hash = f"{name_input.strip()}_{hash_password(password_input.strip())}"
            st.session_state.temp_user_hash = user_hash
        else:
            user_hash = ""
            st.session_state.temp_user_hash = ""
        # 힌트 보여주기
        hint = None
        if st.session_state.temp_user_hash:
            hint = load_hint(st.session_state.temp_user_hash)
        if hint:
            st.info(f"비밀번호 힌트: {hint}")

        submitted = st.form_submit_button("입력 완료")
        if submitted:
            if name_input.strip() and password_input.strip():
                st.session_state.username = name_input.strip()
                st.session_state.password = password_input.strip()
                st.session_state.user_hash = f"{name_input.strip()}_{hash_password(password_input.strip())}"
            else:
                st.warning("이름과 비밀번호를 모두 입력해주세요.")

    # 회원가입(최초 등록) 모드일 때만 힌트 입력 받기
    if st.session_state.temp_user_hash and not os.path.exists(os.path.join("diary_data", st.session_state.temp_user_hash)):
        with st.form("hint_form"):
            hint_input = st.text_input("비밀번호 힌트(선택):")
            submitted_hint = st.form_submit_button("힌트 저장")
            if submitted_hint:
                os.makedirs(os.path.join("diary_data", st.session_state.temp_user_hash), exist_ok=True)
                save_hint(st.session_state.temp_user_hash, hint_input)
                st.success("힌트가 저장되었습니다. 이제 이름/비밀번호를 다시 입력해 로그인하세요.")

if "username" not in st.session_state or "password" not in st.session_state or "user_hash" not in st.session_state:
    st.stop()

USER_FOLDER = os.path.join("diary_data", st.session_state.user_hash)
os.makedirs(USER_FOLDER, exist_ok=True)

# ───── 로그아웃 버튼 ─────
with st.sidebar:
    st.markdown("---")
    if st.button("로그아웃"):
        logout()

st.title(f"📔 {st.session_state.username}의 일기장 🔐")

# ───── 감정/날씨 데이터 ─────
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
        "😐 무덤덤": "n
