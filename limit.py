import streamlit as st
import pandas as pd

# -------------------------------
# 전체 118개 주기율표 데이터 로딩
# -------------------------------
df = pd.read_csv("https://raw.githubusercontent.com/BowenFu/data/master/periodic_table_extended.csv")

# 그룹 단순화: 금속 / 비금속 / 중금속
metal_types = ["Alkali Metal", "Alkaline Earth Metal", "Transition Metal", "Post-Transition Metal", "Lanthanide", "Actinide"]
non_metal_types = ["Nonmetal", "Noble Gas", "Halogen"]

simplified_types = []
for t in df['Type']:
    if t in metal_types:
        simplified_types.append("금속")
    elif t in non_metal_types:
        simplified_types.append("비금속")
    else:
        simplified_types.append("중금속")

df['type'] = simplified_types

# 색상 매핑
color_map = {
    "금속": "#FFD700",
    "비금속": "#87CEFA",
    "중금속": "#D3D3D3"
}
df['color'] = df['type'].map(color_map)

# 박스형 UI 출력
st.set_page_config(page_title="ChemPlay - 주기율표 박스형", layout="wide")
st.title("🧪 ChemPlay: 전체 주기율표 (박스형)")

# 각 원소 위치 좌표 계산
df['x'] = df['Group'] - 1
max_period = df['Period'].max()
df['y'] = df['Period'].apply(lambda p: max_period - p)  # 화면 위에서 아래로 정렬

# 주기(행) 기준으로 출력
y_levels = sorted(df['y'].unique())
for y in y_levels:
    row = df[df['y'] == y].sort_values("x")
    cols = st.columns(18)
    for _, el in row.iterrows():
        with cols[int(el['x'])]:
            if st.button(f"{el['symbol']}", key=f"btn_{el['atomic number']}"):
                st.session_state["selected_element"] = el.to_dict()
            st.markdown(f"""
                <div style='text-align:center; background-color:{el['color']}; padding:8px; border-radius:8px;'>
                    <strong>{el['symbol']}</strong><br>
                    <small>{int(el['atomic number'])}</small>
                </div>
            """, unsafe_allow_html=True)

# 클릭한 원소 정보 출력
if "selected_element" in st.session_state:
    el = st.session_state["selected_element"]
    st.markdown("""
    ---
    ### 🔍 선택한 원소 정보
    """)
    st.write({
        "기호": el["symbol"],
        "이름": el["name"],
        "원자번호": int(el["atomic number"]),
        "족": int(el["Group"]),
        "주기": int(el["Period"]),
        "종류": el["type"]
    })
