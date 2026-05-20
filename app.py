import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.express as px

# 設定網頁標題與圖示
st.set_page_config(page_title="TWSE 籌碼追蹤器", page_icon="📈", layout="wide")

# --- 爬蟲核心邏輯 (加上快取以節省頻寬與防止被擋) ---
@st.cache_data(ttl=3600)  # 資料快取 1 小時
def fetch_twse_data(date_str):
    url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date={date_str}&selectType=ALL&response=json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.twse.com.tw/zh/page/trading/fund/T86.html'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data if data.get('stat') == 'OK' else None
    except:
        return None
    return None

def process_data(all_data_list):
    all_dfs = []
    for day_data in all_data_list:
        df = pd.DataFrame(day_data['data'], columns=day_data['fields'])
        df.columns = [c.strip() for c in df.columns]
        
        foreign_cols = [c for c in df.columns if '外資' in c and '買賣超股數' in c] or \
                       [c for c in df.columns if '外陸資' in c and '買賣超股數' in c]
        total_inst_col = [c for c in df.columns if '三大法人買賣超股數' in c][0]
        
        for col in foreign_cols + [total_inst_col]:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            
        df['外資買賣超(張)'] = (df[foreign_cols].sum(axis=1) / 1000).round(2)
        df['三大法人買賣超(張)'] = (df[total_inst_col] / 1000).round(2)
        
        all_dfs.append(df[['證券代號', '證券名稱', '外資買賣超(張)', '三大法人買賣超(張)']])

    combined_df = pd.concat(all_dfs)
    summary_df = combined_df.groupby(['證券代號', '證券名稱']).sum().reset_index()
    
    # 強制再次四捨五入，並重新命名為「累計」
    summary_df['累計外資(張)'] = summary_df['外資買賣超(張)'].round(2)
    summary_df['累計三大法人(張)'] = summary_df['三大法人買賣超(張)'].round(2)
    
    # 計算日均
    days_count = len(all_data_list)
    summary_df['外資日均(張)'] = (summary_df['累計外資(張)'] / days_count).round(2)
    summary_df['三大法人日均(張)'] = (summary_df['累計三大法人(張)'] / days_count).round(2)
    
    # 移除舊的欄位，保持乾淨
    return summary_df[['證券代號', '證券名稱', '累計外資(張)', '累計三大法人(張)', '外資日均(張)', '三大法人日均(張)']]

# --- Streamlit UI 介面 ---
st.title("📈 TWSE 三大法人籌碼追蹤工具")
st.markdown("只要一鍵點擊，自動抓取證交所官方資料並統計近期的籌碼動向。")

# 側邊欄設定
st.sidebar.header("分析設定")
target_days = st.sidebar.slider("分析天數", min_value=1, max_value=20, value=10)
st.sidebar.info("註：為了遵守證交所爬蟲規範，每次請求後會延遲 4 秒。抓取 10 天大約需要 50 秒。")

if st.sidebar.button("🚀 開始獲取最新資料"):
    collected_days = 0
    current_date = datetime.now()
    all_trading_data = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    while collected_days < target_days:
        date_str = current_date.strftime('%Y%m%d')
        status_text.text(f"🔍 正在檢查 {date_str} 的資料...")
        
        data = fetch_twse_data(date_str)
        
        if data:
            all_trading_data.append(data)
            collected_days += 1
            # 更新進度條
            progress_bar.progress(collected_days / target_days)
            status_text.text(f"✅ 已成功搜集 {collected_days}/{target_days} 個交易日...")
            time.sleep(4)
        
        current_date -= timedelta(days=1)
        # 防止無限循環 (例如遇到長假)
        if (datetime.now() - current_date).days > 40:
            break
            
    if all_trading_data:
        final_df = process_data(all_trading_data)
        
        # --- 數據呈現 ---
        st.success(f"任務完成！已成功分析近 {target_days} 個交易日的籌碼。")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 三大法人累計買超前 10 名")
            top_buy = final_df.sort_values(by='累計三大法人(張)', ascending=False).head(10)
            fig_buy = px.bar(top_buy, x='證券名稱', y='累計三大法人(張)', color='累計三大法人(張)', 
                             color_continuous_scale='Reds', text_auto=True,
                             labels={'累計三大法人(張)': '累計買超(張)'})
            st.plotly_chart(fig_buy, use_container_width=True)
            
        with col2:
            st.subheader("❄️ 三大法人累計賣超前 10 名")
            top_sell = final_df.sort_values(by='累計三大法人(張)', ascending=True).head(10)
            fig_sell = px.bar(top_sell, x='證券名稱', y='累計三大法人(張)', color='累計三大法人(張)', 
                              color_continuous_scale='Blues_r', text_auto=True,
                              labels={'累計三大法人(張)': '累計賣超(張)'})
            st.plotly_chart(fig_sell, use_container_width=True)
            
        # 完整表格呈現
        st.subheader(f"📋 近 {target_days} 日完整統計表 (Top 50 買超)")
        full_buy_50 = final_df.sort_values(by='累計三大法人(張)', ascending=False).head(50)
        st.dataframe(full_buy_50, use_container_width=True)
        
        # 下載按鈕
        csv = full_buy_50.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="📥 下載完整買超前 50 名 CSV",
            data=csv,
            file_name=f'三大法人近{target_days}日買超統計.csv',
            mime='text/csv',
        )
    else:
        st.error("抱歉，無法抓取到資料，請稍後再試。")
else:
    st.info("請點擊左側側邊欄的按鈕開始分析。")

st.divider()
st.caption("資料來源：臺灣證券交易所官方 API | 本工具僅供參考，投資請自行評估風險。")
