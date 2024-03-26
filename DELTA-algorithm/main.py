import math
import os


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


def count_weights(training_data_vectors):
    W = []
    for i in (training_data_vectors[0].keys()):
        for j in i:
            W.append(0)
    for vector in training_data_vectors:
        for v,k in vector.items():
            print(vector)
    


    print(W)
    pass


def delta_algorithm(training_data, testing_data, alfa):
    training_data_vectors = make_vectors(training_data)
    testing_data_vectors = make_vectors(testing_data)
    ## utworzenie wektorow

    ##przeleciec przez zbior treningowy, majac output robimy tak -> jesli atrybut dec jest zgodny z wyliczonym, to nie zmieniamy, a jesli jest zly, to zmieniamy.
    W = count_weights(training_data_vectors)


    return 1


##print("INPUT --> input your own vector")
##print("EXIT --> use file")

##cwd = os.getcwd()
##print('\nFILES in {cwd} :\n--------------------')

##for filename in os.listdir(cwd):
    ##    if (filename.endswith(".txt")):
        ##print(filename)
print("--------------------\n")
##file_training = input("Input training file name [Or type enter to use standard set]:")
##file_testing = input("Input testing file name [Or type enter to use standard set]:")
##if (file_training == ""):
##    file_training = "../iris_training.txt"
##if (file_testing == ""):
##    file_testing = "../iris_test.txt"

##if (not os.path.isfile(file_testing)):
##    print(f"File \'{file_testing}\' doesnt exists! Used file: \'iris_test.txt\'")
file_testing = "../iris_test.txt"
##if (not os.path.isfile(file_training)):
##    print(f"File \'{file_training}\' doesnt exists! Used file: \'iris_training.txt\'")
file_training = "../iris_training.txt"
training_data = read_data(file_training)
testing_data = read_data(file_testing)
with open(file_training, "r") as f:
    line = f.readline()
    dimension = len(line.split()) - 1
while True:

   ## alfa = input("-------DATA FROM FILES-------\nInput value of alfa -> (0,1) [or type input]: ")
    ##if alfa != "input":
        print("\nAccuracy level:", delta_algorithm(training_data, testing_data, 1) * 100)
    ##else:
        while True:

            print("\nVector must be in ", dimension, "dimension!")
            vector = input(f"Input vector in the form:\n-------------------------\n [EXAMPLE] --> : 5.1  3.5 ... "
                           "\n-------------------------\nInput values [{dimension}-DIMENSIONS] [or type exit]: ")
            if vector == "exit":
                break
            while (len(vector.split())) != dimension:
                print("Vector must be in ", dimension, "dimension!")
                vector = input("Input vector: ")

            vector = vector + " vector"
            alfa = input("Input value of K [or type exit]: ")
            if alfa == "exit":
                break
            print("\nCLASSIFICATION:---------------------------------------------------------")
            delta_algorithm(training_data, vector, int(alfa))
            print("\nEND---------------------------------------------------------------------")
