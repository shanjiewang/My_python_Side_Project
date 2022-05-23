# 因為是動態加載的網頁 所以先把全部網頁內容都載完 再一行行寫入csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import bs4
import requests
import os
import csv

input_ = input('請輸入想查詢的關鍵字:')

# 用selenium找到頁面
url = 'https://udn.com/news/index'
driver_path = Service('D:/chromedriver.exe')
driver = webdriver.Chrome(service=driver_path)
driver.get(url)
driver.find_element(By.CLASS_NAME, 'menu-toggler').click()
# 透過css找到搜尋鍵並按下
find_what = driver.find_element(
    By.CSS_SELECTOR, "div.input-holder input[type='search']")
find_what.send_keys(input_)  # 送出要搜尋的字串
time.sleep(3)
driver.find_element(By.CLASS_NAME, 'btn-search').click()
url_1 = driver.current_url  # 找到點入的網址
print(url_1)
time.sleep(3)

# 用bs4找出共幾頁
html = requests.get(url_1)
obj = bs4.BeautifulSoup(html.text, 'lxml')

total_num = obj.find('div', 'search-total').span.text.strip()
print('共', total_num, '篇文章')
total_num = int(int(total_num)/20)
print(total_num)

count_num = 0  # 紀錄滑了幾次
add_num = 100  # 卷軸要滑的距離

# 執行次數至網頁完全載入 才能一次存爬取內容
for top in range(total_num):
    use_keys = driver.find_element(By.TAG_NAME, 'body')
    time.sleep(5)
    count_num += 1
    print('第 %s 次' % count_num)
    add_num += 20  # 因為卷軸會越來越長

    # 讓卷軸不段滑的for
    for down in range(0, add_num, 2):
        use_keys.send_keys(Keys.PAGE_DOWN)  # 往下快快滑到底 讓網頁動態加載
    time.sleep(5)
    use_keys.send_keys(Keys.HOME)   # 再直接滑到最頂
    new_pega = driver.page_source    # 重新抓取加載後的網頁內容
    new_obj = bs4.BeautifulSoup(new_pega, 'lxml')     # 轉成bs4

# print(new_obj)
# time.sleep(5)
org_divs = obj.find(
    'div', 'story-list__holder').find_all('div', 'story-list__news')
# pp=obj.find('div','story-list__holder').find('section','story-list__holder--append') #.find_all('div','story-list__news  ')
print('原本就在的文章數:', len(org_divs))
new_divs = new_obj.find('div', 'story-list__holder').find('section',
                                                          'story-list__holder--append').find_all('div', 'story-list__news')
print('動態加載後文章數:', len(new_divs))

txt_list = []  # 給需要的文字內容建成表格用
photo_list = []   # 給圖片用
photo_dir = 'find_'+input_
file_dir = 'Csvs'

if os.path.exists(photo_dir) == False:
    os.mkdir(photo_dir)
if os.path.exists(file_dir) == False:
    os.mkdir(file_dir)

# 原本就在的文章
for org in org_divs:
    s = org.find('div', 'story-list__text')
    title = s.h2.text.strip()
    date = s.find('time', 'story-list__time').text.strip()
    content = s.p.text.strip()
    photo_src = org.find('div', 'story-list__image').img['data-src']

    print('標題:', title)
    print('日期:', date)
    print('內文:', content)
    print('圖片連結:', photo_src)
    print()
    txt_list.append([title, date, content, photo_src])
    photo_list.append(photo_src)

print(len(txt_list))
print(len(photo_list))
print('-'*70)

df_file = 'find_'+input_+'.csv'

# 動態加載後的文章
for new in new_divs:
    n = new.find('div', 'story-list__text')
    title = n.h2.text.strip()
    date = n.find('time', 'story-list__time').text.strip()
    content = n.p.text.strip()
    photo_src = new.find('div', 'story-list__image').img['data-src']

    print('標題:', title)
    print('日期:', date)
    print('內文:', content)
    print('圖片連結:', photo_src)
    print()
    txt_list.append([title, date, content, photo_src])
    photo_list.append(photo_src)

with open(os.path.join(file_dir, df_file), 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    for row in txt_list:
        try:
            csv_writer.writerow(row)   # 一行行寫入 節省電腦效能 避免內容過多
            print('寫入成功')
        except Exception:
            print('寫入失敗')
            pass
print('====')
print(txt_list)
print(photo_list)

# 下載圖片並存檔
print(len(photo_list))
for photo in photo_list:
    photo_name = os.path.basename(photo).split('.')[0]+str('.jpg')
    print(photo_name)
    try:
        load_photo = requests.get(photo)
        load_photo.raise_for_status()
        print('圖片下載成功')
        photo_file = open(os.path.join(photo_dir, photo_name), 'wb')
        for l in load_photo.iter_content(10240):
            photo_file.write(l)
        photo_file.close()
    except Exception as err:
        print('圖片下載失敗')
print('---所有圖片下載完成---')

driver.close()
