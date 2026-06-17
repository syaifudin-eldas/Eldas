import streamlit as st
import pandas as pd

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Dashboard Akses Internet Sekolah",
    page_icon="🌐",
    layout="wide"
)

# ==========================
# LOAD DATA
# ==========================
file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

# Bersihkan nama kolom
df.columns = df.columns.astype(str).str.strip()

# Bersihkan data teks
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.strip()

# Ubah kolom angka
angka = [
    "Negeri_Internet",
    "Swasta_Internet",
    "Total_Internet",
    "Negeri_Sekolah",
    "Swasta_Sekolah",
    "Total_Sekolah",
    "Diff_Negeri",
    "Diff_Swasta",
    "Diff_Total"
]

for col in angka:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ==========================
# HEADER
# ==========================
st.title("🌐 Indonesia School Internet Dashboard")
st.caption("Monitoring Akses Internet Sekolah Indonesia Tahun 2024")

st.markdown("---")

# ==========================
# FILTER
# ==========================
col1, col2 = st.columns(2)

with col1:
    pilihan_provinsi = st.selectbox(
        "📍 Pilih Provinsi",
        ["Semua"] + sorted(df["Provinsi"].dropna().unique().tolist())
    )

with col2:
    pilihan_pendidikan = st.selectbox(
        "🎓 Pilih Jenjang",
        ["Semua"] + sorted(df["Pendidikan"].dropna().unique().tolist())
    )

filtered = df.copy()

if pilihan_provinsi != "Semua":
    filtered = filtered[
        filtered["Provinsi"] == pilihan_provinsi
    ]

if pilihan_pendidikan != "Semua":
    filtered = filtered[
        filtered["Pendidikan"] == pilihan_pendidikan
    ]

# ==========================
# KPI
# ==========================
total_sekolah = filtered["Total_Sekolah"].sum()
total_internet = filtered["Total_Internet"].sum()
belum_internet = filtered["Diff_Total"].sum()

persentase = 0

if total_sekolah > 0:
    persentase = (
        total_internet /
        total_sekolah
    ) * 100

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "🏫 Total Sekolah",
    f"{int(total_sekolah):,}"
)

k2.metric(
    "🌐 Terhubung Internet",
    f"{int(total_internet):,}"
)

k3.metric(
    "❌ Belum Terhubung",
    f"{int(belum_internet):,}"
)

k4.metric(
    "📊 Persentase",
    f"{persentase:.2f}%"
)

st.progress(min(int(persentase), 100))

st.markdown("---")

# ==========================
# GRAFIK
# ==========================
st.subheader("🏆 Top 10 Provinsi")

grafik = (
    filtered.groupby("Provinsi")["Total_Internet"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(grafik)

# ==========================
# JENJANG PENDIDIKAN
# ==========================
st.subheader("📚 Akses Internet Berdasarkan Jenjang")

jenjang = (
    filtered.groupby("Pendidikan")["Total_Internet"]
    .sum()
)

st.bar_chart(jenjang)

# ==========================
# RANKING
# ==========================
st.subheader("🥇 Ranking Provinsi")

ranking = (
    filtered.groupby("Provinsi")
    .agg({
        "Total_Internet": "sum",
        "Total_Sekolah": "sum"
    })
)

ranking["Persentase"] = (
    ranking["Total_Internet"] /
    ranking["Total_Sekolah"] * 100
)

ranking = ranking.sort_values(
    "Persentase",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

# ==========================
# DATA LENGKAP
# ==========================
with st.expander("📋 Lihat Data Lengkap"):
    st.dataframe(
        filtered,
        use_container_width=True
    )

# ==========================
# DOWNLOAD
# ==========================
csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Data",
    csv,
    "akses_internet_sekolah.csv",
    "text/csv"
)
