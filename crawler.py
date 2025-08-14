import time

from config import Config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from seleniumbase import Driver

def search_web():
    # 使用seleniumbase避免cloudflare驗證
    driver = seleniumbase_driver(Config.org_url)

    # 關鍵字搜尋
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'searchText'))
    )
    element.send_keys(Config.keyword)
    element.submit()

    # cookie彈出視窗
    try:
        cookie_ok_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_ok_button.click()
    except:
        print("no cookie popup")

    result = Config.result
    # 每頁資料擷取
    is_next = True
    while is_next:
        # 逐頁開啟
        for search_one in search_page_by(driver):
            driver.execute_script(f'window.open("{search_one}")')
            driver.switch_to_window(driver.window_handles[1])
            per_page(driver,result)
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
        # 換頁
        is_next = next_to_page(driver)
            
    return result

# 啟動驅動
def seleniumbase_driver(url):
    driver = Driver(uc=True)
    driver.uc_open_with_reconnect(Config.org_url,reconnect_time=6) 
    return driver

# 換頁
def next_to_page(driver):
    for i in range(Config.retry_time):
        try:
            next_page = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.LINK_TEXT,'next')))
            next_page.click()
            return True
        except:
            continue
    print('no next page')
    return False
    
# 搜索結果取得url之生成器
def search_page_by(driver):
    all_urls_page = driver.find_elements(By.CLASS_NAME,'meta__title')

    for url_one in all_urls_page:
        if url_one.text != '':
            one = url_one.find_element(By.TAG_NAME,'a').get_attribute('href')
            yield one

# 論文詳細
def per_page(driver,result):
    time.sleep(1)
    # 獲取論文標題
    title = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'.core-container h1'))
        )

    result['title'].append(title.text)
    print(title.text)

    # 獲取論文url
    url = driver.current_url
    result['Article URL'].append(url)
    print(url)

    # 獲取論文狀態
    type = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'.meta-panel__left-content > .meta-panel__type > span'))
        )
    result['Article Type'].append(type.text)
    print(type.text)

    # DOI
    try:
        doi = driver.find_element(By.XPATH,"//span[@class='doi']/a").get_attribute('href')        
    except:
        doi = ''

    print(doi)  
    result['DOI Number'].append(doi)

    # 發布時間
    try:
        date = driver.find_elements(By.XPATH,"//*[@id='core-content-info']/div[1]/div[2]/span")
        for j in date:
            print(j.get_attribute('textContent'))
        date_time = ';'.join([j.get_attribute('textContent') for j in date])
    except:
        date_time = ''

    print(date_time)
    result['Publication Date'].append(date_time)

    # 下載url
    try:
        D_url = driver.find_element(By.XPATH,"//li[@class='article-tools__item article-tools__pdf']/a").get_attribute('href')
    except:
        D_url = ''

    print(D_url)
    result['PDF download URL'].append(D_url)
    # 期刊名稱
    try:
        name = driver.find_element(By.CSS_SELECTOR,'.linked-article__details span i').get_attribute('textContent')
    except:
        name = ''

    print(name)
    result['Journal Name'].append(name)

    print('==='*20)






    

    

