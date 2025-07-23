import streamlit as st
from datetime import date
import os
import json
import hashlib

# --- 1. 상태 분기 세팅 ---
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- 2. 로그아웃 함수 (rerun 없이 상태만 변경) ---
def logout():
    for k in ["username", "password", "user_hash", "temp_user_hash"]:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state.page = "logout"

# --- 3. 사이드바에서 즉시 로그아웃 반영 ---
with st.sidebar:
    st.markdown("---")
    if st.button("로그아웃"):
        logout()

# --- 4. 로그아웃 안내 페이지 (항상 최상단 분기!) ---
if st.session_state.page == "logout":
    st.success("로그아웃 되었습니다.")
    if st.button("로그인 화면으로 돌아가기"):
        st.session_state.page = "login"
    st.stop()
