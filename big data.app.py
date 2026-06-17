import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Akses Internet Sekolah",
    page_icon="📶",
    layout="wide"
)

file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

st.title("📶 Dashboard Akses Internet Sekolah 2024")
st.markdown("Data jumlah sekolah yang memiliki akses internet tahun 2024")

col1, col2 = st.columns(2)

with col1:
    st.metric("Jumlah Data", len(df))

with col2:
    st.metric("Jumlah Provinsi", df["Provinsi"].nunique())

st.divider()

if "Provinsi" in df.columns:
    provinsi = st.selectbox(
        "Pilih Provinsi",
        ["Semua"] + sorted(df["Provinsi"].unique().tolist())
    )

    if provinsi != "Semua":
        df = df[df["Provinsi"] == provinsi]

st.subheader("📋 Data")

st.dataframe(
    df,
    use_container_width=True
)

if "Total_Internet" in df.columns:
    st.subheader("📊 Grafik Sekolah dengan Akses Internet")

    grafik = (
        df.groupby("Provinsi")["Total_Internet"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(grafik)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Data",
    csv,
    "data_sekolah_internet.csv",
    "text/csv"
)
