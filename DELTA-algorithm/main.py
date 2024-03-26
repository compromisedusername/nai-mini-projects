import math
import os
import random


def read_data(file):
    with open(file, 'r') as p:
        tekst = p.read()
    p.close()
    tekst = tekst.replace(",", ".")
    return tekst


def make_vector(data):
    dict = {}
    column = data.split()
    vector = column[:-1]
    vector.append(-1)
    dict[tuple(vector)] = (column[-1])
    return dict


def make_vectors(data):
    vector = []
    for line in data.splitlines():
        vector.append(make_vector(line))
    return vector


def dot_product(w, t):
    dot_factor = 0.0
    for i in range(0, len(w)):
        dot_factor = dot_factor + float(w[i]) * float(t[i])
    ##print(dot_factor, "<------DOT_FACTOR")
    return dot_factor


def sum_vectors(w, t):
    new_w = []
    for i in range(0, len(w)):
        new_w.append(float(w[i]) + float(t[i]))
    ##print(new_w, "<------NEW WECTOR")
    return new_w


def scale_matrix(matrix, x):
    scaled_matrix = []
    for i in range(0, len(matrix)):
        scaled_matrix.append(float(matrix[i]) * x)
    return scaled_matrix


def new_weight(w, t, alfa, decision_factor):
    return sum_vectors(w, scale_matrix(t, alfa * decision_factor))


def calculate_weights(training_data_vectors, alfa, classname, weight):
    weights_not_change = 0
    old_weight = []
    while weights_not_change < 1:
        for vector in training_data_vectors:
            for v, k in vector.items():
                old_weight = weight
                net = dot_product(weight, v)
                if net >= 0:
                    output = 1
                else:
                    output = 0
                if ((output == 1) & (k != classname)):
                    weight = new_weight(weight, v, alfa, -1)
                    print(v, k, "Output 1, but attribute is other than Iris-setosa!")
                elif ((output == 0) & (k == classname)):
                    weight = new_weight(weight, v, alfa, 1)
                    print(v, k, "Output 0, but attribute is  Iris-setosa!")
        if (old_weight == weight):
            weights_not_change = weights_not_change + 1
            print("NEW WEIGHT: ", weight)
    print("----CALCULATING WEIGHT FINISHED----[", weights_not_change, "]")
    return weight


def delta_algorithm(training_data, testing_data, alfa):
    training_data_vectors = make_vectors(training_data)
    testing_data_vectors = make_vectors(testing_data)
    ## utworzenie wektorow

    weight = []
    for i in training_data_vectors[0].keys():
        for j in i:
            weight.append(random.uniform(-1, 1))
    initial_weight = weight

    weight = calculate_weights(training_data_vectors, alfa, "Iris-setosa", weight)
    classifications = 1
    data_rows = 1
    for vector in testing_data_vectors:
        for v, k in vector.items():
            net = dot_product(weight, v)
            if (net >= 0) & (k == "Iris-setosa"):
                print("Positive classification ", v, k, ", Output -> 1")
                classifications = classifications + 1
            elif (net < 0) & (k != "Iris-setosa"):
                print("Positive classifaction ", v, k, ", Output -> 0")
                classifications = classifications + 1
            else:
                print("Not positive classification ", v, k, "Output ->", net)
        data_rows = data_rows + 1
    accuracy = classifications / data_rows
    print("Accuracy: ", accuracy * 100, "&")
    return weight


print("INPUT --> input your own vector")
print("EXIT --> use file")

cwd = os.getcwd()
print('\nFILES in ', cwd, ' :\n--------------------')

for filename in os.listdir(cwd):
    if (filename.endswith(".txt")):
        print(filename)
print("--------------------\n")
file_training = input("Input training file name [Or type enter to use standard set]:")
file_testing = input("Input testing file name [Or type enter to use standard set]:")
if (file_training == ""):
    file_training = "../iris_training.txt"
if (file_testing == ""):
    file_testing = "../iris_test.txt"

if (not os.path.isfile(file_testing)):
    print(f"File \'{file_testing}\' doesnt exists! Used file: \'iris_test.txt\'")
file_testing = "../iris_test.txt"
if (not os.path.isfile(file_training)):
    print(f"File \'{file_training}\' doesnt exists! Used file: \'iris_training.txt\'")
file_training = "../iris_training.txt"
training_data = read_data(file_training)
testing_data = read_data(file_testing)
with open(file_training, "r") as f:
    line = f.readline()
    dimension = len(line.split()) - 1
alfa = (input("Do you want to input learning rate (alfa)? Type [y/n]"))
while True:
    if (alfa == "y"):
        alfa = float(input("Input learning rate: "))
    else:
        alfa = 0.056789
    weight = delta_algorithm(training_data, testing_data, 0.01)
    next_print = input("Type e for exit: ")
    if (next_print == "e"):
        break;
    while True:
        print(f"Input vector in the form:\n-------------------------\n [EXAMPLE] --> : 5.1  3.5 ... "
              "\n-------------------------\nInput values [in ", dimension, "- DIMENSIONS] [or type exit] ")
        vector = input(":")
        if vector == "exit":
            break
        while (len(vector.split())) != dimension:
            print("Vector must be in ", dimension, "dimension!")
            vector = input("Input vector: ")
        vector = vector + " -1"
        float_vector = vector.split(" ")
        if (dot_product(weight, float_vector) >= 0):
            print(vector," CLASSIFIED AS Iris-setosa")
        else:
            print(vector, " CLASSIFIED AS NON Iris-setosa")

