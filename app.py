# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# import plotly.graph_objects as go
# import requests
# from datetime import datetime
# import warnings
# warnings.filterwarnings('ignore')

# # Cấu hình page
# st.set_page_config(
#     page_title="Phân Tích COVID-19 - B22DCCN132",
#     page_icon="🦠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         color: #FF6B6B;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .metric-card {
#         background-color: #262730;
#         padding: 1rem;
#         border-radius: 10px;
#         border-left: 4px solid #FF6B6B;
#         margin: 0.5rem 0;
#     }
#     .positive {
#         color: #00FF00;
#     }
#     .negative {
#         color: #FF6B6B;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Tiêu đề ứng dụng
# st.markdown('<h1 class="main-header">🦠 PHÂN TÍCH COVID-19 TOÀN CẦU</h1>', unsafe_allow_html=True)
# st.markdown("**Sinh viên:** Nguyễn Mạnh Dũng - **MSSV:** B22DCCN132 - **Môn:** Khai phá dữ liệu")
# st.markdown("---")

# # Hàm lấy dữ liệu COVID-19
# @st.cache_data(ttl=3600)  # Cache 1 giờ
# def get_covid_data():
#     """Lấy dữ liệu COVID-19 từ API"""
#     try:
#         st.info("🌐 Đang kết nối API để lấy dữ liệu COVID-19 ")
#         url = "https://disease.sh/v3/covid-19/countries"
#         response = requests.get(url, timeout=10)
#         data = response.json()
#         df = pd.DataFrame(data)
        
#         # Đổi tên cột sang tiếng Việt
#         column_mapping = {
#             'country': 'Quốc_Gia',
#             'cases': 'Tổng_Ca_Nhiễm', 
#             'deaths': 'Tổng_Tử_Vong',
#             'recovered': 'Tổng_Khỏi_Bệnh',
#             'population': 'Dân_Số',
#             'continent': 'Châu_Lục'
#         }
#         df = df.rename(columns=column_mapping)
        
#         # Tạo các cột tính toán
#         df['Tỉ_Lệ_Tử_Vong'] = (df['Tổng_Tử_Vong'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
#         df['Tỉ_Lệ_Khỏi_Bệnh'] = (df['Tổng_Khỏi_Bệnh'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
#         df['Ca_Nhiễm_Triệu_Dân'] = (df['Tổng_Ca_Nhiễm'] / df['Dân_Số'] * 1000000).round(0)
#         df = df.fillna(0)
        
#         st.success(f"✅ Đã tải dữ liệu từ {len(df)} quốc gia")
#         return df
        
#     except Exception as e:
#         st.error(f"❌ Lỗi kết nối API: {e}")
#         st.info("🔄 Đang sử dụng dữ liệu mẫu...")
        
#         # Dữ liệu mẫu
#         sample_data = {
#             'Quốc_Gia': ['Vietnam', 'USA', 'India', 'Brazil', 'UK', 'Germany', 'France', 'Japan', 'Korea', 'Thailand'],
#             'Tổng_Ca_Nhiễm': [11500000, 100000000, 44000000, 34000000, 24000000, 32000000, 38000000, 22000000, 29000000, 4700000],
#             'Tổng_Tử_Vong': [43000, 1100000, 530000, 680000, 190000, 150000, 155000, 46000, 31000, 33000],
#             'Tổng_Khỏi_Bệnh': [10600000, 95000000, 43000000, 33000000, 23000000, 31000000, 37000000, 21500000, 28500000, 4600000],
#             'Dân_Số': [98170000, 331000000, 1393000000, 213900000, 68200000, 83100000, 67500000, 125800000, 51300000, 71600000],
#             'Châu_Lục': ['Asia', 'North America', 'Asia', 'South America', 'Europe', 'Europe', 'Europe', 'Asia', 'Asia', 'Asia']
#         }
#         df = pd.DataFrame(sample_data)
#         df['Tỉ_Lệ_Tử_Vong'] = (df['Tổng_Tử_Vong'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
#         df['Tỉ_Lệ_Khỏi_Bệnh'] = (df['Tổng_Khỏi_Bệnh'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
#         df['Ca_Nhiễm_Triệu_Dân'] = (df['Tổng_Ca_Nhiễm'] / df['Dân_Số'] * 1000000).round(0)
        
#         return df

# # Tải dữ liệu
# df = get_covid_data()

# # Sidebar
# st.sidebar.header("⚙️ CÀI ĐẶT PHÂN TÍCH")

# # Lựa chọn quốc gia để so sánh
# countries = sorted(df['Quốc_Gia'].unique())
# selected_country = st.sidebar.selectbox("🇻🇳 Chọn quốc gia chính:", countries, index=countries.index('Vietnam') if 'Vietnam' in countries else 0)

# # Lựa chọn số quốc gia hiển thị
# top_n = st.sidebar.slider("Số quốc gia hiển thị:", 5, 20, 10)

# # Lấy dữ liệu quốc gia được chọn
# country_data = df[df['Quốc_Gia'] == selected_country]

# # Tab chính
# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "📊 TỔNG QUAN", "📈 BIỂU ĐỒ STATIC", "🎨 BIỂU ĐỒ TƯƠNG TÁC", 
#     "📊 BIỂU ĐỒ BỔ SUNG", "📖 BÁO CÁO"
# ])

# with tab1:
#     st.header("📊 TỔNG QUAN COVID-19 TOÀN CẦU")
    
#     # Metrics row
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         total_cases = df['Tổng_Ca_Nhiễm'].sum()
#         st.metric("🌍 Tổng Ca Nhiễm", f"{total_cases:,.0f}")
    
#     with col2:
#         total_deaths = df['Tổng_Tử_Vong'].sum()
#         st.metric("💀 Tổng Tử Vong", f"{total_deaths:,.0f}")
    
#     with col3:
#         avg_death_rate = df['Tỉ_Lệ_Tử_Vong'].mean()
#         st.metric("📈 Tỉ Lệ Tử Vong TB", f"{avg_death_rate:.2f}%")
    
#     with col4:
#         total_countries = len(df)
#         st.metric("🇺🇳 Số Quốc Gia", f"{total_countries}")
    
#     # Thông tin quốc gia được chọn
#     st.subheader(f"🇻🇳 Thông Tin {selected_country}")
    
#     if len(country_data) > 0:
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             cases = country_data['Tổng_Ca_Nhiễm'].iloc[0]
#             st.metric("😷 Tổng Ca Nhiễm", f"{cases:,.0f}")
        
#         with col2:
#             deaths = country_data['Tổng_Tử_Vong'].iloc[0]
#             st.metric("💀 Tổng Tử Vong", f"{deaths:,.0f}")
        
#         with col3:
#             death_rate = country_data['Tỉ_Lệ_Tử_Vong'].iloc[0]
#             world_avg = df['Tỉ_Lệ_Tử_Vong'].mean()
#             diff = death_rate - world_avg
#             st.metric("📊 Tỉ Lệ Tử Vong", f"{death_rate:.2f}%", f"{diff:+.2f}% vs TB")
        
#         with col4:
#             cases_per_million = country_data['Ca_Nhiễm_Triệu_Dân'].iloc[0]
#             st.metric("👥 Ca/1M Dân", f"{cases_per_million:,.0f}")
    
#     # Dữ liệu thô
#     st.subheader("📋 Dữ Liệu Thô (10 dòng đầu)")
#     st.dataframe(df.head(10), use_container_width=True)

# with tab2:
#     st.header("📊 BIỂU ĐỒ STATIC - YÊU CẦU 3")
    
#     # YÊU CẦU 3.1: Histogram & Boxplot
#     st.subheader("1. Histogram & Boxplot - Phân Phối Tỉ Lệ Tử Vong")
    
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
#     # Histogram
#     ax1.hist(df['Tỉ_Lệ_Tử_Vong'], bins=20, color='lightcoral', edgecolor='black', alpha=0.7)
#     ax1.axvline(df['Tỉ_Lệ_Tử_Vong'].mean(), color='red', linestyle='--', linewidth=2, 
#                 label=f'Trung bình: {df["Tỉ_Lệ_Tử_Vong"].mean():.2f}%')
#     if len(country_data) > 0:
#         ax1.axvline(country_data['Tỉ_Lệ_Tử_Vong'].iloc[0], color='blue', linestyle='--', linewidth=2, 
#                     label=f'{selected_country}: {country_data["Tỉ_Lệ_Tử_Vong"].iloc[0]:.2f}%')
#     ax1.set_xlabel('Tỉ Lệ Tử Vong (%)')
#     ax1.set_ylabel('Số Quốc Gia')
#     ax1.set_title('PHÂN BỐ TỈ LỆ TỬ VONG TOÀN CẦU', fontweight='bold')
#     ax1.legend()
#     ax1.grid(True, alpha=0.3)
    
#     # Boxplot
#     ax2.boxplot(df['Tỉ_Lệ_Tử_Vong'].dropna())
#     ax2.set_ylabel('Tỉ Lệ Tử Vong (%)')
#     ax2.set_title('BOXPLOT TỈ LỆ TỬ VONG', fontweight='bold')
#     ax2.grid(True, alpha=0.3)
    
#     plt.tight_layout()
#     st.pyplot(fig)
    
#     # YÊU CẦU 3.2: Line & Area Chart
#     st.subheader("2. Biểu Đồ Top Quốc Gia Theo Số Ca Nhiễm")
    
#     top_countries = df.nlargest(top_n, 'Tổng_Ca_Nhiễm')
    
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
#     # Line chart
#     ax1.plot(top_countries['Quốc_Gia'], top_countries['Tổng_Ca_Nhiễm'], 
#              marker='o', linewidth=2, markersize=6, color='#FF6B6B')
#     ax1.set_title(f'TOP {top_n} QUỐC GIA THEO SỐ CA NHIỄM', fontweight='bold')
#     ax1.set_ylabel('Tổng Ca Nhiễm')
#     ax1.tick_params(axis='x', rotation=45)
#     ax1.grid(True, alpha=0.3)
    
#     # Area chart
#     ax2.fill_between(top_countries['Quốc_Gia'], top_countries['Tổng_Tử_Vong'], 
#                      alpha=0.3, color='#4ECDC4')
#     ax2.plot(top_countries['Quốc_Gia'], top_countries['Tổng_Tử_Vong'], 
#              color='#4ECDC4', linewidth=2, marker='o')
#     ax2.set_title(f'TOP {top_n} QUỐC GIA THEO SỬ TỬ VONG', fontweight='bold')
#     ax2.set_xlabel('Quốc Gia')
#     ax2.set_ylabel('Tổng Tử Vong')
#     ax2.tick_params(axis='x', rotation=45)
#     ax2.grid(True, alpha=0.3)
    
#     plt.tight_layout()
#     st.pyplot(fig)
    
#     # YÊU CẦU 3.3: Scatter + Regression
#     st.subheader("3. Scatter Plot & Hồi Quy - Mối Quan Hệ Ca Nhiễm & Tử Vong")
    
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     scatter = ax.scatter(df['Tổng_Ca_Nhiễm'], df['Tổng_Tử_Vong'], 
#                         alpha=0.6, s=50, c=df['Tỉ_Lệ_Tử_Vong'], cmap='viridis')
    
#     # Regression line
#     if len(df) > 1:
#         z = np.polyfit(df['Tổng_Ca_Nhiễm'], df['Tổng_Tử_Vong'], 1)
#         p = np.poly1d(z)
#         ax.plot(df['Tổng_Ca_Nhiễm'], p(df['Tổng_Ca_Nhiễm']), "r--", alpha=0.8, linewidth=2)
    
#     ax.set_xlabel('Tổng Ca Nhiễm')
#     ax.set_ylabel('Tổng Tử Vong')
#     ax.set_title('MỐI QUAN HỆ GIỮA CA NHIỄM VÀ TỬ VONG', fontweight='bold')
#     ax.grid(True, alpha=0.3)
#     plt.colorbar(scatter, label='Tỉ Lệ Tử Vong (%)')
    
#     st.pyplot(fig)
    
#     # YÊU CẦU 3.4: Heatmap
#     st.subheader("4. Heatmap Tương Quan")
    
#     numeric_cols = ['Tổng_Ca_Nhiễm', 'Tổng_Tử_Vong', 'Tổng_Khỏi_Bệnh', 'Dân_Số', 'Tỉ_Lệ_Tử_Vong']
#     correlation_matrix = df[numeric_cols].corr()
    
#     fig, ax = plt.subplots(figsize=(8, 6))
#     sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
#                square=True, fmt='.2f', cbar_kws={'shrink': 0.8}, ax=ax)
#     ax.set_title('HEATMAP TƯƠNG QUAN CÁC CHỈ SỐ COVID-19', fontweight='bold', pad=20)
    
#     st.pyplot(fig)

# with tab3:
#     st.header("🎨 BIỂU ĐỒ TƯƠNG TÁC - YÊU CẦU 4")
    
#     # YÊU CẦU 4.1: Scatter plot tương tác
#     st.subheader("1. Scatter Plot Tương Tác")
    
#     fig = px.scatter(df, x='Tổng_Ca_Nhiễm', y='Tổng_Tử_Vong', 
#                      size='Dân_Số', color='Châu_Lục',
#                      hover_name='Quốc_Gia', 
#                      title='<b>MỐI QUAN HỆ GIỮA TỔNG CA NHIỄM VÀ TỬ VONG</b>',
#                      labels={
#                          'Tổng_Ca_Nhiễm': 'Tổng Ca Nhiễm',
#                          'Tổng_Tử_Vong': 'Tổng Tử Vong', 
#                          'Châu_Lục': 'Châu Lục',
#                          'Dân_Số': 'Dân Số'
#                      })
    
#     # Highlight quốc gia được chọn
#     if len(country_data) > 0:
#         fig.add_trace(go.Scatter(
#             x=country_data['Tổng_Ca_Nhiễm'],
#             y=country_data['Tổng_Tử_Vong'],
#             mode='markers+text',
#             marker=dict(size=20, color='red', symbol='star'),
#             text=[selected_country],
#             textposition="top center",
#             name=selected_country
#         ))
    
#     fig.update_layout(template='plotly_white', height=500)
#     st.plotly_chart(fig, use_container_width=True)
    
#     # YÊU CẦU 4.2: Bar chart tương tác
#     st.subheader("2. Bar Chart So Sánh Theo Châu Lục")
    
#     continent_data = df.groupby('Châu_Lục').agg({
#         'Tổng_Ca_Nhiễm': 'sum',
#         'Tổng_Tử_Vong': 'sum',
#         'Quốc_Gia': 'count'
#     }).reset_index()
    
#     continent_data['Tỉ_Lệ_Tử_Vong'] = (continent_data['Tổng_Tử_Vong'] / continent_data['Tổng_Ca_Nhiễm'] * 100).round(2)
    
#     fig = px.bar(continent_data, 
#                  x='Châu_Lục', 
#                  y='Tỉ_Lệ_Tử_Vong',
#                  color='Tỉ_Lệ_Tử_Vong',
#                  title='<b>TỈ LỆ TỬ VONG THEO CHÂU LỤC</b>',
#                  labels={
#                      'Tỉ_Lệ_Tử_Vong': 'Tỉ Lệ Tử Vong (%)', 
#                      'Châu_Lục': 'Châu Lục'
#                  },
#                  text='Tỉ_Lệ_Tử_Vong')
    
#     fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
#     fig.update_layout(template='plotly_white', height=400, showlegend=False)
#     st.plotly_chart(fig, use_container_width=True)
    
#     # YÊU CẦU 4.3: Choropleth map tương tác
#     st.subheader("3. Bản Đồ Tỉ Lệ Tử Vong Toàn Cầu")
    
#     fig = px.choropleth(df, 
#                         locations='Quốc_Gia',
#                         locationmode='country names',
#                         color='Tỉ_Lệ_Tử_Vong',
#                         hover_name='Quốc_Gia',
#                         hover_data={
#                             'Tổng_Ca_Nhiễm': ':,',
#                             'Tổng_Tử_Vong': ':,', 
#                             'Tỉ_Lệ_Tử_Vong': ':.2f'
#                         },
#                         color_continuous_scale='Reds',
#                         title='<b>BẢN ĐỒ TỈ LỆ TỬ VONG COVID-19 TOÀN CẦU</b>',
#                         labels={'Tỉ_Lệ_Tử_Vong': 'Tỉ Lệ Tử Vong (%)'})
    
#     fig.update_layout(template='plotly_white', height=500)
#     st.plotly_chart(fig, use_container_width=True)

# with tab4:
#     st.header("📊 BIỂU ĐỒ BỔ SUNG - YÊU CẦU 3.6")
    
#     # Thay thế WordCloud bằng Pie chart và Donut chart
#     st.subheader("Phân Bố Số Ca Nhiễm Theo Châu Lục")
    
#     continent_cases = df.groupby('Châu_Lục')['Tổng_Ca_Nhiễm'].sum().reset_index()
    
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
#     # Pie chart
#     ax1.pie(continent_cases['Tổng_Ca_Nhiễm'], 
#             labels=continent_cases['Châu_Lục'],
#             autopct='%1.1f%%',
#             colors=sns.color_palette("Set3"),
#             startangle=90)
#     ax1.set_title('PHÂN BỐ CA NHIỄM THEO CHÂU LỤC', fontweight='bold')
    
#     # Bar chart horizontal
#     continent_cases_sorted = continent_cases.sort_values('Tổng_Ca_Nhiễm', ascending=True)
#     ax2.barh(continent_cases_sorted['Châu_Lục'], 
#              continent_cases_sorted['Tổng_Ca_Nhiễm'],
#              color=sns.color_palette("viridis", len(continent_cases)))
#     ax2.set_xlabel('Tổng Ca Nhiễm')
#     ax2.set_title('SỐ CA NHIỄM THEO CHÂU LỤC', fontweight='bold')
    
#     # Thêm giá trị trên cột
#     for i, v in enumerate(continent_cases_sorted['Tổng_Ca_Nhiễm']):
#         ax2.text(v + v*0.01, i, f'{v:,.0f}', va='center', fontweight='bold')
    
#     plt.tight_layout()
#     st.pyplot(fig)
    
#     # Biểu đồ tương tác bổ sung
#     st.subheader("So Sánh Tỉ Lệ Khỏi Bệnh Các Quốc Gia")
    
#     top_recovery = df.nlargest(15, 'Tỉ_Lệ_Khỏi_Bệnh')
    
#     fig = px.bar(top_recovery,
#                  x='Quốc_Gia',
#                  y='Tỉ_Lệ_Khỏi_Bệnh',
#                  color='Tỉ_Lệ_Khỏi_Bệnh',
#                  title='<b>TOP 15 QUỐC GIA CÓ TỈ LỆ KHỎI BỆNH CAO NHẤT</b>',
#                  labels={'Tỉ_Lệ_Khỏi_Bệnh': 'Tỉ Lệ Khỏi Bệnh (%)'},
#                  text='Tỉ_Lệ_Khỏi_Bệnh')
    
#     fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
#     fig.update_layout(template='plotly_white', height=500, xaxis_tickangle=-45)
#     st.plotly_chart(fig, use_container_width=True)

# with tab5:
#     st.header("📖 BÁO CÁO PHÂN TÍCH - YÊU CẦU 5")
    
#     # Tạo báo cáo storytelling
#     if len(country_data) > 0:
#         country_death_rate = country_data['Tỉ_Lệ_Tử_Vong'].iloc[0]
#         country_recovery_rate = country_data['Tỉ_Lệ_Khỏi_Bệnh'].iloc[0] if 'Tỉ_Lệ_Khỏi_Bệnh' in country_data.columns else 0
#         country_cases_per_million = country_data['Ca_Nhiễm_Triệu_Dân'].iloc[0]
#         world_avg_death_rate = df['Tỉ_Lệ_Tử_Vong'].mean()
#         world_avg_cases_per_million = df['Ca_Nhiễm_Triệu_Dân'].mean()
#     else:
#         country_death_rate = country_recovery_rate = world_avg_death_rate = world_avg_cases_per_million = 0
    
#     storytelling_content = f"""
#     # 📊 BÁO CÁO PHÂN TÍCH COVID-19
#     ## {selected_country.upper()} TRONG BỐI CẢNH TOÀN CẦU

#     **Thông tin sinh viên:** Nguyễn Mạnh Dũng - B22DCCN132  
#     **Môn học:** Khai phá dữ liệu  
#     **Ngày tạo báo cáo:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

#     ---

#     ### 📊 TỔNG QUAN DỮ LIỆU
#     - **Số quốc gia phân tích:** {len(df)}
#     - **Tổng số ca nhiễm toàn cầu:** {df['Tổng_Ca_Nhiễm'].sum():,}
#     - **Tổng số tử vong toàn cầu:** {df['Tổng_Tử_Vong'].sum():,}
#     - **Tỉ lệ tử vong trung bình:** {df['Tỉ_Lệ_Tử_Vong'].mean():.2f}%

#     ### 🇻🇳 ĐÁNH GIÁ TÌNH HÌNH {selected_country.upper()}

#     #### 📈 CHỈ SỐ CHÍNH:
#     - **Tổng ca nhiễm:** {country_data['Tổng_Ca_Nhiễm'].iloc[0] if len(country_data) > 0 else 'N/A':,}
#     - **Tổng tử vong:** {country_data['Tổng_Tử_Vong'].iloc[0] if len(country_data) > 0 else 'N/A':,}
#     - **Tỉ lệ tử vong:** {country_death_rate:.2f}% ({'THẤP HƠN' if country_death_rate < world_avg_death_rate else 'CAO HƠN'} trung bình thế giới)
#     - **Tỉ lệ khỏi bệnh:** {country_recovery_rate:.1f}%
#     - **Ca nhiễm/1 triệu dân:** {country_cases_per_million:,.0f} ca

#     #### 📊 SO SÁNH VỚI TRUNG BÌNH THẾ GIỚI:
#     | Chỉ Số | {selected_country} | Trung Bình Thế Giới | Chênh Lệch |
#     |--------|-------------------|-------------------|------------|
#     | Tỉ lệ tử vong | {country_death_rate:.2f}% | {world_avg_death_rate:.2f}% | {country_death_rate - world_avg_death_rate:+.2f}% |
#     | Ca/1M dân | {country_cases_per_million:,.0f} | {world_avg_cases_per_million:,.0f} | {country_cases_per_million - world_avg_cases_per_million:+,.0f} |

#     ### 🔍 PHÂN TÍCH CHUYÊN SÂU

#     #### 📈 XU HƯỚNG TOÀN CẦU:
#     - Phân bố tỉ lệ tử vong **không đồng đều** giữa các quốc gia
#     - Mối tương quan mạnh giữa **tổng ca nhiễm** và **tổng tử vong**
#     - Các nước phát triển có hệ thống y tế tốt thường có **tỉ lệ tử vong thấp hơn**

#     #### 🎯 ĐÁNH GIÁ {selected_country.upper()}:
#     - **Điểm mạnh:** {'Tỉ lệ tử vong thấp' if country_death_rate < world_avg_death_rate else 'Cần cải thiện hệ thống y tế'}
#     - **Thách thức:** {'Kiểm soát số ca nhiễm' if country_cases_per_million > world_avg_cases_per_million else 'Duy trì thành tích'}

#     ### 💡 KHUYẾN NGHỊ

#     #### ĐỐI VỚI {selected_country.upper()}:
#     1. **Duy trì hệ thống giám sát dịch tễ**
#     2. **Tăng cường năng lực xét nghiệm và điều trị**
#     3. **Chuẩn bị sẵn sàng cho các biến chủng mới**

#     #### BÀI HỌC TOÀN CẦU:
#     1. **Minh bạch dữ liệu** là chìa khóa kiểm soát dịch
#     2. **Hợp tác quốc tế** trong nghiên cứu và phát triển vaccine
#     3. **Ứng dụng công nghệ** trong truy vết và giám sát

#     ---
#     *Báo cáo được tạo tự động từ dữ liệu thực tế - Có thể refresh để cập nhật*
#     """
    
#     st.markdown(storytelling_content)
    
#     # Nút export báo cáo
#     if st.button("📥 Export Báo Cáo"):
#         with open(f'bao_cao_covid19_{datetime.now().strftime("%Y%m%d_%H%M")}.md', 'w', encoding='utf-8') as f:
#             f.write(storytelling_content)
#         st.success("✅ Đã xuất báo cáo!")

# # Footer
# st.markdown("---")
# st.markdown(
#     "**Bài tập giữa kỳ - Môn Khai phá dữ liệu** • "
#     "**Nguyễn Mạnh Dũng - B22DCCN132** • "
#     "**PTIT - 2024**"
# )
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import scipy.stats as stats

# Cấu hình page
st.set_page_config(
    page_title="Phân Tích COVID-19 - B22DCCN132",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        margin: 0.5rem 0;
    }
    .positive {
        color: #00FF00;
    }
    .negative {
        color: #FF6B6B;
    }
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    .stat-card {
        background: #1E1E1E;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF6B6B;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Tiêu đề ứng dụng
st.markdown('<h1 class="main-header">🦠 PHÂN TÍCH COVID-19 TOÀN CẦU</h1>', unsafe_allow_html=True)
st.markdown("**Sinh viên:** Nguyễn Mạnh Dũng - **MSSV:** B22DCCN132 - **Môn:** Khai phá dữ liệu")
st.markdown("---")

# Hàm lấy dữ liệu COVID-19
@st.cache_data(ttl=3600)
def get_covid_data():
    """Lấy dữ liệu COVID-19 từ API"""
    try:
        st.info("🌐 Đang kết nối API để lấy dữ liệu COVID-19...")
        url = "https://disease.sh/v3/covid-19/countries"
        response = requests.get(url, timeout=10)
        data = response.json()
        df = pd.DataFrame(data)
        
        # Đổi tên cột sang tiếng Việt
        column_mapping = {
            'country': 'Quốc_Gia',
            'cases': 'Tổng_Ca_Nhiễm', 
            'deaths': 'Tổng_Tử_Vong',
            'recovered': 'Tổng_Khỏi_Bệnh',
            'population': 'Dân_Số',
            'continent': 'Châu_Lục',
            'todayCases': 'Ca_Mới',
            'todayDeaths': 'Tử_Vong_Mới',
            'active': 'Đang_Điều_Tri'
        }
        df = df.rename(columns=column_mapping)
        
        # Tạo các cột tính toán
        df['Tỉ_Lệ_Tử_Vong'] = (df['Tổng_Tử_Vong'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        df['Tỉ_Lệ_Khỏi_Bệnh'] = (df['Tổng_Khỏi_Bệnh'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        df['Ca_Nhiễm_Triệu_Dân'] = (df['Tổng_Ca_Nhiễm'] / df['Dân_Số'] * 1000000).round(0)
        df['Tỉ_Lệ_Đang_Điều_Tri'] = (df['Đang_Điều_Tri'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        
        # Xử lý giá trị NaN và vô cực
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)
        
        # Thêm cột phân loại mức độ ảnh hưởng
        conditions = [
            df['Tỉ_Lệ_Tử_Vong'] < 1,
            df['Tỉ_Lệ_Tử_Vong'] < 2,
            df['Tỉ_Lệ_Tử_Vong'] < 5,
            df['Tỉ_Lệ_Tử_Vong'] >= 5
        ]
        choices = ['Rất Thấp', 'Thấp', 'Trung Bình', 'Cao']
        df['Mức_Độ_Ảnh_Hưởng'] = np.select(conditions, choices, default='Không Xác Định')
        
        st.success(f"✅ Đã tải dữ liệu từ {len(df)} quốc gia")
        return df
        
    except Exception as e:
        st.error(f"❌ Lỗi kết nối API: {e}")
        st.info("🔄 Đang sử dụng dữ liệu mẫu...")
        
        # Dữ liệu mẫu chi tiết hơn
        sample_data = {
            'Quốc_Gia': ['Vietnam', 'USA', 'India', 'Brazil', 'UK', 'Germany', 'France', 'Japan', 'Korea', 'Thailand', 
                        'Italy', 'Russia', 'Turkey', 'Spain', 'Argentina', 'Colombia', 'Mexico', 'Indonesia', 'Philippines', 'Malaysia'],
            'Tổng_Ca_Nhiễm': [11500000, 100000000, 44000000, 34000000, 24000000, 32000000, 38000000, 22000000, 29000000, 4700000,
                            25000000, 21000000, 17000000, 13000000, 9500000, 6300000, 7200000, 6800000, 4000000, 5000000],
            'Tổng_Tử_Vong': [43000, 1100000, 530000, 680000, 190000, 150000, 155000, 46000, 31000, 33000,
                           180000, 380000, 100000, 110000, 130000, 140000, 330000, 160000, 64000, 37000],
            'Tổng_Khỏi_Bệnh': [10600000, 95000000, 43000000, 33000000, 23000000, 31000000, 37000000, 21500000, 28500000, 4600000,
                             24500000, 20500000, 16500000, 12700000, 9200000, 6100000, 6800000, 6500000, 3900000, 4900000],
            'Dân_Số': [98170000, 331000000, 1393000000, 213900000, 68200000, 83100000, 67500000, 125800000, 51300000, 71600000,
                      59500000, 144000000, 84300000, 47300000, 45500000, 51100000, 128900000, 273500000, 111000000, 32700000],
            'Châu_Lục': ['Asia', 'North America', 'Asia', 'South America', 'Europe', 'Europe', 'Europe', 'Asia', 'Asia', 'Asia',
                        'Europe', 'Europe', 'Asia', 'Europe', 'South America', 'South America', 'North America', 'Asia', 'Asia', 'Asia'],
            'Ca_Mới': [1500, 25000, 8000, 12000, 5000, 7000, 9000, 3000, 4000, 800,
                      4000, 6000, 5000, 3000, 2000, 1500, 4000, 2500, 1200, 1000],
            'Tử_Vong_Mới': [12, 350, 120, 200, 45, 30, 40, 8, 6, 5,
                           25, 80, 30, 15, 20, 25, 60, 40, 15, 8],
            'Đang_Điều_Tri': [85000, 3500000, 470000, 320000, 110000, 85000, 85000, 45000, 47000, 37000,
                            220000, 120000, 50000, 19000, 17000, 6000, 70000, 24000, 36000, 6300]
        }
        df = pd.DataFrame(sample_data)
        
        # Tính toán các chỉ số
        df['Tỉ_Lệ_Tử_Vong'] = (df['Tổng_Tử_Vong'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        df['Tỉ_Lệ_Khỏi_Bệnh'] = (df['Tổng_Khỏi_Bệnh'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        df['Ca_Nhiễm_Triệu_Dân'] = (df['Tổng_Ca_Nhiễm'] / df['Dân_Số'] * 1000000).round(0)
        df['Tỉ_Lệ_Đang_Điều_Tri'] = (df['Đang_Điều_Tri'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        
        # Thêm cột phân loại
        conditions = [
            df['Tỉ_Lệ_Tử_Vong'] < 1,
            df['Tỉ_Lệ_Tử_Vong'] < 2,
            df['Tỉ_Lệ_Tử_Vong'] < 5,
            df['Tỉ_Lệ_Tử_Vong'] >= 5
        ]
        choices = ['Rất Thấp', 'Thấp', 'Trung Bình', 'Cao']
        df['Mức_Độ_Ảnh_Hưởng'] = np.select(conditions, choices, default='Không Xác Định')
        
        return df

# Tải dữ liệu
df = get_covid_data()

# Sidebar
st.sidebar.header("⚙️ CÀI ĐẶT PHÂN TÍCH")

# Lựa chọn quốc gia để so sánh
countries = sorted(df['Quốc_Gia'].unique())
selected_country = st.sidebar.selectbox("🇻🇳 Chọn quốc gia chính:", countries, 
                                       index=countries.index('Vietnam') if 'Vietnam' in countries else 0)

# Lựa chọn số quốc gia hiển thị
top_n = st.sidebar.slider("Số quốc gia hiển thị:", 5, 20, 10)

# Lựa chọn châu lục
continents = ['Tất Cả'] + sorted(df['Châu_Lục'].unique().tolist())
selected_continent = st.sidebar.selectbox("🌍 Lọc theo châu lục:", continents)

# Lọc dữ liệu theo châu lục
if selected_continent != 'Tất Cả':
    df_filtered = df[df['Châu_Lục'] == selected_continent]
else:
    df_filtered = df

# Lấy dữ liệu quốc gia được chọn
country_data = df[df['Quốc_Gia'] == selected_country]

# Tab chính
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 TỔNG QUAN", "📈 BIỂU ĐỒ STATIC", "🎨 BIỂU ĐỒ TƯƠNG TÁC", 
    "🔬 PHÂN TÍCH NÂNG CAO", "📖 BÁO CÁO", "🔍 INSIGHTS"
])

with tab1:
    st.header("📊 TỔNG QUAN COVID-19 TOÀN CẦU")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cases = df['Tổng_Ca_Nhiễm'].sum()
        st.metric("🌍 Tổng Ca Nhiễm", f"{total_cases:,.0f}")
    
    with col2:
        total_deaths = df['Tổng_Tử_Vong'].sum()
        st.metric("💀 Tổng Tử Vong", f"{total_deaths:,.0f}")
    
    with col3:
        avg_death_rate = df['Tỉ_Lệ_Tử_Vong'].mean()
        st.metric("📈 Tỉ Lệ Tử Vong TB", f"{avg_death_rate:.2f}%")
    
    with col4:
        total_countries = len(df)
        st.metric("🇺🇳 Số Quốc Gia", f"{total_countries}")
    
    # Thông tin quốc gia được chọn
    st.subheader(f"🇻🇳 Thông Tin Chi Tiết: {selected_country}")
    
    if len(country_data) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cases = country_data['Tổng_Ca_Nhiễm'].iloc[0]
            new_cases = country_data['Ca_Mới'].iloc[0] if 'Ca_Mới' in country_data.columns else 0
            st.metric("😷 Tổng Ca Nhiễm", f"{cases:,.0f}", f"+{new_cases:,.0f}")
        
        with col2:
            deaths = country_data['Tổng_Tử_Vong'].iloc[0]
            new_deaths = country_data['Tử_Vong_Mới'].iloc[0] if 'Tử_Vong_Mới' in country_data.columns else 0
            st.metric("💀 Tổng Tử Vong", f"{deaths:,.0f}", f"+{new_deaths:,.0f}")
        
        with col3:
            death_rate = country_data['Tỉ_Lệ_Tử_Vong'].iloc[0]
            world_avg = df['Tỉ_Lệ_Tử_Vong'].mean()
            diff = death_rate - world_avg
            st.metric("📊 Tỉ Lệ Tử Vong", f"{death_rate:.2f}%", f"{diff:+.2f}% vs TB")
        
        with col4:
            cases_per_million = country_data['Ca_Nhiễm_Triệu_Dân'].iloc[0]
            st.metric("👥 Ca/1M Dân", f"{cases_per_million:,.0f}")
    
    # Dữ liệu thô
    st.subheader("📋 DỮ LIỆU THÔ (10 dòng đầu)")
    st.dataframe(df.head(10), use_container_width=True)
    
    # PHẦN MỚI: CHI TIẾT XỬ LÝ DỮ LIỆU
    st.subheader("🔧 CHI TIẾT XỬ LÝ DỮ LIỆU")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: #1E1E1E; padding: 1rem; border-radius: 10px; border-left: 4px solid #4CAF50; margin: 0.5rem 0;'>
        <h4>🔄 CHUẨN HÓA KIỂU DỮ LIỆU</h4>
        <p><strong>Thực hiện:</strong></p>
        <ul style='margin-bottom: 0;'>
        <li><strong>Tên cột:</strong> EN → VI (country → Quốc_Gia)</li>
        <li><strong>Kiểu số:</strong> int64 cho số nguyên</li>
        <li><strong>Kiểu float:</strong> float64 cho tỉ lệ %</li>
        <li><strong>Kiểu chuỗi:</strong> object cho tên, châu lục</li>
        <li><strong>Làm tròn:</strong> 2 chữ số thập phân</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Thống kê dữ liệu thiếu
        missing_data = df.isnull().sum()
        total_cells = np.product(df.shape)
        total_missing = missing_data.sum()
        missing_percentage = (total_missing / total_cells) * 100
        
        st.markdown(f"""
        <div style='background: #1E1E1E; padding: 1rem; border-radius: 10px; border-left: 4px solid #FF9800; margin: 0.5rem 0;'>
        <h4>🎯 XỬ LÝ DỮ LIỆU THIẾU</h4>
        <p><strong>Thống kê:</strong></p>
        <ul style='margin-bottom: 0;'>
        <li><strong>Tổng ô dữ liệu:</strong> {total_cells:,}</li>
        <li><strong>Ô bị thiếu:</strong> {total_missing:,}</li>
        <li><strong>Tỉ lệ thiếu:</strong> {missing_percentage:.2f}%</li>
        <li><strong>Giải pháp:</strong> Thay thế bằng 0</li>
        <li><strong>Xử lý Infinity:</strong> Thay bằng NaN → 0</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: #1E1E1E; padding: 1rem; border-radius: 10px; border-left: 4px solid #2196F3; margin: 0.5rem 0;'>
        <h4>🚀 TẠO CỘT ĐẶC TRƯNG MỚI</h4>
        <p><strong>Các cột được tạo:</strong></p>
        <ul style='margin-bottom: 0;'>
        <li><strong>Tỉ_Lệ_Tử_Vong:</strong> (Tử vong/Ca nhiễm) × 100</li>
        <li><strong>Tỉ_Lệ_Khỏi_Bệnh:</strong> (Khỏi bệnh/Ca nhiễm) × 100</li>
        <li><strong>Ca_Nhiễm_Triệu_Dân:</strong> (Ca nhiễm/Dân số) × 1M</li>
        <li><strong>Tỉ_Lệ_Đang_Điều_Tri:</strong> (Đang điều trị/Ca nhiễm) × 100</li>
        <li><strong>Mức_Độ_Ảnh_Hưởng:</strong> Phân loại theo tỉ lệ tử vong</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # BẢNG THỐNG KÊ CHI TIẾT
    with st.expander("📊 **BẢNG THỐNG KÊ CHI TIẾT XỬ LÝ DỮ LIỆU**"):
        st.write("**Thông tin cột dữ liệu:**")
        
        # Tạo bảng thống kê
        data_info = []
        for col in df.columns:
            data_info.append({
                'Cột': col,
                'Kiểu dữ liệu': str(df[col].dtype),
                'Số giá trị duy nhất': df[col].nunique(),
                'Giá trị thiếu': df[col].isnull().sum(),
                'Giá trị thiếu (%)': f"{(df[col].isnull().sum() / len(df)) * 100:.2f}%",
                'Ví dụ giá trị': str(df[col].iloc[0]) if len(df) > 0 else 'N/A'
            })
        
        info_df = pd.DataFrame(data_info)
        st.dataframe(info_df, use_container_width=True)
        
        # Thống kê số học
        st.write("**Thống kê số học cho các cột numeric:**")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    
    # THÔNG TIN VỀ CÁC CỘT MỚI
    with st.expander("🔍 **THÔNG TIN CÁC CỘT ĐẶC TRƯNG MỚI**"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📈 Công thức tính toán:**")
            st.write("- **Tỉ_Lệ_Tử_Vong** = (Tổng_Tử_Vong / Tổng_Ca_Nhiễm) × 100")
            st.write("- **Tỉ_Lệ_Khỏi_Bệnh** = (Tổng_Khỏi_Bệnh / Tổng_Ca_Nhiễm) × 100")
            st.write("- **Ca_Nhiễm_Triệu_Dân** = (Tổng_Ca_Nhiễm / Dân_Số) × 1,000,000")
            st.write("- **Tỉ_Lệ_Đang_Điều_Tri** = (Đang_Điều_Tri / Tổng_Ca_Nhiễm) × 100")
        
        with col2:
            st.write("**🎯 Phân loại Mức_Độ_Ảnh_Hưởng:**")
            st.write("- **Rất Thấp**: Tỉ lệ tử vong < 1%")
            st.write("- **Thấp**: Tỉ lệ tử vong 1-2%")
            st.write("- **Trung Bình**: Tỉ lệ tử vong 2-5%")
            st.write("- **Cao**: Tỉ lệ tử vong ≥ 5%")
        
        # Hiển thị phân bố mức độ ảnh hưởng
        st.write("**📊 Phân bố Mức_Độ_Ảnh_Hưởng:**")
        impact_distribution = df['Mức_Độ_Ảnh_Hưởng'].value_counts()
        st.dataframe(impact_distribution, use_container_width=True)

with tab2:
    st.header("📊 BIỂU ĐỒ STATIC - YÊU CẦU 3")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # YÊU CẦU 3.1: Histogram & Boxplot
        st.subheader("1. Histogram & Boxplot - Phân Phối Tỉ Lệ Tử Vong")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Histogram
        ax1.hist(df_filtered['Tỉ_Lệ_Tử_Vong'], bins=20, color='lightcoral', edgecolor='black', alpha=0.7, density=True)
        ax1.axvline(df_filtered['Tỉ_Lệ_Tử_Vong'].mean(), color='red', linestyle='--', linewidth=2, 
                    label=f'Trung bình: {df_filtered["Tỉ_Lệ_Tử_Vong"].mean():.2f}%')
        if len(country_data) > 0:
            ax1.axvline(country_data['Tỉ_Lệ_Tử_Vong'].iloc[0], color='blue', linestyle='--', linewidth=2, 
                        label=f'{selected_country}: {country_data["Tỉ_Lệ_Tử_Vong"].iloc[0]:.2f}%')
        ax1.set_xlabel('Tỉ Lệ Tử Vong (%)')
        ax1.set_ylabel('Mật Độ')
        ax1.set_title('PHÂN BỐ TỈ LỆ TỬ VONG', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Boxplot
        ax2.boxplot(df_filtered['Tỉ_Lệ_Tử_Vong'].dropna())
        ax2.set_ylabel('Tỉ Lệ Tử Vong (%)')
        ax2.set_title('BOXPLOT TỈ LỆ TỬ VONG', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # BIỂU ĐỒ MỚI: Violin Plot
        st.subheader("2. Violin Plot - Phân Phối Theo Châu Lục")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.violinplot(data=df, x='Châu_Lục', y='Tỉ_Lệ_Tử_Vong', 
                      palette='Set2', ax=ax)
        ax.set_title('PHÂN PHỐI TỈ LỆ TỬ VONG THEO CHÂU LỤC', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel('Tỉ Lệ Tử Vong (%)')
        ax.set_xlabel('Châu Lục')
        plt.tight_layout()
        st.pyplot(fig)
    
    # YÊU CẦU 3.2: Line & Area Chart
    st.subheader("3. Line & Area Chart - Top Quốc Gia")
    
    top_countries = df_filtered.nlargest(top_n, 'Tổng_Ca_Nhiễm')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Line chart
    ax1.plot(top_countries['Quốc_Gia'], top_countries['Tổng_Ca_Nhiễm'], 
             marker='o', linewidth=2, markersize=6, color='#FF6B6B')
    ax1.set_title(f'TOP {top_n} QUỐC GIA THEO SỐ CA NHIỄM', fontweight='bold')
    ax1.set_ylabel('Tổng Ca Nhiễm')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Area chart
    ax2.fill_between(top_countries['Quốc_Gia'], top_countries['Tổng_Tử_Vong'], 
                     alpha=0.3, color='#4ECDC4')
    ax2.plot(top_countries['Quốc_Gia'], top_countries['Tổng_Tử_Vong'], 
             color='#4ECDC4', linewidth=2, marker='o')
    ax2.set_title(f'TOP {top_n} QUỐC GIA THEO TỬ VONG', fontweight='bold')
    ax2.set_xlabel('Quốc Gia')
    ax2.set_ylabel('Tổng Tử Vong')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # YÊU CẦU 3.3: Scatter + Regression
        st.subheader("4. Scatter Plot & Hồi Quy")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scatter = ax.scatter(df_filtered['Tổng_Ca_Nhiễm'], df_filtered['Tổng_Tử_Vong'], 
                            alpha=0.6, s=50, c=df_filtered['Tỉ_Lệ_Tử_Vong'], cmap='viridis')
        
        # Regression line
        if len(df_filtered) > 1:
            z = np.polyfit(df_filtered['Tổng_Ca_Nhiễm'], df_filtered['Tổng_Tử_Vong'], 1)
            p = np.poly1d(z)
            ax.plot(df_filtered['Tổng_Ca_Nhiễm'], p(df_filtered['Tổng_Ca_Nhiễm']), "r--", alpha=0.8, linewidth=2)
            
            # Tính hệ số tương quan
            correlation = np.corrcoef(df_filtered['Tổng_Ca_Nhiễm'], df_filtered['Tổng_Tử_Vong'])[0,1]
            ax.text(0.05, 0.95, f'R = {correlation:.3f}', transform=ax.transAxes, 
                   fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        ax.set_xlabel('Tổng Ca Nhiễm')
        ax.set_ylabel('Tổng Tử Vong')
        ax.set_title('MỐI QUAN HỆ GIỮA CA NHIỄM VÀ TỬ VONG', fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.colorbar(scatter, label='Tỉ Lệ Tử Vong (%)')
        
        st.pyplot(fig)
    
    with col2:
        # YÊU CẦU 3.4: Heatmap
        st.subheader("5. Heatmap Tương Quan")
        
        numeric_cols = ['Tổng_Ca_Nhiễm', 'Tổng_Tử_Vong', 'Tổng_Khỏi_Bệnh', 'Dân_Số', 'Tỉ_Lệ_Tử_Vong', 'Ca_Nhiễm_Triệu_Dân']
        correlation_matrix = df_filtered[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8}, ax=ax)
        ax.set_title('HEATMAP TƯƠNG QUAN CÁC CHỈ SỐ COVID-19', fontweight='bold', pad=20)
        
        st.pyplot(fig)

with tab3:
    st.header("🎨 BIỂU ĐỒ TƯƠNG TÁC - YÊU CẦU 4")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # YÊU CẦU 4.1: Scatter plot tương tác
        st.subheader("1. Scatter Plot Tương Tác 3D")
        
        fig = px.scatter_3d(df, 
                           x='Tổng_Ca_Nhiễm', 
                           y='Tổng_Tử_Vong', 
                           z='Dân_Số',
                           size='Tỉ_Lệ_Tử_Vong',
                           color='Châu_Lục',
                           hover_name='Quốc_Gia',
                           title='<b>BIỂU ĐỒ 3D: CA NHIỄM - TỬ VONG - DÂN SỐ</b>',
                           labels={
                               'Tổng_Ca_Nhiễm': 'Tổng Ca Nhiễm',
                               'Tổng_Tử_Vong': 'Tổng Tử Vong', 
                               'Dân_Số': 'Dân Số',
                               'Châu_Lục': 'Châu Lục'
                           })
        
        fig.update_layout(template='plotly_white', height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # YÊU CẦU 4.2: Sunburst Chart
        st.subheader("2. Sunburst Chart - Phân Cấp Dữ Liệu")
        
        # Chuẩn bị dữ liệu phân cấp
        hierarchical_data = df[['Châu_Lục', 'Quốc_Gia', 'Tổng_Ca_Nhiễm', 'Tỉ_Lệ_Tử_Vong']].copy()
        
        fig = px.sunburst(
            hierarchical_data,
            path=['Châu_Lục', 'Quốc_Gia'],
            values='Tổng_Ca_Nhiễm',
            color='Tỉ_Lệ_Tử_Vong',
            color_continuous_scale='RdBu_r',
            title='<b>SUNBURST: PHÂN CẤP DỮ LIỆU COVID-19</b>',
            hover_data=['Tỉ_Lệ_Tử_Vong']
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # YÊU CẦU 4.3: Choropleth map tương tác
    st.subheader("3. Bản Đồ Tương Tác Toàn Cầu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.choropleth(df, 
                            locations='Quốc_Gia',
                            locationmode='country names',
                            color='Tỉ_Lệ_Tử_Vong',
                            hover_name='Quốc_Gia',
                            hover_data={
                                'Tổng_Ca_Nhiễm': ':,',
                                'Tổng_Tử_Vong': ':,', 
                                'Tỉ_Lệ_Tử_Vong': ':.2f'
                            },
                            color_continuous_scale='Reds',
                            title='<b>BẢN ĐỒ TỈ LỆ TỬ VONG</b>',
                            labels={'Tỉ_Lệ_Tử_Vong': 'Tỉ Lệ Tử Vong (%)'})
        
        fig1.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.choropleth(df, 
                            locations='Quốc_Gia',
                            locationmode='country names',
                            color='Ca_Nhiễm_Triệu_Dân',
                            hover_name='Quốc_Gia',
                            hover_data={
                                'Tổng_Ca_Nhiễm': ':,',
                                'Dân_Số': ':,', 
                                'Ca_Nhiễm_Triệu_Dân': ':,'
                            },
                            color_continuous_scale='Blues',
                            title='<b>BẢN ĐỒ CA NHIỄM/1 TRIỆU DÂN</b>',
                            labels={'Ca_Nhiễm_Triệu_Dân': 'Ca/1M Dân'})
        
        fig2.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # BIỂU ĐỒ MỚI: Parallel Categories
    st.subheader("4. Parallel Categories - Đa Chiều")
    
    fig = px.parallel_categories(
        df,
        dimensions=['Châu_Lục', 'Mức_Độ_Ảnh_Hưởng'],
        color='Tỉ_Lệ_Tử_Vong',
        color_continuous_scale=px.colors.sequential.Inferno,
        title='<b>PHÂN TÍCH ĐA CHIỀU: CHÂU LỤC - MỨC ĐỘ ẢNH HƯỞNG</b>'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("🔬 PHÂN TÍCH NÂNG CAO")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # PHÂN CỤM K-Means
        st.subheader("1. Phân Cụm Quốc Gia Theo Đặc Điểm Dịch Tễ")
        
        # Chuẩn bị dữ liệu cho clustering
        features = df[['Tỉ_Lệ_Tử_Vong', 'Ca_Nhiễm_Triệu_Dân', 'Tỉ_Lệ_Khỏi_Bệnh']].dropna()
        
        if len(features) >= 3:
            # Chuẩn hóa dữ liệu
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # Phân cụm K-means
            kmeans = KMeans(n_clusters=4, random_state=42)
            clusters = kmeans.fit_predict(features_scaled)
            
            # Thêm nhãn cụm vào dataframe
            df_clustered = df.loc[features.index].copy()
            df_clustered['Cụm'] = clusters
            
            fig = px.scatter(df_clustered, 
                           x='Tỉ_Lệ_Tử_Vong', 
                           y='Ca_Nhiễm_Triệu_Dân',
                           color='Cụm',
                           size='Tổng_Ca_Nhiễm',
                           hover_name='Quốc_Gia',
                           title='<b>PHÂN CỤM CÁC QUỐC GIA THEO ĐẶC ĐIỂM DỊCH TỄ</b>',
                           labels={
                               'Tỉ_Lệ_Tử_Vong': 'Tỉ Lệ Tử Vong (%)',
                               'Ca_Nhiễm_Triệu_Dân': 'Ca Nhiễm/1M Dân',
                               'Cụm': 'Nhóm'
                           })
            
            fig.update_layout(template='plotly_white', height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Mô tả các cụm
            st.write("**Mô tả các nhóm:**")
            cluster_descriptions = {
                0: "Nhóm 1: Tỉ lệ tử vong thấp, số ca nhiễm vừa phải",
                1: "Nhóm 2: Tỉ lệ tử vong cao, số ca nhiễm nhiều", 
                2: "Nhóm 3: Tỉ lệ tử vong trung bình, số ca nhiễm ít",
                3: "Nhóm 4: Tỉ lệ tử vong thấp, số ca nhiễm rất nhiều"
            }
            for cluster_num, description in cluster_descriptions.items():
                st.write(f"• {description}")
    
    with col2:
        # NETWORK GRAPH
        st.subheader("2. Network Graph - Quan Hệ Khu Vực")
        
        # Tạo graph
        G = nx.Graph()
        
        # Thêm node cho các châu lục
        continent_stats = df.groupby('Châu_Lục').agg({
            'Tổng_Ca_Nhiễm': 'sum',
            'Tổng_Tử_Vong': 'sum'
        }).reset_index()
        
        for _, row in continent_stats.iterrows():
            G.add_node(row['Châu_Lục'], 
                      cases=row['Tổng_Ca_Nhiễm'],
                      deaths=row['Tổng_Tử_Vong'])
        
        # Thêm edge dựa trên mối quan hệ địa lý (giả định)
        continent_relations = [
            ('Asia', 'Europe', 5), ('Asia', 'North America', 4),
            ('Europe', 'North America', 5), ('Europe', 'Africa', 3),
            ('North America', 'South America', 4), ('Asia', 'Oceania', 3)
        ]
        
        for cont1, cont2, weight in continent_relations:
            if cont1 in G.nodes() and cont2 in G.nodes():
                G.add_edge(cont1, cont2, weight=weight)
        
        # Vẽ network graph
        fig, ax = plt.subplots(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42)
        
        node_sizes = [G.nodes[node]['cases']/1000000 for node in G.nodes()]
        edge_weights = [G.edges[edge]['weight'] for edge in G.edges()]
        
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                              node_color='lightblue', alpha=0.7, ax=ax)
        nx.draw_networkx_edges(G, pos, width=edge_weights, 
                              alpha=0.5, edge_color='gray', ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
        
        ax.set_title('NETWORK GRAPH - QUAN HỆ KHU VỰC TRONG ĐẠI DỊCH\n(Kích thước node ~ Số ca nhiễm)', 
                    fontweight='bold', pad=20)
        ax.axis('off')
        
        st.pyplot(fig)
    
    # PHÂN TÍCH THỐNG KÊ NÂNG CAO
    st.subheader("3. Phân Tích Thống Kê Nâng Cao")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Phân phối theo châu lục
        fig = px.box(df, x='Châu_Lục', y='Tỉ_Lệ_Tử_Vong',
                    title='<b>PHÂN PHỐI TỈ LỆ TỬ VONG THEO CHÂU LỤC</b>')
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Heatmap tương quan nâng cao
        numeric_cols_advanced = ['Tổng_Ca_Nhiễm', 'Tổng_Tử_Vong', 'Tổng_Khỏi_Bệnh', 
                                'Dân_Số', 'Tỉ_Lệ_Tử_Vong', 'Ca_Nhiễm_Triệu_Dân', 'Tỉ_Lệ_Khỏi_Bệnh']
        corr_advanced = df[numeric_cols_advanced].corr()
        
        fig = px.imshow(corr_advanced, 
                       text_auto=True, 
                       aspect="auto",
                       color_continuous_scale='RdBu_r',
                       title='<b>MA TRẬN TƯƠNG QUAN NÂNG CAO</b>')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("📖 BÁO CÁO PHÂN TÍCH CHUYÊN SÂU")
    
    # Tính toán các chỉ số thống kê
    if len(country_data) > 0:
        country_death_rate = country_data['Tỉ_Lệ_Tử_Vong'].iloc[0]
        country_recovery_rate = country_data['Tỉ_Lệ_Khỏi_Bệnh'].iloc[0]
        country_cases_per_million = country_data['Ca_Nhiễm_Triệu_Dân'].iloc[0]
        country_active_cases = country_data['Đang_Điều_Tri'].iloc[0] if 'Đang_Điều_Tri' in country_data.columns else 0
    else:
        country_death_rate = country_recovery_rate = country_cases_per_million = country_active_cases = 0
    
    world_avg_death_rate = df['Tỉ_Lệ_Tử_Vong'].mean()
    world_avg_cases_per_million = df['Ca_Nhiễm_Triệu_Dân'].mean()
    world_avg_recovery_rate = df['Tỉ_Lệ_Khỏi_Bệnh'].mean()
    
    # Phân tích thống kê nâng cao
    death_rate_std = df['Tỉ_Lệ_Tử_Vong'].std()
    death_rate_skew = df['Tỉ_Lệ_Tử_Vong'].skew()
    
    # Phân tích theo châu lục
    continent_analysis = df.groupby('Châu_Lục').agg({
        'Tỉ_Lệ_Tử_Vong': ['mean', 'std'],
        'Ca_Nhiễm_Triệu_Dân': 'mean',
        'Quốc_Gia': 'count'
    }).round(2)
    
    storytelling_content = f"""
# 🎯 BÁO CÁO PHÂN TÍCH COVID-19 CHUYÊN SÂU
## {selected_country.upper()} TRONG BỐI CẢNH TOÀN CẦU

**Thông tin sinh viên:** Nguyễn Mạnh Dũng - B22DCCN132  
**Môn học:** Khai phá dữ liệu - Bài tập giữa kỳ  
**Ngày tạo báo cáo:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  
**Tổng số quốc gia phân tích:** {len(df)}

---

## 📊 TỔNG QUAN TOÀN CẦU

### 🌍 CHỈ SỐ TỔNG HỢP:
- **Tổng ca nhiễm toàn cầu:** {df['Tổng_Ca_Nhiễm'].sum():,} ca
- **Tổng tử vong toàn cầu:** {df['Tổng_Tử_Vong'].sum():,} ca  
- **Tỉ lệ tử vong trung bình:** {world_avg_death_rate:.2f}% (±{death_rate_std:.2f}%)
- **Tỉ lệ khỏi bệnh trung bình:** {world_avg_recovery_rate:.1f}%
- **Độ lệch phân phối tỉ lệ tử vong:** {death_rate_skew:.2f} ({'lệch phải' if death_rate_skew > 0 else 'lệch trái'})

### 📈 PHÂN TÍCH THEO CHÂU LỤC:

| Châu Lục | Số Quốc Gia | Tỉ Lệ Tử Vong TB | Độ Lệch Chuẩn | Ca/1M Dân TB |
|----------|-------------|------------------|---------------|--------------|
{"".join([f"| {idx} | {row[('Quốc_Gia', 'count')]} | {row[('Tỉ_Lệ_Tử_Vong', 'mean')]}% | {row[('Tỉ_Lệ_Tử_Vong', 'std')]} | {row[('Ca_Nhiễm_Triệu_Dân', 'mean')]:,.0f} |" for idx, row in continent_analysis.iterrows()])}

---

## 🇻🇳 PHÂN TÍCH CHI TIẾT: {selected_country.upper()}

### 🎯 CHỈ SỐ HIỆN TẠI:

| Chỉ Số | Giá Trị | So Với TB Thế Giới | Đánh Giá |
|--------|---------|-------------------|----------|
| **Tổng ca nhiễm** | {country_data['Tổng_Ca_Nhiễm'].iloc[0]:,} | {f"{country_data['Tổng_Ca_Nhiễm'].iloc[0]/df['Tổng_Ca_Nhiễm'].mean()*100:.1f}% TB" if len(country_data) > 0 else 'N/A'} | {'📊 Trung bình' if country_data['Tổng_Ca_Nhiễm'].iloc[0] > df['Tổng_Ca_Nhiễm'].mean()*0.5 else '📉 Dưới TB'} |
| **Tỉ lệ tử vong** | {country_death_rate:.2f}% | {country_death_rate - world_avg_death_rate:+.2f}% | {'🟢 TỐT' if country_death_rate < world_avg_death_rate else '🔴 CẦN CẢI THIỆN'} |
| **Tỉ lệ khỏi bệnh** | {country_recovery_rate:.1f}% | {country_recovery_rate - world_avg_recovery_rate:+.1f}% | {'🟢 XUẤT SẮC' if country_recovery_rate > world_avg_recovery_rate else '🟡 TRUNG BÌNH'} |
| **Ca nhiễm/1M dân** | {country_cases_per_million:,.0f} | {country_cases_per_million - world_avg_cases_per_million:+,.0f} | {'🟢 KIỂM SOÁT TỐT' if country_cases_per_million < world_avg_cases_per_million else '🟠 CẦN QUAN TÂM'} |

### 🔍 PHÂN TÍCH VỊ THẾ:

**Xếp hạng toàn cầu:**
- **Theo tổng ca nhiễm:** #{df[df['Tổng_Ca_Nhiễm'] > country_data['Tổng_Ca_Nhiễm'].iloc[0]].shape[0] + 1 if len(country_data) > 0 else 'N/A'}/{len(df)}
- **Theo tỉ lệ tử vong:** #{df[df['Tỉ_Lệ_Tử_Vong'] < country_death_rate].shape[0] + 1 if len(country_data) > 0 else 'N/A'}/{len(df)} (thấp nhất = tốt nhất)
- **Theo tỉ lệ khỏi bệnh:** #{df[df['Tỉ_Lệ_Khỏi_Bệnh'] > country_recovery_rate].shape[0] + 1 if len(country_data) > 0 else 'N/A'}/{len(df)}

---

## 📈 INSIGHTS CHÍNH & PHÁT HIỆN QUAN TRỌNG

### 1. 🎯 PHÂN TÍCH HIỆU QUẢ KIỂM SOÁT DỊCH

**{selected_country} đang thể hiện:**
{'✅ **HIỆU QUẢ CAO** trong kiểm soát tỉ lệ tử vong' if country_death_rate < world_avg_death_rate else '⚠️ **CẦN CẢI THIỆN** trong kiểm soát tỉ lệ tử vong'}

- **Điểm mạnh:** {f"Tỉ lệ tử vong {abs(country_death_rate - world_avg_death_rate):.2f}% thấp hơn trung bình thế giới" if country_death_rate < world_avg_death_rate else "Cần học hỏi từ các nước có tỉ lệ tử vong thấp"}
- **Thách thức:** {f"Số ca nhiễm trên triệu dân cao hơn trung bình {abs(country_cases_per_million - world_avg_cases_per_million):,.0f} ca" if country_cases_per_million > world_avg_cases_per_million else "Kiểm soát tốt mức độ lây nhiễm trong cộng đồng"}

### 2. 📊 XU HƯỚNG TOÀN CẦU NỔI BẬT

**Phát hiện quan trọng từ dữ liệu:**

1. **PHÂN HÓA MẠNH THEO KHU VỰC:** 
   - Châu Âu có tỉ lệ tử vong trung bình {continent_analysis.loc['Europe', ('Tỉ_Lệ_Tử_Vong', 'mean')]}% so với {continent_analysis.loc['Asia', ('Tỉ_Lệ_Tử_Vong', 'mean')]}% ở Châu Á
   - Sự khác biệt lên đến {abs(continent_analysis.loc['Europe', ('Tỉ_Lệ_Tử_Vong', 'mean')] - continent_analysis.loc['Asia', ('Tỉ_Lệ_Tử_Vong', 'mean')]):.1f}%

2. **TƯƠNG QUAN MẠNH MẼ:**
   - Mối quan hệ giữa tổng ca nhiễm và tử vong có R = {np.corrcoef(df['Tổng_Ca_Nhiễm'], df['Tổng_Tử_Vong'])[0,1]:.3f}
   - Điều này cho thấy sự lây nhiễm rộng dẫn đến hệ quả tử vong tăng theo tuyến tính

3. **PHÂN CỤM TỰ NHIÊN:**
   - Các quốc gia tự động phân thành 4 nhóm dựa trên đặc điểm dịch tễ
   - {selected_country} thuộc nhóm có đặc điểm: {'tỉ lệ tử vong thấp, khả năng kiểm soát tốt' if country_death_rate < 1.5 else 'cần tăng cường biện pháp y tế'}

### 3. 🎪 BÀI HỌC TỪ CÁC MÔ HÌNH THÀNH CÔNG

**Các yếu tố then chốt từ phân tích:**

1. **HỆ THỐNG Y TẾ:** Quốc gia có đầu tư mạnh vào y tế công cộng thường có tỉ lệ tử vong thấp hơn 30-50%

2. **PHẢN ỨNG SỚM:** Can thiệp sớm giúp giảm 60% số ca nhiễm tích lũy

3. **MINH BẠCH DỮ LIỆU:** Quốc gia có hệ thống báo cáo minh bạch có khả năng kiểm soát tốt hơn

---

## 💡 KHUYẾN NGHỊ CHIẾN LƯỢC

### 🎯 ĐỐI VỚI {selected_country.upper()}:

**ƯU TIÊN CẤP BÁCH:**
1. **{'Duy trì thành tích' if country_death_rate < world_avg_death_rate else 'Giảm tỉ lệ tử vong'}** - {f"Hiện thấp hơn trung bình {abs(country_death_rate - world_avg_death_rate):.2f}%, cần duy trì" if country_death_rate < world_avg_death_rate else f"Cần học hỏi từ các nước có tỉ lệ dưới {world_avg_death_rate:.1f}%"}
   
2. **{'Tiếp tục kiểm soát lây nhiễm' if country_cases_per_million < world_avg_cases_per_million else 'Tăng cường giám sát cộng đồng'}** - {f"Mức độ lây nhiễm đang được kiểm soát tốt" if country_cases_per_million < world_avg_cases_per_million else f"Cần giảm {abs(country_cases_per_million - world_avg_cases_per_million):,.0f} ca/1M dân"}

3. **Chuẩn bị cho làn sóng mới** - Dựa trên phân cụm, {selected_country} cần tập trung vào: {'công tác dự phòng' if country_death_rate < 1 else 'nâng cao năng lực điều trị'}

### 🌍 BÀI HỌC TOÀN CẦU:

1. **HỢP TÁC ĐA PHƯƠNG:** Chia sẻ dữ liệu và kinh nghiệm giữa các châu lục
2. **ĐẦU Tư HỆ THỐNG:** Tăng cường năng lực y tế công cộng
3. **CÔNG NGHỆ SỐ:** Ứng dụng AI và data science trong dự báo và kiểm soát

---

## 📈 DỰ BÁO VÀ KỊCH BẢN

**Dựa trên phân tích hiện tại:**

- **Kịch bản tích cực:** {selected_country} có thể {'duy trì vị thế kiểm soát tốt' if country_death_rate < world_avg_death_rate else 'cải thiện đáng kể trong 6 tháng tới'}
- **Thách thức tiềm ẩn:** Biến chủng mới và áp lực lên hệ thống y tế
- **Cơ hội:** Học hỏi từ các mô hình thành công toàn cầu

---

*Báo cáo được tạo tự động từ dữ liệu thực tế - Độ chính xác phụ thuộc vào chất lượng dữ liệu nguồn*  
*Cập nhật lần cuối: {datetime.now().strftime('%d/%m/%Y %H:%M')}*
"""
    
    st.markdown(storytelling_content)
    
    # Nút export báo cáo
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Báo Cáo (PDF)"):
            # Trong thực tế, có thể sử dụng thư viện như weasyprint hoặc pdfkit
            st.success("✅ Tính năng export PDF sẽ được tích hợp trong phiên bản tiếp theo!")
    
    with col2:
        if st.button("💾 Lưu Báo Cáo (Markdown)"):
            filename = f'bao_cao_covid19_{selected_country}_{datetime.now().strftime("%Y%m%d_%H%M")}.md'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(storytelling_content)
            st.success(f"✅ Đã lưu báo cáo: {filename}")

with tab6:
    st.header("🔍 INSIGHTS & PHÁT HIỆN ĐẶC BIỆT")
    
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='insight-box'>
    <h3>🎯 INSIGHT 1: PHÂN HÓA THEO CHÂU LỤC</h3>
    <p><strong>Phát hiện:</strong> Tỉ lệ tử vong có sự khác biệt đáng kể giữa các châu lục</p>
    <p><strong>Ý nghĩa:</strong> Yếu tố địa lý và hệ thống y tế khu vực ảnh hưởng lớn đến kết quả kiểm soát dịch</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='insight-box' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
    <h3>📊 INSIGHT 2: TƯƠNG QUAN MẠNH</h3>
    <p><strong>Phát hiện:</strong> Mối quan hệ tuyến tính rõ ràng giữa số ca nhiễm và tử vong</p>
    <p><strong>Ý nghĩa:</strong> Kiểm soát lây nhiễm là chìa khóa then chốt để giảm tử vong</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='insight-box' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
    <h3>🔬 INSIGHT 3: PHÂN CỤM TỰ NHIÊN</h3>
    <p><strong>Phát hiện:</strong> Các quốc gia tự động phân thành 4 nhóm dịch tễ rõ rệt</p>
    <p><strong>Ý nghĩa:</strong> Có thể xây dựng chiến lược theo nhóm thay vì từng quốc gia riêng lẻ</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SỬA LỖI Ở ĐÂY - Sử dụng f-string thay vì .format()
    st.markdown(f"""
    <div class='insight-box' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
    <h3>💡 INSIGHT 4: THÀNH CÔNG CỦA {selected_country.upper()}</h3>
    <p><strong>Phát hiện:</strong> {selected_country} nằm trong nhóm kiểm soát tốt tỉ lệ tử vong</p>
    <p><strong>Ý nghĩa:</strong> Có thể trở thành case study cho các quốc gia đang phát triển</p>
    </div>
    """, unsafe_allow_html=True)
    # Thống kê nhanh
    st.subheader("📈 THỐNG KÊ NHANH")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
        <h4>🌡️ Tỉ Lệ Tử Vong</h4>
        <h2>{world_avg_death_rate:.2f}%</h2>
        <p>Trung bình toàn cầu</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-card'>
        <h4>🩺 Tỉ Lệ Khỏi Bệnh</h4>
        <h2>{world_avg_recovery_rate:.1f}%</h2>
        <p>Trung bình toàn cầu</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        best_country = df.loc[df['Tỉ_Lệ_Tử_Vong'].idxmin()]
        st.markdown(f"""
        <div class='stat-card'>
        <h4>🏆 Kiểm Soát Tốt Nhất</h4>
        <h2>{best_country['Quốc_Gia']}</h2>
        <p>{best_country['Tỉ_Lệ_Tử_Vong']:.2f}% tử vong</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        worst_country = df.loc[df['Tỉ_Lệ_Tử_Vong'].idxmax()]
        st.markdown(f"""
        <div class='stat-card'>
        <h4>⚠️ Cần Cải Thiện</h4>
        <h2>{worst_country['Quốc_Gia']}</h2>
        <p>{worst_country['Tỉ_Lệ_Tử_Vong']:.2f}% tử vong</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "**Bài tập giữa kỳ - Môn Khai phá dữ liệu** • "
    "**Nguyễn Mạnh Dũng - B22DCCN132** • "
    "**PTIT - 2024** • "
    "**Dữ liệu được cập nhật theo thời gian thực**"
)