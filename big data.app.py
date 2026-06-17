import streamlit as st
import pandas as pd

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Indonesia Internet School Dashboard",
    page_icon="🌐",
    layout="wide"
)

# =====================
# LOAD DATA
# =====================
file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# =====================
# HEADER
# =====================
st.title("🌐 Indonesia School Internet Dashboard")
st.caption("Monitoring Akses Internet Sekolah Indonesia Tahun 2024")

st.markdown("---")

# =====================
# SIDEBAR
# =====================
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=100
)

st.sidebar.title("Filter Data")

provinsi = st.sidebar.selectbox(
    "Provinsi",
    ["Semua"] + sorted(df["Provinsi"].unique())
)

pendidikan = st.sidebar.selectbox(
    "Jenjang",
    ["Semua"] + sorted(df["Pendidikan"].unique())
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

# =====================
# KPI
# =====================
total_sekolah = int(filtered["Total_Sekolah"].sum())
total_internet = int(filtered["Total_Internet"].sum())
belum_internet = int(filtered["Diff_Total"].sum())

persen = (
    total_internet /
    total_sekolah * 100
    if total_sekolah > 0 else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🏫 Total Sekolah",
    f"{total_sekolah:,}"
)

c2.metric(
    "🌐 Terkoneksi",
    f"{total_internet:,}"
)

c3.metric(
    "❌ Belum Terkoneksi",
    f"{belum_internet:,}"
)

c4.metric(
    "📊 Persentase",
    f"{persen:.2f}%"
)

st.progress(min(int(persen),100))

st.markdown("---")

# =====================
# TOP PROVINSI
# =====================
left,right = st.columns(2)

with left:

    st.subheader(
        "🏆 Top 10 Provinsi"
    )

    top = (
        filtered
        .groupby("Provinsi")
        ["Total_Internet"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(top)

with right:

    st.subheader(
        "📚 Distribusi Jenjang"
    )

    pendidikan_data = (
        filtered
        .groupby("Pendidikan")
        ["Total_Internet"]
        .sum()
    )

    st.bar_chart(
        pendidikan_data
    )

# =====================
# RANKING
# =====================
st.subheader(
    "🏅 Ranking Provinsi"
)

ranking = (
    filtered
    .groupby("Provinsi")
    .agg({
        "Total_Internet":"sum",
        "Total_Sekolah":"sum"
    })
    .reset_index()
)

ranking["Persentase"] = (
    ranking["Total_Internet"]
    /
    ranking["Total_Sekolah"]
    *100
)

ranking = ranking.sort_values(
    "Persentase",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

# =====================
# DETAIL DATA
# =====================
with st.expander(
    "📋 Lihat Data Lengkap"
):
    st.dataframe(
        filtered,
        use_container_width=True
    )

# =====================
# DOWNLOAD
# =====================
csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Data",
    csv,
    "akses_internet_sekolah.csv",
    "text/csv"
)

# =====================
# FOOTER
# =====================
st.markdown("---")

st.caption(
    "Dashboard dibuat menggunakan Streamlit | Data Akses Internet Sekolah Indonesia 2024"
)
