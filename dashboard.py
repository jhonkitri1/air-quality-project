import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur konfigurasi halaman
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("☁️ Dashboard Kualitas Udara: Stasiun Aotizhongxin")

# Memuat data yang SUDAH BERSIH
@st.cache_data
def load_data():
    # Membaca file main_data.csv yang sudah dibersihkan dari Jupyter Notebook
    df = pd.read_csv("main_data.csv")
    return df

datasensor = load_data()

# Membuat Sidebar untuk Filter Tahun
st.sidebar.header("Filter Data")
min_year = int(datasensor['year'].min())
max_year = int(datasensor['year'].max())
selected_year = st.sidebar.slider("Pilih Rentang Tahun", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Menerapkan filter ke dataset berdasarkan tahun
filtered_df = datasensor[(datasensor['year'] >= selected_year[0]) & (datasensor['year'] <= selected_year[1])]

# Menampilkan metrik sekilas
st.subheader("Ringkasan Data")
col1, col2 = st.columns(2)
with col1:
    st.metric("Rata-rata PM2.5", f"{filtered_df['PM2.5'].mean():.2f}")
with col2:
    st.metric("Total Data Terekam", len(filtered_df))

# Visualisasi 1: Tren
st.subheader("Tren Rata-rata Polusi PM2.5 per Tahun")
avg_pm25_yearly = filtered_df.groupby('year')['PM2.5'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=avg_pm25_yearly, x='year', y='PM2.5', marker='o', linewidth=2, color='firebrick', ax=ax)
ax.set_xticks(avg_pm25_yearly['year'].unique()) 
st.pyplot(fig)

# Visualisasi 2: Hubungan Cuaca dan Polusi
st.subheader("Pengaruh Cuaca terhadap Polusi PM2.5")
fig2, ax2 = plt.subplots(1, 2, figsize=(15, 5))
sns.scatterplot(data=filtered_df, x='TEMP', y='PM2.5', alpha=0.3, color='steelblue', ax=ax2[0])
ax2[0].set_title('Suhu (Celcius) vs PM2.5')
sns.scatterplot(data=filtered_df, x='RAIN', y='PM2.5', alpha=0.3, color='darkorange', ax=ax2[1])
ax2[1].set_title('Curah Hujan vs PM2.5')
st.pyplot(fig2)

# Visualisasi 3: Proporsi Kategori (Analisis Lanjutan)
st.subheader("Proporsi Kategori Kualitas Udara")
# Menghitung jumlah data berdasarkan Kategori_Udara yang sudah dibuat di notebook
kategori_counts = filtered_df['Kategori_Udara'].value_counts()
fig3, ax3 = plt.subplots(figsize=(6, 6))
ax3.pie(kategori_counts, labels=kategori_counts.index, autopct='%1.1f%%', colors=['coral', 'mediumseagreen', 'gold', 'firebrick'], startangle=90, wedgeprops={'width': 0.4})
st.pyplot(fig3)