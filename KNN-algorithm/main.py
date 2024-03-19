import math


def read_data(file):
    with open(file, 'r') as p:
        tekst = p.read()
    p.close()
    tekst = tekst.replace(",", ".")
    return tekst


def euclidean_distance(p, q):
    squared_sum = 0
    for i in range(len(p)):
        diff = float(p[i]) - float(q[i])
        squared_sum += diff * diff
    return math.sqrt(squared_sum)


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


def get_verdiction(sorted_list_of_distance, k):
    k_smallest_elements = sorted_list_of_distance[:k]
    count_attribut = {}
    print(k_smallest_elements)
    for i in k_smallest_elements:
        data = i['data']['training']
        if data not in count_attribut:
            count_attribut[data] = 1
        else:
            count_attribut[data] += 1
    print('classified: ',max(count_attribut.keys()), )
    return max(count_attribut.keys())



def knn_classification(training_data, testing_data, k):

    if k <= 0:
        return 0
    training_data_vectors = make_vectors(training_data)
    testing_data_vectors = make_vectors(testing_data)

    classifications = {} ## klasyfikacje dla danych testowych
    list_of_distance = [] ## lista slownikow odleglosci
    i = 1
    for vec1 in testing_data_vectors:
        for k1, v1 in vec1.items():
            for vec2 in training_data_vectors:
                for k2, v2 in vec2.items():
                    distance = euclidean_distance(k1, k2)
                    list_of_distance.append({'distance': distance, 'data': ({'test': v1, 'training': v2})})
            list_of_distance.sort(key=lambda x: (x['distance'], x['data']['training']))
            classified_output = get_verdiction(list_of_distance, k)

            classifications[i] = (v1 == classified_output)
            i = i + 1
            list_of_distance = []
    positive_classification = 0
    for k, v in classifications.items():
        if v:
            positive_classification += 1
    return positive_classification / len(classifications)

print("INPUT --> input your own vector")
print("EXIT --> use file")
training_data = read_data("iris_training_T.txt")
testing_data = read_data("iris_test.txt")
while True:
    k = input("Input value of K [or type input]: ")
    if k != "input":
        print("\nAccuracy level:", knn_classification(training_data, testing_data, int(k))*100)
    else:
        while True:
            vector = input("\n\nInput vector in the form:\n-------------------------\n 5.1  3.5  1.4  0.2 ...\n-------------------------\nInput values [or type exit]: ")
            if vector == "exit":
                break
            vector = vector + " vector"
            k = input("Input value of K [Or type exit]: ")

            print("\n------------------------------------------------------------------------")
            knn_classification(training_data, vector, int(k))
            print("\n------------------------------------------------------------------------")


