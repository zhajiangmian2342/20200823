import time

from common import get_case_id
from common.mongo import Mongo

commands = [
    {
        "command": "get",
        "parameter": {
            "value": "http://121.42.15.146:9090/mtx/"
        }
    },
    {
        "command": "find",
        "parameter": {
            "by": "css selector",
            "selector": ".menu-hd>a:nth-child(3)"
        }
    },
    {
        "command": "click",
        "parameter": {}
    },
    {
        "command": "find",
        "parameter": {
            "by": "xpath",
            "selector": "//label[text()='登录账号']/following-sibling::input"
        }
    },
    {
        "command": "send",
        "parameter": {
            "value": "yaoyao"
        }
    },
    {
        "command": "find",
        "parameter": {
            "by": "xpath",
            "selector": '//label[text()="登录密码"]/following-sibling::input'
        }
    },
    {
        "command": "send",
        "parameter": {
            "value": "yaoyao"
        }
    },
    {
        "command": "find",
        "parameter": {
            "by": "xpath",
            "selector": '//button[text()="登录"]'
        }
    },
    {
        "command": "click",
        "parameter": {}
    },
]

from automation.kwLibrary import KeyWord

class Service:
    def __init__(self):
        self.db = Mongo()

    def execute(self, commands):
        # 给el一个初始值
        try:
            element = None
            kw = KeyWord()
            # func = getattr(kw,函数的名字(command对应的命令))
            for command in commands:
                element = getattr(kw, command['command'])(element, command['parameter'])
                # 需要加一个等待，否则代码运行的快，页面上有些操作可能不能顺利完成
                time.sleep(3)
            kw.base_quit_driver()
            # 运行结果是成功还是失败
            return True
        except:
            return False



    def save(self,data):
        data.setdefault('_id',get_case_id())
        return self.db.insert('automation', 'cases', data)

    def trigger(self,data):
        '''
        1.查询数据库 commands
        2.execute这个函数
        '''
        filter = {'_id':data.get('id')}
        cases = self.db.search('automation','cases', filter)
        for case in cases:
            result = self.execute(case['commands'])
            report = {
                '_id':get_case_id(),
                'case_id':case['_id'],
                'case_name':case['casename'],
                'result':result
            }
            self.db.insert('automation', 'report', report)


if __name__ == '__main__':
    Service().execute(commands)