import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

st.title("Bab 2 Pemerintahan")
st.subheader("", divider='rainbow')

data = pd.read_excel("data/penduduk/jumlah_pns.xlsx")
sort_data = data.sort_values(by=['tahun', 'namakec'], ascending=True)
sort_data2 = data.sort_values(by=['tahun', 'namakec'], ascending=False)

pilihankec = sort_data['namakec'].unique()
pilihantahun = sort_data2['tahun'].unique()

# Pilihan tema warna
warna_options = {
    'Pastel2': px.colors.qualitative.Pastel2,
    'Greens': px.colors.sequential.Greens,
    'Viridis': px.colors.sequential.Viridis,
    'Inferno': px.colors.sequential.Inferno,
    'Set1': px.colors.qualitative.Set1,
    'Set2': px.colors.qualitative.Set2,
    'Set3': px.colors.qualitative.Set3,
    'Pastel1': px.colors.qualitative.Pastel1,
    'Blues': px.colors.sequential.Blues,
    'Reds': px.colors.sequential.Reds,
    'YlGnBu': px.colors.sequential.YlGnBu,
    'YlOrRd': px.colors.sequential.YlOrRd,
    'RdBu': px.colors.diverging.RdBu,
    'Spectral': px.colors.diverging.Spectral
}

kol1a, kol1b, kol1c, kol1d = st.columns(4)
with kol1a:
    pilihkec = st.selectbox("Filter Kecamatan", pilihankec, key='kec1')
with kol1b:
    pilihwarna = st.selectbox("Pilih Tema Warna:", options=list(warna_options.keys()))

# JUMLAH KK
with st.container(border=True):
    st.info(f"Jumlah PNS di Kantor Kecamatan {pilihkec}")
    kol1d, kol1e = st.columns(2)
    if pilihkec:
        tabel = data[(data['namakec'] == pilihkec)]
        
        with kol1d:
            with st.container(border=True):
                pilihtahun = st.selectbox("Filter Tahun", pilihantahun)
                if pilihtahun:
                    data = tabel[tabel['tahun'] == pilihtahun]
                    
                    pie_kk = px.pie(data, values='jumlah_pns', names='jenis_kelamin', 
                                    color_discrete_sequence=warna_options[pilihwarna])
                    pie_kk.update_layout(
                            legend=dict(
                                orientation="h",  # Horizontal orientation
                                yanchor="top",    # Anchor the legend to the top
                                y=-0.2,           # Position the legend below the chart
                                xanchor="center",  # Center the legend horizontally
                                x=0.5              # Center the legend at the middle of the chart
                            )
                        )
                    st.plotly_chart(pie_kk, use_container_width=True)
        with kol1e:
            pivot = tabel.pivot_table(index=['namakec', 'tahun'], columns='jenis_kelamin', values='jumlah_pns').reset_index()
        
            st.dataframe(pivot, hide_index=True, use_container_width=True)
            
        st.subheader("", divider='rainbow')
        bar_kk = px.bar(tabel, x='tahun', y='jumlah_pns', color='jenis_kelamin', 
                            color_discrete_sequence=warna_options[pilihwarna])
        bar_kk.update_layout(legend=dict(
                                orientation="h",  # Horizontal orientation
                                yanchor="top",    # Anchor the legend to the top
                                y=-0.2,           # Position the legend below the chart
                                xanchor="center",  # Center the legend horizontally
                                x=0.5              # Center the legend at the middle of the chart
                            ))
        with st.container(border=True):
            st.plotly_chart(bar_kk, use_container_width=True)
    
st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-pns-kota-bandung-berdasarkan-perangkat-daerah-dan-jenis-kelamin")