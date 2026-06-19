import streamlit as st
import pandas as pd

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Dashboard Akses Internet Sekolah",
    page_icon="🌐",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================
st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
}

div[data-testid="metric-container"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 15px;
}

.stDownloadButton button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD DATA
# =====================================
file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

df.columns = df.columns.str.strip()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.strip()

kolom_angka = [
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

for col in kolom_angka:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

# =====================================
# HEADER
# =====================================
st.markdown("""
<div style="
background:linear-gradient(90deg,#2563eb,#06b6d4);
padding:30px;
border-radius:20px;
text-align:center;
color:white;
">
<h1>🌐 Indonesia School Internet Dashboard</h1>
<p>Monitoring Akses Internet Sekolah Indonesia Tahun 2024</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================
# FILTER
# =====================================
c1, c2 = st.columns(2)

with c1:
    provinsi = st.selectbox(
        "📍 Pilih Provinsi",
        ["Semua"] + sorted(df["Provinsi"].dropna().unique())
    )

with c2:
    pendidikan = st.selectbox(
        "🎓 Pilih Jenjang",
        ["Semua"] + sorted(df["Pendidikan"].dropna().unique())
    )

filtered = df.copy()

if provinsi != "Semua":
    filtered = filtered[
        filtered["Provinsi"] == provinsi
    ]

if pendidikan != "Semua":
    filtered = filtered[
        filtered["Pendidikan"] == pendidikan
    ]

# =====================================
# KPI
# =====================================
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

with k1:
    st.metric(
        "🏫 Total Sekolah",
        f"{int(total_sekolah):,}"
    )

with k2:
    st.metric(
        "🌐 Terhubung",
        f"{int(total_internet):,}"
    )

with k3:
    st.metric(
        "❌ Belum Terhubung",
        f"{int(belum_internet):,}"
    )

with k4:
    st.metric(
        "📊 Persentase",
        f"{persentase:.2f}%"
    )

st.progress(
    min(int(persentase), 100)
)

st.divider()

# =====================================
# TOP 5 PROVINSI
# =====================================
ranking = (
    filtered
    .groupby("Provinsi")
    .agg({
        "Total_Internet":"sum",
        "Total_Sekolah":"sum"
    })
)

ranking["Persentase"] = (
    ranking["Total_Internet"]
    /
    ranking["Total_Sekolah"]
    * 100
)

ranking = ranking.sort_values(
    "Persentase",
    ascending=False
)

st.subheader("🏆 Top 5 Provinsi")

top5 = ranking.head(5)

for i, (prov, row) in enumerate(top5.iterrows(), start=1):

    medal = "🏅"

    if i == 1:
        medal = "🥇"
    elif i == 2:
        medal = "🥈"
    elif i == 3:
        medal = "🥉"

    st.write(
        f"{medal} {prov} — {row['Persentase']:.2f}%"
    )

st.divider()

# =====================================
# GRAFIK
# =====================================
g1, g2 = st.columns(2)

with g1:

    st.subheader("🏆 Top 10 Provinsi")

    top_prov = (
        filtered
        .groupby("Provinsi")
        ["Total_Internet"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_prov)

with g2:

    st.subheader("📚 Distribusi Jenjang")

    jenjang = (
        filtered
        .groupby("Pendidikan")
        ["Total_Internet"]
        .sum()
    )

    st.bar_chart(jenjang)

# =====================================
# RANKING
# =====================================
st.subheader("🥇 Ranking Provinsi")

st.dataframe(
    ranking,
    use_container_width=True
)

# =====================================
# DATA LENGKAP
# =====================================
with st.expander("📋 Data Lengkap"):

    st.dataframe(
        filtered,
        use_container_width=True
    )

# =====================================
# DOWNLOAD
# =====================================
csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Data CSV",
    csv,
    "akses_internet_sekolah.csv",
    "text/csv"
)

# =====================================
# FOOTER
# =====================================
st.divider()

st.markdown("""
<center>
<h4>🌐 Dashboard Akses Internet Sekolah Indonesia 2024</h4>
<p>Powered by Streamlit & Pandas</p>
</center>
""", unsafe_allow_html=True)
