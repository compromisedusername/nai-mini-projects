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
    column = data.split()
    vector = column[:-1]
    return [vector, column[-1]]


def make_vectors(data):
    vector = []
    for line in data.splitlines():
        vector.append(make_vector(line))
    return vector


def kmeans_algorithm(vectors, use_kmeans, k_groups):
    if use_kmeans:
        centroids = make_initial_centroids_kmeansplusplus(k_groups, vectors)
    else:
        centroids = make_initial_centroids_random(k_groups, vectors)
    print(centroids, "CENTROIDS")

    iterations = 0

    while True:
        iterations += 1
        square_distances = 0
        clusters = {}
        for vec, att in vectors:
            distances = []
            for cluster_number in range(0, len(centroids)):
                distance = euclidean_square_distance(vec, centroids[cluster_number])
                distances.append([vec, distance, cluster_number, att])

            min_distance = min(distances, key=lambda x: x[1])
            square_distances += min_distance[1]

            cluster_id = min_distance[2]
            vector = min_distance[0]
            distance = min_distance[1]

            if cluster_id not in clusters:
                clusters[cluster_id] = [min_distance]
            else:  # elif vector not in clusters[cluster_id]:
                clusters[cluster_id].append(min_distance)

        check_centroids = centroids.copy()

        for cluster_id, points in clusters.items():
            new_centroid = calculate_new_centroid(points)
            centroids[cluster_id] = new_centroid

        print("Old centroid: ", check_centroids,
              "\nNew centroid: ", centroids,
              "\nIterations: ", iterations,
              "\nSQUARE DISTANCE: ", square_distances)

        if check_centroids == centroids:
            break

    return clusters


def calculate_new_centroid(c):
    cluster = []
    for vec, dist, cluster_id, attribute in c: # i
        cluster.append(vec)
    centroid = [0 for _ in range(0, len(cluster[0]))]
    for j in range(0, len(cluster[0])):
        for i in range(0, len(cluster)):
            centroid[j] += float(cluster[i][j])
        centroid[j] /= len(cluster)
    return centroid


def euclidean_square_distance(vector, point):
    distance = 0
    for x in range(0, len(vector)):
        distance += ((float(vector[x]) - float(point[x])) ** 2)
    return distance


def make_initial_centroids_random(k, vectors):
    centroids = []
    for i in range(0, k):
        centroids.append(vectors[random.randint(0, len(vectors) - 1)][0])
    return centroids


def make_initial_centroids_kmeansplusplus(k, vectors):
    centroids = []
    centroids.append(vectors[0][0])
    vectors_and_distance = {}
    vectors_already_taken = []
    vector_set = set(([tuple(x[0]) for x in vectors]))

    for x in range(0, k - 1):
        for vec in vector_set:
            distance = euclidean_square_distance(vec, centroids[x])
            key = tuple(vec)
            if not key in vectors_and_distance and vec not in vectors_already_taken:
                vectors_and_distance[key] = [distance]
            elif vec not in vectors_already_taken:
                vectors_and_distance[key].append(distance)
        max_k = (max(vectors_and_distance.items(), key=lambda item: sum(item[1])))
        print(sorted(vectors_and_distance.items(), key=lambda item: sum(item[1])))
        print("CHOSEN MAX", max_k)

        centroids.append(
            max_k[0])  # dodajemy do centroidow, wektor ktorego kwadraty sum odleglosci od centroidow sa najwieksze
        vectors_already_taken.append(
            (max_k[0]))  # dodajemy wektor ktory dodalismy wyzej, by uniknac powtarzania sie centroidow

    return centroids


def process_results(result):
    for cluster_id, cluster_data in result.items():
        attributes = {}
        print("Cluster ID:", cluster_id, ", Size:", len(cluster_data))

        for vec in cluster_data:
            if vec[3] not in attributes:
                attributes[vec[3]] = 1
            else:
                attributes[vec[3]] += 1

        entropy = 0
        total_instances = len(cluster_data)
        for attribute_count in attributes.values():
            probability = attribute_count / total_instances
            entropy -= probability * math.log2(probability)

        print("Entropy:", entropy)
        print("Attribute distribution:")
        for attribute, count in attributes.items():
            print(attribute, ":", (count / total_instances) * 100, "%")
        print()


while True:
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
    use_kmeans = input("Use kmeans++ algorithm for calculate initial centroids? Type 'YES' or 'NO': ")
    groups_amount = int(input("Input number of groups: "))
    if(groups_amount <= 0 or groups_amount >= len(vectors)):
        print("Group amount is incorrect!")
        continue
    result = kmeans_algorithm(vectors, use_kmeans.lower() == "yes", groups_amount )
    print("-------------------------------RESULTS------------------------------")
    process_results(result)
    continue_loop = input("Continue? Type 'anything' to continue or 'NO' for stop:")
    if continue_loop.lower() == "no":
        break
