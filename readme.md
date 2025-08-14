# 論文網站爬蟲

## 專案介紹

搜索論文網站並進行關鍵字論文搜尋，並下載相關資料，最後儲存成csv檔

## 安裝

- numpy 2.2.6
- pandas 2.3.1
- selenium 4.34.2
- seleniumbase 4.40.8

## Config

|參數|類型|說明|舉例|
|-----|-----|-----|-----|
|org_url|str|網站路徑|'https://www.annalsofoncology.org/'|
|keyword|str|搜尋關鍵字|'breast cancer'|
|retry_time|int|換頁重試次數|3|
|save_place|str|csv檔路徑|'result.csv'|
|result|dict|空資料集|{ 'title':[],<br> 'Article URL':[],<br> 'Article Type':[],<br> 'DOI Number':[],<br> Publication Date':[],<br> 'PDF download URL':[],<br> 'Journal Name':[] }|

## Usage

```bash
pip install -r requirements.txt
python main.py
```
