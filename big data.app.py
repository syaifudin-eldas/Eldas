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

# Hapus spasi nama kolom
df.columns = df.columns.str.strip()

st.title("📶 Dashboard Akses Internet Sekolah 2024")

col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Data", len(df))
col2.metric("Jumlah Provinsi", df["Provinsi"].nunique())
col3.metric("Jenjang Pendidikan", df["Pendidikan"].nunique())

st.divider()

provinsi = st.selectbox(
    "Pilih Provinsi",
    ["Semua"] + sorted(df["Provinsi"].unique())
)

if provinsi != "Semua":
    df = df[df["Provinsi"] == provinsi]

st.subheader("📊 Top 10 Sekolah Berakses Internet")

grafik = (
    df.groupby("Provinsi")["Total_Internet"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(grafik)

st.subheader("📋 Data Lengkap")
st.dataframe(df, use_container_width=True)
