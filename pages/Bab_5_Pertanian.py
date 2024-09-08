import streamlit as st
import pandas as pd
import plotly_express as px
import openpyxl

st.set_page_config(layout='wide')

st.title("Bab 5 Pertanian")
st.subheader("", divider='rainbow')

produksi_sayur = pd.read_excel("data/penduduk/jumlah_produksi_sayuran.xlsx")
produksi_sayur = produksi_sayur.fillna(0)

populasi_unggas = pd.read_excel("data/penduduk/jumlah_populasi_unggas.xlsx")
populasi_unggas = populasi_unggas.fillna(0)

populasi_ternak = pd.read_excel("data/penduduk/jumlah_populasi_ternak.xlsx")
populasi_ternak = populasi_ternak.fillna(0)

produksi_telur = pd.read_excel("data/penduduk/jumlah_produksi_telur.xlsx")
produksi_telur = produksi_telur.fillna(0)

pilihankec = populasi_ternak['namakec'].unique()


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

# PRODUKSI SAYURAN
with st.container(border=True):
    st.success(f"Jumlah Produksi Tanaman Sayuran di Kecamatan {pilihkec} (Kwintal)")
    if pilihkec:
        tabel = produksi_sayur[(produksi_sayur['namakec'] == pilihkec)]
        bar_kk = px.bar(tabel, x='tahun', y='jumlah_produksi', color='jenis_komoditas', 
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

        with st.expander("Lihat Tabel"):
            pivot = tabel.pivot_table(index=['namakec', 'tahun'], columns='jenis_komoditas', values='jumlah_produksi').reset_index()
            st.dataframe(pivot, hide_index=True, use_container_width=True)
        
        
        produksi_sayur = produksi_sayur.sort_values(by='tahun', ascending=False)
        pilihantahun_sayur = produksi_sayur['tahun'].unique()
        pilihtahun_sayur = st.selectbox("Filter Tahun", pilihantahun_sayur, key='tahun1')

        
        kol1d, kol1e = st.columns(2)
        
        if pilihtahun_sayur:
            datasayur = tabel[tabel['tahun'] == pilihtahun_sayur]
        
            with kol1d:
                bar_sayur = px.bar(datasayur, x='jenis_komoditas', y='jumlah_produksi', color='jenis_komoditas', 
                            color_discrete_sequence=warna_options[pilihwarna])
                bar_sayur.update_layout(showlegend=False)
                with st.container(border=True):
                    st.plotly_chart(bar_sayur, use_container_width=True)
            
            with kol1e:
                    piesayur = px.pie(datasayur, names='jenis_komoditas', values='jumlah_produksi', 
                            color_discrete_sequence=warna_options[pilihwarna])
                    piesayur.update_layout(legend=dict(
                                            orientation="h",  # Horizontal orientation
                                            yanchor="top",    # Anchor the legend to the top
                                            y=-0.2,           # Position the legend below the chart
                                            xanchor="center",  # Center the legend horizontally
                                            x=0.5              # Center the legend at the middle of the chart
                                        ))
                    with st.container(border=True):
                        st.plotly_chart(piesayur, use_container_width=True)
            
            
    st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-produksi-tanaman-sayuran-berdasarkan-kecamatan-dan-jenis-sayuran-di-kota-bandung")    
st.subheader("", divider='rainbow')
    
# POPULASI UNGGAS
with st.expander("POPULASI UNGGAS"):
    st.success(f"Jumlah Populasi Unggas di Kecamatan {pilihkec} (Ekor)")
    if pilihkec:
        tabel_unggas = populasi_unggas[(populasi_unggas['namakec'] == pilihkec)]
        bar_unggas = px.bar(tabel_unggas, x='tahun', y='jumlah', color='kategori_unggas', 
                    color_discrete_sequence=warna_options[pilihwarna])
        bar_unggas.update_layout(legend=dict(
                                orientation="h",  # Horizontal orientation
                                yanchor="top",    # Anchor the legend to the top
                                y=-0.2,           # Position the legend below the chart
                                xanchor="center",  # Center the legend horizontally
                                x=0.5              # Center the legend at the middle of the chart
                            ))
        
        kola, kolb = st.columns(2)
        with kola:
            with st.container(border=True):
                st.plotly_chart(bar_unggas, use_container_width=True)

        with kolb:
            with st.container(border=True):
                pivot = tabel_unggas.pivot_table(index=['namakec', 'tahun'], columns='kategori_unggas', values='jumlah').reset_index()
                st.dataframe(pivot, hide_index=True, use_container_width=True)
        
        
        populasi_unggas = populasi_unggas.sort_values(by='tahun', ascending=False)
        pilihantahun_unggas = populasi_unggas['tahun'].unique()
        pilihtahun_unggas = st.selectbox("Filter Tahun", pilihantahun_unggas, key='tahun2')

        
        kol1d, kol1e = st.columns(2)
        
        if pilihtahun_unggas:
            tabel_unggas = populasi_unggas[(populasi_unggas['namakec'] == pilihkec)]
            data_unggas = tabel_unggas[(tabel_unggas['tahun'] == pilihtahun_unggas)]
            
            with kol1d:
                bar_unggas2 = px.bar(data_unggas, x='kategori_unggas', y='jumlah', color='kategori_unggas', 
                            color_discrete_sequence=warna_options[pilihwarna])
                bar_unggas2.update_layout(showlegend=False)
                with st.container(border=True):
                    st.plotly_chart(bar_unggas2, use_container_width=True)
            
            with kol1e:
                    pieunggas = px.pie(data_unggas, names='kategori_unggas', values='jumlah', 
                            color_discrete_sequence=warna_options[pilihwarna])
                    pieunggas.update_layout(legend=dict(
                                            orientation="h",  # Horizontal orientation
                                            yanchor="top",    # Anchor the legend to the top
                                            y=-0.2,           # Position the legend below the chart
                                            xanchor="center",  # Center the legend horizontally
                                            x=0.5              # Center the legend at the middle of the chart
                                        ))
                    with st.container(border=True):
                        st.plotly_chart(pieunggas, use_container_width=True)
            
            
    st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-populasi-unggas-di-kota-bandung")    
st.subheader("", divider='rainbow')

# POPULASI TERNAK
with st.expander("POPULASI TERNAK"):
    st.success(f"Jumlah Populasi Ternak di Kecamatan {pilihkec} (Ekor)")
    if pilihkec:
        tabel_ternak = populasi_ternak[(populasi_ternak['namakec'] == pilihkec)]
        tabel_ternak['tahun'] = tabel_ternak['tahun'].astype(str)
        bar_ternak = px.bar(tabel_ternak, x='tahun', y='jumlah', color='kategori_ternak', 
                    color_discrete_sequence=warna_options[pilihwarna])
        bar_ternak.update_layout(legend=dict(
                                orientation="h",  # Horizontal orientation
                                yanchor="top",    # Anchor the legend to the top
                                y=-0.2,           # Position the legend below the chart
                                xanchor="center",  # Center the legend horizontally
                                x=0.5              # Center the legend at the middle of the chart
                            ))
        kolc, kold = st.columns(2)
        with kolc:
            with st.container(border=True):
                st.plotly_chart(bar_ternak, use_container_width=True)

        with kold:
            with st.container(border=True):
                pivot = tabel_ternak.pivot_table(index=['namakec', 'tahun'], columns='kategori_ternak', values='jumlah').reset_index()
                st.dataframe(pivot, hide_index=True, use_container_width=True)
        
        
        populasi_ternak = populasi_ternak.sort_values(by='tahun', ascending=False)
        pilihantahun_ternak = populasi_ternak['tahun'].unique()
        pilihtahun_ternak = st.selectbox("Filter Tahun", pilihantahun_ternak, key='tahun3')

        
        kol1d, kol1e = st.columns(2)
        
        if pilihtahun_ternak:
            tabel_ternak = populasi_ternak[(populasi_ternak['namakec'] == pilihkec)]
            data_ternak = tabel_ternak[(tabel_ternak['tahun'] == pilihtahun_ternak)]
            
            with kol1d:
                bar_ternak2 = px.bar(data_ternak, x='kategori_ternak', y='jumlah', color='kategori_ternak', 
                            color_discrete_sequence=warna_options[pilihwarna])
                bar_ternak2.update_layout(showlegend=False)
                with st.container(border=True):
                    st.plotly_chart(bar_ternak2, use_container_width=True)
            
            with kol1e:
                    pieternak = px.pie(data_ternak, names='kategori_ternak', values='jumlah', 
                            color_discrete_sequence=warna_options[pilihwarna])
                    pieternak.update_layout(legend=dict(
                                            orientation="h",  # Horizontal orientation
                                            yanchor="top",    # Anchor the legend to the top
                                            y=-0.2,           # Position the legend below the chart
                                            xanchor="center",  # Center the legend horizontally
                                            x=0.5              # Center the legend at the middle of the chart
                                        ))
                    with st.container(border=True):
                        st.plotly_chart(pieternak, use_container_width=True)
            
    st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-populasi-ternak-di-kota-bandung")    
st.subheader("", divider='rainbow')

# PRODUKSI TELUR
with st.expander("PRODUKSI TELUR"):
    st.success(f"Jumlah Produksi Telur di Kecamatan {pilihkec} (Kilogram)")
    if pilihkec:
        tabel_telur = produksi_telur[(produksi_telur['namakec'] == pilihkec)]
        tabel_telur['tahun'] = tabel_telur['tahun'].astype(str)
        bar_telur = px.bar(tabel_telur, x='tahun', y='jumlah_telur', 
                    color_discrete_sequence=warna_options[pilihwarna])
        
        kolc, kold = st.columns(2)
        with kolc:
            with st.container(border=True):
                st.plotly_chart(bar_telur, use_container_width=True)

        with kold:
            with st.container(border=True):
                #pivot = tabel_ternak.pivot_table(index=['namakec', 'tahun'], columns='kategori_ternak', values='jumlah').reset_index()
                st.dataframe(tabel_telur, hide_index=True, use_container_width=True)
           
    st.link_button("Sumber Data", url="https://opendata.bandung.go.id/dataset/jumlah-produksi-telur-menurut-kecamatan-di-kota-bandung")    
st.subheader("", divider='rainbow')