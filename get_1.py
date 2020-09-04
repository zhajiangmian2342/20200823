import os

from locust import TaskSet,HttpUser,task,between


# 任务类-继承任务类
class MyGetTask(TaskSet):
    def on_start(self):
        print('start in task============')

    def on_stop(self):
        print('stop in task=============')
    # 类属性
    url = '/pinter/com/getSku'
    # 具体的任务，需要加装饰器
    @task
    def get_test(self):
        # 定义一个参数  参数
        self.query_data = {'id': 1}
        # 发起请求
        # 用上下文管理器with 发起请求，并把我们的请求赋值给一个变量
        with self.client.get(self.url,params=self.query_data,name='get接口',timeout=10,catch_response=True) as response:
            # 获取响应
            resp_str = response.text
            print(f'响应数据为:{resp_str}')
            # 断言
            if 'success' in resp_str:
                # 请求成功
                response.success()
            else:
                # 请求失败 failure(字符串的参数)
                response.failure(resp_str)


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
    os.system('locust -f get_1.py')