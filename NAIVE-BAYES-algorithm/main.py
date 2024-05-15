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


def count_attributes(training_data):
    attribute_count = {}
    for vec in training_data:
        for vector, attribute in vec.items():
            if attribute not in attribute_count:
                attribute_count[attribute] = 1
            else:
                attribute_count[attribute] += 1
    return attribute_count

def probabilites(training_data):
    attribute_count = count_attributes(training_data)
    dict_probabilites = {} # " i[...]attribute "
    for vec in training_data:
        for vector, attribute in vec.items():
            for i in range(0,len(vector)):
                key = str(i)+str(vector[i])+str(attribute)
                if key not in dict_probabilites:
                    dict_probabilites[key] = 1
                else:
                    dict_probabilites[key] += 1
    unique_attribute_amount = len(attribute_count)

    # tutaj zaczniemy wygladzac dane
    for key_p, val_p in dict_probabilites.items(): # klucz i wartosci w slowniku ktory przechowuje  pod kluczem [ 'i' 'val' 'attribute' ] ich ilosci wystapien *i to nr kolumny*
        dict_probabilites[key_p] += 1 # dodajemy jedynke przy wygladzaniu
        for key_c, val_p in attribute_count.items(): # klucz i wartosc w slowniku przechowujacy pod kluczem attribute ich ilosci wystapien
            if key_c in key_p:
                dict_probabilites[key_p] /= (attribute_count[key_c] + unique_attribute_amount) # do mianownika dodajemy ilosc unikatowych atrybutow

    return dict_probabilites, attribute_count


def naive_bayes_classification(training_data, testing_data):


    training_data_vectors = make_vectors(training_data)
    testing_data_vectors = make_vectors(testing_data)

    attribute_count = probabilites(make_vectors(training_data))[1]
    smoothed_probabilites = probabilites(make_vectors(training_data))[0]

    classified_output = 0
    classifications = 0 ## klasyfikacje dla danych testowych
    bad_classifications = 0
    attribute = ""
    i = 1
    for vec1 in testing_data_vectors: # dla kazdego wektora testowego ...
        probability_every_attribute = {}
        for attribute_c, amount_count in attribute_count.items(): # dla kazdego atrybutu ze zbioru atrybutow i ich wystapien...
            for vector_test, attribute_v in vec1.items(): # dla kazdej wartosci i atrybutu ze zbioru testowego ...
                attribute = attribute_v
                for i in range(0, len(vector_test)): # klucz i wartosci w slowniku ktory przechowuje  pod kluczem [ 'i' 'val' 'attribute' ] ich ilosci wystapien *i to nr kolumny*
                        key = str(i)+str(vector_test[i]) + str(attribute_c)
                        if key in smoothed_probabilites:
                            if attribute_c not in probability_every_attribute:
                                probability_every_attribute[attribute_c] = (smoothed_probabilites[key])
                            else:
                                probability_every_attribute[attribute_c] *= (smoothed_probabilites[key])
                        else:
                            if attribute_c not in probability_every_attribute:
                                probability_every_attribute[attribute_c] = (1/attribute_count[attribute_c])
                            else:
                                probability_every_attribute[attribute_c] *= (1/attribute_count[attribute_c])
        print(probability_every_attribute)
        max_value = max(probability_every_attribute.items(), key=lambda x: x[1])
        print(attribute, "-> CLASSIFIED AS: ", max_value[0])
        if max_value[0] == attribute:
            classifications += 1
        else:
            bad_classifications += 1

        print("Precision: ", classifications / (classifications + bad_classifications))
        print("Fulfilness: ", classifications / (classifications ))
    return classifications/len(testing_data_vectors)

def main():
    print("INPUT --> input your own vector")
    print("EXIT --> use file")
    import os

    print("\nFILES:\n--------------------")
    cwd = os.getcwd()
    for filename in os.listdir(cwd):
        if (filename.endswith(".txt")):
            print(filename)
    print("--------------------\n")
    file_training = input("Input training file name: ")
    file_testing = input("Input testing file name: ")
    if (file_training == ""):
        file_training = "iris_training.txt"
    if (file_testing == ""):
        file_testing = "iris_test.txt"

    if (not os.path.isfile(file_testing)):
        print(f"File \'{file_testing}\' doesnt exists! Used file: \'iris_test.txt\'")
        file_testing = "iris_test.txt"
    if (not os.path.isfile(file_training)):
        print(f"File \'{file_training}\' doesnt exists! Used file: \'iris_training.txt\'")
        file_training = "iris_training.txt"
    training_data = read_data(file_training)
    testing_data = read_data(file_testing)
    while True:

        print("\nAccuracy level:", naive_bayes_classification(training_data, testing_data) * 100)
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
            k = input("Type exit to exit: ")
            if k == "exit":
                break
            print("\nCLASSIFICATION:---------------------------------------------------------")
            naive_bayes_classification(training_data, vector)
            print("\nEND---------------------------------------------------------------------")

main()

