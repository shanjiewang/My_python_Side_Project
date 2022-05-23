# 進中時新聞網 把體育的最新新聞總覽文章全抓下來 並另存照片
# 用selenium跑完動態瀏覽 用bs4抓靜態頁面

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait
# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import bs4
import os
import csv
import pandas as pd

url = 'https://www.chinatimes.com'
driver_path = Service('D:/chromedriver.exe')
driver = webdriver.Chrome(service=driver_path)
driver.get(url)

driver.find_element(
    By.CSS_SELECTOR, '.main-nav-wrapper ul li[data-id="sports"]').click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, '.article-list .more a').click()
time.sleep(1)

# 去抓最後一頁 知道總共有幾頁
total_page = driver.find_elements(By.CSS_SELECTOR, '.pagination li')[13]
print(total_page.text)
total_page.click()  # 確定抓到最後一頁標籤再click
time.sleep(2)

# 拆解網址
new_urls = driver.current_url  # 要記得用driver才抓得到current_url當下的頁面
# print(new_urls)
front_url = new_urls.split('=')[0]   # page前網址
other = new_urls.split('=')[1].split('&')[1]   # 網址後面那些字串
total_num = new_urls.split('=')[1].split('&')[0]   # 總頁數
print(total_num)

# 回到第1頁 是數字的1 比較好寫for
first_page = driver.find_elements(By.CSS_SELECTOR, '.pagination li')[2]
print(first_page.text)
time.sleep(2)
first_page.click()

print('是全網址嗎:', front_url, '=頁數&', other)
count_t = 0  # 頁數
count_f = 0  # 每頁內文數
all_list = []

# 確定抓到最後一頁標籤再click
for t in range(1, int(total_num)+1):
    new_url = front_url+'='+str(t)+str('&')+other
    # print(new_url)

    # 轉換成bs4
    new_html = requests.get(new_url)
    new_obj = bs4.BeautifulSoup(new_html.text, 'lxml')

    find_divs = new_obj.find(
        'ul', 'vertical-list').find_all('div', 'articlebox-compact')

    count_t += 1
    print('\n***第', count_t, '頁***\n')

    for f in find_divs:
        title = f.h3.text.strip()
        date = f.find('time').find('span', 'date').text.strip()
        category = f.find('div', 'category').a.text.strip()
        content = f.p.text.strip()
        url_href = f.find('div', 'cropper').a['href']
        url_href = url+url_href
        img_href = f.find('div', 'cropper').img['src']
#         print(title)
#         print(date)
#         print(category)
#         print(content)
#         print(url_href)
#         print(img_href)
        all_list.append([title, date, category, content, url_href, img_href])
        # print(all_list[count_f])
        count_f += 1
        print(len(all_list))
        print('-'*70)


# 存成csv
df_1 = pd.DataFrame(all_list, columns=['標題', '日期', '類別', '內文', '內文網址', '圖片網址'])
df_1.to_csv('chinatimesWeb.csv')

# 下載圖片區
img_Dir = 'chinatimesWeb'
if os.path.exists(img_Dir) == False:
    os.mkdir(img_Dir)
img_list = list(df_1['圖片網址'])  # 將圖片網址欄位轉換成list比較好處理
print(img_list)

for img in img_list:
    try:
        loads_img = requests.get(img)
        # load_img.raise_for_status()
        print(img, '圖片下載完成')
        img_file = open(os.path.join(img_Dir, os.path.basename(img)), 'wb')
        for l in loads_img.iter_content(10240):
            img_file.write(l)
        img_file.close()
    except Exception as err:
        # 如果圖片下載失敗  1.一定是打錯字   2.loads_img和img_file寫錯   3.註解load_img.raise_for_status()
        print('圖片下載失敗')
print('---所有圖片下載完成---')

driver.close()
df_1
