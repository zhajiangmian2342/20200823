# webservice接口 参数是xml形式，响应也是xml类型的
# 具体的地址：
# http://ws.webxml.com.cn/WebServices/MobileCodeWS.asmx
import os
import random
from locust import TaskSet, HttpUser, task, between


# 任务类-继承任务类
class MyGetTask(TaskSet):
    def on_start(self):
        print('start in task============')

    def on_stop(self):
        print('stop in task=============')

    # 类属性
    url = '/WebServices/MobileCodeWS.asmx'
    xml_header = {'Content-type':'text/xml'}

    # 具体的任务，需要加装饰器
    @task
    def xml_test(self):
        # 定义一个参数  参数
        # 	userName=admin&password=1234
        phone_num = str(random.randint(10000,99999))
        self.xml_data = f'''
        <?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getMobileCodeInfo xmlns="http://WebXml.com.cn/">
      <mobileCode>{phone_num}</mobileCode>
      <userID></userID>
    </getMobileCodeInfo>
  </soap:Body>
</soap:Envelope>
        '''
        # 发起请求
        # 用上下文管理器with 发起请求，并把我们的请求赋值给一个变量
        with self.client.post(self.url, data=self.xml_data, headers=self.xml_header,name='参数xml的post请求', timeout=10,
                             catch_response=True) as response:
            # 获取响应text 获取文本的响应，json获取json类型的响应,content 获取的是二进制的响应(不常用)
            resp_text = response.text
            print(f'响应数据为:{resp_text}')
            # 断言
            if phone_num in resp_text:
                # 请求成功
                response.success()
            else:
                # 请求失败 failure(字符串的参数)
                response.failure('no data')


class MyGetUser(HttpUser):
    # 通过这个字段去关联任务类和用户类 tasks 数据类型是列表
    tasks = [MyGetTask]
    host = 'http://ws.webxml.com.cn'
    wait_time = between(2, 2)

    def on_start(self):
        print('start in user============')

    def on_stop(self):
        print('stop in user=============')


if __name__ == '__main__':
    os.system('locust -f xml_1.py')