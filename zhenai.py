from bs4 import BeautifulSoup
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


driver = webdriver.Chrome(
    '/home/wcg/software/chromedriver', options=chrome_options)


def get_html(uid):
    driver.get('http://album.zhenai.com/u/{}'.format(uid))
    return driver.page_source


def get_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    avatar = soup.find_all(class_='logo f-fl')[0]['style']
    user_id = soup.find_all(class_='id')[0].get_text()
    user_info = soup.find_all(class_='des f-cl')[0].get_text()
    images = soup.find_all(class_='photoItem z-cursor-big active')
    print(avatar, user_id, user_info, images)


def main():
    tasks = ['1628055964']
    for i in tasks:
        html = get_html(i)
        get_info(html)


if __name__ == '__main__':
    main()
