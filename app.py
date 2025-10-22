import streamlit as st
import sys

# Kiểm tra và import an toàn
try:
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
    
    # Thử import wordcloud, nếu lỗi thì bỏ qua
    try:
        from wordcloud import WordCloud
        HAS_WORDCLOUD = True
    except ImportError:
        HAS_WORDCLOUD = False
        
    HAS_ALL_DEPS = True
except Exception as e:
    st.error(f"❌ Lỗi import: {e}")
    HAS_ALL_DEPS = False
# Thêm ở đầu app.py - TRÊN TẤT CẢ CÁC IMPORT KHÁC
import streamlit as st
import sys
import os

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import plotly.graph_objects as go
    from wordcloud import WordCloud
    import requests
    from datetime import datetime
    import warnings
    warnings.filterwarnings('ignore')
    
    HAS_ALL_DEPS = True
except ImportError as e:
    st.error(f"📦 Thiếu package: {e}")
    HAS_ALL_DEPS = False

# Phần còn lại của code...
# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import requests
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

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
</style>
""", unsafe_allow_html=True)

# Tiêu đề ứng dụng
st.markdown('<h1 class="main-header">🦠 PHÂN TÍCH COVID-19 TOÀN CẦU</h1>', unsafe_allow_html=True)
st.markdown("**Sinh viên:** Nguyễn Mạnh Dũng - **MSSV:** B22DCCN132 - **Môn:** Khai phá dữ liệu")
st.markdown("---")

# Hàm lấy dữ liệu COVID-19
@st.cache_data(ttl=3600)  # Cache 1 giờ
def get_covid_data():
    """Lấy dữ liệu COVID-19 từ API"""
    try:
        st.info("🌐 Đang kết nối API để lấy dữ liệu COVID-19 mới nhất...")
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
            'continent': 'Châu_Lục'
        }
        df = df.rename(columns=column_mapping)
        
        # Tạo các cột tính toán
        df['Tỉ_Lệ_Tử_Vong'] = (df['Tổng_Tử_Vong'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        df['Tỉ_Lệ_Khỏi_Bệnh'] = (df['Tổng_Khỏi_Bệnh'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        df['Ca_Nhiễm_Triệu_Dân'] = (df['Tổng_Ca_Nhiễm'] / df['Dân_Số'] * 1000000).round(0)
        df = df.fillna(0)
        
        st.success(f"✅ Đã tải dữ liệu từ {len(df)} quốc gia")
        return df
        
    except Exception as e:
        st.error(f"❌ Lỗi kết nối API: {e}")
        st.info("🔄 Đang sử dụng dữ liệu mẫu...")
        
        # Dữ liệu mẫu
        sample_data = {
            'Quốc_Gia': ['Vietnam', 'USA', 'India', 'Brazil', 'UK', 'Germany', 'France', 'Japan', 'Korea', 'Thailand'],
            'Tổng_Ca_Nhiễm': [11500000, 100000000, 44000000, 34000000, 24000000, 32000000, 38000000, 22000000, 29000000, 4700000],
            'Tổng_Tử_Vong': [43000, 1100000, 530000, 680000, 190000, 150000, 155000, 46000, 31000, 33000],
            'Tổng_Khỏi_Bệnh': [10600000, 95000000, 43000000, 33000000, 23000000, 31000000, 37000000, 21500000, 28500000, 4600000],
            'Dân_Số': [98170000, 331000000, 1393000000, 213900000, 68200000, 83100000, 67500000, 125800000, 51300000, 71600000],
            'Châu_Lục': ['Asia', 'North America', 'Asia', 'South America', 'Europe', 'Europe', 'Europe', 'Asia', 'Asia', 'Asia']
        }
        df = pd.DataFrame(sample_data)
        df['Tỉ_Lệ_Tử_Vong'] = (df['Tổng_Tử_Vong'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        df['Tỉ_Lệ_Khỏi_Bệnh'] = (df['Tổng_Khỏi_Bệnh'] / df['Tổng_Ca_Nhiễm'] * 100).round(2)
        df['Ca_Nhiễm_Triệu_Dân'] = (df['Tổng_Ca_Nhiễm'] / df['Dân_Số'] * 1000000).round(0)
        
        return df

# Tải dữ liệu
df = get_covid_data()

# Sidebar
st.sidebar.header("⚙️ CÀI ĐẶT PHÂN TÍCH")

# Lựa chọn quốc gia để so sánh
countries = sorted(df['Quốc_Gia'].unique())
selected_country = st.sidebar.selectbox("🇻🇳 Chọn quốc gia chính:", countries, index=countries.index('Vietnam') if 'Vietnam' in countries else 0)

# Lựa chọn số quốc gia hiển thị
top_n = st.sidebar.slider("Số quốc gia hiển thị:", 5, 20, 10)

# Lấy dữ liệu quốc gia được chọn
country_data = df[df['Quốc_Gia'] == selected_country]

# Tab chính
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 TỔNG QUAN", "📈 BIỂU ĐỒ STATIC", "🎨 BIỂU ĐỒ TƯƠNG TÁC", 
    "☁️ WORDCLOUD", "📖 BÁO CÁO"
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
    st.subheader(f"🇻🇳 Thông Tin {selected_country}")
    
    if len(country_data) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cases = country_data['Tổng_Ca_Nhiễm'].iloc[0]
            st.metric("😷 Tổng Ca Nhiễm", f"{cases:,.0f}")
        
        with col2:
            deaths = country_data['Tổng_Tử_Vong'].iloc[0]
            st.metric("💀 Tổng Tử Vong", f"{deaths:,.0f}")
        
        with col3:
            death_rate = country_data['Tỉ_Lệ_Tử_Vong'].iloc[0]
            world_avg = df['Tỉ_Lệ_Tử_Vong'].mean()
            diff = death_rate - world_avg
            st.metric("📊 Tỉ Lệ Tử Vong", f"{death_rate:.2f}%", f"{diff:+.2f}% vs TB")
        
        with col4:
            cases_per_million = country_data['Ca_Nhiễm_Triệu_Dân'].iloc[0]
            st.metric("👥 Ca/1M Dân", f"{cases_per_million:,.0f}")
    
    # Dữ liệu thô
    st.subheader("📋 Dữ Liệu Thô (10 dòng đầu)")
    st.dataframe(df.head(10), use_container_width=True)

with tab2:
    st.header("📊 BIỂU ĐỒ STATIC - YÊU CẦU 3")
    
    # YÊU CẦU 3.1: Histogram & Boxplot
    st.subheader("1. Histogram & Boxplot - Phân Phối Tỉ Lệ Tử Vong")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histogram
    ax1.hist(df['Tỉ_Lệ_Tử_Vong'], bins=20, color='lightcoral', edgecolor='black', alpha=0.7)
    ax1.axvline(df['Tỉ_Lệ_Tử_Vong'].mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Trung bình: {df["Tỉ_Lệ_Tử_Vong"].mean():.2f}%')
    if len(country_data) > 0:
        ax1.axvline(country_data['Tỉ_Lệ_Tử_Vong'].iloc[0], color='blue', linestyle='--', linewidth=2, 
                    label=f'{selected_country}: {country_data["Tỉ_Lệ_Tử_Vong"].iloc[0]:.2f}%')
    ax1.set_xlabel('Tỉ Lệ Tử Vong (%)')
    ax1.set_ylabel('Số Quốc Gia')
    ax1.set_title('PHÂN BỐ TỈ LỆ TỬ VONG TOÀN CẦU', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Boxplot
    ax2.boxplot(df['Tỉ_Lệ_Tử_Vong'].dropna())
    ax2.set_ylabel('Tỉ Lệ Tử Vong (%)')
    ax2.set_title('BOXPLOT TỈ LỆ TỬ VONG', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # YÊU CẦU 3.2: Line & Area Chart
    st.subheader("2. Biểu Đồ Top Quốc Gia Theo Số Ca Nhiễm")
    
    top_countries = df.nlargest(top_n, 'Tổng_Ca_Nhiễm')
    
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
    ax2.set_title(f'TOP {top_n} QUỐC GIA THEO SỬ TỬ VONG', fontweight='bold')
    ax2.set_xlabel('Quốc Gia')
    ax2.set_ylabel('Tổng Tử Vong')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # YÊU CẦU 3.3: Scatter + Regression
    st.subheader("3. Scatter Plot & Hồi Quy - Mối Quan Hệ Ca Nhiễm & Tử Vong")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter = ax.scatter(df['Tổng_Ca_Nhiễm'], df['Tổng_Tử_Vong'], 
                        alpha=0.6, s=50, c=df['Tỉ_Lệ_Tử_Vong'], cmap='viridis')
    
    # Regression line
    if len(df) > 1:
        z = np.polyfit(df['Tổng_Ca_Nhiễm'], df['Tổng_Tử_Vong'], 1)
        p = np.poly1d(z)
        ax.plot(df['Tổng_Ca_Nhiễm'], p(df['Tổng_Ca_Nhiễm']), "r--", alpha=0.8, linewidth=2)
    
    ax.set_xlabel('Tổng Ca Nhiễm')
    ax.set_ylabel('Tổng Tử Vong')
    ax.set_title('MỐI QUAN HỆ GIỮA CA NHIỄM VÀ TỬ VONG', fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.colorbar(scatter, label='Tỉ Lệ Tử Vong (%)')
    
    st.pyplot(fig)
    
    # YÊU CẦU 3.4: Heatmap
    st.subheader("4. Heatmap Tương Quan")
    
    numeric_cols = ['Tổng_Ca_Nhiễm', 'Tổng_Tử_Vong', 'Tổng_Khỏi_Bệnh', 'Dân_Số', 'Tỉ_Lệ_Tử_Vong']
    correlation_matrix = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
               square=True, fmt='.2f', cbar_kws={'shrink': 0.8}, ax=ax)
    ax.set_title('HEATMAP TƯƠNG QUAN CÁC CHỈ SỐ COVID-19', fontweight='bold', pad=20)
    
    st.pyplot(fig)

with tab3:
    st.header("🎨 BIỂU ĐỒ TƯƠNG TÁC - YÊU CẦU 4")
    
    # YÊU CẦU 4.1: Scatter plot tương tác
    st.subheader("1. Scatter Plot Tương Tác")
    
    fig = px.scatter(df, x='Tổng_Ca_Nhiễm', y='Tổng_Tử_Vong', 
                     size='Dân_Số', color='Châu_Lục',
                     hover_name='Quốc_Gia', 
                     title='<b>MỐI QUAN HỆ GIỮA TỔNG CA NHIỄM VÀ TỬ VONG</b>',
                     labels={
                         'Tổng_Ca_Nhiễm': 'Tổng Ca Nhiễm',
                         'Tổng_Tử_Vong': 'Tổng Tử Vong', 
                         'Châu_Lục': 'Châu Lục',
                         'Dân_Số': 'Dân Số'
                     })
    
    # Highlight quốc gia được chọn
    if len(country_data) > 0:
        fig.add_trace(go.Scatter(
            x=country_data['Tổng_Ca_Nhiễm'],
            y=country_data['Tổng_Tử_Vong'],
            mode='markers+text',
            marker=dict(size=20, color='red', symbol='star'),
            text=[selected_country],
            textposition="top center",
            name=selected_country
        ))
    
    fig.update_layout(template='plotly_white', height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # YÊU CẦU 4.2: Bar chart tương tác
    st.subheader("2. Bar Chart So Sánh Theo Châu Lục")
    
    continent_data = df.groupby('Châu_Lục').agg({
        'Tổng_Ca_Nhiễm': 'sum',
        'Tổng_Tử_Vong': 'sum',
        'Quốc_Gia': 'count'
    }).reset_index()
    
    continent_data['Tỉ_Lệ_Tử_Vong'] = (continent_data['Tổng_Tử_Vong'] / continent_data['Tổng_Ca_Nhiễm'] * 100).round(2)
    
    fig = px.bar(continent_data, 
                 x='Châu_Lục', 
                 y='Tỉ_Lệ_Tử_Vong',
                 color='Tỉ_Lệ_Tử_Vong',
                 title='<b>TỈ LỆ TỬ VONG THEO CHÂU LỤC</b>',
                 labels={
                     'Tỉ_Lệ_Tử_Vong': 'Tỉ Lệ Tử Vong (%)', 
                     'Châu_Lục': 'Châu Lục'
                 },
                 text='Tỉ_Lệ_Tử_Vong')
    
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(template='plotly_white', height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # YÊU CẦU 4.3: Choropleth map tương tác
    st.subheader("3. Bản Đồ Tỉ Lệ Tử Vong Toàn Cầu")
    
    fig = px.choropleth(df, 
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
                        title='<b>BẢN ĐỒ TỈ LỆ TỬ VONG COVID-19 TOÀN CẦU</b>',
                        labels={'Tỉ_Lệ_Tử_Vong': 'Tỉ Lệ Tử Vong (%)'})
    
    fig.update_layout(template='plotly_white', height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("☁️ WORDCLOUD - YÊU CẦU 3.6")
    
    # Tạo wordcloud
    word_freq = {}
    for _, row in df.iterrows():
        size = max(10, int(row['Tổng_Ca_Nhiễm'] / 1000000))
        word_freq[row['Quốc_Gia']] = size
    
    wordcloud = WordCloud(width=800, height=400, 
                          background_color='white',
                          colormap='Reds',
                          max_words=50).generate_from_frequencies(word_freq)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('WORDCLOUD CÁC QUỐC GIA THEO SỐ CA NHIỄM\n(Kích thước thể hiện mức độ ảnh hưởng)', 
                fontsize=14, fontweight='bold', pad=20)
    
    st.pyplot(fig)

with tab5:
    st.header("📖 BÁO CÁO PHÂN TÍCH - YÊU CẦU 5")
    
    # Tạo báo cáo storytelling
    if len(country_data) > 0:
        country_death_rate = country_data['Tỉ_Lệ_Tử_Vong'].iloc[0]
        country_cases_per_million = country_data['Ca_Nhiễm_Triệu_Dân'].iloc[0]
        world_avg_death_rate = df['Tỉ_Lệ_Tử_Vong'].mean()
        world_avg_cases_per_million = df['Ca_Nhiễm_Triệu_Dân'].mean()
    else:
        country_death_rate = world_avg_death_rate = world_avg_cases_per_million = 0
    
    storytelling_content = f"""
    # 📊 BÁO CÁO PHÂN TÍCH COVID-19
    ## {selected_country.upper()} TRONG BỐI CẢNH TOÀN CẦU

    **Thông tin sinh viên:** Nguyễn Mạnh Dũng - B22DCCN132  
    **Môn học:** Khai phá dữ liệu  
    **Ngày tạo báo cáo:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

    ---

    ### 📊 TỔNG QUAN DỮ LIỆU
    - **Số quốc gia phân tích:** {len(df)}
    - **Tổng số ca nhiễm toàn cầu:** {df['Tổng_Ca_Nhiễm'].sum():,}
    - **Tổng số tử vong toàn cầu:** {df['Tổng_Tử_Vong'].sum():,}
    - **Tỉ lệ tử vong trung bình:** {df['Tỉ_Lệ_Tử_Vong'].mean():.2f}%

    ### 🇻🇳 ĐÁNH GIÁ TÌNH HÌNH {selected_country.upper()}

    #### 📈 CHỈ SỐ CHÍNH:
    - **Tổng ca nhiễm:** {country_data['Tổng_Ca_Nhiễm'].iloc[0] if len(country_data) > 0 else 'N/A':,}
    - **Tổng tử vong:** {country_data['Tổng_Tử_Vong'].iloc[0] if len(country_data) > 0 else 'N/A':,}
    - **Tỉ lệ tử vong:** {country_death_rate:.2f}% ({'THẤP HƠN' if country_death_rate < world_avg_death_rate else 'CAO HƠN'} trung bình thế giới)
    - **Ca nhiễm/1 triệu dân:** {country_cases_per_million:,.0f} ca

    #### 📊 SO SÁNH VỚI TRUNG BÌNH THẾ GIỚI:
    | Chỉ Số | {selected_country} | Trung Bình Thế Giới | Chênh Lệch |
    |--------|-------------------|-------------------|------------|
    | Tỉ lệ tử vong | {country_death_rate:.2f}% | {world_avg_death_rate:.2f}% | {country_death_rate - world_avg_death_rate:+.2f}% |
    | Ca/1M dân | {country_cases_per_million:,.0f} | {world_avg_cases_per_million:,.0f} | {country_cases_per_million - world_avg_cases_per_million:+,.0f} |

    ### 🔍 PHÂN TÍCH CHUYÊN SÂU

    #### 📈 XU HƯỚNG TOÀN CẦU:
    - Phân bố tỉ lệ tử vong **không đồng đều** giữa các quốc gia
    - Mối tương quan mạnh giữa **tổng ca nhiễm** và **tổng tử vong**
    - Các nước phát triển có hệ thống y tế tốt thường có **tỉ lệ tử vong thấp hơn**

    #### 🎯 ĐÁNH GIÁ {selected_country.upper()}:
    - **Điểm mạnh:** {'Tỉ lệ tử vong thấp' if country_death_rate < world_avg_death_rate else 'Cần cải thiện hệ thống y tế'}
    - **Thách thức:** {'Kiểm soát số ca nhiễm' if country_cases_per_million > world_avg_cases_per_million else 'Duy trì thành tích'}

    ### 💡 KHUYẾN NGHỊ

    #### ĐỐI VỚI {selected_country.upper()}:
    1. **Duy trì hệ thống giám sát dịch tễ**
    2. **Tăng cường năng lực xét nghiệm và điều trị**
    3. **Chuẩn bị sẵn sàng cho các biến chủng mới**

    #### BÀI HỌC TOÀN CẦU:
    1. **Minh bạch dữ liệu** là chìa khóa kiểm soát dịch
    2. **Hợp tác quốc tế** trong nghiên cứu và phát triển vaccine
    3. **Ứng dụng công nghệ** trong truy vết và giám sát

    ---
    *Báo cáo được tạo tự động từ dữ liệu thực tế - Có thể refresh để cập nhật*
    """
    
    st.markdown(storytelling_content)
    
    # Nút export báo cáo
    if st.button("📥 Export Báo Cáo"):
        with open(f'bao_cao_covid19_{datetime.now().strftime("%Y%m%d_%H%M")}.md', 'w', encoding='utf-8') as f:
            f.write(storytelling_content)
        st.success("✅ Đã xuất báo cáo!")

# Footer
st.markdown("---")
st.markdown(
    "**Bài tập giữa kỳ - Môn Khai phá dữ liệu** • "
    "**Nguyễn Mạnh Dũng - B22DCCN132** • "
    "**PTIT - 2024**"
)