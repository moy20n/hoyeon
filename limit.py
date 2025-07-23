import streamlit as st
import pandas as pd

# -------------------------------
# 전체 주기율표 데이터 (요약)
# -------------------------------
data = [
    ("H",  "Hydrogen",     1,  1, 1, "비금속", 0, 0),
    ("He", "Helium",       2, 18, 1, "비금속", 17, 0),
    ("Li", "Lithium",      3,  1, 2, "금속", 0, 1),
    ("Be", "Beryllium",    4,  2, 2, "금속", 1, 1),
    ("B",  "Boron",        5, 13, 2, "중금속", 12, 1),
    ("C",  "Carbon",       6, 14, 2, "비금속", 13, 1),
    ("N",  "Nitrogen",     7, 15, 2, "비금속", 14, 1),
    ("O",  "Oxygen",       8, 16, 2, "비금속", 15, 1),
    ("F",  "Fluorine",     9, 17, 2, "비금속", 16, 1),
    ("Ne", "Neon",        10, 18, 2, "비금속", 17, 1),
    ("Na", "Sodium",      11,  1, 3, "금속", 0, 2),
    ("Mg", "Magnesium",   12,  2, 3, "금속", 1, 2),
    ("Al", "Aluminum",    13, 13, 3, "금속", 12, 2),
    ("Si", "Silicon",     14, 14, 3, "중금속", 13, 2),
    ("P",  "Phosphorus",  15, 15, 3, "비금속", 14, 2),
    ("S",  "Sulfur",      16, 16, 3, "비금속", 15, 2),
    ("Cl", "Chlorine",    17, 17, 3, "비금속", 16, 2),
    ("Ar", "Argon",       18, 18, 3, "비금속", 17, 2),
    ("K",  "Potassium",   19,  1, 4, "금속", 0, 3),
    ("Ca", "Calcium",     20,  2, 4, "금속", 1, 3),
    ("Sc", "Scandium",    21,  3, 4, "중금속", 2, 3),
    ("Ti", "Titanium",    22,  4, 4, "중금속", 3, 3),
    ("V",  "Vanadium",    23,  5, 4, "중금속", 4, 3),
    ("Cr", "Chromium",    24,  6, 4, "중금속", 5, 3),
    ("Mn", "Manganese",   25,  7, 4, "중금속", 6, 3),
    ("Fe", "Iron",        26,  8, 4, "중금속", 7, 3),
    ("Co", "Cobalt",      27,  9, 4, "중금속", 8, 3),
    ("Ni", "Nickel",      28, 10, 4, "중금속", 9, 3),
    ("Cu", "Copper",      29, 11, 4, "중금속", 10, 3),
    ("Zn", "Zinc",        30, 12, 4, "중금속", 11, 3),
]

cols = ["symbol", "name", "atomic_number", "group", "period", "type", "x", "y"]
df = pd.DataFrame(data, columns=cols)

# 색상 맵핑
color_map = {
    "금속": "#FFD700",
    "비금속": "#87CEFA",
    "중금속": "#D3D3D3"
}
df["color"] = df["type"].map(color_map)

# 박스형 UI 출력
st.set_page_config(page_title="ChemPlay - 주기율표 박스형", layout="wide")
st.title("🧪 ChemPlay: 전체 주기율표 (박스형)")

# 주기(행) 기준으로 정렬해서 출력
y_levels = sorted(df["y"].unique())
for y in y_levels:
    row = df[df["y"] == y].sort_values("x")
    cols = st.columns(18)
    for _, el in row.iterrows():
        with cols[el["x"]]:
            st.markdown(f"""
                <div style='text-align:center; background-color:{el['color']}; padding:10px; border-radius:8px;'>
                    <strong>{el['symbol']}</strong><br>
                    <small>{el['atomic_number']}</small>
                </div>
            """, unsafe_allow_html=True)

st.info("⚠️ 현재는 30개 원소까지만 표시됨. 전체 118개 확장은 다음 단계에서 가능해요!")
