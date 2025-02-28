import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="ข้อมูลสถิติ รพ.", page_icon="📊", layout="wide")

uploaded_files = st.file_uploader("📂 อัปโหลดไฟล์ CSV", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file)

        # ✅ ลบช่องว่างจากชื่อคอลัมน์
        df.columns = df.columns.str.strip()
        st.write("🔎 คอลัมน์ในไฟล์:", df.columns.tolist())  # Debug

        if df.empty:
            st.error(f"⚠️ ไฟล์ **{file.name}** ไม่มีข้อมูล!")
            continue

        columns = df.columns.tolist()

        x_axis = st.selectbox(f"📌 เลือกแกน X ({file.name})", columns, key=f"x_{file.name}")
        y_axis = st.selectbox(f"📌 เลือกแกน Y ({file.name})", columns, key=f"y_{file.name}")

        # ✅ ตรวจสอบว่า X และ Y มีอยู่จริง
        if x_axis not in df.columns or y_axis not in df.columns:
            st.error(f"⚠️ ไม่พบคอลัมน์ {x_axis} หรือ {y_axis} ในไฟล์ {file.name}")
            st.stop()

        # ✅ ตรวจสอบว่า Y เป็นตัวเลข
        if not pd.api.types.is_numeric_dtype(df[y_axis]):
            st.error(f"⚠️ คอลัมน์ {y_axis} ต้องเป็นตัวเลขเท่านั้น!")
            continue

        df = df.sort_values(by=y_axis, ascending=False)

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(x_axis, type='nominal', sort=df[x_axis].tolist()),
            y=alt.Y(y_axis, type='quantitative')
        ).properties(title=f" {file.name}", width=800, height=400)

        st.altair_chart(chart, use_container_width=True)
