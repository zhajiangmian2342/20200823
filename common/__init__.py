# 构造_id  原则-唯一的，不重复  当前时间-uuid也是唯一的
import smtplib
import time
import uuid
import re
from email.header import Header
from email.mime.text import MIMEText


def get_case_id():
    # time 和uuid进行拼接
    # 时间函数
    prefix = time.strftime('%Y%m%d%H%M%S')
    # print(prefix)
    # uuid  索引0和3是变化的
    li = str(uuid.uuid1()).split('-')
    suffix = li[0] + li[3]
    case_id = prefix + suffix
    return case_id
    # print(case_id)


# 替换变量
def derivation(data, results):
    '''

    :param data: 前端收集到的数据里面具体的一个字符串
    :param results: 从variable库，variable这个表中查询到的数据,列表的形式
    :return:
    '''

    # 判断url，params..是否存在变量,如果有，我们做解析，如果没有的话，返回原来data
    # {ip} 正则表达式匹配出来
    def _exist_variable():
        variable = re.findall(r'\$\{(.*?)\}', data)

        # 如果有值，那就是有变量
        if variable:
            return variable[0].strip()
        else:
            return None

    # data为空或者我们根本数据库里面没有这个变量名
    if not data and not results:
        return data

    # 做解析
    varible = _exist_variable()
    print(varible)
    if varible:
        for result in results:
            if varible == result['name']:
                return data.replace('${' + varible + '}', result['value'])
    else:
        return data


# 替换关键字函数
def evaluation(params, results):
    '''
    提取关键字，然后进行运算，最终得到运算结果
    :param params: 参数字典
    :param results: 查询关键字表得到的关键字列表
    :return:
    '''

    def _exist_variable(param):
        variable = re.findall(r'\@\{(.*?)\}', param)

        # 如果有值，那就是有变量
        if variable:
            return list(map(lambda x: x.strip(), variable))
        else:
            return None

    # 如果params是空值或者变量没有设置的时候则不处理
    if not params or not results:
        return params
    for param in params.values():

        # 先判断param这里面是否有关键字
        variable = _exist_variable(param)
        if variable is None:
            continue
        # v就是列表里面的元素--关键字 没有@{}
        for v in variable:
            # 遍历查询出来的结果results
            for result in results:
                if v == result['name']:
                    snippet = result['snippet']
                    content = {'data': {'params': params}}
                    exec(snippet, content)
                    return content['result']
    return params


def smtp_service(sender,receive,message):
    '''
    具体创建的smpt的服务及发送邮件的封装
    :param sender:
    :param receive:
    :param message:
    :return:
    '''
    try:
        smpt = smtplib.SMTP()
        smpt.connect('smtp.163.com')
        username = 'mtx_testfan@163.com'
        password = 'OUOVHPLCYUVXEMHH'
        # 登录邮箱
        smpt.login(username, password)
        smpt.sendmail(sender, receive, message.as_string())
        print(f'email send {receive} success')
    except:
        print(f'email send{receive} fail')

def send_mail(sender,receive,template):
    '''
    供外界调用的接口
    :return:
    '''
    title = '夭夭测试平台报警邮件'
    message = MIMEText(template, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = receive
    message['Subject'] = Header(title, 'utf-8')
    smtp_service(sender, receive, message)


if __name__ == '__main__':
    # # get_case_id()
    # data = derivation('{ip}/service/regeo', [{'name': 'ip', 'value': 'haha'}])
    # print(data)
    sender = 'mtx_testfan@163.com'
    receiver = '3512937625@qq.com'
    message = '''
     <h3>报警信息</h3>
    <label style='background-color:red'>请求次数：{total}</label></br>
    <label style='background-color:red'>平均响应时间: {average}</label></br>
    <label style='background-color:red'>最小响应时间：{minimum}</label></br>
    <label style='background-color:red'>最大响应时间：{maximum}</label></br>   
    '''
    # total, average, minimum, maximum
    message = message.format(**{
        'total': 1,
        'average': 2,
        'minimum': 3,
        'maximum': 4,
    })
    send_mail(sender, receiver, message)
