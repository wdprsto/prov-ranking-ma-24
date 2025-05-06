import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Distribusi SKD - Ranking MA 2024",
    page_icon="📊",
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
    .metric-container {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3B82F6;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
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

# Title and header
col1, col2 = st.columns([2, 3])
with col1:
    st.title("📊 Distribusi Nilai SKD Per Provinsi")
    st.markdown("""
    Dashboard ini menyajikan analisis mendalam terkait distribusi nilai SKD peserta seleksi CASN Mahkamah Agung 2024 
    berdasarkan provinsi. Anda dapat memfilter data berdasarkan provinsi dan formasi jabatan tertentu.
    """)
with col2:
    st.image('data/SCI_About_banner01@2x.png', use_column_width=True)

# Filters section
st.subheader("🔍 Filter Data")

col1, col2 = st.columns(2)
with col1:
    selected_provinces = st.multiselect(
        "Pilih Provinsi:",
        options=provinces,
        default=["JAKARTA", "JAWA BARAT", "JAWA TENGAH"]
    )

with col2:
    selected_jabatan = st.multiselect(
        "Pilih Formasi Jabatan:",
        options=jabatan_list,
        default=[jabatan_list[0]]
    )

# Convert selected job positions to codes
selected_jabatan_codes = [jabatan_reverse_map.get(job) for job in selected_jabatan]

# Apply filters
if selected_provinces and selected_jabatan:
    filtered_df = df[
        (df["LOKASI_SKB"].isin(selected_provinces)) & 
        (df["jabatan"].isin(selected_jabatan_codes))
    ]
elif selected_provinces:
    filtered_df = df[df["LOKASI_SKB"].isin(selected_provinces)]
elif selected_jabatan:
    filtered_df = df[df["jabatan"].isin(selected_jabatan_codes)]
else:
    filtered_df = df

# Show warning if no data matches filter
if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih. Silakan ubah filter Anda.")
else:
    # Overview statistics section
    st.subheader("📈 Statistik Ringkasan")
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-value">{filtered_df['nilai_skd'].mean():.2f}</div>
                <div class="metric-label">Rata-rata SKD</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-value">{filtered_df['nilai_skd'].median():.2f}</div>
                <div class="metric-label">Median SKD</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-value">{filtered_df['nilai_skd'].max()}</div>
                <div class="metric-label">Nilai SKD Tertinggi</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-container">
                <div class="metric-value">{filtered_df['nilai_skd'].min()}</div>
                <div class="metric-label">Nilai SKD Terendah</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # SKD Distribution by Province
    st.sugibheader("📊 Distribusi Nilai SKD berdasarkan Provinsi")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Histogram", "Boxplot", "Komponen SKD"])
    
    with tab2:
        # Boxplot for distribution comparison
        if len(filtered_df['LOKASI_SKB'].unique()) > 1:
            # Calculate median for sorting
            province_median = filtered_df.groupby('LOKASI_SKB')['nilai_skd'].median().sort_values(ascending=False)
            ordered_provinces = province_median.index.tolist()
            
            fig = px.box(
                filtered_df,
                x='LOKASI_SKB',
                y='nilai_skd',
                color='LOKASI_SKB',
                category_orders={"LOKASI_SKB": ordered_provinces},
                title="Perbandingan Distribusi Nilai SKD antar Provinsi",
                labels={'LOKASI_SKB': 'Provinsi', 'nilai_skd': 'Nilai SKD'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Insight:** 
            Boxplot menunjukkan perbandingan distribusi nilai SKD di setiap provinsi. Kotak menunjukkan rentang nilai dari kuartil 1 hingga kuartil 3, 
            dengan garis di tengah sebagai nilai median. Titik-titik di luar kotak menunjukkan outlier atau nilai yang jauh dari distribusi umum.
            Provinsi dengan boxplot lebih tinggi menunjukkan performa SKD yang lebih baik secara keseluruhan.
            """)
        else:
            st.info("Pilih lebih dari satu provinsi untuk melihat perbandingan boxplot.")
    
    with tab1:
        # Histogram analysis with province selector
        selected_province_hist = st.selectbox(
            "Pilih Provinsi untuk Histogram:",
            options=filtered_df['LOKASI_SKB'].unique()
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Add bin size option
            bins = st.slider("Jumlah Bin:", min_value=5, max_value=30, value=15)
            
            # Province statistics
            province_data = filtered_df[filtered_df['LOKASI_SKB'] == selected_province_hist]
            
            st.markdown("##### Statistik SKD Provinsi")
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-value">{len(province_data)}</div>
                    <div class="metric-label">Jumlah Peserta Lulus</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-value">{province_data['nilai_skd'].mean():.2f}</div>
                    <div class="metric-label">Rata-rata SKD</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-value">{province_data['nilai_skd'].std():.2f}</div>
                    <div class="metric-label">Standar Deviasi</div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col2:
            # Create histogram
            fig = px.histogram(
                province_data,
                x='nilai_skd',
                nbins=bins,
                title=f"Distribusi Nilai SKD di {selected_province_hist}",
                color_discrete_sequence=['#3B82F6'],
                labels={'nilai_skd': 'Nilai SKD', 'count': 'Jumlah Peserta'}
            )
            
            # Add mean line
            mean_value = province_data['nilai_skd'].mean()
            fig.add_vline(
                x=mean_value, 
                line_dash="dash", 
                line_color="red",
                annotation_text=f"Rata-rata: {mean_value:.2f}"
            )
            
            # Add passing threshold if available
            fig.add_vline(
                x=301, 
                line_dash="dash", 
                line_color="green",
                annotation_text="Passing Grade: 301"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Analysis of SKD components (TWK, TIU, TKP)
        st.markdown("##### Analisis Komponen SKD (TWK, TIU, TKP)")
        
        # Allow province comparison
        comp_provinces = st.multiselect(
            "Pilih Provinsi untuk Perbandingan Komponen:",
            options=filtered_df['LOKASI_SKB'].unique(),
            default=filtered_df['LOKASI_SKB'].unique()[:min(3, len(filtered_df['LOKASI_SKB'].unique()))]
        )
        
        if comp_provinces:
            # Calculate average components by province
            component_avg = filtered_df[filtered_df['LOKASI_SKB'].isin(comp_provinces)].groupby('LOKASI_SKB')[['twk', 'tiu', 'tkp']].mean().reset_index()
            
            # Create grouped bar chart
            fig = px.bar(
                component_avg,
                x='LOKASI_SKB',
                y=['twk', 'tiu', 'tkp'],
                barmode='group',
                title="Perbandingan Rata-rata Komponen SKD antar Provinsi",
                labels={
                    'LOKASI_SKB': 'Provinsi',
                    'value': 'Nilai Rata-rata',
                    'variable': 'Komponen'
                },
                color_discrete_map={
                    'twk': '#3B82F6',  # Blue for TWK
                    'tiu': '#10B981',  # Green for TIU
                    'tkp': '#F59E0B'   # Amber for TKP
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)


        # Job Position Analysis in Selected Provinces
        st.subheader("📊 Analisis Formasi Jabatan di Provinsi Terpilih")
        
        # Show only if we have multiple job positions
        if len(selected_jabatan) > 1 or (not selected_jabatan and len(filtered_df['jabatan'].unique()) > 1):
            # Get job statistics
            job_stats = filtered_df.groupby('jabatan').agg({
                'nilai_skd': ['mean', 'median', 'min', 'max', 'count']
            }).reset_index()
            
            # Flatten the MultiIndex columns
            job_stats.columns = ['jabatan', 'mean', 'median', 'min', 'max', 'count']
            
            # Map job codes to full names for display
            job_stats['jabatan_full'] = job_stats['jabatan'].map(jabatan_map)
            
            # Sort by mean score
            job_stats = job_stats.sort_values('mean', ascending=False)
            
            # Create horizontal bar chart
            fig = px.bar(
                job_stats,
                y='jabatan_full',
                x='mean',
                error_x=job_stats['max'] - job_stats['mean'],
                labels={
                    'jabatan_full': 'Formasi Jabatan',
                    'mean': 'Rata-rata Nilai SKD',
                    'count': 'Jumlah Pelamar'
                },
                title="Perbandingan Nilai SKD antar Formasi Jabatan di Provinsi Terpilih",
                color='count',
                color_continuous_scale='Viridis',
                orientation='h',
                height=500
            )
            
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Display summary table
            st.markdown("##### Tabel Ringkasan Nilai SKD per Jabatan")
            
            # Prepare table data
            table_data = job_stats[['jabatan_full', 'mean', 'median', 'min', 'max', 'count']]
            table_data.columns = ['Formasi Jabatan', 'Rata-rata', 'Median', 'Minimum', 'Maksimum', 'Jumlah Pelamar']
            
            # Format numeric columns
            for col in ['Rata-rata', 'Median', 'Minimum', 'Maksimum']:
                table_data[col] = table_data[col].round(2)
            
            # Display table
            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Pilih lebih dari satu formasi jabatan untuk melihat perbandingan nilai SKD antar formasi.")
        
   
# Footer
st.markdown("""
---
Dashboard Distribusi SKD Mahkamah Agung 2024 | Data: Mahkamah Agung 2024
""") 