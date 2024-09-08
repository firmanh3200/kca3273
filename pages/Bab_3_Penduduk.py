import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

st.title("Bab 3 Kependudukan")
st.subheader("", divider='rainbow')

data = pd.read_excel("data/penduduk/jumlah_penduduk.xlsx")
sort_data = data.sort_values(by=['tahun', 'semester', 'namakec', 'namakel'], ascending=[False,False,True,True])

pilihankec = sort_data['namakec'].unique()
pilihantahun = sort_data['tahun'].unique()
pilihansemester = sort_data['semester'].unique()

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
    pilihtahun = st.selectbox("Filter Tahun", pilihantahun, key='tahun1')
with kol1c:
    pilihsem = st.selectbox("Filter Semester", pilihansemester, key='sem1')
with kol1d:
    pilihwarna = st.selectbox("Pilih Tema Warna:", options=list(warna_options.keys()))

# JUMLAH KK
with st.container(border=True):
    st.info(f"Jumlah Penduduk di Kecamatan {pilihkec}, Semester {pilihsem} Tahun {pilihtahun}")
    kol1d, kol1e, kol1f = st.columns(3)
    if pilihkec and pilihtahun and pilihsem:
        tabel = data[(data['namakec'] == pilihkec) & (data['tahun'] == pilihtahun) & (data['semester'] == pilihsem)]
        tabel = tabel[['namakel', 'jumlah_penduduk']].sort_values(by='jumlah_penduduk', ascending=False)
        
        with kol1d:
            pie_kk = px.pie(tabel, values='jumlah_penduduk', names='namakel', 
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
            with st.container(border=True):
                st.plotly_chart(pie_kk, use_container_width=True)
        with kol1e:
            bar_kk = px.bar(tabel, x='namakel', y='jumlah_penduduk', color='namakel', 
                            color_discrete_sequence=warna_options[pilihwarna])
            bar_kk.update_layout(showlegend=False)
            with st.container(border=True):
                st.plotly_chart(bar_kk, use_container_width=True)
        with kol1f:
            st.dataframe(tabel, hide_index=True, use_container_width=True)
    
    st.subheader("", divider='rainbow')
    st.info(f"Perkembangan Jumlah Penduduk di Kecamatan {pilihkec}")
    data['sem'] = data['semester'].astype(str) + '-' + data['tahun'].astype(str)
    tren_kk = data[data['namakec'] == pilihkec]
    area_kk = px.area(tren_kk, x='sem', y='jumlah_penduduk', color='namakel', 
                            color_discrete_sequence=warna_options[pilihwarna])
    st.plotly_chart(area_kk, use_container_width=True)
    
    st.subheader("", divider='rainbow')
    barkk = px.bar(tren_kk, x='sem', y='jumlah_penduduk', color='namakel', 
                            color_discrete_sequence=warna_options[pilihwarna])
    st.plotly_chart(barkk, use_container_width=True)
    
    st.subheader("", divider='rainbow')
    line_kk = px.line(tren_kk, x='sem', y='jumlah_penduduk', color='namakel', 
                            color_discrete_sequence=warna_options[pilihwarna])
    st.plotly_chart(line_kk, use_container_width=True)
    
    
st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-penduduk-kota-bandung-berdasarkan-jenis-kelamin-2")