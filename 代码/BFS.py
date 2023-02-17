import numpy as np
import datetime

m = 0  # 步骤数
time = ''  # 耗时
nodes = 0  # 节点数
stack = []  # 存储步骤
judge = 0  # 标记是否有解


def ma(Block, Goal, N):
    # 节点状态类
    class State:
        def __init__(self, state, directionFlag=None, parent=None):
            self.state = state  # 状态是一个 ndarray 具有一个形状(3,3)来存储状态
            self.direction = ['up', 'down', 'right', 'left']  # 移动方向
            if directionFlag:  # 向哪个方向移动
                self.direction.remove(directionFlag)
            self.parent = parent  # 父节点
            self.symbol = 0  # 零点

        # 获取方向
        def getDirection(self):
            return self.direction

        # 输出N数码状态
        def showInfo(self):
            stack.append(self.state)  # 将步骤添加到栈中
            # for i in range(N):
            #     for j in range(N):
            #         print(self.state[i, j], end='  ')
            #     print("\n")
            # print('->')
            return

        # 获取0的位置
        def getEmptyPos(self):
            postion = np.where(self.state == self.symbol)
            return postion

        # 获得子节点
        def generateSubStates(self):
            if not self.direction:
                return []
            subStates = []  # 存储子节点
            boarder = len(self.state) - 1  # 边界
            # the maximum of the x,y
            row, col = self.getEmptyPos()
            global nodes
            if 'left' in self.direction and col > 0:  # it can move to left
                s = self.state.copy()
                temp = s.copy()
                s[row, col] = s[row, col - 1]
                s[row, col - 1] = temp[row, col]
                news = State(s, directionFlag='right', parent=self)
                subStates.append(news)
            if 'up' in self.direction and row > 0:  # it can move to upper place
                s = self.state.copy()
                temp = s.copy()
                s[row, col] = s[row - 1, col]
                s[row - 1, col] = temp[row, col]
                news = State(s, directionFlag='down', parent=self)
                subStates.append(news)
            if 'down' in self.direction and row < boarder:  # it can move to down place
                s = self.state.copy()
                temp = s.copy()
                s[row, col] = s[row + 1, col]
                s[row + 1, col] = temp[row, col]
                news = State(s, directionFlag='up', parent=self)
                subStates.append(news)
            if self.direction.count('right') and col < boarder:  # it can move to right place
                s = self.state.copy()
                temp = s.copy()
                s[row, col] = s[row, col + 1]
                s[row, col + 1] = temp[row, col]
                news = State(s, directionFlag='left', parent=self)
                subStates.append(news)
            return subStates

        # BFS算法
        def solve(self, start_time):
            # generate a empty openTable
            openTable = []
            # generate a empty closeTable
            closeTable = []
            # append the origin state to the openTable
            openTable.append(self)
            steps = 1

            # start the loop
            while len(openTable) > 0:
                # 超时处理
                if (datetime.datetime.now()-start_time).total_seconds() > 20:
                    print("Time running out, break !")
                    return None, None
                n = openTable.pop(0)  # pop第一个元素
                closeTable.append(n)  # 记录已访问过的节点
                subStates = n.generateSubStates()  # 子状态
                path = []  # 路径
                for s in subStates:
                    if (s.state == s.answer).all():  # 结束
                        while s.parent and s.parent != originState:
                            path.append(s.parent)
                            s = s.parent
                        path.reverse()  # 路径反转
                        return path, steps + 1
                openTable.extend(subStates)
                steps += 1
            else:
                return None, None

    # set the origin state of the puzzle
    originState = State(np.array(Block))
    # and set the right answer in terms of the origin
    State.answer = np.array(Goal)
    s1 = State(state=originState.state)  # 初始状态类State

    start_t = datetime.datetime.now()
    path, steps = s1.solve(start_t)  # 搜索
    end_t = datetime.datetime.now()

    global m
    if path:  # if find the solution
        for node in path:
            # print the path from the origin to final state
            node.showInfo()
            m = m + 1
        # print(State.answer)
        # print("Total steps is %d" % steps)
    else:
        m = -1
        global judge
        judge = 1

    stack.append(State.answer)
    global nodes
    nodes = steps
    global time
    time = (end_t - start_t).total_seconds()
    time = str(time) + "s"
    if judge == 0:
        print("length =", m)  # 步数
        print("time = ", time)  # 耗时
        print("Nodes =", steps)  # 搜索树包含节点个数
