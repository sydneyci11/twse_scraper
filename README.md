# 📈 台灣證券交易所三大法人籌碼追蹤工具 (TWSE Tracker)

<p align="left">
  <a href="#中文說明">中文說明</a> | 
  <a href="#english-description">English Description</a>
</p>

---

## 中文說明

一個基於 Python 與 Streamlit 打造的輕量化台灣股市籌碼面統計工具，透過直接呼叫臺灣證券交易所 (TWSE) 官方開放 API，自動統計近期三大法人資金連續佈局或調節的焦點個股，並提供視覺化圖表與數據下載功能。

### 線上體驗

👉 **[https://sydneyci-twse-scraper.streamlit.app/](https://sydneyci-twse-scraper.streamlit.app/)**

### 核心功能

| 功能 | 說明 |
|------|------|
| **自動抓取數據** | 一鍵獲取近 1 ~ 20 個交易日的官方三大法人買賣日報 |
| **智能日期偵測** | 自動跳過週末與國定假日，精準鎖定有開盤的交易日 |
| **數據清洗與聚合** | 自動將股數換算為張數，並加總累計買賣超 |
| **資料快取優化** | 同一小時內重複查詢自動啟用快取，保護伺服器效能 |
| **互動式圖表** | 使用 Plotly 呈現買超/賣超前 10 名的視覺化長條圖 |
| **匯出 CSV** | 一鍵下載，`utf-8-sig` 編碼確保 Excel 開啟不亂碼 |

### 技術棧

- **語言**：Python 3.10+
- **網頁框架**：Streamlit
- **數據處理**：Pandas
- **圖表套件**：Plotly
- **資料來源**：[臺灣證券交易所 (TWSE) 官方開放 API](https://openapi.twse.com.tw/)

### 本地開發與啟動

1. **Clone 專案**
   ```bash
   git clone https://github.com/sydneyci11/twse_scraper.git
   cd twse_scraper
   ```

2. **建立虛擬環境並安裝套件**
   ```bash
   python -m venv .venv
   ./.venv/bin/pip install -r requirements.txt
   ```

3. **啟動應用程式**
   ```bash
   ./.venv/bin/streamlit run app.py
   ```

4. 開啟瀏覽器前往 `http://localhost:8501`

### ❗️ 免責聲明 ❗️

> 本工具僅供學術研究與個人參考使用，**不構成任何投資建議**。投資有風險，請自行評估。

---

## English Description

A lightweight Taiwan stock market institutional flow analysis tool built with Python and Streamlit. By integrating the official Taiwan Stock Exchange (TWSE) open API, it automatically aggregates recent institutional investor trends and provides interactive visualizations and data export capabilities.

### Live Demo

👉 **[https://sydneyci-twse-scraper.streamlit.app/](https://sydneyci-twse-scraper.streamlit.app/)**

### Key Features

| Feature | Description |
|---------|-------------|
| **Automatic Data Retrieval** | Fetch official daily institutional investor reports for the last 1–20 trading days with one click |
| **Smart Date Detection** | Automatically skips weekends and national holidays to target valid trading days |
| **Data Cleaning & Aggregation** | Converts share counts to lot counts (1,000 shares) and sums cumulative net buy/sell |
| **Cache Optimization** | Repeated queries within the same hour use cached data to protect server performance |
| **Interactive Visualizations** | High-quality bar charts showing the Top 10 net buyers and sellers using Plotly |
| **CSV Export** | One-click download in `utf-8-sig` format for full Microsoft Excel compatibility |

### Tech Stack

- **Language**: Python 3.10+
- **Framework**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Data Source**: [Taiwan Stock Exchange (TWSE) Official Open API](https://openapi.twse.com.tw/)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/sydneyci11/twse_scraper.git
   cd twse_scraper
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv .venv
   ./.venv/bin/pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   ./.venv/bin/streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501`

### ❗️ Disclaimer ❗️

> This tool is for **educational and personal reference only** and does not constitute any investment advice. Investing involves risk; please evaluate accordingly.

---

<div align="center">
  Made with interest using Python & Streamlit &nbsp;|&nbsp; Data from <a href="https://openapi.twse.com.tw/">TWSE Open API</a>
</div>
