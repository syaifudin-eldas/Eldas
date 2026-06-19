import streamlit as st
import pandas as pd

# =====================================
# KONFIGURASI HALAMAN
# =====================================
st.set_page_config(
    page_title="Dashboard Akses Internet Sekolah",
    page_icon="🌐",
    layout="wide"
)

# =====================================
# CUSTOM CSS PREMIUM
# =====================================
st.markdown("""
st.markdown("""
<style>

.stApp{
background:
radial-gradient(circle at top left,#2563eb22,transparent 30%),
radial-gradient(circle at top right,#06b6d422,transparent 30%),
linear-gradient(135deg,#020617,#0f172a,#111827);
}

/* KPI */
div[data-testid="metric-container"]{
background:rgba(255,255,255,0.05);
backdrop-filter:blur(15px);
border:1px solid rgba(255,255,255,0.08);
padding:20px;
border-radius:20px;
box-shadow:0 8px 30px rgba(0,0,0,.4);
}

/* Hover KPI */
div[data-testid="metric-container"]:hover{
transform:translateY(-3px);
transition:.3s;
}

/* Table */
[data-testid="stDataFrame"]{
border-radius:20px;
overflow:hidden;
}

/* Download Button */
.stDownloadButton button{
width:100%;
height:55px;
border-radius:15px;
font-weight:bold;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"]{
background:rgba(255,255,255,0.05);
border-radius:12px;
}

/* Progress */
.stProgress > div > div > div{
background:linear-gradient(
90deg,
#06b6d4,
#2563eb
);
}

</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD DATA
# =====================================
file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

df.columns = df.columns.astype(str).str.strip()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.strip()

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
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

# =====================================
# HEADER PREMIUM
# =====================================
st.markdown("""
<div style="
background: linear-gradient(
90deg,
#2563eb,
#06b6d4,
#14b8a6
);
padding:35px;
border-radius:25px;
text-align:center;
color:white;
margin-bottom:20px;
box-shadow:0px 10px 30px rgba(0,0,0,0.4);
">

<h1>🌐 Indonesia School Internet Dashboard</h1>

<p style="font-size:18px;">
Monitoring Akses Internet Sekolah Indonesia Tahun 2024
</p>

</div>
""", unsafe_allow_html=True)

st.info(
    "📊 Dashboard interaktif untuk analisis akses internet sekolah berdasarkan provinsi dan jenjang pendidikan."
)

# =====================================
# FILTER
# =====================================
col1, col2 = st.columns(2)

with col1:
    pilihan_provinsi = st.selectbox(
        "📍 Pilih Provinsi",
        ["Semua"] + sorted(
            df["Provinsi"]
            .dropna()
            .unique()
            .tolist()
        )
    )

with col2:
    pilihan_pendidikan = st.selectbox(
        "🎓 Pilih Jenjang",
        ["Semua"] + sorted(
            df["Pendidikan"]
            .dropna()
            .unique()
            .tolist()
        )
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
    "📈 Persentase",
    f"{persentase:.2f}%"
)

st.progress(
    min(
        int(persentase),
        100
    )
)

st.markdown("---")

# =====================================
# GRAFIK
# =====================================
top5 = ranking.head(5)

st.subheader("🏆 Top 5 Provinsi Terbaik")

for i,(prov,row) in enumerate(top5.iterrows(),1):

    medal = "🏅"

    if i == 1:
        medal = "🥇"
    elif i == 2:
        medal = "🥈"
    elif i == 3:
        medal = "🥉"

    st.markdown(
        f"{medal} **{prov}** — {row['Persentase']:.2f}%"
)
    st.subheader(
        "🏆 Top 10 Provinsi"
    )

    grafik = (
        filtered
        .groupby("Provinsi")
        ["Total_Internet"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(grafik)

with g2:
    st.subheader(
        "📚 Distribusi Jenjang"
    )

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
st.subheader(
    "🥇 Ranking Provinsi"
)

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

st.dataframe(
    ranking,
    use_container_width=True
)

# =====================================
# DATA LENGKAP
# =====================================
with st.expander(
    "📋 Lihat Data Lengkap"
):
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
    "📥 Download Data",
    csv,
    "akses_internet_sekolah.csv",
    "text/csv"
)

# =====================================
# FOOTER
# =====================================
st.markdown("---")

st.caption(
    "Dashboard Akses Internet Sekolah Indonesia 2024 | Powered by Streamlit"
)
