#! /usr/bin/python

from kmeans import KMeans
import matplotlib.pyplot as plt


def func1():
    f = open('../data/sentence_vector.txt', 'r')
    vectors = []
    for line in f:
        line = line.strip().split("\t")
        str_vector = line[1].split(" ")
        float_vector = map(lambda x: float(x), str_vector)
        vectors.append(float_vector)
    return vectors


def test():
    vectors = []
    with open('../data/train.txt', 'r') as f:
        for line in f:
            line = line.strip().split("\t")
            vectors.append([float(line[0]), float(line[1])])
    return vectors


if __name__ == '__main__':

    vectors = test()

    kmeans = KMeans(vectors, 10)
    groups = kmeans.train()

    plt.figure()
    for k, v in groups.iteritems():
        x = []
        y = []
        for point in v:
            x.append(point[0])
            y.append(point[1])

        plt.scatter(x, y)

    plt.show()

