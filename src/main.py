#! /usr/bin/python

from kmeans import KMeans
from kmeans_plus import KMeansPlus
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

    kmeans = KMeansPlus(vectors, 4)
    #kmeans = KMeans(vectors, 4)
    groups, center = kmeans.train()

    for k, v in groups.iteritems():
        print k, v

    plt.figure()
    for k, v in groups.iteritems():
        x = []
        y = []
        for point in v:
            x.append(vectors[point][0])
            y.append(vectors[point][1])

        plt.scatter(x, y)

    x = [v[0] for v in center]
    y = [v[1] for v in center]
    plt.scatter(x, y)

    plt.show()

