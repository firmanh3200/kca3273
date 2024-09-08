import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

st.title("Bab 4 Kesehatan")
st.subheader("", divider='rainbow')

data = pd.read_excel("data/penduduk/jumlah_balita_stunting.xlsx")
sort_data = data.sort_values(by=['namakec', 'namakel', 'jumlah_balita'], ascending=[False,False,True])
pivot_tabel = sort_data.pivot_table(index=['namakec', 'namakel'], columns='keterangan', values='jumlah_balita').reset_index()

pilihankec = sort_data['namakec'].unique()

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
    st.info(f"Jumlah Balita Stunting di Kecamatan {pilihkec} Tahun 2023")
    kol1d, kol1e = st.columns(2)
    if pilihkec:
        tabel = sort_data[(sort_data['namakec'] == pilihkec)]
        
        with kol1d:
            pie_kk = px.pie(tabel, values='jumlah_balita', names='keterangan', 
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
            bar_kk = px.bar(tabel, x='keterangan', y='jumlah_balita', color='keterangan', 
                            color_discrete_sequence=warna_options[pilihwarna])
            bar_kk.update_layout(showlegend=False)
            with st.container(border=True):
                st.plotly_chart(bar_kk, use_container_width=True)
        
        tabeljk = pivot_tabel[(pivot_tabel['namakec'] == pilihkec)]
        del tabeljk['namakec']
        st.dataframe(tabeljk, hide_index=True, use_container_width=True)

    st.subheader("", divider='rainbow')
    keterangan = sort_data['keterangan'].unique()
    pilihan = st.selectbox("Filter Keterangan", keterangan)
    
    dataterpilih = sort_data[(sort_data['namakec'] == pilihkec)]
    st.warning(f"{pilihan} di Kecamatan {pilihkec} Tahun 2023")
    kol2a, kol2b = st.columns(2)
    if pilihan:
        dataterpilih2 = dataterpilih[dataterpilih['keterangan'] == pilihan]
        with kol2a:
            trimep = px.treemap(dataterpilih2, path=['namakel'], 
                                values='jumlah_balita', color_discrete_sequence=warna_options[pilihwarna])
            with st.container(border=True):
                st.plotly_chart(trimep, use_container_width=True)
        with kol2b:
            bulet = px.sunburst(dataterpilih2, path=['namakec', 'namakel'], values='jumlah_balita')
            with st.container(border=True):
                st.plotly_chart(bulet, use_container_width=True)
            
    # st.subheader("", divider='rainbow')
    # st.info(f"Perkembangan Jumlah Penduduk di Kecamatan {pilihkec}")
    # datagender['sem'] = datagender['semester'].astype(str) + '-' + datagender['tahun'].astype(str)
    # tren_kk = datagender[datagender['namakec'] == pilihkec]
    # area_kk = px.area(tren_kk, x='sem', y='jumlah_penduduk', color='tipe_goldar', 
    #                         color_discrete_sequence=warna_options[pilihwarna])
    # st.plotly_chart(area_kk, use_container_width=True)
    
    # st.subheader("", divider='rainbow')
    # barkk = px.bar(tren_kk, x='sem', y='jumlah_penduduk', color='tipe_goldar', 
    #                         color_discrete_sequence=warna_options[pilihwarna])
    # st.plotly_chart(barkk, use_container_width=True)
    
    # st.subheader("", divider='rainbow')
    # line_kk = px.line(tren_kk, x='sem', y='jumlah_penduduk', color='tipe_goldar', 
    #                         color_discrete_sequence=warna_options[pilihwarna])
    # st.plotly_chart(line_kk, use_container_width=True)
    
    
st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-balita-stunting-berdasarkan-kelurahan-di-kota-bandung")