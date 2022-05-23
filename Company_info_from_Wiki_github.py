# 爬文台積電及鴻海簡史 selenium輸入抓 用dict 合併相同key變df
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import bs4
import requests
import pandas as pd

url = 'https://zh.wikipedia.org/wiki/Wikipedia:%E9%A6%96%E9%A1%B5'
driver_path = Service('D:\chromedriver.exe')
driver = webdriver.Chrome(service=driver_path)
driver.get(url)

company_name_list = ['台積電', '叡揚資訊', '華碩',
                     '友達', '鴻海', '葡萄王', '三洋電機', '台塑']  # ,'鴻海','華碩'
big_company_list = []
big_name_list = [list() for n in range(len(company_name_list))]
big_content_list = [list() for n in range(len(company_name_list))]

for c in company_name_list:
    driver.find_element(
        By.CSS_SELECTOR, '.vector-search-box-input').send_keys(c)
    driver.find_element(By.CSS_SELECTOR, '#searchButton').click()
    time.sleep(2)
    # 因為每個公司的資訊標題不同 所以要轉成list區隔
    name_list, content_list = [], []
    # 每次新增到大list後要清空在放下一個公司的資訊
    name_list.clear()
    content_list.clear()

    obj_soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
    obj_info = obj_soup.find('table', 'infobox').tbody.find_all('tr')
    for info in obj_info:
        index = info.find('th', 'fn org')
        en_index = info.find('td', style='text-align:center')
        th_row = info.find('th', scope='row')
        td = info.td
        # 如果tr內有符合 公司名稱 的標籤
        if index:
            print(index.text.strip())
            name = index.text.strip()
        # 如果tr內有符合 公司英文名稱 的標籤
        if en_index:
            print(en_index.text.strip())
        # 如果tr內有符合 公司資訊 的標籤
        if th_row and td:
            print(th_row.text.strip(), '-', td.text.strip())
            # 先把公司資訊加到list
            name_list.append(th_row.text.strip())  # 標題
            content_list.append(td.text.strip())   # 內容
            # 轉成{標題:內容}的dict
            company_dict = dict(zip(name_list, content_list))
    # print(company_dict)
    # 把公司名稱當keys 建立更大的dict以做區隔 {公司:{標題:內容}}
    company_dict = {name: company_dict}
    # 再加到list
    big_company_list.append(company_dict)
print(big_company_list)  # 重要格式

driver.close()

# 建立空list
value_list = [list() for n in range(len(big_company_list))
              ]  # 大list的values 就是標題和內容資訊
df_list = [list() for n in range(len(big_company_list))]

for i, obj in enumerate(big_company_list):
    # print(obj)
    # dict.kes()或values()一定要轉list才能使用
    value_list[i] = list(obj.values())
#     print(value_list[i][0].keys())
#     print(value_list[i][0].values())

    # 橫向印出
    # df=pd.DataFrame([value_list[i][0].values()],columns=value_list[i][0].keys(),index=obj.keys())
    df_list[i] = pd.DataFrame(value_list[i][0].values(
    ), index=value_list[i][0].keys(), columns=obj.keys())
    # print(df[i])

df_ = df_list[0]   # 一開始=索引1的df
n = 0
for i in range(len(df_list)):
    # print(df[i])
    print(n)
    n += 1
    # 超過len(list)就跳出
    if n < len(df_list):
        # 某df.merge(要合併的df ,how合併方式='inner'相同的才留著 'outer'全都留著 ,left_index某df的index要引入嗎 ,right_index要合併的df的index要引入嗎)
        # 每次合併完的df就成為索引1的df
        df_ = df_.merge(df_list[n], how='outer',
                        left_index=True, right_index=True)
        print('-'*30)
    else:
        break
df_ = df_.T  # 轉換方向
df_.to_csv('Csvs/Company_info_from_Wiki.csv')
print(df_)
