import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


# 把每个正则出来的数字（可能含前缀）转变为坐标存储
def add_cord(num, cord_list, last_signal):
    # 如果前缀是单引号，则直接在上一个坐标上加上数值
    diff_map = {"'": 1, '"' : 2}
    if num[0] in diff_map:
        last_signal = diff_map[num[0]]
        num = num[1:]
    if last_signal == 1:
        cord_list.append(cord_list[-1] + float(num))
    elif last_signal == 2:
        cord_list.append(cord_list[-1] * 2 + float(num) - cord_list[-2])
    else:
        cord_list.append(float(num))
    return cord_list, last_signal


def IAMonDo_visualize(filename, min_trace=0, max_trace=-1):
    with open(filename, 'r') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'xml')

    for trace in soup.find_all('trace')[min_trace : max_trace]:
        trace_list = trace.string.split(',')
        # X,Y存坐标信息。signal存最后一次前缀信息，0表示显式绝对值，1表示一级差值，2表示二级差值
        X = []
        Y = []
        X_signal = 0
        Y_signal = 0
        for tl in trace_list:
            a = re.sub(r'([\'"\-]+)', r' \1', tl)
            tl_xy = re.search(r'([\'"\-\d\.]+)[\s]+([\'"\-\d\.]+)', a).groups()
            X, X_signal = add_cord(tl_xy[0], X, X_signal)
            Y, Y_signal = add_cord(tl_xy[1], Y, Y_signal)
        plt.plot(X, Y, color='black', linewidth='1')
    plt.gca().invert_xaxis()
    plt.show()

if __name__ == '__main__':
    filename = r'001.inkml'
    min_trace = 0
    max_trace = -1
    IAMonDo_visualize(filename, min_trace, max_trace)
