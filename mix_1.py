import os
import uuid
import random

from locust import TaskSet, HttpUser, task, between


# 任务类-继承任务类
class MyGetTask(TaskSet):
    def on_start(self):
        print('start in task============')

    def on_stop(self):
        print('stop in task=============')

    # 类属性


    # 具体的任务，需要加装饰器
    @task(1)
    def kjson_test(self):
        url = '/pinter/com/buy'
        # 定义一个参数  参数
        # 	userName=admin&password=1234
        self.post_data = {'param': {"skuId":123,"num":10}}
        # 发起请求
        # 用上下文管理器with 发起请求，并把我们的请求赋值给一个变量
        with self.client.post(url, data=self.post_data, name='参数k等于json的post请求', timeout=10,
                             catch_response=True) as response:
            # 获取响应text 获取文本的响应，json获取json类型的响应,content 获取的是二进制的响应(不常用)
            resp_dict = response.json()
            print(f'响应数据为:{resp_dict}')
            # 断言
            if resp_dict['message'] == 'success':
                # 请求成功
                response.success()
            else:
                # 请求失败 failure(字符串的参数)
                response.failure('no data')

    @task(3)
    def json_test(self):
        url = '/pinter/com/register'
        # 定义一个参数  参数
        # 	userName=admin&password=1234
        self.json_data = {"userName":"test","password":"1234","gender":1,"phoneNum":"110","email":"beihe@163.com","address":"Beijing"}
        # 修改电话号码和地址
        phoneNum = random.randint(1000,8888)
        address = str(uuid.uuid1())
        print(f'address的值是{address}')
        self.json_data['phoneNum'] = phoneNum
        self.json_data['address'] = address
        # 发起请求
        # 用上下文管理器with 发起请求，并把我们的请求赋值给一个变量
        with self.client.post(url, json=self.json_data, name='参数为json的post请求', timeout=10,
                              catch_response=True) as response:
            # 获取响应text 获取文本的响应，json获取json类型的响应,content 获取的是二进制的响应(不常用)
            resp_dict = response.json()
            print(f'响应数据为:{resp_dict}')
            # 断言
            if resp_dict['message'] == '注册成功':
                # 请求成功
                response.success()
            else:
                # 请求失败 failure(字符串的参数)
                response.failure('no data')


class MyGetUser(HttpUser):
    # 通过这个字段去关联任务类和用户类 tasks 数据类型是列表
    tasks = [MyGetTask]
    host = 'http://localhost:8080'
    wait_time = between(2, 2)

    def on_start(self):
        print('start in user============')

    def on_stop(self):
        print('stop in user=============')


if __name__ == '__main__':
    os.system('locust -f mix_1.py')