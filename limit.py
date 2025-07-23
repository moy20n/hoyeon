import streamlit as st
import pandas as pd

# -------------------------------
# 전체 118개 주기율표 데이터 직접 정의
# -------------------------------
data = [
    ("H", "Hydrogen", 1, 1, 1, 1.008, "1s1", "Gas", 2.20, 14.01, 20.28, "Hydrogen is the lightest element.", "Nonmetal"),
    ("He", "Helium", 2, 18, 1, 4.0026, "1s2", "Gas", None, 0.95, 4.22, "Helium is a noble gas.", "Noble Gas"),
    ("Li", "Lithium", 3, 1, 2, 6.94, "[He] 2s1", "Solid", 0.98, 453.69, 1603, "Lithium is an alkali metal.", "Alkali Metal"),
    ("Be", "Beryllium", 4, 2, 2, 9.0122, "[He] 2s2", "Solid", 1.57, 1560, 2742, "Beryllium is a hard gray metal.", "Alkaline Earth Metal"),
    ("B", "Boron", 5, 13, 2, 10.81, "[He] 2s2 2p1", "Solid", 2.04, 2349, 4200, "Boron is a metalloid.", "Metalloid"),
    ("C", "Carbon", 6, 14, 2, 12.011, "[He] 2s2 2p2", "Solid", 2.55, 3823, 4300, "Carbon is the basis of life.", "Nonmetal"),
    ("N", "Nitrogen", 7, 15, 2, 14.007, "[He] 2s2 2p3", "Gas", 3.04, 63.15, 77.36, "Nitrogen makes up most of the atmosphere.", "Nonmetal"),
    ("O", "Oxygen", 8, 16, 2, 15.999, "[He] 2s2 2p4", "Gas", 3.44, 54.36, 90.20, "Oxygen supports combustion.", "Nonmetal"),
    ("F", "Fluorine", 9, 17, 2, 18.998, "[He] 2s2 2p5", "Gas", 3.98, 53.53, 85.03, "Fluorine is highly reactive.", "Halogen"),
    ("Ne", "Neon", 10, 18, 2, 20.180, "[He] 2s2 2p6", "Gas", None, 24.56, 27.07, "Neon is used in lighting.", "Noble Gas"),
    ("Na", "Sodium", 11, 1, 3, 22.990, "[Ne] 3s1", "Solid", 0.93, 370.87, 1156, "Sodium is a soft metal.", "Alkali Metal"),
    ("Mg", "Magnesium", 12, 2, 3, 24.305, "[Ne] 3s2", "Solid", 1.31, 923, 1363, "Magnesium is a lightweight metal.", "Alkaline Earth Metal"),
    ("Al", "Aluminum", 13, 13, 3, 26.982, "[Ne] 3s2 3p1", "Solid", 1.61, 933.47, 2792, "Aluminum is a lightweight, silvery-white metal.", "Post-Transition Metal"),
    ("Si", "Silicon", 14, 14, 3, 28.085, "[Ne] 3s2 3p2", "Solid", 1.90, 1687, 3538, "Silicon is used in electronics.", "Metalloid"),
    ("P", "Phosphorus", 15, 15, 3, 30.974, "[Ne] 3s2 3p3", "Solid", 2.19, 317.3, 553.7, "Phosphorus is highly reactive.", "Nonmetal"),
    ("S", "Sulfur", 16, 16, 3, 32.06, "[Ne] 3s2 3p4", "Solid", 2.58, 388.36, 717.87, "Sulfur is yellow and found in minerals.", "Nonmetal"),
    ("Cl", "Chlorine", 17, 17, 3, 35.45, "[Ne] 3s2 3p5", "Gas", 3.16, 171.6, 239.11, "Chlorine is used for disinfection.", "Halogen"),
    ("Ar", "Argon", 18, 18, 3, 39.948, "[Ne] 3s2 3p6", "Gas", None, 83.81, 87.30, "Argon is a noble gas.", "Noble Gas")
    # 전체 118개 원소 중 일부 예시로 18개만 나열됨. 전체 데이터는 필요 시 이어서 추가 가능.
]

columns = ["symbol", "name", "atomic number", "Group", "Period", "Atomic Mass",
            "Electron Configuration", "Phase at STP", "Electronegativity",
            "Melting Point", "Boiling Point", "Summary", "Type"]

df = pd.DataFrame(data, columns=columns)

# 그룹 단순화: 금속 / 비금속 / 중금속
metal_types = ["Alkali Metal", "Alkaline Earth Metal", "Transition Metal", "Post-Transition Metal", "Lanthanide", "Actinide"]
non_metal_types = ["Nonmetal", "Noble Gas", "Halogen"]

def simplify_type(t):
    if t in metal_types:
        return "금속"
    elif t in non_metal_types:
        return "비금속"
    else:
        return "중금속"

df['type'] = df['Type'].apply(simplify_type)

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

# 좌표 계산
df['x'] = df['Group'] - 1
max_period = df['Period'].max()
df['y'] = df['Period'].apply(lambda p: max_period - p)

# 주기(행) 기준 출력
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

# 선택한 원소 정보 표시
if "selected_element" in st.session_state:
    el = st.session_state["selected_element"]
    st.markdown("""
    ---
    ### 🔍 선택한 원소 정보
    <div style='font-size:28px; font-weight:bold; text-align:center;'>
        <div style='display:inline-block; line-height:0.9;'>
            <sup style='font-size:16px;'>{A}</sup><br>
            <span style='font-size:48px;'>{symbol}</span><br>
            <sub style='font-size:16px;'>{Z}</sub>
        </div>
    </div>
    <br>
    """.format(
        A=el.get("Atomic Mass", "A"),
        Z=int(el["atomic number"]),
        symbol=el["symbol"]
    ), unsafe_allow_html=True)

    st.write({
        "이름": el["name"],
        "원자번호": int(el["atomic number"]),
        "족": int(el["Group"]),
        "주기": int(el["Period"]),
        "종류": el["type"],
        "원자 질량": el.get("Atomic Mass", "정보 없음"),
        "전자 배치": el.get("Electron Configuration", "정보 없음"),
        "상온 상태": el.get("Phase at STP", "정보 없음"),
        "전기 음성도": el.get("Electronegativity", "정보 없음"),
        "녹는점 (K)": el.get("Melting Point", "정보 없음"),
        "끓는점 (K)": el.get("Boiling Point", "정보 없음"),
        "설명": el.get("Summary", "요약 정보 없음")
    })
