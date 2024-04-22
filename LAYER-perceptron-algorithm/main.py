import math
import os
import random


def read_data(file):
    with open(file, 'r',encoding="utf-8") as p:
        tekst = p.read()
    p.close()
    return tekst


def make_vector(data, attirbute = "-"):
    dict = {}
    vector = []
    letters = "abcdefghijklmnopqrstuvwxyz"
    for letter in letters:
        dict[letter] = 0

    letters_count = 0

    for line in data:
        for letter in line.lower():
            if letter in letters:
                dict[letter] += 1
                letters_count += 1

    for i in dict.items():
        vector.append(i[1]/letters_count)
    vector.append(-1)

    dict = {tuple(vector): attirbute}
    return dict


def make_vectors(dir):
    vector = []
    for dir_in in os.listdir(dir):
        dirpath = dir+"/"+dir_in
        for file in os.listdir(dirpath):
            filepath = (dirpath+"/"+file)
            vector.append(make_vector(read_data(filepath),dir_in))
    return vector







def dot_product(w, t):
    dot_factor = 0.0
    for i in range(0, len(w)):
        dot_factor = dot_factor + float(w[i]) * float(t[i])
    ##print(dot_factor, "<------DOT_FACTOR")
    return dot_factor


def sum_vectors(x, w):
    new_w = []
    for i in range(0, len(x)):
        new_w.append(float(x[i]) + float(w[i]))
    return new_w


def scale_matrix(matrix, x):
    scaled_matrix = []
    for i in range(0, len(matrix)):
        scaled_matrix.append(float(matrix[i]) * x)
    return scaled_matrix


def new_weight(w, t, alfa, decision_factor):
    return sum_vectors(w, scale_matrix(t, alfa * decision_factor))


def calculate_weights(training_data_vectors, alfa, classname, weight):

    missed_classifications = 1
    while(missed_classifications > 0):
        missed_classifications = 0
        for vector in training_data_vectors:
            for v, k in vector.items():
                net = dot_product(weight, v)
                if ((net >= 0) & (k != classname)):
                    weight = new_weight(weight, v, alfa, -1)
                    print( "For ",k, " output 1, but attribute is  ",classname, "NET VALUE: ",net)
                    missed_classifications += 1
                elif ((net < 0) & (k == classname)):
                    weight = new_weight(weight, v, alfa, 1)
                    print( "For ",k, " output 0, but attribute is ",classname, "NET VALUE: ",net)
                    missed_classifications += 1
    return weight




def layer_perceptron(alfa):

    training_data_vectors = make_vectors("data_training")
    testing_data_vectors = make_vectors("data_testing")

    random_weights = []
    weights = {}
    for i in range(0,27):
        random_weights.append(random.uniform(-1, 1))

    classifications = 1
    data_rows = 1

    for language in os.listdir("data_training"):
        weights[language] = calculate_weights(training_data_vectors, alfa, language, random_weights) ## mamy policzone wagi
    for vector in testing_data_vectors:
        for v, k in vector.items():
            dot_products = {}
            for weight in weights.items():
                dot_products[weight[0]]=(dot_product(v,weight[1]))
            language, max_val = max(dot_products.items(), key=lambda item: item[1])
            if(k == language):
                classifications += 1
            print(k,max_val, "classified as", language )
            data_rows += 1
    print("Accuracy: ", (classifications / data_rows)*100, "%")
    return weights




def classify_input_text(weights):
    text = []
    print("Enter/Paste your text. Press Ctrl-D to finish the current session of input.")
    while True:
        try:
            line = input()
            if line.strip() == ":q":
                print("Exiting program.")
        except EOFError:
            print("End of current input session.")
            break
        text.append(line)


    print(text)
    input_text_vector = make_vector(text)
    for vector in input_text_vector:
            dot_products = {}
            for weight in weights.items():
                dot_products[weight[0]] = (dot_product(vector, weight[1]))
            language, max_val = max(dot_products.items(), key=lambda item: item[1])
            print( max_val, " Given text classified as: ", language)





calculated_weights = layer_perceptron(0.05)
classify_input_text(calculated_weights)