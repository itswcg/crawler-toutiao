from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import html2text
import pdfkit
from PyPDF2 import PdfFileMerger

driver = webdriver.Chrome('/usr/local/bin/chromedriver')


def get_urls(url):
    driver.get(url)
    time.sleep(1)
    driver.refresh()
    driver.implicitly_wait(2)
    for i in range(10000):
        #driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        ActionChains(driver).key_down(Keys.DOWN).perform()
        print(f'已完成{i}次')

    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    body = soup.find_all(class_='link title')
    for i in range(len(body)):
        # title = body[i].get_text()
        url = 'https://www.toutiao.com' + body[i].get('href')
        print(f'已完成{i}个')
        with open('urls.txt', 'a') as f:
            f.writelines(url)
            f.write('\n')
    driver.quit()


def get_htmls():
    with open('urls.txt', 'r') as f:
        urls = f.readlines()
    l = len(urls)
    htmls = []
    for i in range(l):
        print(urls[i])
        driver.get(urls[i])
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            body = str(soup.find_all(class_='article-title')[0]) + str(soup.find_all(
                class_='article-sub')[0]) + str(soup.find_all(class_='article-content')[0])
        except IndexError:
            driver.refresh()
            time.sleep(2)
        if not os.path.exists('htmls'):
            os.mkdir('htmls')
        with open(f'htmls/{i}.html', 'w') as f:
            f.write(body)
        print(f'{i}.html 完成, 共{l}个')
        time.sleep(3)
    driver.quit()


def markdown():
    for i in range(100):
        with open(f'htmls/{i}.html', 'r') as f:
            data = f.read()
        html = html2text.html2text(data)
        with open(f'htmls/m{i}.md', 'w') as f:
            f.write(html)
        print(f'{i}完成')


def pdf():
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'outline-depth': 10,
    }
    htmls = []
    for i in range(100):
        with open(f'htmls/{i}.html', 'r') as f:
            data = f.read()
        htmls.append(f'htmls/{i}.html')
        print(f'完成{i}个')
    pdfkit.from_file(htmls, 'out.pdf', options=options)


def merge_pdf():  # 上面pdf函数，不能处理很多的html，所以要分下来，再合并
    merger = PdfFileMerger()
    for i in range(100):
        merger.append(open(f'htmls/{i}.pdf', 'rb'))
    merger.write(open('out.pdf', 'wb'))


if __name__ == '__main__':
    get_urls('https://www.toutiao.com/c/user/6855346091/#mid=6854352286')
    get_htmls()
