import streamlit as st
from datetime import date
import os
import json

# 저장 폴더
DIARY_FOLDER = "diary_data"
os.makedirs(DIARY_FOLDER, exist_ok=True)

# 감정 이모지
EMOTIONS = {
    "😊 행복": "happy",
    "😢 슬픔": "sad",
    "😡 화남": "angry",
    "😨 불안": "anxious",
    "😐 무덤덤": "neutral"
}

# 날씨 이모지
WEATHERS = {
    "☀️ 맑음": "sunny",
    "⛅ 구름": "cloudy",
    "🌧️ 비": "rainy",
    "🌨️ 눈": "snowy",
    "🌫️ 안개": "foggy",
    "🌩️ 천둥번개": "stormy"
}

# 파일 경로
def get_diary_path(date_str):
    return os.path.join(DIARY_FOLDER, f"{date_str}.json")

# 저장
def save_diary(date_str, text, emotion, weather):
    entry = {"text": text, "emotion": emotion, "weather": weather}
    with open(get_diary_path(date_str), "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False)

# 불러오기
def load_diary(date_str):
    path = get_diary_path(date_str)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# 검색
def search_diaries(keyword):
    results = []
    for filename in os.listdir(DIARY_FOLDER):
        if filename.endswith(".json"):
            with open(os.path.join(DIARY_FOLDER, filename), "r", encoding="utf-8") as f:
                entry = json.load(f)
                if keyword in entry["text"]:
                    results.append((filename.replace(".json", ""), entry))
    return results


# ──────────────────────────────────────────────────────────────
st.title("📔 나만의 감정 일기장")

menu = st.sidebar.selectbox("메뉴 선택", ["✍️ 일기 쓰기", "🔍 일기 검색", "📅 지난 일기 보기"])

# ──────────────────────── 일기 쓰기
if menu == "✍️ 일기 쓰기":
    st.header("오늘의 일기 쓰기")
    selected_date = st.date_input("날짜 선택", date.today())
    date_str = selected_date.isoformat()

    emotion = st.selectbox("오늘의 감정은?", list(EMOTIONS.keys()))
    weather = st.selectbox("오늘의 날씨는?", list(WEATHERS.keys()))
    text = st.text_area("일기 내용 입력", height=300)

    if st.button("💾 저장하기"):
        save_diary(date_str, text, EMOTIONS[emotion], WEATHERS[weather])
        st.success("일기가 저장되었습니다.")

# ──────────────────────── 일기 보기
elif menu == "📅 지난 일기 보기":
    st.header("저장된 일기 보기")
    diary_files = sorted(os.listdir(DIARY_FOLDER))
    diary_dates = [f.replace(".json", "") for f in diary_files]
    
    if diary_dates:
        selected_date = st.selectbox("날짜 선택", diary_dates)
        entry = load_diary(selected_date)
        if entry:
            st.markdown(f"### 📅 {selected_date}")
            st.markdown(f"**감정:** {entry['emotion']}")
            st.markdown(f"**날씨:** {entry['weather']}")
            st.text_area("내용", entry["text"], height=300, disabled=True)
    else:
        st.info("아직 저장된 일기가 없습니다.")

# ──────────────────────── 검색
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
