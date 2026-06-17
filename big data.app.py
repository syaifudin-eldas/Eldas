import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Akses Internet Sekolah 2024",
    page_icon="📶",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

# rapikan nama kolom
df.columns = [c.strip() for c in df.columns]

# rapikan isi text
df["Provinsi"] = df["Provinsi"].astype(str).str.strip()
df["Pendidikan"] = df["Pendidikan"].astype(str).str.strip()

# ubah ke numerik
kolom_angka = [
    "Total_Internet",
    "Total_Sekolah",
    "Diff_Total"
]

for col in kolom_angka:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# HEADER
# =========================
st.title("📶 Dashboard Akses Internet Sekolah 2024")
st.markdown(
    "Dashboard visualisasi jumlah sekolah yang memiliki akses internet berdasarkan provinsi dan jenjang pendidikan."
)

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("🔍 Filter Data")

pendidikan = st.sidebar.multiselect(
    "Pilih Jenjang Pendidikan",
    sorted(df["Pendidikan"].unique()),
    default=sorted(df["Pendidikan"].unique())
)

provinsi = st.sidebar.multiselect(
    "Pilih Provinsi",
    sorted(df["Provinsi"].unique()),
    default=sorted(df["Provinsi"].unique())
)

filtered = df[
    (df["Pendidikan"].isin(pendidikan))
    &
    (df["Provinsi"].isin(provinsi))
]

# =========================
# KPI
# =========================
total_sekolah = int(filtered["Total_Sekolah"].sum())
total_internet = int(filtered["Total_Internet"].sum())
belum_internet = int(filtered["Diff_Total"].sum())

persentase = (
    total_internet / total_sekolah * 100
    if total_sekolah > 0 else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏫 Total Sekolah", f"{total_sekolah:,}")
c2.metric("🌐 Memiliki Internet", f"{total_internet:,}")
c3.metric("❌ Belum Internet", f"{belum_internet:,}")
c4.metric("📊 Persentase", f"{persentase:.1f}%")

st.divider()

# =========================
# CHART 1
# =========================
prov_data = (
    filtered.groupby("Provinsi", as_index=False)
    .agg({
        "Total_Internet":"sum",
        "Total_Sekolah":"sum"
    })
)

fig1 = px.bar(
    prov_data.sort_values("Total_Internet", ascending=False),
    x="Provinsi",
    y="Total_Internet",
    title="Jumlah Sekolah dengan Akses Internet per Provinsi"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# CHART 2
# =========================
jenjang = (
    filtered.groupby("Pendidikan", as_index=False)
    .agg({
        "Total_Internet":"sum"
    })
)

fig2 = px.pie(
    jenjang,
    names="Pendidikan",
    values="Total_Internet",
    title="Distribusi Akses Internet Berdasarkan Jenjang"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# TOP 10
# =========================
st.subheader("🏆 Top 10 Provinsi dengan Sekolah Berinternet Terbanyak")

top10 = (
    prov_data
    .sort_values("Total_Internet", ascending=False)
    .head(10)
)

fig3 = px.bar(
    top10,
    x="Provinsi",
    y="Total_Internet",
    text="Total_Internet"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Data Lengkap")

st.dataframe(
    filtered,
    use_container_width=True
)

# =========================
# DOWNLOAD
# =========================
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Data Hasil Filter",
    csv,
    file_name="akses_internet_sekolah_2024.csv",
    mime="text/csv"
)
