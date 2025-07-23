import streamlit as st
import pandas as pd

# -------------------------------
# 전체 주기율표 데이터 정의 (대표적인 118개 원소 좌표화용 위치 포함)
# -------------------------------
data = [
    ("H", 1, 1, 1), ("He", 2, 18, 1),
    ("Li", 3, 1, 2), ("Be", 4, 2, 2), ("B", 5, 13, 2), ("C", 6, 14, 2), ("N", 7, 15, 2), ("O", 8, 16, 2), ("F", 9, 17, 2), ("Ne", 10, 18, 2),
    ("Na", 11, 1, 3), ("Mg", 12, 2, 3), ("Al", 13, 13, 3), ("Si", 14, 14, 3), ("P", 15, 15, 3), ("S", 16, 16, 3), ("Cl", 17, 17, 3), ("Ar", 18, 18, 3),
    ("K", 19, 1, 4), ("Ca", 20, 2, 4), ("Sc", 21, 3, 4), ("Ti", 22, 4, 4), ("V", 23, 5, 4), ("Cr", 24, 6, 4), ("Mn", 25, 7, 4),
    ("Fe", 26, 8, 4), ("Co", 27, 9, 4), ("Ni", 28, 10, 4), ("Cu", 29, 11, 4), ("Zn", 30, 12, 4),
    ("Ga", 31, 13, 4), ("Ge", 32, 14, 4), ("As", 33, 15, 4), ("Se", 34, 16, 4), ("Br", 35, 17, 4), ("Kr", 36, 18, 4),
    ("Rb", 37, 1, 5), ("Sr", 38, 2, 5), ("Y", 39, 3, 5), ("Zr", 40, 4, 5), ("Nb", 41, 5, 5), ("Mo", 42, 6, 5), ("Tc", 43, 7, 5),
    ("Ru", 44, 8, 5), ("Rh", 45, 9, 5), ("Pd", 46, 10, 5), ("Ag", 47, 11, 5), ("Cd", 48, 12, 5),
    ("In", 49, 13, 5), ("Sn", 50, 14, 5), ("Sb", 51, 15, 5), ("Te", 52, 16, 5), ("I", 53, 17, 5), ("Xe", 54, 18, 5),
    ("Cs", 55, 1, 6), ("Ba", 56, 2, 6), ("La", 57, 3, 9), ("Hf", 72, 4, 6), ("Ta", 73, 5, 6), ("W", 74, 6, 6), ("Re", 75, 7, 6),
    ("Os", 76, 8, 6), ("Ir", 77, 9, 6), ("Pt", 78, 10, 6), ("Au", 79, 11, 6), ("Hg", 80, 12, 6),
    ("Tl", 81, 13, 6), ("Pb", 82, 14, 6), ("Bi", 83, 15, 6), ("Po", 84, 16, 6), ("At", 85, 17, 6), ("Rn", 86, 18, 6),
    ("Fr", 87, 1, 7), ("Ra", 88, 2, 7), ("Ac", 89, 3, 10), ("Rf", 104, 4, 7), ("Db", 105, 5, 7), ("Sg", 106, 6, 7), ("Bh", 107, 7, 7),
    ("Hs", 108, 8, 7), ("Mt", 109, 9, 7), ("Ds", 110, 10, 7), ("Rg", 111, 11, 7), ("Cn", 112, 12, 7),
    ("Nh", 113, 13, 7), ("Fl", 114, 14, 7), ("Mc", 115, 15, 7), ("Lv", 116, 16, 7), ("Ts", 117, 17, 7), ("Og", 118, 18, 7),
    # 란탄족
    ("Ce", 58, 4, 9), ("Pr", 59, 5, 9), ("Nd", 60, 6, 9), ("Pm", 61, 7, 9), ("Sm", 62, 8, 9), ("Eu", 63, 9, 9),
    ("Gd", 64, 10, 9), ("Tb", 65, 11, 9), ("Dy", 66, 12, 9), ("Ho", 67, 13, 9), ("Er", 68, 14, 9), ("Tm", 69, 15, 9), ("Yb", 70, 16, 9), ("Lu", 71, 17, 9),
    # 악티늄족
    ("Th", 90, 4, 10), ("Pa", 91, 5, 10), ("U", 92, 6, 10), ("Np", 93, 7, 10), ("Pu", 94, 8, 10), ("Am", 95, 9, 10),
    ("Cm", 96, 10, 10), ("Bk", 97, 11, 10), ("Cf", 98, 12, 10), ("Es", 99, 13, 10), ("Fm", 100, 14, 10), ("Md", 101, 15, 10), ("No", 102, 16, 10), ("Lr", 103, 17, 10)
]

columns = ["symbol", "atomic number", "Group", "Period"]
df = pd.DataFrame(data, columns=columns)

# 좌표 및 색상 지정
df["x"] = df["Group"] - 1
max_period = df["Period"].max()
df["y"] = df["Period"] - 1

# 색상 매핑 예시
metals = ["Li", "Be", "Na", "Mg", "Al", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "Cs", "Ba", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Fr", "Ra", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn"]
nonmetals = ["H", "C", "N", "O", "F", "P", "S", "Cl", "Se", "Br", "I", "At", "Ts"]
noblegases = ["He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"]

def assign_color(symbol):
    if symbol in metals:
        return "#FFD700"  # 금속 - 금색
    elif symbol in nonmetals:
        return "#90EE90"  # 비금속 - 연두색
    elif symbol in noblegases:
        return "#87CEFA"  # 비활성기체 - 하늘색
    else:
        return "#D3D3D3"  # 기타 - 회색

df["color"] = df["symbol"].apply(assign_color)

# Streamlit 페이지 설정
st.set_page_config(page_title="ChemPlay - 주기율표 배치", layout="wide")
st.title("🧪 ChemPlay: 전체 주기율표 배치")

# 범례 출력
with st.expander("🧾 색상 범례 보기"):
    st.markdown("""
    <div style='display:flex; gap:1rem;'>
        <div style='background-color:#FFD700; padding:5px 10px; border-radius:5px;'>금속</div>
        <div style='background-color:#90EE90; padding:5px 10px; border-radius:5px;'>비금속</div>
        <div style='background-color:#87CEFA; padding:5px 10px; border-radius:5px;'>비활성기체</div>
        <div style='background-color:#D3D3D3; padding:5px 10px; border-radius:5px;'>기타</div>
    </div>
    """, unsafe_allow_html=True)

# UI 출력
y_levels = sorted(df["y"].unique())
for y in y_levels:
    row = df[df["y"] == y].sort_values("x")
    cols = st.columns(18)
    for _, el in row.iterrows():
        with cols[int(el["x"])]:
            st.markdown(f"""
                <div style='background-color:{el['color']}; padding:8px; border-radius:6px; text-align:center;'>
                    <button style='all:unset; cursor:pointer; width:100%; font-weight:bold; color:black;' onclick="window.location.href='#{el['symbol']}'">
                        {el['symbol']}
                    </button>
                </div>
                """, unsafe_allow_html=True)
            if st.button("", key=f"btn_{el['atomic number']}"):
                st.session_state["selected_element"] = el.to_dict()
            st.markdown(f"""
                <style>
                div[data-testid="element-container"] > div:has(button[data-testid="baseButton-module"])[data-testid="stButton"] {{
                    background-color: {el['color']} !important;
                    border-radius: 6px;
                    padding: 10px;
                    text-align: center;
                    color: black;
                    font-weight: bold;
                }}
                </style>
            """, unsafe_allow_html=True)

# 클릭한 원소 정보
if "selected_element" in st.session_state:
    el = st.session_state["selected_element"]
    st.markdown(f"""
    <div style='position:fixed; top:20%; left:50%; transform:translateX(-50%); background:#fff; padding:20px; border:2px solid #ccc; border-radius:10px; z-index:1000; box-shadow:0 0 20px rgba(0,0,0,0.3); width:300px;'>
        <h4 style='text-align:center;'>🔍 선택한 원소 정보</h4>
        <ul style='list-style:none; padding:0; font-size:16px;'>
            <li><strong>기호:</strong> {el['symbol']}</li>
            <li><strong>원자번호:</strong> {el['atomic number']}</li>
            <li><strong>족:</strong> {el['Group']}</li>
            <li><strong>주기:</strong> {el['Period']}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    el = st.session_state["selected_element"]
    st.markdown(f"""
    ---
    ### 🔍 선택한 원소 정보
    - 기호: {el['symbol']}
    - 원자번호: {el['atomic number']}
    - 족: {el['Group']}
    - 주기: {el['Period']}
    """)
