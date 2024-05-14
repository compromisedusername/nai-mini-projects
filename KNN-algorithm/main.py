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


    classified_data = ""
    max_count = 0

    sorted_count_attribut = sorted(count_attribut.items(), key=lambda x: (x[1], x[0]))

    for v,k in sorted_count_attribut:
        if k > max_count:
            max_count = k
            classified_data = v
        #print(v,k, "<-----ELEMENTY")
    #print(classified_data,"<-----CLASSIFIED, ELEMENTS: ", max_count)
    return classified_data



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
            if v1 != "vector":
                print("Testing data: " ,v1,", Classified data: ", classified_output)
            else:
                print("Classified data: ", classified_output)
            i = i + 1
            list_of_distance = []
    positive_classification = 0
    for k, v in classifications.items():
        if v:
            positive_classification += 1
    return positive_classification / len(classifications)

print("INPUT --> input your own vector")
print("EXIT --> use file")
import os

print("\nFILES:\n--------------------")
cwd = os.getcwd()
for filename in os.listdir(cwd):
  if(filename.endswith(".txt")):
    print(filename)
print("--------------------\n")
file_training=input("Input training file name: ")
file_testing=input("Input testing file name: ")
if(file_training == ""):
    file_training = "iris_training.txt"
if(file_testing == ""):
    file_testing = "iris_test.txt"

if( not os.path.isfile(file_testing)):
    print(f"File \'{file_testing}\' doesnt exists! Used file: \'iris_test.txt\'")
    file_testing="iris_test.txt"
if( not os.path.isfile(file_training)):
    print(f"File \'{file_training}\' doesnt exists! Used file: \'iris_training.txt\'")
    file_training="iris_training.txt"
training_data = read_data(file_training)
testing_data = read_data(file_testing)
while True:


    k = input("-------DATA FROM FILES-------\nInput value of K [or type input]: ")
    if k != "input":
        print("\nAccuracy level:", knn_classification(training_data, testing_data, int(k))*100)
    else:
        while True:
            with open(file_training, "r") as f:
                line = f.readline()
                dimension = len(line.split()) - 1
            print("\nVector must be in ", dimension, "dimension!")
            vector = input("Input vector in the form:\n-------------------------\n 5.1  3.5  1.4  0.2 "
                           "...\n-------------------------\nInput values [or type exit]: ")
            if vector == "exit":
                break
            while (len(vector.split())) != dimension:
                print("Vector must be in ", dimension, "dimension!")
                vector = input("Input vector: ")

            vector = vector + " vector"
            k = input("Input value of K [or type exit]: ")
            if k == "exit":
                break
            print("\nCLASSIFICATION:---------------------------------------------------------")
            knn_classification(training_data, vector, int(k))
            print("\nEND---------------------------------------------------------------------")


