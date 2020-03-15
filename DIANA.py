import math
import numpy as np
import pylab as pl


# 加载数据
def loadData(filename):
    dataSet = np.loadtxt(filename, delimiter='\t', encoding="UTF-8-sig")
    return dataSet


# 计算欧式距离
def dist(X, Y):
    # X 代表坐标(x1, x2)   Y 代表坐标(y1, y2)
    return math.sqrt(math.pow(X[0] - Y[0], 2) + math.pow(X[1] - Y[1], 2))


# 找到具有最大直径的簇
def find_Maxdis(M):
    avg_Dissimilarity = []  # 平均相异度数组
    max_Dissimilarity = -1  # 最大平均相异度
    numOrder = 0
    # M 为 (n, n) 矩阵, 对每个点计算平均相异度
    for i in range(len(M)):
        dis = 0
        for j in range(len(M[i])):
            if i != j:
                dis += M[i][j]
        avg_Dissimilarity.append(dis / (len(M) - 1))
        # print(str(avg_Dissimilarity[i])+ "    " + str(i))
    # 在找到平均相异度的最大值
    for m in range(len(avg_Dissimilarity)):
        if max_Dissimilarity < avg_Dissimilarity[m]:
            max_Dissimilarity = avg_Dissimilarity[m]
            numOrder = m
    # print(str(max_Dissimilarity) + "    " + str(k))

    # 返回当前平均相异度最大的簇的序号和平均相异度
    return numOrder, max_Dissimilarity


def DIANA(dataSet, k):
    '''第一步，找到具有最大直径的簇，对簇中的每个点计算平均相异度 ["找出最突出的点"],
	挑选一个最大平均相异度的点放入splinter group中, 剩余点放在old party中.'''
    C = []  # 初始簇, 所有对象为一个簇
    M = []  # 每个对象间的距离矩阵
    for ci in dataSet:
        # 先构造一维数组, 每一个对象为一个一维数组
        c = []
        c.append(ci)
        # 再将一维数组加入到数组中, 便构成了二维数组.
        C.append(ci)
    for ci in dataSet:
        Mi = []
        for cj in dataSet:
            Mi.append(dist(ci, cj))
        M.append(Mi)
    # 挑选一个最大平均相异度的点放入splinter group中, 剩余点放在old party中.
    numOrder, max_Dissimilarity = find_Maxdis(M)
    splinter_group = []
    old_party = []
    C_num = list(range(len(dataSet)))
    splinter_group.append(numOrder)
    C_num.remove(numOrder)
    for num in C_num:
        old_party.append(num)
    '''第二步，在old party里找出   
                        **到splinter group的距离**
                            小于
                        **到old party的距离的点**
                    将该点放入splinter group中,
            Repeat ["不停地找最突出的点加入splinter group"]
            Until 没有新的old party的点被分配给splinter group；
            Splinter group 和old party为被选中的簇分裂成的两个簇，与其他簇一起组成新的簇集合
            END'''
    i = 1
    while i != k:
        # 在old party里找出**到splinter group的距离**小于**到old party的距离的点**
        dis_Old_Old = 0
        dis_Old_Splinter = 0
        for old in old_party:
            print(splinter_group)
            # print(old_party)

            # 在old party里先找到old party的距离---这里指平均距离
            for old_other in old_party:
                # 自己到自己的距离为零, 所以不做其它处理
                dis_Old_Old += M[old][old_other]
            dis_Old_Old = dis_Old_Old / (len(old_party)-1)
            print("dis_Old_Old: " + str(dis_Old_Old))

            # 在old party里然后再找到splinter group的距离---这里指平均距离
            for splinter in splinter_group:
                dis_Old_Splinter += M[old][splinter]
            dis_Old_Splinter = dis_Old_Splinter / (len(splinter_group))
            print("dis_Old_Splinter: " + str(dis_Old_Splinter))

            # 比较后, 将满足条件的点放在splinter group中
            if dis_Old_Splinter < dis_Old_Old:
                splinter_group.append(old)
                print("每次加入到splinter_group的点: "+str(old))
            else:
                print("不满足条件的点: " + str(old))
            print("\n")
        i = i + 1


if __name__ == "__main__":
    dataSet = loadData('test.txt')
    # print(dataSet)
    k = 2  # k代表预设的最终聚类簇数
    DIANA(dataSet, k)
