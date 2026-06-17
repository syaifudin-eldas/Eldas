import streamlit as st
import pandas as pd

file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"

url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

st.title("Jumlah Sekolah Akses Internet 2024")

st.dataframe(df)