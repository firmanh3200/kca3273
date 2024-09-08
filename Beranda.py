import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly_express as px
import plotly.graph_objs as go
#import openpyxl

st.set_page_config(layout='wide')

st.title("Statistik Kota Bandung")
st.subheader("", divider='rainbow')

def kependudukan():
    with st.container(border=True):
        st.subheader("Kependudukan")
        penduduk_kabkot_umur = pd.read_excel('data/proyeksi-kabkot-umur.xlsx')
        penduduk_kabkot_umur['Tahun'] = penduduk_kabkot_umur['Tahun'].astype(str)
        
        penduduk_kabkot_jk = pd.read_excel('data/proyeksi-kabkot-jk.xlsx')
        penduduk_kabkot_jk['Tahun'] = penduduk_kabkot_jk['Tahun'].astype(int)

### KABKOT        
        penduduk_kabkotjk = penduduk_kabkot_jk.drop(penduduk_kabkot_jk[penduduk_kabkot_jk['Wilayah'] == 'JAWA BARAT'].index)
        
        kabkotjk = penduduk_kabkotjk.melt(id_vars=['Tahun', 'Wilayah'], value_vars=['Laki-laki', 'Perempuan'], 
                                                    var_name='Jenis Kelamin', value_name='Penduduk')
                    
        st.subheader("Penduduk Jawa Barat menurut Kabupaten/ Kota, 2020 - 2045")
        kabkot1 = st.container(border=True)
        with kabkot1:
            penduduk_kabkot_umur['Laki-laki'] = penduduk_kabkot_umur['Laki-laki'] * -1
           
            tahun_terunik = penduduk_kabkot_jk['Tahun'].unique()
            tahun_min = int(tahun_terunik.min())
            tahun_max = int(tahun_terunik.max())

            tahun_terpilih = st.slider('Filter Tahun', tahun_min, tahun_max, key='filtertahun1')
                           
            
### TREEMAP TOTAL KABKOT          
            with st.container(border=True):
                st.info(f"Proyeksi Penduduk Kabupaten Kota (Jiwa), {tahun_terpilih}")
                
                fig1f = px.treemap(kabkotjk[kabkotjk['Tahun'] == tahun_terpilih],
                                    path=['Wilayah', 'Jenis Kelamin'], values='Penduduk')
                st.plotly_chart(fig1f)
### PIE TOTAL KABKOT
            with st.container(border=True):
                st.info(f"Sebaran Penduduk Kabupaten Kota (Jiwa), {tahun_terpilih}")
                penduduk_kabkotjk = penduduk_kabkot_jk.drop(penduduk_kabkot_jk[penduduk_kabkot_jk['Wilayah'] == 'JAWA BARAT'].index)
    
                fig1g = px.pie(penduduk_kabkotjk[penduduk_kabkotjk['Tahun'] == tahun_terpilih],
                                names='Wilayah', values='Total')
                st.plotly_chart(fig1g)

        st.subheader("", divider='blue')
### KABKOT JENIS KELAMIN
        kabkot2 = st.container(border=True)
        with kabkot2:            
            kabkot_terpilih = st.selectbox("Filter Kabupaten/Kota", penduduk_kabkot_umur.Wilayah.unique())
        
            with st.container(border=True, height=550):
                st.info(f"PIRAMIDA PENDUDUK {kabkot_terpilih}")
                            
                fig1e = px.bar(penduduk_kabkot_umur[(penduduk_kabkot_umur['Wilayah'] == kabkot_terpilih)], 
                            x=['Laki-laki', 'Perempuan'], y='Umur', labels={'variable':''},
                                orientation='h', animation_frame='Tahun', animation_group='Umur',
                                color_discrete_map={'Laki-laki':'brown', 'Perempuan':'orange'})
                # Menempatkan legenda di bawah tengah
                fig1e.update_layout(
                    xaxis_title="",
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5
                    )
                )
                if kabkot_terpilih:
                    st.plotly_chart(fig1e)

            with st.container(border=True, height=550):
                st.info(f"PENDUDUK {kabkot_terpilih} MENURUT JENIS KELAMIN")
                
                tahun_terpilih2 = st.slider('Filter Tahun', tahun_min, tahun_max, key='filtertahun2')
                
                fig1h = px.pie(kabkotjk[(kabkotjk['Wilayah'] == kabkot_terpilih) & (kabkotjk['Tahun'] == tahun_terpilih2)], 
                            names='Jenis Kelamin', values='Penduduk', hover_data=['Wilayah', 'Tahun'], color='Jenis Kelamin',
                            color_discrete_map={'Laki-laki':'brown', 'Perempuan':'orange'}, height=375)
                fig1h.update_layout(
                    xaxis_title="",
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5
                    )
                )
                st.plotly_chart(fig1h)
        
    with st.expander("UNDUH SUMBER DATA"):
        tabel, publikasi, metadata, standardata = st.tabs(['TABEL', 'PUBLIKASI', 'METADATA', 'STANDAR DATA'])
        with tabel:
            st.link_button("Buka Tautan", "https://jabar.bps.go.id/subject/12/kependudukan.html#subjekViewTab3")
        with publikasi:
            st.link_button("Buka Tautan", "https://jabar.bps.go.id/publication.html")
        with metadata:
            st.link_button("Buka Tautan", "https://sirusa.web.bps.go.id/metadata/")
        with standardata:
            st.link_button("Buka Tautan", "https://indah.bps.go.id/standar-data-statistik-nasional")
        
    return kabkot1
kabkot1 = kependudukan()
