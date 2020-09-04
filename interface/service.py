import requests

from common.mongo import Mongo
from interface.compare import Compare
from common import get_case_id, derivation, evaluation
from flask import g


class Service:
    def __init__(self):
        self.db = Mongo()
        g.data = []

    def make_request(self,data):
        '''
        发起请求，获取响应
        :param data: 获取的参数值
        :return: 响应值
        '''
        method = data.get('method')
        url = data.get('url')
        kwargs = {}
        # 对http请求头信息做校验
        if 'header' in data and data.get('header')!={'': ''} and data.get('header'):
                kwargs['header'] = data['header']
        # 对http的参数做校验
        if 'params' in data and data.get('params'):
            kwargs['params'] = data['params']
        if 'form_data' in data and data.get('form_data'):
            kwargs['data'] = data['form_data']
        if 'json_data' in data and data.get('json_data'):
            kwargs['json'] = data['json_data']


        response = requests.request(method=method,url=url ,**kwargs)
        # print(response)
        # print(response.status_code)
        # print(response.json())
        # return response.json()
        data['response'] = {
            'code': response.status_code,
            'json': response.json()
        }
        return data

    @staticmethod
    def make_assert(data):
        compare = Compare()
        for expr in data['assert']:
         # 预期值
         expect = expr['expected']
        # 获取条件
         func = expr['condition']
         if expr['source'] == 'code':
             # 实际结果
             tmp = str(data['response']['code'])
         else:

             # 响应-保存到一个便令tmp
             tmp = data['response']['json']
             # 对响应体对判断，开始进行分隔符处理 字符串->列表
             for item in expr['expression'].split('.'):
                 # 如果报错 就证明 item是int值索引
                 try:
                    tmp = tmp[item]
                 except:
                    tmp = tmp[int(item)]
         # print(tmp)
         # 取数据结束->断言处理 真假  反射 def eqls(self,actual,expected):
         result = getattr(compare, func)(tmp,expect)

         #把断言结果放在data里面，然后在传给前端。
         expr.setdefault('result', result)

         return data
         # 替换变量

    def execute_snippet(self, data):
        '''
        执行关键字函数的代码，得到返回值，替换掉参数当中的关键字
        :param data:
        :return:
        '''
        # 查库，把关键字表当中的信息查询出来
        results = self.db.search('variable','keyword',{})
        # 对传进来的参数进行一个处理：首先判断有没有关键字参数，有的做一个替换
        result = evaluation(data['params'],results)
        data['params']['sign']= result
        return data


    def replace_variable(self, data):
        '''

        :param data:
        :return:
        '''
        filter = {
            'team': data.get('team'),
            'project': data.get('project')
        }
        # 列表-想拓展这个列表  extend([])
        results = self.db.search('variable', 'variable', filter)
        # todo 把那个提取出来的参数对应的值，从这个位置加入到变量库当中
        results.extend(g.data)
        if 'url' in data:
            data['url'] = derivation(data['url'], results)
        if 'header' in data:
            for key in data['header']:
                data['header'][key] = derivation(data['header'][key], results)

        if 'params' in data:
            for key in data['params']:
                data['params'][key] = derivation(data['params'][key], results)
        return data

    def extract_parameter(self, data):
        '''

        :param data:
        :return:
        '''
        # 'extract': [{'expression': 'data.adcode', 'expected': 'sid'}]
        print(data)
        if 'extract' not in data or not data['extract']:
            return data
        for extract in data['extract']:
            expr = extract['expression']
            # name=sid 值是多少？？？
            name = extract['expected']
            tmp = data['response']['json']
            for item in expr.split('.'):
                try:
                    tmp = tmp[int(item)]
                except:
                    # name的值就是tmp  320583
                    # {'name':name,'value':tmp}
                    # [{'name':name,'value':tmp}]
                    # 2.sid = 320583 应在存在哪里 flask中 g 接口 请求 响应
                    # 发起请求g产生，请求完成（获取响应）g就会销毁  g的数据格式是字典
                    # 1.如何在请求之前替换第二个接口的参数
                    tmp = tmp[item]
            g.data.append({'name':name,'value':tmp})
        return data
    # 核心
    def run(self,data):
        '''
        统一运行接口用例的方法，你以后对请求有什么特殊函数方法的添加，
        直接写在这里面就可以了
        :param data:
        :return:
        '''

        data = self.replace_variable(data)
        data = self.execute_snippet(data)
        data = self.make_request(data)
        data = self.make_assert(data)
        data = self.extract_parameter(data)
        return data

    def save_cases(self,data):
        '''

        :param data:
        :return:
        '''
        # 构造_id  原则-唯一的，不重复
        case_id = get_case_id()

        # 然后_id放到data里面去
        data.setdefault('_id',case_id)
        # 把data数据保存到数据库
        id = self.db.insert('interface','cases',data)
        return id

    def interface_team_and_project(self):
        '''
        查库:查的是哪一个库，哪一个表
        返回的数据结构data {'team1':[project1,project1],'team2':[project1,project2...]}
        :return:
        '''
        menu = {}
        # 把有的数据都给我返回过来
        filter = {
            'page': 0,
            'limit': 0
        }
        results = self.db.search('variable','variable', filter)
        # print(results)
        # 遍历results，然后构造最终我们想要的data数据
        for result in results:
            if result['team'] not in menu:
                menu.setdefault(result['team'],[result['project']])
            else:
                menu[result['team']].append(result['project'])
        # set 循环遍历menu里面的key，然后去重他的值
        for team in menu:
            # 修改值 之前的值=去重之后的值
            menu[team] = list(set(menu[team]))

        return menu

    def interface_list(self,data):
        '''

        :return:
        '''
        data = self.db.search('interface', 'cases', data)
        return data

    def interface_delete(self, data):
        '''

        :param data:
        :return:
        '''
        count, id_list = 0, data.get('id_list')
        for id in id_list:
            filter = {'_id': id}
            result = self.db.delete('interface', 'cases', filter)
            count += result
        return count

    def interface_search(self,data):
        '''

        :param data:
        :return:
        '''
        filter = {
            '_id': data.get('id')
        }
        data = self.db.search('interface','cases',filter)
        return data

    def interface_update(self,data):
        '''

        :param data:
        :return:
        '''
        filter = {
            '_id':data.get('id')
        }
        data = self.db.update('interface','cases',filter,data)
        return data

    def save_suite(self,data):
        '''

        :return:
        '''
        data.setdefault('_id',get_case_id())
        result = self.db.insert('interface','suite', data)
        return result

    def suite_list(self,data):
        '''

        :param data:
        :return:
        '''
        result = self.db.search('interface','suite', data)
        return result

    def suite_delete(self, data):
        '''

        :param data:
        :return:
        '''
        count, id_list = 0, data.get('id_list')
        for id in id_list:
            filter = {'_id': id}
            result = self.db.delete('interface', 'suite', filter)
            count += result
        return count

    def trigger(self,data):
        '''

        :param data:
        :return:
        '''
        filter = {
            '_id':data.get('id')
        }
        # suite是列表
        suite = self.db.search('interface','suite',filter)
        print('suite的值是', suite)
        if not suite:
            return filter['_id']

        # 为了把运行接口放在report这个库里面,所以在这个位置定义一个储存数据的容器
        result = {
            '_id':get_case_id(),
            'team':suite[0]['team'],
            'project':suite[0]['project'],
            'result':[]

        }


        for case_id in suite[0]['cases']:
            # case是列表
            case = self.db.search('interface','cases',{'_id': case_id})
            # 调用一个运行接口用例的方法
            case = self.run(case[0])
            result['result'].append(case)


        self.db.insert('interface','report',result)

        return result['_id']






