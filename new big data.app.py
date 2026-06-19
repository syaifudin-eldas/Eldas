import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Indonesia School Internet Dashboard",
    page_icon="🌐",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.stApp{
    background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
}

.metric-card{
    background: rgba(255,255,255,0.05);
    border-radius:20px;
    padding:20px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
}

.metric-card h1,.metric-card h3{
    color:white;
}
</style>
""", unsafe_allow_html=True)

file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].astype(str).str.strip()

angka = [
    "Negeri_Internet","Swasta_Internet","Total_Internet",
    "Negeri_Sekolah","Swasta_Sekolah","Total_Sekolah",
    "Diff_Negeri","Diff_Swasta","Diff_Total"
]

for col in angka:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

with st.sidebar:
    st.title("🌐 Dashboard")
    st.info("Monitoring akses internet sekolah Indonesia 2024")
    st.write("Jumlah Provinsi:", df["Provinsi"].nunique())
    st.write("Jumlah Jenjang:", df["Pendidikan"].nunique())

st.markdown("""
<div style="background:linear-gradient(90deg,#2563eb,#06b6d4);
padding:30px;border-radius:20px;text-align:center;color:white;">
<h1>🌐 Indonesia School Internet Dashboard</h1>
<p>Monitoring Akses Internet Sekolah Indonesia Tahun 2024</p>
</div>
""", unsafe_allow_html=True)

c1,c2 = st.columns(2)

with c1:
    provinsi = st.selectbox("📍 Pilih Provinsi",
        ["Semua"] + sorted(df["Provinsi"].dropna().unique()))

with c2:
    pendidikan = st.selectbox("🎓 Pilih Jenjang",
        ["Semua"] + sorted(df["Pendidikan"].dropna().unique()))

filtered = df.copy()

if provinsi != "Semua":
    filtered = filtered[filtered["Provinsi"] == provinsi]

if pendidikan != "Semua":
    filtered = filtered[filtered["Pendidikan"] == pendidikan]

total_sekolah = filtered["Total_Sekolah"].sum()
total_internet = filtered["Total_Internet"].sum()
belum_internet = filtered["Diff_Total"].sum()

persentase = 0
if total_sekolah > 0:
    persentase = total_internet / total_sekolah * 100

k1,k2,k3,k4 = st.columns(4)

cards = [
    ("🏫 Total Sekolah", int(total_sekolah)),
    ("🌐 Terhubung", int(total_internet)),
    ("❌ Belum Terhubung", int(belum_internet)),
    ("📊 Persentase", f"{persentase:.2f}%")
]

for col, (judul, nilai) in zip([k1,k2,k3,k4], cards):
    with col:
        st.markdown(f"""
        <div class="metric-card">
        <h3>{judul}</h3>
        <h1>{nilai}</h1>
        </div>
        """, unsafe_allow_html=True)

st.progress(min(int(persentase),100))

ranking = filtered.groupby("Provinsi").agg({
    "Total_Internet":"sum",
    "Total_Sekolah":"sum"
})

ranking["Persentase"] = (
    ranking["Total_Internet"] / ranking["Total_Sekolah"] * 100
)

ranking = ranking.sort_values("Persentase", ascending=False)

g1,g2 = st.columns(2)

with g1:
    top_prov = (
        filtered.groupby("Provinsi")["Total_Internet"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig = px.bar(
        x=top_prov.values,
        y=top_prov.index,
        orientation="h",
        title="Top 10 Provinsi"
    )

    fig.update_layout(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

with g2:
    fig2 = go.Figure(
        data=[go.Pie(
            labels=["Terhubung","Belum Terhubung"],
            values=[total_internet,belum_internet],
            hole=0.6
        )]
    )

    fig2.update_layout(
        paper_bgcolor="#0f172a",
        font_color="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

st.subheader("🥇 Ranking Provinsi")
st.dataframe(ranking, use_container_width=True)

with st.expander("📋 Data Lengkap"):
    st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Data CSV",
    csv,
    "akses_internet_sekolah.csv",
    "text/csv"
)

st.markdown("---")
st.markdown(
    "<center><h4>🌐 Dashboard Akses Internet Sekolah Indonesia 2024</h4></center>",
    unsafe_allow_html=True
)
