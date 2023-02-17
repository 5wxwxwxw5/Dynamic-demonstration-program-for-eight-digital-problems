import os
import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter import messagebox
import math
import random

import psutil

import A
import A2
import A3
import BFS
import time
import DFS
import  randn


start_e = []  # 输入的初始数字
end_e = []   # 输入的目标数字
result1 = []  # 产生的初始随机数字
result2 = []  # 产生的目标随机数字
str_nc = ""   # 内存占用

A_show = []  # A*算法的步骤
A_2_show = []  # A*2算法的步骤
A_3_show = []  # A*3算法的步骤
B_show = []  # BFS算法的步骤
D_show = []  # DFS算法的步骤
R_show = []  #Randon算法的步骤


# 创建方格，并向方格中输入数字
def get():
    N = int(e1.get())
    k = 0
    for i in range(0, int(math.sqrt(int(N) + 1))):
        for j in range(0, int(math.sqrt(int(N) + 1))):
            start_e.append(e1)
            end_e.append(e1)
            start_e[k] = tk.Entry(window, show=None, font=('Arial', 10))
            start_e[k].place(x=10 + i * 50, y=70 + j * 50, width=40, height=40)
            end_e[k] = tk.Entry(window, show=None, font=('Arial', 10))
            end_e[k].place(x=250 + i * 50, y=70 + j * 50, width=40, height=40)
            k = k + 1


# 获取方格的数字，并根据选择的算法调用相应的方法
def start_game():
    s = int(math.sqrt(int(int(e1.get())) + 1))
    Block = [[0] * s for i in range(s)]
    Goal = [[0] * s for i in range(s)]
    k = 0
    if len(result1) == int(e1.get()) + 1 and len(result1) == int(e1.get()) + 1:  # 调用随机数
        for i in range(0, s):
            for j in range(0, s):
                Block[j][i] = result1[k]
                Goal[j][i] = result2[k]
                k = k + 1
    else:
        for i in range(0, s):  # 调用输入的数字
            for j in range(0, s):
                Block[j][i] = int(start_e[k].get())
                Goal[j][i] = int(end_e[k].get())
                k = k + 1
    info = psutil.virtual_memory()
    if v.get() == 1:
        A_(Block, Goal)
    if v.get() == 2:
        DFS_(Block, Goal, s)
    if v.get() == 3:
        BFS_(Block, Goal, s)
    if v.get() == 4:
        A_2(Block, Goal)
    if v.get() == 5:
        A_3(Block, Goal)
    if v.get() == 6:
        RANDON(Block, Goal, s)
    str_nc = str(psutil.Process(os.getpid()).memory_info().rss/8589934592) + "GB"
    move_num = tk.Label(window, text=str_nc, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=380, width=250)
    print(u'内存使用：', str_nc)
    print(f'总内存： {info.total/8589934592}GB')
    print(u'cpu个数：', psutil.cpu_count())

# 产生随机数
def ran():
    N = int(e1.get())
    global result1
    global result2
    result1 = random.sample(range(0, N + 1), N + 1)
    result2 = random.sample(range(0, N + 1), N + 1)
    k = 0
    for i in range(0, int(math.sqrt(N + 1))):
        for j in range(0, int(math.sqrt(N + 1))):
            tk.Label(window, text=result1[k]).place(x=10 + i * 50, y=70 + j * 50, width=40, height=40)
            tk.Label(window, text=result2[k]).place(x=250 + i * 50, y=70 + j * 50, width=40, height=40)
            k = k + 1


# A*算法
def A_(Block, Goal):
    x = 25
    if x==0:
        y = 0
    else:
        y = 4
    m = 0
    while m<x:
        if m < 13:
            tk.Label(window, text="                  \n                   \n                     \n                    \n                   \n                           \n                           ", bg='#FFFFF0').place(x=10 + m * 75, y=420 )  # 搜索步骤
        elif m < 26:
            tk.Label(window, text="                  \n                   \n                     \n                    \n                   \n                           \n                           ", bg='#FFFFF0').place(x=10 + (m - 13) * 75, y=500 )  # 搜索步骤
        m = m+1
    for i in range(y):
        for j in range(y):
            tk.Label(window, text="               \n                \n                  \n                 \n", font=('宋体', 25),bg='#FFFFF0').place(x=600+j*70, y=20 + i * 70, width=60, height=60)  # 搜索过程
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=380, width=250)
    A_show.clear()
    window.update()
    # print("block:")
    # print(Block)
    # print("goal:")
    # print(Goal)
    # time.sleep(1)
    # if len(Block) == 8:
    #     # 转一维列表
    #     onedi = [Block[0][i] for i in range(3)] + [Block[1][2]] + \
    #             [Block[2][i] for i in range(2, -1, -1)] + [Block[1][i] for i in range(2)]
    #     oxe = 0  # 计算逆序
    #     for i in range(1, 9):
    #         if onedi[i] != 0:
    #             for j in range(i):
    #                 oxe += 1 if onedi[j] > onedi[i] else 0
    #     if oxe%2!=0:
    #         messagebox.showinfo("提示", "没有路径到达")
    #         return
    # elif len(Block) == 15:
    #     pass
    Len = len(Block)
    x = []
    y = []
    x_rev = 0
    y_rev = 0
    for i in range(Len):
        for j in range(Len):
            x.append(Block[i][j])
            y.append(Goal[i][j])
    for i in range(len(x)):
        if i == 0:
            continue
        for j in range(i):
            if x[j] > x[i]:
                x_rev = x_rev + 1
            if y[j] > y[i]:
                y_rev = y_rev + 1
    if (x_rev % 2) != (y_rev % 2):
        messagebox.showinfo("提示", "没有路径到达")
        return

    A.ma(Block, Goal)  # 调用A*算法进行搜索

    def show_block(block, k):
        print("---------------")
        i = 0
        A_show.append(block)
        for b in block:
            for j in range(0, int(math.sqrt(int(e1.get()) + 1))):
                tk.Label(window, text=b[j], font=('宋体', 25)).place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
            i = i + 1
            print(b)  # 在控制台输出搜索步骤
            if k < 13:
                tk.Label(window, text=b).place(x=10 + k * 75, y=430 + (i - 1) * 22)  # 搜索步骤
            elif k < 26:
                tk.Label(window, text=b).place(x=10 + (k - 13) * 75, y=530 + (i - 1) * 22)  # 搜索步骤
        time.sleep(1)
        window.update()

    if A.judge == 0:  # 有路径
        k = 0
        while len(A.stack) != 0:
            t = A.stack.pop()
            show_block(t, k)  # 展示路径
            k = k + 1
    else:
        A.judge = 0
        messagebox.showinfo("提示", "没有路径到达")

    # 搜索结果
    move_num = tk.Label(window, text=A.m, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text=A.time, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text=A.nodes, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    A.nodes = 0
    A.m = 0

# A*算法2
def A_2(Block, Goal):
    x = 25
    if x == 0:
        y = 0
    else:
        y = 4
    m = 0
    while m < x:
        if m < 13:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + m * 75, y=420)  # 搜索步骤
        elif m < 26:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + (m - 13) * 75, y=500)  # 搜索步骤
        m = m + 1
    for i in range(y):
        for j in range(y):
            tk.Label(window, text="               \n                \n                  \n                 \n",
                     font=('宋体', 25), bg='#FFFFF0').place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=380, width=250)
    A_2_show.clear()
    window.update()
    # if len(Block) == 8:
    #     # 转一维列表
    #     onedi = [Block[0][i] for i in range(3)] + [Block[1][2]] + \
    #             [Block[2][i] for i in range(2, -1, -1)] + [Block[1][i] for i in range(2)]
    #     oxe = 0  # 计算逆序
    #     for i in range(1, 9):
    #         if onedi[i] != 0:
    #             for j in range(i):
    #                 oxe += 1 if onedi[j] > onedi[i] else 0
    #     if oxe%2!=0:
    #         messagebox.showinfo("提示", "没有路径到达")
    #         return
    # elif len(Block) == 15:
    #     pass
    Len = len(Block)
    x = []
    y = []
    x_rev = 0
    y_rev = 0
    for i in range(Len):
        for j in range(Len):
            x.append(Block[i][j])
            y.append(Goal[i][j])
    for i in range(len(x)):
        if i == 0:
            continue
        for j in range(i):
            if x[j] > x[i]:
                x_rev = x_rev + 1
            if y[j] > y[i]:
                y_rev = y_rev + 1
    if (x_rev % 2) != (y_rev % 2):
        messagebox.showinfo("提示", "没有路径到达")
        return

    A2.ma(Block, Goal)  # 调用A*2算法进行搜索

    def show_block(block, k):
        print("---------------")
        i = 0
        A_2_show.append(block)
        for b in block:
            for j in range(0, int(math.sqrt(int(e1.get()) + 1))):
                tk.Label(window, text=b[j], font=('宋体', 25)).place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
            i = i + 1
            print(b)  # 在控制台输出搜索步骤
            if k < 13:
                tk.Label(window, text=b).place(x=10 + k * 75, y=430 + (i - 1) * 22)  # 搜索步骤
            elif k < 26:
                tk.Label(window, text=b).place(x=10 + (k - 13) * 75, y=530 + (i - 1) * 22)  # 搜索步骤
        time.sleep(1)
        window.update()

    if A2.judge == 0:  # 有路径
        k = 0
        while len(A2.stack) != 0:
            t = A2.stack.pop()
            show_block(t, k)  # 展示路径
            k = k + 1
    else:
        A2.judge = 0
        messagebox.showinfo("提示", "没有路径到达")

    # 搜索结果
    move_num = tk.Label(window, text=A2.m, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text=A2.time, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text=A2.nodes, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    A2.nodes = 0
    A2.m = 0

# A*算法2
def A_3(Block, Goal):
    x = 25
    if x == 0:
        y = 0
    else:
        y = 4
    m = 0
    while m < x:
        if m < 13:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + m * 75, y=420)  # 搜索步骤
        elif m < 26:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + (m - 13) * 75, y=500)  # 搜索步骤
        m = m + 1
    for i in range(y):
        for j in range(y):
            tk.Label(window, text="               \n                \n                  \n                 \n",
                     font=('宋体', 25), bg='#FFFFF0').place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=380, width=250)
    A_3_show.clear()
    window.update()
    # if len(Block) == 8:
    #     # 转一维列表
    #     onedi = [Block[0][i] for i in range(3)] + [Block[1][2]] + \
    #             [Block[2][i] for i in range(2, -1, -1)] + [Block[1][i] for i in range(2)]
    #     oxe = 0  # 计算逆序
    #     for i in range(1, 9):
    #         if onedi[i] != 0:
    #             for j in range(i):
    #                 oxe += 1 if onedi[j] > onedi[i] else 0
    #     if oxe%2!=0:
    #         messagebox.showinfo("提示", "没有路径到达")
    #         return
    # elif len(Block) == 15:
    #     pass
    Len = len(Block)
    x = []
    y = []
    x_rev = 0
    y_rev = 0
    for i in range(Len):
        for j in range(Len):
            x.append(Block[i][j])
            y.append(Goal[i][j])
    for i in range(len(x)):
        if i == 0:
            continue
        for j in range(i):
            if x[j] > x[i]:
                x_rev = x_rev + 1
            if y[j] > y[i]:
                y_rev = y_rev + 1
    if (x_rev % 2) != (y_rev % 2):
        messagebox.showinfo("提示", "没有路径到达")
        return

    A3.ma(Block, Goal)  # 调用A*2算法进行搜索

    def show_block(block, k):
        print("---------------")
        i = 0
        A_3_show.append(block)
        for b in block:
            for j in range(0, int(math.sqrt(int(e1.get()) + 1))):
                tk.Label(window, text=b[j], font=('宋体', 25)).place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
            i = i + 1
            print(b)  # 在控制台输出搜索步骤
            if k < 13:
                tk.Label(window, text=b).place(x=10 + k * 75, y=430 + (i - 1) * 22)  # 搜索步骤
            elif k < 26:
                tk.Label(window, text=b).place(x=10 + (k - 13) * 75, y=530 + (i - 1) * 22)  # 搜索步骤
        time.sleep(1)
        window.update()

    if A3.judge == 0:  # 有路径
        k = 0
        while len(A3.stack) != 0:
            t = A3.stack.pop()
            show_block(t, k)  # 展示路径
            k = k + 1
    else:
        A3.judge = 0
        messagebox.showinfo("提示", "没有路径到达")

    # 搜索结果
    move_num = tk.Label(window, text=A3.m, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text=A3.time, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text=A3.nodes, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    A3.nodes = 0
    A3.m = 0

# 宽度优先搜索
def BFS_(Block, Goal, s):
    x = 25
    if x == 0:
        y = 0
    else:
        y = 4
    m = 0
    while m < x:
        if m < 13:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + m * 75, y=420)  # 搜索步骤
        elif m < 26:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + (m - 13) * 75, y=500)  # 搜索步骤
        m = m + 1
    for i in range(y):
        for j in range(y):
            tk.Label(window, text="               \n                \n                  \n                 \n",
                     font=('宋体', 25), bg='#FFFFF0').place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=380, width=250)
    B_show.clear()
    window.update()
    Len = len(Block)
    x = []
    y = []
    x_rev = 0
    y_rev = 0
    for i in range(Len):
        for j in range(Len):
            x.append(Block[i][j])
            y.append(Goal[i][j])
    for i in range(len(x)):
        if i == 0:
            continue
        for j in range(i):
            if x[j] > x[i]:
                x_rev = x_rev + 1
            if y[j] > y[i]:
                y_rev = y_rev + 1
    if (x_rev % 2) != (y_rev % 2):
        messagebox.showinfo("提示", "没有路径到达")
        return

    BFS.ma(Block, Goal, s)  # 调用BFS算法进行搜索

    def show_block(block, k):
        print("---------------")
        i = 0
        B_show.append(block)
        for b in block:
            for j in range(0, int(math.sqrt(int(e1.get()) + 1))):
                tk.Label(window, text=b[j], font=('宋体', 25)).place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
            i = i + 1
            print(b)  # 在控制台输出搜索步骤
            if k < 13:
                tk.Label(window, text=b).place(x=10 + k * 75, y=430 + (i - 1) * 22)  # 搜索步骤
            elif k < 26:
                tk.Label(window, text=b).place(x=10 + (k - 13) * 75, y=530 + (i - 1) * 22)  # 搜索步骤
        time.sleep(1)
        window.update()

    if BFS.judge == 0:   # 有路径
        k = 0
        while len(BFS.stack) != 0:
            t = BFS.stack.pop(0)
            show_block(t, k)  # 展示路径
            k = k + 1
    else:
        BFS.judge = 0
        messagebox.showinfo("提示", "没有路径到达")

    # 搜索结果
    move_num = tk.Label(window, text=BFS.m, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text=BFS.time, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text=BFS.nodes, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    BFS.nodes = 0
    BFS.m = 0


# 深度优先搜索
def DFS_(Block, Goal, s):
    x = 25
    if x == 0:
        y = 0
    else:
        y = 4
    m = 0
    while m < x:
        if m < 13:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + m * 75, y=420)  # 搜索步骤
        elif m < 26:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + (m - 13) * 75, y=500)  # 搜索步骤
        m = m + 1
    for i in range(y):
        for j in range(y):
            tk.Label(window, text="               \n                \n                  \n                 \n",
                     font=('宋体', 25), bg='#FFFFF0').place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=380, width=250)
    D_show.clear()
    window.update()
    Len = len(Block)
    x = []
    y = []
    x_rev = 0
    y_rev = 0
    for i in range(Len):
        for j in range(Len):
            x.append(Block[i][j])
            y.append(Goal[i][j])
    for i in range(len(x)):
        if i == 0:
            continue
        for j in range(i):
            if x[j] > x[i]:
                x_rev = x_rev + 1
            if y[j] > y[i]:
                y_rev = y_rev + 1
    if (x_rev % 2) != (y_rev % 2):
        print("no")
        messagebox.showinfo("提示", "没有路径到达")
        return

    DFS.ma(Block, Goal, s)  # 调用DFS算法进行搜索

    def show_block(block, k):
        print("---------------")
        i = 0
        D_show.append(block)
        for b in block:
            for j in range(0, int(math.sqrt(int(e1.get()) + 1))):
                tk.Label(window, text=b[j], font=('宋体', 25)).place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
            i = i + 1
            print(b)  # 在控制台输出搜索步骤
            if k < 13:
                tk.Label(window, text=b).place(x=10 + k * 75, y=430 + (i - 1) * 22)  # 搜索步骤
            elif k < 26:
                tk.Label(window, text=b).place(x=10 + (k - 13) * 75, y=530 + (i - 1) * 22)  # 搜索步骤
        time.sleep(1)
        window.update()

    if DFS.judge == 0:   # 有路径
        k = 0
        while len(DFS.stack) != 0:
            t = DFS.stack.pop(0)
            show_block(t, k)  # 展示路径
            k = k + 1
    else:
        DFS.judge = 0
        messagebox.showinfo("提示", "没有路径到达")

    # 搜索结果
    move_num = tk.Label(window, text=DFS.m, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text=DFS.time, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text=DFS.nodes, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    DFS.nodes = 0
    DFS.m = 0

# 随机搜索
def RANDON(Block, Goal, s):
    x = 25
    if x == 0:
        y = 0
    else:
        y = 4
    m = 0
    while m < x:
        if m < 13:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + m * 75, y=420)  # 搜索步骤
        elif m < 26:
            tk.Label(window,
                     text="                  \n                   \n                     \n                    \n                   \n                           \n                           ",
                     bg='#FFFFF0').place(x=10 + (m - 13) * 75, y=500)  # 搜索步骤
        m = m + 1
    for i in range(y):
        for j in range(y):
            tk.Label(window, text="               \n                \n                  \n                 \n",
                     font=('宋体', 25), bg='#FFFFF0').place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    move_num = tk.Label(window, text="                   ", font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=380, width=250)
    B_show.clear()
    window.update()
    Len = len(Block)
    x = []
    y = []
    x_rev = 0
    y_rev = 0
    for i in range(Len):
        for j in range(Len):
            x.append(Block[i][j])
            y.append(Goal[i][j])
    for i in range(len(x)):
        if i == 0:
            continue
        for j in range(i):
            if x[j] > x[i]:
                x_rev = x_rev + 1
            if y[j] > y[i]:
                y_rev = y_rev + 1
    if (x_rev % 2) != (y_rev % 2):
        messagebox.showinfo("提示", "没有路径到达")
        return
    randn.ma(Block, Goal, s)  # 调用BFS算法进行搜索

    def show_block(block, k):
        print("---------------")
        i = 0
        R_show.append(block)
        for b in block:
            for j in range(0, int(math.sqrt(int(e1.get()) + 1))):
                tk.Label(window, text=b[j], font=('宋体', 25)).place(x=600 + j * 70, y=20 + i * 70, width=60, height=60)  # 搜索过程
            i = i + 1
            print(b)  # 在控制台输出搜索步骤
            if k < 13:
                tk.Label(window, text=b).place(x=10 + k * 75, y=430 + (i - 1) * 22)  # 搜索步骤
            elif k < 26:
                tk.Label(window, text=b).place(x=10 + (k - 13) * 75, y=530 + (i - 1) * 22)  # 搜索步骤
        time.sleep(1)
        window.update()

    if randn.judge == 0:   # 有路径
        k = 0
        while len(randn.stack) != 0:
            t = randn.stack.pop(0)
            show_block(t, k)  # 展示路径
            k = k + 1
    else:
        randn.judge = 0
        messagebox.showinfo("提示", "没有路径到达")

    # 搜索结果
    move_num = tk.Label(window, text=randn.m, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=650, y=300)
    move_num = tk.Label(window, text=randn.time, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=620, y=340, width=200)
    move_num = tk.Label(window, text=randn.nodes, font=('宋体', 15), width=5, bg='#FFFAF0')
    move_num.place(x=900, y=300, width=100)
    randn.nodes = 0
    randn.m = 0




# 搜索步骤查询
def more():
    def got():
        if v.get() == 1:  # A*搜索步骤
            # print(len(A_show))
            x= len(A_show[int(e.get())])
            for i in range(x):
                tk.Label(next, text=A_show[int(e.get())-1][i], font=('宋体', 17), bg='#FFFAF0').place(x=40, y=150+i*40)
            tk.Label(next, text=">", font=('宋体', 30), bg='#FFFAF0').place(x=180, y=200)
            for i in range(x):
                tk.Label(next, text=A_show[int(e.get())][i], font=('宋体', 17), bg='#FFFAF0').place(x=270, y=150+40*i)

        if v.get() == 3:  # DFS搜索步骤
            # print(len(B_show))
            x = len(B_show[int(e.get())])
            for i in range(x):
                tk.Label(next, text=B_show[int(e.get())-1][i], font=('宋体', 17), bg='#FFFAF0').place(x=20, y=150+i*40)
            tk.Label(next, text=">", font=('宋体', 30), bg='#FFFAF0').place(x=200, y=200)
            for i in range(x):
                tk.Label(next, text=B_show[int(e.get())][i], font=('宋体', 17), bg='#FFFAF0').place(x=240, y=150+i*40)
        if v.get() == 2:  # BFS搜索步骤
            # print(len(D_show))
            x = len(D_show[int(e.get())])
            for i in range(x):
                tk.Label(next, text=D_show[int(e.get())-1][i], font=('宋体', 17), bg='#FFFAF0').place(x=20, y=150+i*40)
            tk.Label(next, text=">", font=('宋体', 30), bg='#FFFAF0').place(x=200, y=200)
            for i in range(x):
                tk.Label(next, text=D_show[int(e.get())][i], font=('宋体', 17), bg='#FFFAF0').place(x=240, y=150+i*40)
        if v.get() == 4:  # A*算法2
            # print(len(A_2_show))
            x = len(A_2_show[int(e.get())])
            for i in range(x):
                tk.Label(next, text=A_2_show[int(e.get())-1][i], font=('宋体', 17), bg='#FFFAF0').place(x=40, y=150+i*40)
            tk.Label(next, text=">", font=('宋体', 30), bg='#FFFAF0').place(x=180, y=200)
            for i in range(x):
                tk.Label(next, text=A_2_show[int(e.get())][i], font=('宋体', 17), bg='#FFFAF0').place(x=270, y=150+i*40)
        if v.get() == 5:  # A*算法3
            # print(len(A_3_show))
            x = len(A_3_show[int(e.get())])
            for i in range(x):
                tk.Label(next, text=A_3_show[int(e.get())-1][i], font=('宋体', 17), bg='#FFFAF0').place(x=40, y=150+i*40)
            tk.Label(next, text=">", font=('宋体', 30), bg='#FFFAF0').place(x=180, y=200)
            for i in range(x):
                tk.Label(next, text=A_3_show[int(e.get())][i], font=('宋体', 17), bg='#FFFAF0').place(x=270, y=150+i*40)
        if v.get() == 2:  # 随机决策步骤
            # print(len(R_show))
            x = len(R_show[int(e.get())])
            for i in range(x):
                tk.Label(next, text=R_show[int(e.get())-1][i], font=('宋体', 17), bg='#FFFAF0').place(x=20, y=150+i*40)
            tk.Label(next, text=">", font=('宋体', 30), bg='#FFFAF0').place(x=200, y=200)
            for i in range(x):
                tk.Label(next, text=R_show[int(e.get())][i], font=('宋体', 17), bg='#FFFAF0').place(x=240, y=150+i*40)


    # 创建新窗口
    next = tk.Toplevel()
    next.geometry('400x400')
    next.config(background="#FFFFF0")
    tk.Label(next, text='您需要查询的步骤:', font=('宋体', 17), bg='#FFFAF0').place(x=0, y=20)
    e = tk.Entry(next, show=None, font=('Arial', 10))
    e.place(x=50, y=60, width=180, height=30)
    tk.Button(next, text='确定', command=got, bg='white').place(x=260, y=60, width=50, height=30)


if __name__ == '__main__':
    window = tk.Tk()  # 第1步，实例化object，建立窗口window
    window.title('8数码/15数码')  # 第2步，给窗口的可视化起名字
    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('1000x640')  # 这里的乘是小x

    # 设置4个框架
    frm_1 = tk.Frame(window, width=500, height=400, bg='#E0FFFF').grid(rowspan=6, columnspan=3)
    frm_2 = tk.LabelFrame(window, width=500, height=300, bg='#FFFFF0', text='搜索过程', font=18).grid(row=0, column=3,
                                                                                                  rowspan=4)
    frm_3 = tk.Frame(window, width=500, height=100, bg='#FFFAF0').grid(row=4, column=3, rowspan=2)
    frm_4 = tk.LabelFrame(window, width=1000, height=240, bg='#FFFFF0', text='搜索步骤  '
                                                                             '由于空间大小限制，最多能显示25步'
                                                                             '，详情点击<更多>按钮'
                          , font=18).grid(row=6, column=0, columnspan=6)

    # 选择算法
    v = tk.IntVar()
    v.set(1)
    tk.Radiobutton(window, text='A*算法', variable=v, value=1,
                   bg='#E0FFFF', font=10, anchor='w').place(x=35, y=270)
    tk.Radiobutton(window, text='A*算法2', variable=v, value=4,
                   bg='#E0FFFF', font=10, anchor='w').place(x=180, y=270)
    tk.Radiobutton(window, text='A*算法3', variable=v, value=5,
                   bg='#E0FFFF', font=10, anchor='w').place(x=330, y=270)
    tk.Radiobutton(window, text='深度优先算法', variable=v, value=2,
                   bg='#E0FFFF', font=10, anchor='w').place(x=35, y=300)
    tk.Radiobutton(window, text='广度优先算法', variable=v, value=3,
                   bg='#E0FFFF', font=10, anchor='w').place(x=180, y=300)
    tk.Radiobutton(window, text='随机决策算法', variable=v, value=6,
                   bg='#E0FFFF', font=10, anchor='w').place(x=330, y=300)

    # 开始8数码或者15数码游戏
    button_start = tk.Button(window, text='开始搜索',
                             bg='white', font=('宋体', 13),
                             command=start_game)
    button_start.place(x=320, y=340, width=100, height=28)

    tk.Label(window, text='数码N：', font=('宋体', 16), bg='#E0FFFF').place(x=50, y=340)
    e1 = tk.Entry(window, show=None, font=('Arial', 10))
    e1.place(x=130, y=340, width=70, height=28)  # 显示成明文形式
    tk.Button(window, text='ok', command=get, bg='white').place(x=200, y=340, width=40, height=28)

    # 设置初始和目标状态
    tk.Label(window, text='初始状态', font=('宋体', 12), bg='#E0FFFF').place(x=5, y=20)
    tk.Label(window, text='目标状态', font=('宋体', 12), bg='#E0FFFF').place(x=250, y=20)
    tk.Button(window, text='产生随机数', bg='white', font=('宋体', 10), command=ran).place(x=345, y=20, width=80, height=28)

    # 输出结束时的相关消息
    move = tk.Label(window, text='步数:', font=('宋体', 15), bg='#FFFAF0')
    move.place(x=550, y=300)
    move = tk.Label(window, text='节点数:', font=('宋体', 15), bg='#FFFAF0')
    move.place(x=800, y=300)
    move = tk.Label(window, text='耗时:', font=('宋体', 15), bg='#FFFAF0')
    move.place(x=550, y=340)
    move = tk.Label(window, text='内存:', font=('宋体', 15), bg='#FFFAF0')
    move.place(x=550, y=380)
    tk.Button(window, text='更多', bg='white', font=('宋体', 13), command=more).place(x=850, y=350, width=100, height=28)


    # 主窗口循环显示
    window.mainloop()
