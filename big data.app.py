import streamlit as st
import pandas as pd

file_id = "1lIzy0UBFPth_csvflUUYpdv5zpr7fUmc"
url = f"https://drive.google.com/uc?id={file_id}"

df = pd.read_csv(url)

st.write("Kolom yang terbaca:")
st.write(df.columns.tolist())

st.dataframe(df.head())
