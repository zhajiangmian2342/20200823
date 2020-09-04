import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class KeyWord:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    # 找元素的方法(显性等待)
    def find(self, el, parameter):
        by = parameter['by']
        selector = parameter['selector']

        el = WebDriverWait(self.driver, timeout=30, poll_frequency=1).until(lambda x: x.find_element(by, selector))
        return el

    # 点击
    def click(self,el,parameter):
        el.click()
        return el

    # 打开浏览器
    def get(self, el, parameter):
        url = parameter['value']
        self.driver.get(url)

    # 输入(清空,在输入)
    def send(self,el, parameter):
        value = parameter['value']
        el.clear()
        el.send_keys(value)
        return el

    def wait(self, el, parameter):
        # 从excel里面读取的数据是字符串类型
        value = parameter['value']
        time.sleep(int(value))

    def base_quit_driver(self):
        self.driver.quit()