import math
import csv


def read_data(plik):
    with open(plik, 'r') as p:
        tekst = p.read()
    p.close()
    tekst = tekst.replace(",", ".")
    return tekst


def euclidean_distance(p, q):
    quadratic_sum = 0
    for i in range(len(p)):
        diff = float(p[i]) - float(q[i])
        quadratic_sum += diff * diff
    return math.sqrt(quadratic_sum)


def make_vector(data):
    dict = {}
    column = data.split()
    vector = column[:-1]
    dict[tuple(vector)] = (column[-1])
    return dict


def make_vectors(data):
    vector = []
    for line in data.splitlines():
        vector.append(make_vector(line))
    return vector


def get_k_smallest(vectors, k):
    return sorted(vectors.keys())[:k]


def get_verdiction(vectors, dict, k):
    count_attribut = {}
    for i in range(0, k):
        count_attribut[dict[vectors[i]]] = count_attribut.get(dict[vectors[i]], 0) + 1
    return max(count_attribut.keys())




def print_classified_vector(distance, smallest, k):
    dist = {}
    for i in range(0, k):
        dist[i] = (distance[smallest[i]])
    return dist

def knn_classification(training_data, testing_data, k):
    training_data_vectors = make_vectors(training_data)
    testing_data_vectors = make_vectors(testing_data)

    distance_dict = {}
    classifications = {}

    i = 1
    for vec1 in testing_data_vectors:
        for k1, v1 in vec1.items():
            for vec2 in training_data_vectors:
                for k2, v2 in vec2.items():
                    distance = euclidean_distance(k1, k2)
                    distance_dict[distance] = tuple([v1, v2])
            k_smallest = get_k_smallest(distance_dict, k)
           ## print("Dla wiersza ", i, " -> ", k_smallest, print_classified_vector(distance_dict, k_smallest, k))
            print("Wyliczony kwiatek -> ", get_verdiction(k_smallest, distance_dict, k)[1])
            print("Kwiatek z listy testowej -> ", v1)
            print("")
            classifications[i] = (v1 == get_verdiction(k_smallest, distance_dict, k)[1])
            i = i + 1
            distance_dict = {}

    positive_classification = 0
    for k, v in classifications.items():
        if v:
            positive_classification = 1 + positive_classification


    return positive_classification / len(classifications)


training_data = read_data("iris_training.txt")
testing_data = read_data("iris_test.txt")

k = input("Input value of K.")

print("\nZgodność na poziomie:", knn_classification(training_data, testing_data, int(k))*100)
