import math

def distance_squared(a, b):
    return sum([(a[i]-b[i])**2 for i in range(len(a))])



def nearest_neighbor(data, current_value):
    return min(map(lambda kv : (euclidean_distance_sq(current_value, kv[0]), kv[1]), data.items()))[1]
