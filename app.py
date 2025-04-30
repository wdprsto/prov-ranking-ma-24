import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO
import statsmodels

# Page configuration
st.set_page_config(
    page_title="Ranking Mahkamah Agung 2024",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS to reduce margins and make the app more minimalist
st.markdown("""
<style>
    .block-container {
        padding-top: 3.5rem;
        padding-bottom: 2rem;
    }
    .main > div {
        padding-left: 3.5rem;
        padding-right: 3.5rem;
    }
    h1, h2, h3 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stAlert {
        padding: 0.5rem !important;
    }
    div[data-testid="stForm"] {
        border: 0px;
        padding: 0px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/recap_hasil_akhir_ma_24.csv")
    return df

# Load province and jabatan lists
@st.cache_data
def load_lists():
    with open("data/province_list.txt", "r") as f:
        provinces = [line.strip() for line in f.readlines()]
    
    with open("data/jabatan_list.txt", "r") as f:
        jabatan_list = [line.strip() for line in f.readlines()]
    
    jabatan_map = {
        'apkaap': 'ANALIS PENGELOLAAN KEUANGAN APBN AHLI PERTAMA',
        'app': 'ANALIS PERKARA PERADILAN',
        'aap': 'ARSIPARIS AHLI PERTAMA',
        'ap': 'AUDITOR AHLI PERTAMA',
        'at': 'AUDITOR TERAMPIL',
        'dgap': 'DOKTER GIGI AHLI PERTAMA',
        'dh': 'DOKUMENTALIS HUKUM',
        'pksti': 'PENATA KELOLA SISTEM DAN TEKNOLOGI INFORMASI',
        'pk': 'PENATA KEPROTOKOLAN',
        'ptpap': 'PENGEMBANG TEKNOLOGI PEMBELAJARAN AHLI PERTAMA',
        'pt': 'PERAWAT TERAMPIL',
        'tsp': 'TEKNISI SARANA DAN PRASARANA',
        'tgmt': 'TERAPIS GIGI DAN MULUT TERAMPIL',
        'wap': 'WIDYAISWARA AHLI PERTAMA'
    }
    
    return provinces, jabatan_list, jabatan_map

# Prepare data
df = load_data()
provinces, jabatan_list, jabatan_map = load_lists()

# Generate reverse map for dropdown display
jabatan_reverse_map = {v: k for k, v in jabatan_map.items()}

# st.title("Ranking CAT per Provinsi 2024")
# Title and hero section
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("""
    ### 🏛️ Data Integrasi SKD+SKB Mahkamah Agung
    
    **Data ini berisi nilai integrasi SKD+SKB hasil ujian CAT instansi Mahkamah Agung. Dengan menginputkan nama formasi, nilai dan asal provinsi, kamu akan mengetahui ranking kamu di provinsi tersebut.**
    
    Gunakan formulir di bawah untuk melihat posisi ranking kamu!
    """)

with col2:
    st.image('data/SCI_About_banner01@2x.png', use_column_width=True)

# Documentation section
with st.expander("⚠️ Peringatan"):
    st.markdown("""
    **Disclaimer:**
    
    Data domisili diasumsikan sama dengan lokasi pelaksanaan SKB peserta. Apabila ada usulan perubahan, silahkan hubungi pengembang.
    """)
    
# Input form
st.markdown("### 📝 Masukkan Data Anda")

col1, col2, col3 = st.columns(3)

with col1:
    selected_jabatan = st.selectbox(
        "Pilih Formasi Jabatan:",
        options=jabatan_list,
        # format_func=lambda x: f"{jabatan_reverse_map.get(x, '')} - {x}" if x in jabatan_reverse_map.keys() else x
    )

with col2:
    selected_province = st.selectbox(
        "Pilih Provinsi (Lokasi SKB):",
        options=provinces
    )

with col3:
    nilai_akhir = st.number_input(
        "Masukkan Nilai Akhir Anda:",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=0.01,
        format="%.2f"
    )

# Process data when user clicks the button
if st.button("Cek Ranking Saya", type="primary"):
    # Filter the dataframe based on jabatan and province
    filtered_df = df[(df['jabatan'] == jabatan_reverse_map[selected_jabatan]) & (df['LOKASI_SKB'] == selected_province)]
    
    if filtered_df.empty:
        st.warning(f"Tidak ada data untuk formasi {selected_jabatan} di provinsi {selected_province}.")
    else:
        # Calculate user's rank based on nilai_akhir
        total_peserta = len(filtered_df)
        user_rank = (filtered_df['nilai_akhir'] > nilai_akhir).sum() + 1
        kuota = filtered_df['kuota_provinsi'].iloc[0] if not filtered_df['kuota_provinsi'].isna().all() else 0
        
        # Prepare result display
        st.markdown("### 📊 Hasil Analisis")
        
        # Create columns for displaying results
        col1, col2 = st.columns(2)
        
        # Display user ranking and status
        with col1:
            st.metric("Ranking Anda", f"{user_rank} dari {total_peserta}")
            
            if kuota > 0:
                if user_rank <= kuota:
                    st.success(f"Selamat! Berdasarkan nilai, Anda berada di dalam kuota ({int(kuota)}) untuk provinsi {selected_province}! 🎉")
                else:
                    st.error(f"Maaf, ranking Anda berada di luar kuota. Kuota untuk {selected_province} adalah {kuota}.")
            else:
                st.info("Kuota untuk provinsi ini tidak tersedia dalam data.")
        
        # Show top performers
        with col2:
            # Sort dataframe by nilai_akhir in descending order
            top_df = filtered_df.sort_values(by='nilai_akhir', ascending=False)
            
            # Get top 3 and user position
            top_3 = top_df.head(3)
            
            st.markdown("#### Top Performers di Provinsi Anda")
            
            # Create a table for top performers
            leaderboard = pd.DataFrame({
                'Ranking': range(1, len(top_3) + 1),
                'Nama': top_3['nama'].values,
                'Nilai Akhir': top_3['nilai_akhir'].values.round(3)
            })
            
            st.dataframe(leaderboard, use_container_width=True, hide_index=True)
            
            # If user is not in top 3, show their position
            if user_rank > 3:
                # Display user's expected position (hypothetical)
                st.markdown("...")
                user_position = pd.DataFrame({
                    'Ranking': [user_rank],
                    'Nama': ["Anda"],
                    'Nilai Akhir': [nilai_akhir]
                })
                st.dataframe(user_position, use_container_width=True, hide_index=True)
        
        # Additional visualization and analysis
        st.markdown("### 📈 Analisis Tambahan")
        
        # tab1, tab2 = st.tabs(["Distribusi Nilai", "Perbandingan Komponen"])
        # tab1 = st.tabs(['Distribusi Nilai',''])

        # with tab1:
            # Distribution of nilai_akhir in the province for the selected jabatan
        fig = px.histogram(
            filtered_df, 
            x='nilai_akhir',
            nbins=20,
            title=f"Distribusi Nilai Akhir untuk {selected_jabatan} di {selected_province}",
            labels={'nilai_akhir': 'Nilai Akhir', 'count': 'Jumlah Peserta'},
            color_discrete_sequence=['#3B82F6']
        )
        
        # Add a vertical line for user's nilai_akhir
        fig.add_vline(x=nilai_akhir, line_dash="dash", line_color="red", annotation_text="Nilai Anda")
        
        # If there's a kuota, add a reference line for the cut-off score
        if kuota > 0 and kuota < len(filtered_df):
            cutoff_score = filtered_df.sort_values('nilai_akhir', ascending=False).iloc[int(kuota)-1]['nilai_akhir']
            fig.add_vline(x=cutoff_score, line_dash="dash", line_color="green", annotation_text="Batas Kuota")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        st.markdown("#### Statistik Nilai")
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.metric("Nilai Tertinggi", f"{filtered_df['nilai_akhir'].max():.3f}")
        
        with stats_col2:
            st.metric("Nilai Rata-rata", f"{filtered_df['nilai_akhir'].mean():.3f}")
        
        with stats_col3:
            st.metric("Nilai Terendah", f"{filtered_df['nilai_akhir'].min():.3f}")
        
        with stats_col4:
            if kuota > 0 and kuota < len(filtered_df):
                st.metric("Nilai Batas Kuota", f"{cutoff_score:.3f}")
            else:
                st.metric("Nilai Batas Kuota", "N/A")
        
        # with tab2:
        #     if 'nilai_skd' in filtered_df.columns and 'nilai_skb' in filtered_df.columns:
        #         # Create synthetic user data for comparison
        #         user_data = {
        #             'nama': ['Anda'],
        #             'nilai_akhir': [nilai_akhir],
        #             'nilai_skd': [filtered_df['nilai_skd'].mean()],  # We don't have user's SKD, use mean as placeholder
        #             'nilai_skb': [filtered_df['nilai_skb'].mean()]   # We don't have user's SKB, use mean as placeholder
        #         }
        #         user_df = pd.DataFrame(user_data)
                
        #         # Get top 5 for comparison
        #         comparison_df = pd.concat([
        #             top_df.head(5)[['nama', 'nilai_akhir', 'nilai_skd', 'nilai_skb']],
        #             user_df
        #         ])
                
        #         # Create a bar chart comparing nilai_akhir
        #         fig1 = px.bar(
        #             comparison_df,
        #             x='nama',
        #             y='nilai_akhir',
        #             title="Perbandingan Nilai Akhir",
        #             labels={'nama': 'Peserta', 'nilai_akhir': 'Nilai Akhir'},
        #             color_discrete_sequence=['#3B82F6'],
        #             text_auto='.3f'
        #         )
        #         st.plotly_chart(fig1, use_container_width=True)
                
        #         # Create a components breakdown
        #         fig2 = px.bar(
        #             comparison_df,
        #             x='nama',
        #             y=['nilai_skd', 'nilai_skb'],
        #             title="Komponen Nilai (SKD dan SKB)",
        #             labels={'nama': 'Peserta', 'value': 'Nilai', 'variable': 'Komponen'},
        #             color_discrete_sequence=['#3B82F6', '#10B981'],
        #             barmode='group'
        #         )
        #         st.plotly_chart(fig2, use_container_width=True)
                
        #         st.info("""
        #         **Catatan:** Komponen nilai SKD dan SKB untuk "Anda" merupakan perkiraan berdasarkan nilai rata-rata peserta lain, 
        #         karena Anda hanya memasukkan nilai akhir.
        #         """)
        #     else:
        #         st.warning("Data komponen nilai tidak lengkap untuk analisis ini.")

# Documentation section
with st.expander("ℹ️ Tentang Dashboard Ini"):
    st.markdown("""
    ### Informasi Dashboard
    
    Dashboard ini menampilkan data ranking peserta seleksi CASN Mahkamah Agung 2024 berdasarkan nilai integrasi SKD+SKB.
    
    **Cara Penggunaan:**
    
    1. Pilih formasi jabatan yang Anda lamar
    2. Pilih provinsi lokasi SKB Anda
    3. Masukkan nilai akhir Anda
    4. Klik tombol "Cek Ranking Saya"
    
    **Fitur Dashboard:**
    
    - Menampilkan ranking Anda di antara seluruh peserta dengan formasi dan provinsi yang sama
    - Menunjukkan status kelulusan berdasarkan kuota yang tersedia
    - Menampilkan peserta dengan nilai tertinggi di formasi dan provinsi Anda
    - Visualisasi distribusi nilai untuk analisis perbandingan
    
    **Disclaimer:**
    
    Dashboard ini menggunakan data dari Mahkamah Agung 2024. Hasil analisis bersifat informatif dan tidak menggantikan pengumuman resmi dari instansi terkait.
    """)

# Footer
st.markdown("""
---
Dashboard dibuat menggunakan Streamlit | Data: Mahkamah Agung 2024
""") 