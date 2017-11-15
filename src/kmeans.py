#! /usr/bin/python
# coding=utf-8

import math
import random
import matplotlib.pyplot as plt


class KMeans:
    def __init__(self, vectors, k):
        self.vectors = vectors  # n * m的矩阵，m为向量维度，n为像两个数
        self.k = k
        self.result = dict()
        self.debug = False
        self.threshold = 0.001

    def init_center(self, vectors):
        center = []
        for i in range(0, self.k):
            v = random.choice(vectors)
            center.append(v)
            vectors.remove(v)
        return center

    @staticmethod
    def add_vector(v1, v2):
        return map(lambda x, y: x + y, v1, v2)

    @staticmethod
    def distance(v1, v2):
        dxy = map(lambda x, y: x - y, v1, v2)
        return math.sqrt(sum(map(lambda x: x * x, dxy)))

    @staticmethod
    def min_index(tuple_list):
        min_value = tuple_list[0]
        index = 0
        for i, v in enumerate(tuple_list):
            if v < min_value:
                min_value = v
                index = i
        return index

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

        local_center = center
        while True:
            local_groups = dict()
            for idx, v in enumerate(self.vectors):
                # 求距center中最近的点
                dist_vec = [self.distance(c, v) for c in local_center]
                min_index = self.min_index(dist_vec)
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
