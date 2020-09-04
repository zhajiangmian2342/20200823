import os

from common import get_case_id, send_mail

CMD = "locust --headless -u {user} -r {rps} -t {time} --csv=locust --host={host} -f locust_study.py"
class Service:
    def excute(self,data):
        '''
        1.开始压测
        2.我们要读取locust_stats.csv文件里面 请求，最大，平均，最小的请求数
        3.我们把上面字段的内容提出出来 然后以邮件的形式发送
        :param data:
        :return:
        '''
        # 获取data里面的code的值
        id = get_case_id()
        code = data.get('code')
        # 把页面的code值写到文件中
        f = open('locust_study.py','w',encoding='utf-8')
        f.write(code)
        f.close()
        # cmd进行格式化 data = {‘code’：，} 字典
        cmd = CMD.format(**data)
        os.system(cmd)
        # locust_stats.csv 文件名字固定
        # 读取文件里面的内容
        file = open('locust_stats.csv')
        lines = file.readlines()
        print(lines)
        # total,average,minimum,maximum
        total = lines[2].split(',')[2]
        average = lines[2].split(',')[5]
        minimum = lines[2].split(',')[6]
        maximum = lines[2].split(',')[7]
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
            'total': total,
            'average': average,
            'minimum': minimum,
            'maximum': maximum,
        })
        send_mail(sender, receiver, message)
        # 发送邮件
        return id