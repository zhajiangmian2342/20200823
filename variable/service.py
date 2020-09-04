import json
import re

from common import get_case_id
from common.mongo import Mongo


class Service:
    def __init__(self):
        self.db = Mongo()

    def delete(self,data):
        '''
        删除，filter->_id过滤，去删除。
        count:最终删除的满足条件的数据个数
        :return:
        '''
        count, collection = 0, data.get('type')
        for id in data.get('id_list'):
            filter = {'_id': id}
            result = self.db.delete('variable',collection,filter)
            count += result
        return count

    def update(self,data):
        '''
        filter:_id唯一
        :param data:
        :return:
        '''
        collection = data.get('type')
        filter = {
            '_id':data.get('id')
        }

        return self.db.update('variable',collection,filter,data)




    def aggregate(self,data):
        '''
        type:表名
        key:pipeline 的关键字段
        :param data:
        :return:
        '''
        # 数据表
        collection = data.get('type')
        # key 聚合的关键字无非就是team或者project
        key = data.get('key')
        pipeline = [
            {'$group': {'_id': '$' + key}}

        ]
        data = self.db.aggregate('variable', collection, pipeline)
        return data

    def search(self, data):
        '''
        查询数据库，然后获取数据,data->filter过滤条件,type->表名
        :param data:
        :return:
        '''
        collection = data.get('type')
        return self.db.search('variable',collection, data)

    def create(self,data):
        '''
        _id一定是我们自己随机生成的
        :param data:
        :return:
        '''
        # 生成随机id
        _id =get_case_id()
        # 获取数据库表
        collection = data.get('type')
        # 把_id放到data数据里面
        data.setdefault('_id',_id)
        # 把data数据插入数据库
        id = self.db.insert('variable',collection,data)
        return id


    def debug(self, data):
        '''
        关键字的调试
        :param data:
        :return:
        '''
        print(data)
        # 把json字符串转换成字典  python字典 = json.loads(字符串)
        mock = json.loads(data.get('mock'))
        # 以字典的形式传递参数
        content = {'data':mock}
        snippet = data.get('snippet')
        # 1.想判断是否有这个函数 2.定义函数+调用函数，并且把调用函数返回的值赋值给一个变量
        # func = [test(data)]代表的是调用
        func = re.findall(r'def\s+(.+?):',snippet)
        if func:
        # snippet只是定义函数的过程,所以要拼接调用函数的代码
            snippet += '\n'+'result='+func[0]
            exec(snippet, content)
        # 运行的结果存储在content的result字段里面
        return content['result']

    def save(self, data):
        '''
        1.把_id(自己重新生成),函数名字，mock数据，snippet代码段(包括调用过程的)都保存到数据中
        2. variable,keyword
        :param data:
        :return:
        '''
        mock = json.loads(data.get('mock'))
        snippet = data.get('snippet')
        # 函数的名字，即关键字
        name = re.findall(r'def\s+(.+?)\(', snippet)
        name = name[0] if name else ""
        func = re.findall(r'def\s+(.+?):', snippet)
        if func:
            snippet += '\n' + 'result='+ func[0]
        # 把数据存储到数据库的过程
        result = self.db.insert('variable','keyword',{
            '_id':get_case_id(),
            'name':name,    # 函数的名字
            'mock':mock,   # 调试的数据
            'snippet':snippet  # 具体需要运行的代码+调用过程
        })
        return result

