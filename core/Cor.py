# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/7 18:01
@file: Cor.py
"""

import psutil,time
def network():
    p = psutil
    before_recv = p.net_io_counters().bytes_recv
    before_send = p.net_io_counters().bytes_sent

    time.sleep(3600)
    # 每个小时
    now_recv = p.net_io_counters().bytes_recv
    now_send = p.net_io_counters().bytes_sent

    delta_send = (now_send - before_send) / 1024000
    delta_recv = (now_recv - before_recv) / 1024000
    return (int(delta_send),int(delta_recv))

def Cor():
    # 返回一个小时内，CPU/内存 使用率% 和使用的宽带 上传/下载量 M
    new = network()
    # 返回 ('25.7%', '2.3%', '0Mb', '0Mb')
    return (str(psutil.virtual_memory().percent)+'%',str(psutil.cpu_percent(True))+'%',str(new[0])+'Mb',str(new[1])+'Mb')

if __name__ == '__main__':
    print('内存使用率:{}%'.format(psutil.virtual_memory().percent))
    print('CPU使用率:{}%'.format(psutil.cpu_percent(True)))
    new = network()
    print('宽带上传量:{}MB'.format(new[0]))
    print('宽带下载量:{}MB'.format(new[1]))