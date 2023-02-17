import numpy as np
import datetime

m = 0  # 步骤数
time = ''  # 耗时
nodes = 0  # 节点数
stack = []  # 存储步骤
judge = 0  # 标记是否有解
limit = 5


def ma(Block, Goal, N):
    # 节点状态类
    class State:
        def __init__(self, state, directionFlag=None, parent=None, deep=0):
            self.state = state  # state is a ndarray with a shape(3,3) to storage the state
            self.direction = ['up', 'down', 'right', 'left']
            if directionFlag:
                self.direction.remove(directionFlag)
            # record the possible directions to generate the sub-states
            self.parent = parent
            self.symbol = 0
            self.deep = deep

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
            if self.direction.count('right') and col < boarder:  # it can move to right place
                s = self.state.copy()
                temp = s.copy()
                s[row, col] = s[row, col + 1]
                s[row, col + 1] = temp[row, col]
                deep = self.deep + 1
                news = State(s, directionFlag='left', parent=self, deep=deep)
                subStates.append(news)
                nodes = nodes + 1
            if 'down' in self.direction and row < boarder:  # it can move to down place
                s = self.state.copy()
                temp = s.copy()
                s[row, col] = s[row + 1, col]
                s[row + 1, col] = temp[row, col]
                deep = self.deep + 1
                news = State(s, directionFlag='up', parent=self, deep=deep)
                subStates.append(news)
                nodes = nodes + 1
            if 'up' in self.direction and row > 0:  # it can move to upper place
                s = self.state.copy()
                temp = s.copy()
                s[row, col] = s[row - 1, col]
                s[row - 1, col] = temp[row, col]
                deep = self.deep + 1
                news = State(s, directionFlag='down', parent=self, deep=deep)
                subStates.append(news)
                nodes = nodes + 1
            if 'left' in self.direction and col > 0:  # it can move to left
                s = self.state.copy()
                temp = s.copy()
                s[row, col] = s[row, col - 1]
                s[row, col - 1] = temp[row, col]
                deep = self.deep + 1
                news = State(s, directionFlag='right', parent=self, deep=deep)
                subStates.append(news)
                nodes = nodes + 1
            return subStates

        # DFS算法
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
                if (datetime.datetime.now()-start_time).total_seconds() > 20:
                    print("Time running out, break !")
                    return None, None
                n = openTable.pop()  # pop最后一个元素
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
                    flag = 0
                    for t in closeTable:
                        if (np.array(t.state) == np.array(s.state)).all():
                            flag = 1
                    if flag == 0:
                        if N == 4 and s.deep <= limit:
                            openTable.append(s)  # 在末尾加新的列表
                        if N == 3:
                            openTable.append(s)
                steps += 1
            else:
                return None, None

    # set the origin state of the puzzle
    originState = State(np.array(Block))
    # and set the right answer in terms of the origin
    State.answer = np.array(Goal)
    s1 = State(state=originState.state, deep=0)  # 初始状态类State

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
        stack.append(State.answer)
    else:
        m = -1
        global judge
        judge = 1

    global nodes
    nodes = steps
    global time
    time = (end_t - start_t).total_seconds()
    time = str(time) + "s"
    if judge == 0:
        print("length =", m)  # 步数
        print("time = ", time)  # 耗时
        print("Nodes =", steps)  # 搜索树包含节点个数
