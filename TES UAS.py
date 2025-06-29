import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 Analisis Produksi dan Konsumsi Kopi Dunia (1990-2020)")

path_prod = r"./Coffee_production.csv"
path_cons = r"./Coffee_domestic_consumption.csv"

df_prod = pd.read_csv(path_prod)
df_cons = pd.read_csv(path_cons)

tahun_cols_prod = df_prod.columns[2:-1]
df_prod_long = df_prod.melt(
    id_vars=['Country'],
    value_vars=tahun_cols_prod,
    var_name='Year',
    value_name='Production (000 bags)'
)

tahun_cols_cons = df_cons.columns[2:-1]
df_cons_long = df_cons.melt(
    id_vars=['Country'],
    value_vars=tahun_cols_cons,
    var_name='Year',
    value_name='Domestic Consumption (000 bags)'
)

df_prod_long['Year'] = df_prod_long['Year'].str[:4].astype(int)
df_cons_long['Year'] = df_cons_long['Year'].str[:4].astype(int)

st.header("🔍 Filter Negara dan Tahun")

negara_list = sorted(list(set(df_prod_long['Country']).intersection(set(df_cons_long['Country']))))
selected_negara = st.selectbox("Pilih Negara:", negara_list)

min_year = df_prod_long['Year'].min()
max_year = df_prod_long['Year'].max()

year_range = st.slider("Pilih Rentang Tahun:", int(min_year), int(max_year), (int(min_year), int(max_year)))

df_prod_filtered = df_prod_long[
    (df_prod_long['Country'] == selected_negara) &
    (df_prod_long['Year'] >= year_range[0]) &
    (df_prod_long['Year'] <= year_range[1])
]

df_cons_filtered = df_cons_long[
    (df_cons_long['Country'] == selected_negara) &
    (df_cons_long['Year'] >= year_range[0]) &
    (df_cons_long['Year'] <= year_range[1])
]

st.header(f"📈 Grafik Produksi vs Konsumsi Kopi di {selected_negara}")

fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=df_prod_filtered, x='Year', y='Production (000 bags)', marker='o', label='Produksi', ax=ax)
sns.lineplot(data=df_cons_filtered, x='Year', y='Domestic Consumption (000 bags)', marker='s', label='Konsumsi', ax=ax)

ax.set_xlabel('Tahun')
ax.set_ylabel('Jumlah (000 bags)')
ax.set_title(f'Produksi dan Konsumsi Kopi di {selected_negara} ({year_range[0]} - {year_range[1]})')
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.header("📝 Analisis Total")

total_prod = df_prod_filtered['Production (000 bags)'].sum()
total_cons = df_cons_filtered['Domestic Consumption (000 bags)'].sum()

st.write(f"**Total Produksi:** {total_prod:,.0f} ribu bags")
st.write(f"**Total Konsumsi:** {total_cons:,.0f} ribu bags")

if total_prod > total_cons:
    st.success(f"✅ Produksi lebih tinggi dari konsumsi di {selected_negara}.")
else:
    st.warning(f"⚠️ Konsumsi lebih tinggi dari produksi di {selected_negara}.")

st.caption("📌 Sumber Data: International Coffee Organization (ICO) - Kaggle Dataset")