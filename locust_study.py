
import os

from locust import TaskSet,HttpUser,task,between

class MyGetTask(TaskSet):
    url = '/'
    @task
    def get_test(self):
        with self.client.get(self.url,name='get接口',timeout=10,catch_response=True) as response:
            resp_str = response.text
            if 'baidu' in resp_str:
                response.success()
            else:
                response.failure(resp_str)

class MyGetUser(HttpUser):
    tasks = [MyGetTask]
    host = 'https://www.baidu.com/'
    wait_time = between(2, 2)
             