# 把排行榜玄幻小說前3名全部下載下來
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import bs4
import os

fantasys_data_list = []

url = 'https://www.bqkan8.com'
driver_path = Service('D:/chromedriver.exe')
driver = webdriver.Chrome(service=driver_path)
driver.get(url)

driver.find_element(By.CSS_SELECTOR, '.nav').find_elements(
    By.TAG_NAME, 'li')[-2].click()
obj_soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

# 直接找到玄幻小說前3名網址
obj_fantasys = obj_soup.find_all('div', 'block bd')[1].find_all('li', 'top')
for fantasy in obj_fantasys:
    fantasys_title = fantasy.a.text
    print(fantasy.a['href'], fantasys_title)
    fantasys_url = url+fantasy.a['href']
    fantasys_data_list.append([fantasy.a.text, fantasys_url])

print(fantasys_data_list)


def Loads_txts_fn(f_title, f_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
    html = requests.get(f_url)
    html.encoding = 'gbk'
    obj_soup = bs4.BeautifulSoup(html.text, 'lxml')

    txt_dir = f_title+'_dir'
    if os.path.exists(txt_dir) == False:
        os.mkdir(txt_dir)

    # 要移除的多餘內容
    remove_list = ['&1t;/p>', '&nbsp;', ' ', '/', '?', '\\',
                   '请记住本书首发域名：www.bqkan8.com。笔趣阁手机版阅读网址：m.bqkan8.com']

    obj_div = obj_soup.find('div', 'listmain').dl.find_all('dd')
    # 如果爬到一半斷掉 可以從這裡改變數字 obj_div[630:650]
    for i, obj in enumerate(obj_div[630:640]):
        story = ''  # 變空值存下一回
        # print(i)  # 用索引方式得知前12回不要 所以從第12開始[12:]
        book_title = obj.text.strip()+'.txt'
        book_url = 'https://www.bqkan8.com'+obj.a['href']
        remove_ = '('+book_url+')'
        remove_list.append(remove_)

        # 進入文章網頁抓內文
        content_html = requests.get(book_url)
        content_html.encoding = 'gbk'
        content_soup = bs4.BeautifulSoup(content_html.text, 'lxml')

        content_h1 = content_soup.find('h1').text.strip()+'\n'
        story = story+content_h1+'\n'
        # 因為要檢查 所以後面不可加不可加text.strip()
        content_txt = content_soup.find('div', id='content')
        # 一段一段檢查 要檢查的內文要是完整的html 不可加text.strip()
        for content in content_txt:
            if type(content) == bs4.element.NavigableString:
                txt_content = content.text.strip()  # 這裡就一定要加text.strip() 不然下面無法判斷type=str
                # print(txt_content)
                if type(txt_content) == str and txt_content != '':
                    txt_content = content
                    for r in remove_list:
                        txt_content = txt_content.replace(r, '')
                    story = story+txt_content+'\n\n'
    #         else:
    #             print('NO')
        # print(story)
        txt_file = open(os.path.join(txt_dir, book_title),
                        'w', newline='', encoding='utf-8')
        try:
            txt_file.write(story)
            print('儲存成功', book_title)
            print(i)
        except Exception:
            print('儲存失敗')
    print('全部儲存完成')
    txt_file.close()


# 依序把前3名的所有小說內容存成txt
for f_title, f_url in fantasys_data_list:
    print(f_title)
    print(f_url)
    Loads_txts_fn(f_title, f_url)  # def要在前面才可執行

driver.close()
