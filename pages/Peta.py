import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly_express as px
import requests

st.set_page_config(layout='wide')

geojson_data = requests.get(
    "https://raw.githubusercontent.com/firmanh3200/batas-administrasi-indonesia/refs/heads/master/Kel_Desa/desa3273.json"
).json()

data = pd.read_csv(
    'data/jumlah_kk.csv', sep=';',
    dtype={'KODE_KD':'str', 'jumlah_kk':'float',
           'bps_nama_kecamatan':'str', 'bps_desa_kelurahan':'str'}
)

filter_data = data.query("bps_nama_kecamatan == 'CIBEUNYING KIDUL' and tahun == 2023 and semester == 1")

st.title("Statistik Kota Bandung")
st.subheader("", divider='rainbow')

with st.container(border=True):
    kolom1, kolom2 = st.columns(2)
    data = data.sort_values(by=['tahun', 'semester'], ascending=[False, True])
    pilihantahun = data['tahun'].unique()
    pilihansem = data['semester'].unique()
    
    with kolom1:
        tahunterpilih = st.selectbox("Filter Tahun", pilihantahun)
    
    with kolom2:
        semterpilih = st.selectbox("Filter Semester", pilihansem)
        
    if tahunterpilih and semterpilih:
        st.subheader(f"Sebaran Kepala Keluarga di Kota Bandung, Semester {semterpilih} Tahun {tahunterpilih}")

        fig = px.choropleth_mapbox(
            data_frame=data[(data['tahun'] == tahunterpilih) & (data['semester'] == semterpilih)],
            geojson=geojson_data,
            locations="KODE_KD",
            color="jumlah_kk",
            color_continuous_scale="Viridis_r",
            opacity=0.7,
            featureidkey="properties.KODE_KD",
            zoom=11,
            center={"lat": -6.914845, "lon": 107.609836},
            mapbox_style="carto-positron",
            hover_name="kemendagri_nama_desa_kelurahan",
            hover_data=["kemendagri_nama_kecamatan", "kemendagri_nama_desa_kelurahan", 'tahun', 'semester', "jumlah_kk"]
        )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
st.subheader("", divider='rainbow')
st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-kepala-keluarga-berdasarkan-kelurahan-di-kota-bandung")
st.link_button("Sumber Peta", url="https://github.com/Alf-Anas/batas-administrasi-indonesia") 

