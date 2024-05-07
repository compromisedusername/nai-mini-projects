import os
import random


def read_data(file):
    with open(file, 'r') as p:
        tekst = p.read()
    p.close()
    tekst = tekst.replace(",", ".")
    return tekst


def make_vector(data):
    column = data.split()
    vector = column[:-1]
    return [vector,column[-1]]


def make_vectors(data):
    vector = []
    for line in data.splitlines():
        vector.append(make_vector(line))
    return vector

def kmeans_algorithm(vectors):

    k_groups = int(input("Input number of groups: "))
    if k_groups > len(vectors):
        print("Too many groups for given data set!")
        return

    centroids = make_initial_centroids(k_groups, vectors)
    print(centroids, "CENTROIDS")

    square_distances = 0
    clusters = {}
    changes = 0

    while True:
        for vec, att in vectors:
            distances = []
            for cluster_number in range(0, len(centroids)):
                distance = euclidean_square_distance(vec, centroids[cluster_number])
                distances.append([vec, distance, cluster_number])

            min_distance = min(distances, key=lambda x: x[1])
            square_distances += min_distance[1]

            #print(square_distances, "SQUARE DISTANCE")

            cluster_id = min_distance[2]

            if cluster_id not in clusters:
                clusters[cluster_id] = [min_distance]
            else:
                clusters[cluster_id].append(min_distance)

        check_centroids = centroids.copy()

        for cluster_id, points in clusters.items():
            new_centroid = calculate_new_centroid(points)
            centroids[cluster_id] = new_centroid
        print(check_centroids)
        print(centroids)
        if check_centroids == centroids:
            break
    return clusters
def kmeans_algorithm2(vectors):

    k_groups = int(input("Input number of groups: "))
    if(k_groups > len(vectors)):
        print("To much groups for given data set!")
        return
    centroids = make_initial_centroids(k_groups,vectors)
    print(centroids, "CENTROIDS")

    square_distances = 0
    clusters = {}
    changes = 0

    while True:
        for vec,att in vectors: # dla kazdego wektora ze zbioru
            distances = [] # lista dystansow punkt -> centroid
            for cluster_number in range(0, len(centroids)): # dla kazdego centroidu
                distance = euclidean_square_distance(vec, centroids[cluster_number]) # dystans wektor -> centroid
                distances.append([vec, distance, cluster_number]) # lista dystansow wektor -> wszystkie centroidy [wektor, dystans, numer klastra]
                if cluster_number in clusters: # jesli dany klaster jest w slowniku klastrow
                    new_centroid = calculate_new_centroid(clusters[cluster_number]) # liczmy nowy centroid dla konkretnego klastra
                    if centroids[cluster_number] == new_centroid: # jesli ....
                        1#changes += 1
                    centroids[cluster_number] = new_centroid # aktualizujemy centroid

            min_distance = min(distances, key=lambda x: x[1]) # najmniejszy dystans od centroidu, x[1] to odleglosc z listy distances
            square_distances += min_distance[1] # dodajemy najmniejsza odleglosc do sumy kwadratow odleglosci

            print(square_distances, "SQUARE DISTANCE")

            cluster_id = min_distance[2] # min_distance[2] to numer klastra. clusters to slownik z kluczami [0....k_groups]

            if cluster_id not in clusters: # jesli slownik clusters nie posiada jeszcze zadnych punktrow, inicjujemy go
                clusters[cluster_id] = [min_distance]
            else: # slownik clusters posiada juz minimum jeden punkt
                clusters[cluster_id].append(min_distance) # dodajemy najmniejsze punkty do klastra

            changes += 1
            print(centroids, "CENTROIDY")
            if changes >= 150:
                return clusters


def calculate_new_centroid(c):
    cluster = []
    for i,j,k in c:
        cluster.append(i)
    centroid = [0 for _ in range(0,len(cluster[0]))]
    for j in range(0, len(cluster[0])):
        for i in range(0, len(cluster)):
            centroid[j] += float(cluster[i][j])
        centroid[j] /= len(cluster)
    return centroid


def euclidean_square_distance(vector, point):
    distance = 0
    for x in range(0,len(vector)):
        distance += ((float(vector[x])-float(point[x]))**2)
    return distance

def make_initial_centroids(k,vectors):
    centroids = []
    centroids.append(vectors[0][0])
    vectors_and_distance = {}
    vectors_already_taken = []
    vector_set = set(([tuple(x[0]) for x in vectors]))

    for x in range(0, k-1):
        for vec in vector_set:
            distance = euclidean_square_distance(vec,centroids[x])
            key = tuple(vec)
            if not key in vectors_and_distance and vec not in vectors_already_taken:
                vectors_and_distance[key] = [distance]
            elif vec not in vectors_already_taken:
                vectors_and_distance[key].append(distance)
        max_k = (max(vectors_and_distance.items(), key=lambda item: sum(item[1])))
        print(sorted(vectors_and_distance.items(),key=lambda item: sum(item[1])))
        print("CHOSEN MAX",max_k)

        centroids.append( max_k[0]) # dodajemy do centroidow, wektor ktorego kwadraty sum odleglosci od centroidow sa najwieksze
        vectors_already_taken.append((max_k[0])) # dodajemy wektor ktory dodalismy wyzej, by uniknac powtarzania sie centroidow

    return centroids

print("INPUT --> input your own vector")
print("EXIT --> use file")

cwd = os.getcwd()
print('\nFILES in ', cwd, ' :\n--------------------')

for filename in os.listdir(cwd):
    if (filename.endswith(".txt")):
        print(filename)
print("--------------------\n")
file = input("Input  file name [Or type enter to use standard set]:")
if (file == ""):
    file = "../iris_training.txt"

if (not os.path.isfile(file)):
    print(f"File \'{file}\' doesnt exists! Used file: \'iris_training.txt\'")
    file = "../iris_training.txt"
data = read_data(file)
vectors = make_vectors(data)
result = kmeans_algorithm(vectors)
print("-------------------------------RESULTS------------------------------")
for elem in result.items():
    print(len(elem[1]))


