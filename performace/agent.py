import datetime
import time

import psutil

from common.mongo import Mongo
import socket

class Agent():
    def __init__(self):
        self.mongo=Mongo()

    def get_ip(self):
        '''
        通过socket库可以获取机器名，通过机器名可以获取ip地址
        :return:
        '''
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip

    def get_cpu(self):
        '''
        interval代表我们获取cpu数据的时间间隔，percpu为True时，如果机器多核，则返回多个核数据
        data的值是[9.2, 6.2, 25.0, 9.4, 10.9, 0.0, 1.6, 1.6, 1.6, 7.8, 3.1, 3.1]
        :return:
        '''
        result = {}
        data = psutil.cpu_percent(interval=1, percpu=True)
        print(f'data的值是{data}')
        # cpu的总数据/cpu的核数= 每一个cpu的数据
        result['avg'] = sum(data)/psutil.cpu_count()
        # cpu的空闲值
        result['idle'] = 100-result['avg']
        # cpu的总数据
        result['data']=data

    def get_memory(self):
        '''
        psutil.virtual_memory()
svmem(total=8457662464, available=3598602240, percent=57.5, used=4859060224, free=3598602240)
        :return:
        '''
        result = {}
        # 获取系统内存的使用情况
        data = psutil.virtual_memory()
        print(f'memory data的值是{data}')
        # 内存总量
        result['total'] = data.total
        # 可用内存
        result['available'] = data.available
        # 使用了的百分比
        result['percent'] = data.percent
        # 已使用内存
        result['used'] = data.used
        return result

    def get_disk(self):
        '''
        partitions的值是[sdiskpart(device='C:\\', mountpoint='C:\\', fstype='NTFS', opts='rw,fixed'), sdiskpart(device='D:\\', mountpoint='D:\\', fstype='NTFS', opts='rw,fixed')]

        :return:
        '''
        result = {
            'total': 0,
            'used': 0,
            'available': 0,
            'percent': 0
        }
        # 先获取硬盘分区，再跟进分区获取硬盘信息，Mac这里直接用/代替disk_partitions()
        partitions = psutil.disk_partitions()
        print(f'partitions的值是{partitions}')
        # 计算每一个分区的数据，然后汇总成硬盘使用总量
        for partition in partitions:
            data = psutil.disk_usage(partition.device)
            result['total'] += data.total
            result['used'] += data.used
            result['available'] += data.free
        result['percent'] = 100 * result['used'] / result['total']
        return result

    def get_network(self):
        """
        获取网卡接受与发送的bytes和packet数据。
        psutil.net_io_counters()
        snetio(bytes_sent=3398615, bytes_recv=14170744,
        packets_sent=28431, packets_recv=25604, errin=0, errout=255, dropin=0, dropout=0)
        :return:
        """
        result = {
            'bytes': {},
            'packets': {}
        }
        data = psutil.net_io_counters()
        result['bytes']['sent'] = data.bytes_sent
        result['bytes']['receive'] = data.bytes_recv
        result['packets']['sent'] = data.packets_sent
        result['packets']['receive'] = data.packets_recv
        return result


    # 入口，直接调用这个函数
    def monitor(self, interval):
        """
        :param interval:
        :return:
        """
        collection = self.get_ip()
        while True:
            result = {
                'time': datetime.datetime.now(),
                'cpu': self.get_cpu(),
                'memory': self.get_memory(),
                'disk': self.get_disk(),
                'network': self.get_network(),
            }
            #if result['cpu']['avg'] > 20:
            #    send_email("3512937625@qq.com", "<h1>CPU使用率大于20%，实际是{0}</h1>".format(result['cpu']['avg']))
            print("将机器{0}数据写入数据库{1}".format(collection, result))
            # self.mongo.insert("monitor", collection, result)
            time.sleep(interval)


if __name__ == '__main__':
    agent = Agent()
    # agent.monitor(1)
    # agent.get_ip()
    # agent.get_cpu()
    agent.get_disk()
    # agent.get_memory()
    # agent.get_network()