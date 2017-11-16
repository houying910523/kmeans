#! /usr/bin/python
# coding=utf-8

import math
import random
import matplotlib.pyplot as plt


class KMeansPlus:
    def __init__(self, vectors, k):
        self.vectors = vectors  # n * m的矩阵，m为向量维度，n为像两个数
        self.k = k
        self.result = dict()
        self.debug = False
        self.threshold = 0.0001

    def init_center(self, vectors):
        center = []
        r = int(random.random() * len(vectors))
        c1 = vectors[r]
        center.append(c1)
        vectors.pop(r)

        for i in range(1, self.k):
            #计算每个点到聚类中心最近的距离
            min_dist_2_center = []
            print "计算第" + str(i) + "个初始点"
            for idx, v in enumerate(vectors):
                dist_2_centers = [self.distance(v, c) for c in center]
                min_index, min_value = self.find_min(dist_2_centers)
                min_dist_2_center.append((idx, v, min_value))

            # 选出最近距离中最远的那个
            max_dist_tuple = min_dist_2_center[0]
            for t in min_dist_2_center:
                if t[2] >= max_dist_tuple[2]:
                    max_dist_tuple = t

            center.append(max_dist_tuple[1])
            vectors.pop(max_dist_tuple[0])

        return center

    @staticmethod
    def add_vector(v1, v2):
        return map(lambda x, y: x + y, v1, v2)

    @staticmethod
    def distance(v1, v2):
        dxy = map(lambda x, y: x - y, v1, v2)
        return math.sqrt(sum(map(lambda x: x * x, dxy)))

    @staticmethod
    def find_min(tuple_list):
        min_value = tuple_list[0]
        index = 0
        for i, v in enumerate(tuple_list):
            if v < min_value:
                min_value = v
                index = i
        return index, min_value

    def debug_view(self, local_center, local_groups):
        center_x = [local_center[v][0] for v in local_groups.keys()]
        center_y = [local_center[v][1] for v in local_groups.keys()]

        for k, v in local_groups.iteritems():
            x = []
            y = []
            for point in self.vectors[v]:
                x.append(point[0])
                y.append(point[1])

            center_x.remove(local_center[k][0])
            center_y.remove(local_center[k][1])
            plt.figure()
            plt.scatter(center_x, center_y)
            plt.scatter(x, y)
            plt.scatter([local_center[k][0]], [local_center[k][1]])
            plt.show()

    def train(self):
        groups = {}  # key是数字，value用来存储已经分类的向量的索引

        vectors = [v for v in self.vectors]

        center = self.init_center(vectors)  # 用来存储聚簇的中心点,[[x1,x2,x3,...],[x1,x2,x3,...],...]
        print "初始化完成。。。"
        print center
        local_center = center
        while True:
            print "【迭代】"
            local_groups = dict()
            for idx, v in enumerate(self.vectors):
                # 求距center中最近的点
                dist_vec = [self.distance(c, v) for c in local_center]
                min_index, min_value = self.find_min(dist_vec)
                # 把该点加到相应的组里
                if min_index != -1:
                    local_groups.setdefault(min_index, []).append(idx)

            print len(local_groups)

            sum_vectors = [
                (reduce(self.add_vector, map(lambda i: self.vectors[i], group_index_list)), len(group_index_list))
                for group_index_list in local_groups.values()]
            mean_vector = [map(lambda x: x / sum_vector[1], sum_vector[0]) for sum_vector in sum_vectors]

            if self.debug:
                self.debug_view(local_center, local_groups)

            if reduce(lambda x, y: x and y,
                      [(self.distance(t[0], t[1]) < self.threshold) for t in zip(local_center, mean_vector)]):
                groups = local_groups
                center = local_center
                break

            local_center = mean_vector

        return groups, center
