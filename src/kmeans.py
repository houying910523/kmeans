#! /usr/bin/python
# coding=utf-8

import math
import random


class KMeans:
    def __init__(self, vectors, k):
        self.vectors = vectors  # n * m的矩阵，m为向量维度，n为像两个数
        self.k = k
        self.result = dict()

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
        index = -1
        for i, v in enumerate(tuple_list):
            if v <= min_value:
                index = i
        return index

    def train(self):
        groups = {}  # key是数字，value用来存储已经分类的点

        vectors = [v for v in self.vectors]

        center = self.init_center(vectors)  # 用来存储聚簇的中心点,[[x1,x2,x3,...],[x1,x2,x3,...],...]

        local_center = center
        while True:
            orig_vectors = [v for v in self.vectors]
            local_groups = dict()
            for v in orig_vectors:
                # 求距center中最近的点
                min_index = self.min_index([self.distance(c, v) for c in local_center])
                # 把该点加到相应的组里
                if min_index != -1:
                    # print "add to group " + str(min_index)
                    local_groups.setdefault(min_index, []).append(v)

            print len(local_groups)

            sum_vectors = [(reduce(self.add_vector, group_vector_list), len(group_vector_list)) for group_vector_list in local_groups.values()]
            mean_vector = [map(lambda x: x / sum_vector[1], sum_vector[0]) for sum_vector in sum_vectors]

            print mean_vector
            if reduce(lambda x, y: x and y,
                      [(self.distance(t[0], t[1]) < 0.01) for t in zip(local_center, mean_vector)]):
                groups = local_groups
                break

            local_center = mean_vector

        return groups
