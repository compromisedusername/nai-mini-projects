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
    return sorted(vectors.keys())[:k+1]


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


def print_distance_dict(distance_dict):
    count_vectors = 1
    for k, v in distance_dict.items():
        count_vectors = count_vectors + 1
        print(k , v)
    print(count_vectors)

def knn_classification(training_data, testing_data, k):
    training_data_vectors = make_vectors(training_data)
    testing_data_vectors = make_vectors(testing_data)

    distance_dict = {} ## slownik z parami [odlegosc --> tuple(zaklasyfikowany kwiat, podany testowy kwiat)]
    classifications = {} ## klasyfikacje dla danych testowych
    losted_nieghbourhoods = [] ## zgubieni sasiedzi przez nadpisanie sasiada gdy dzieli ich ta sama odleglosc

    i = 1
    for vec1 in testing_data_vectors:
        for k1, v1 in vec1.items():
            for vec2 in training_data_vectors:
                for k2, v2 in vec2.items():
                    distance = euclidean_distance(k1, k2)
                    if distance in distance_dict:
                        losted_nieghbourhoods.append({distance: tuple([v1, v2])})
                    distance_dict[distance] = tuple([v1, v2])
            print( losted_nieghbourhoods, "ZGUBIENI SOMSIEDZI")
            k_smallest = get_k_smallest(distance_dict, k)
            print(len(distance_dict), "<----------- WIELKOSC DISTANCE_DICT")
            print(len(k_smallest), "<----------- WIELKOSC k_SMALLEST")

            ##            print("Dla wiersza ", i, " -> ", k_smallest, print_classified_vector(distance_dict, k_smallest, k))
            ##print("Classification based on training data -> ", get_verdiction(k_smallest, distance_dict, k)[0])
            ##print("input data -> ", v1)
            ##print("")
            classifications[i] = (v1 == get_verdiction(k_smallest, distance_dict, k)[1])
            i = i + 1
            ##print_distance_dict(distance_dict)
            distance_dict = {}
        losted_nieghbourhoods = []

    positive_classification = 0
    for k, v in classifications.items():
        if v:
            positive_classification = 1 + positive_classification


    return positive_classification / len(classifications)


training_data = read_data("iris_training.txt")
testing_data = read_data("iris_test.txt")
while True:
    k = input("Input value of K: [Or type input]")
    if k != "input":
        print("\nAccuracy level:", knn_classification(training_data, testing_data, int(k))*100)
    else:
        while True:
            vector = input("\n\nInput vector in the form:\n-------------------------\n 5.1  3.5  1.4  0.2 ...\n-------------------------\nInput:")
            vector = vector + " vector"
            k = input("Input value of K: [Or type exit]")
            if k == "exit":
                break
            print("\n------------------------------------------------------------------------")
            print("Accuracy level:", knn_classification(training_data, vector, int(k))*100, "\n------------------------------------------------------------------------")


