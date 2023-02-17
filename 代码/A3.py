import heapq  # 堆
import copy
import datetime

m = 0  # 步骤数
time = ''  # 耗时
nodes = 0  # 节点数
stack = []  # 存储步骤
BLOCK = [[]]  # 给定状态
GOAL = [[]]  # 目标状态

# 4个方向
direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]

# OPEN表
OPEN = []

# 节点的总数
SUM_NODE_NUM = 0

judge = 0  # 标记是否有解


def ma(Block, Goal):
    # 状态节点
    class State(object):
        def __init__(self, gn=0, hn=0, state=None, hash_value=None, par=None):
            self.gn = gn
            self.hn = hn
            self.fn = self.gn + self.hn
            self.child = []  # 孩子节点
            self.par = par  # 父节点
            self.state = state  # 局面状态
            self.hash_value = hash_value  # 哈希值

        def __lt__(self, other):  # 用于堆的比较，返回距离最小的
            return self.fn < other.fn

        def __eq__(self, other):  # 相等的判断
            return self.hash_value == other.hash_value

        def __ne__(self, other):  # 不等的判断
            return not self.__eq__(other)

    # 计算启发距离
    def distance_fn(cur_node, end_node):
        cur_state = cur_node.state  # 当前数码矩阵的状态
        end_state = end_node.state  # 目标数码矩阵的状态
        dist1 = 0
        dist2 = 0
        N = len(cur_state)  # N表示几数码
        for i in range(N):
            for j in range(N):
                num = cur_state[i][j]
                for p in range(N):
                    k = 0
                    for q in range(N):
                        if end_state[p][q] == num:
                            dist1 = dist1 + abs(i-p) + abs(j-q)
                            k = 1
                            break
                    if k == 1:
                        break
        for i in range(N):
            for j in range(N):
                if cur_state[i][j] == end_state[i][j]:
                    continue
                dist2 = dist2 + 1  # 以“不在位”的数码数作为启发信息的度量

        if dist1 == 0:
            return 0
        else:
            return dist2/dist1

    # 生成子节点
    def generate_child(cur_node, end_node, hash_set, open_table, dis_fn):
        if cur_node == end_node:
            heapq.heappush(open_table, end_node)  # OK的点加入open表
            return
        num = len(cur_node.state)
        for i in range(0, num):
            for j in range(0, num):
                if cur_node.state[i][j] != 0:
                    continue
                for d in direction:  # 四个偏移方向，对零点移动
                    x = i + d[0]
                    y = j + d[1]
                    if x < 0 or x >= num or y < 0 or y >= num:  # 越界了
                        continue

                    # 记录扩展节点的个数
                    global SUM_NODE_NUM
                    SUM_NODE_NUM += 1

                    # 移动
                    state = copy.deepcopy(cur_node.state)  # 复制父节点的状态
                    state[i][j], state[x][y] = state[x][y], state[i][j]  # 交换位置

                    # 判重
                    h = hash(str(state))  # 哈希时要先转换成字符串
                    if h in hash_set:  # 重复了
                        continue
                    hash_set.add(h)  # 加入哈希表

                    gn = cur_node.gn + 1  # 已经走的距离函数
                    hn = dis_fn(cur_node, end_node)  # 启发的距离函数
                    node = State(gn, hn, state, h, cur_node)  # 新建节点
                    cur_node.child.append(node)  # 加入到孩子队列
                    heapq.heappush(open_table, node)  # 加入到堆中

    # 打印路径
    def print_path(node):
        num = node.gn  # 即步骤数
        global stack
        stack = []  # 模拟栈

        # 存储每一步
        while node.par is not None:
            stack.append(node.state)
            node = node.par
        stack.append(node.state)

        return num

    # A*3算法
    def A_start(start, end, distance, generate_child_fn, time_limit=20):
        root = State(0, 0, start, hash(str(BLOCK)), None)  # 根节点
        end_state = State(0, 0, end, hash(str(GOAL)), None)  # 最后的节点
        if root == end_state:
            print("start == end !")

        OPEN.append(root)
        heapq.heapify(OPEN)

        node_hash_set = set()  # 存储节点的哈希值
        node_hash_set.add(root.hash_value)
        start_time = datetime.datetime.now()
        global judge

        while len(OPEN) != 0:
            top = heapq.heappop(OPEN)  # 返回 root 节点，即 heap 中最小的元素。
            if top == end_state:  # 结束后直接输出路径
                return print_path(top)
            # 产生孩子节点，孩子节点加入OPEN表
            generate_child_fn(cur_node=top, end_node=end_state, hash_set=node_hash_set,
                              open_table=OPEN, dis_fn=distance)

            # 超时处理
            cur_time = datetime.datetime.now()
            if (cur_time - start_time).seconds > time_limit:
                print("Time running out, break !")
                print("Number of nodes:", SUM_NODE_NUM)
                judge = 1
                return -1

        print("No road !")  # 没有路径
        judge = 1
        return -1

    GOAL = Goal # 目标状态
    OPEN = []  # 这里别忘了清空
    BLOCK = Block # 初始状态

    start_t = datetime.datetime.now()  # 记录初始时间
    length = A_start(BLOCK, GOAL,  distance_fn, generate_child, time_limit=20)  # A*算法
    end_t = datetime.datetime.now()  # 记录结束时间

    if length != -1:
        print("length =", length)  # 步数
        print("time = ", (end_t - start_t).total_seconds(), "s")  # 耗时
        print("Nodes =", SUM_NODE_NUM)  # 搜索树包含节点个数

    # 返回给主函数的参数
    global m
    m = length
    global time
    time = (end_t - start_t).total_seconds()
    time = str(time) + "s"
    global nodes
    nodes = SUM_NODE_NUM
