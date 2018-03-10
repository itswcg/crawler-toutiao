from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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


if __name__ == '__main__':
    get_urls('https://www.toutiao.com/c/user/6855346091/#mid=6854352286')
