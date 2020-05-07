import numpy as np
from graph import *
from graph import matrix_to_string, draw_graph
from collections import OrderedDict

d = 0
p = 0
BIGINT = 922337203


def is_connected(graph, v=1):
    visited = np.zeros(graph.vertex_count, bool)
    stack = np.array([], int)
    stack = np.append(stack, v)
    vertex_count = 0
    visited[v - 1] = True

    while stack.shape[0] != 0:
        vertex = stack[stack.shape[0] - 1]
        stack = np.delete(stack, stack.shape[0] - 1)
        vertex_count += 1
        for neighbour in graph.neighbours_lists[vertex - 1]:
            if not visited[neighbour]:
                visited[neighbour] = True
                stack = np.append(stack, neighbour + 1)

    if vertex_count == graph.vertex_count:
        return True
    else:
        return False


def random_connected_graph():
    connected = False

    while not connected:
        graph = random_graph(7, 10)
        graph = convert(graph, AdjacencyList)
        if is_connected(graph):
            connected = True

    return graph


def relax(u, v, graph):
    global d, p
    if d[v] > (d[u] + graph.weights_matrix[u][v]):
        d[v] = d[u] + graph.weights_matrix[u][v]
        p[v] = u


def dijkstra(graph, v=1):
    global d, p
    n = graph.vertex_count
    d = np.zeros(n, int)
    p = np.zeros(n, int)
    Q = np.zeros(n, bool)
    for vertex in range(n):
        d[vertex] = BIGINT
        p[vertex] = -1
        Q[vertex] = False
    d[v - 1] = 0

    S = np.array([], int)

    while S.shape[0] != n:
        j = 0
        while Q[j]:
            j += 1
        u = j
        while j < n:
            if not Q[j] and (d[j] < d[u]):
                u = j
            j += 1
        Q[u] = True
        S = np.append(S, u)
        for neighbour in graph.neighbours_lists[u]:
            if neighbour not in S:
                relax(u, neighbour, graph)

    ptr = 0
    weights = []
    nodes_and_neighbours = OrderedDict()
    for i in range(n):
        weights.append(d[i])
        nodes_and_neighbours[i + 1] = []
        j = i
        while j > -1:
            S[ptr] = j
            ptr += 1
            j = p[j]
        while ptr > 0:
            ptr -= 1
            nodes_and_neighbours[i + 1].append(S[ptr] + 1)
    return weights, nodes_and_neighbours


def print_dijkstry(weights, nodes_and_neighbours, v=1):
    print("-----DIJKSTRY-----")
    print(f"START: s = {v}")
    for node, neighbours in nodes_and_neighbours.items():
        print(f"d({node}) = {weights[node - 1]} ==> [", end="")
        print(*neighbours, sep=" - ", end="]\n")


def distance_matrix(graph):
    n = graph.vertex_count
    dist_matrix = []
    for i in range(1, n + 1):
        weights,_ = dijkstra(graph, i)
        dist_matrix.append(weights)
    return dist_matrix


def print_distance_matrix(dist_matrix):
    print("Macierz Odleglosci")
    row_description = [str(i) for i in range(1, len(dist_matrix) + 1)]
    col_description = [str(i) for i in range(1, len(dist_matrix) + 1)]
    result = matrix_to_string(dist_matrix,row_description,col_description)
    print(result)

def center_index(weighted_graph):
    dist_matrix = distance_matrix(weighted_graph)

    min_sum = -1
    min_index = -1
    for index, distance_list in enumerate(dist_matrix):
        if (index == 0):
            min_sum = sum(distance_list)
            min_index = index
        elif (min_sum > sum(distance_list)):
            min_sum = sum(distance_list)
            min_index = index

    return min_index

def minmax_center_index(weighted_graph):
    dist_matrix = distance_matrix(weighted_graph)

    min_max = -1
    min_index = -1
    for index, distance_list in enumerate(dist_matrix):
        if (index == 0):
            min_max = max(distance_list)
            min_index = index
        elif (min_max > max(distance_list)):
            min_max = max(distance_list)
            min_index = index

    return min_index


def main():
    print("PROJEKCIK 3 GRAFY")

    print("--------AD1--------")
    graph = random_connected_graph()
    graph = WeightedGraph(graph)

    weights, nodes_and_neighbours = dijkstra(graph)
    print("--------AD2--------")
    print_dijkstry(weights, nodes_and_neighbours)
    draw_graph(graph)

    print("--------AD3--------")
    dist_matrix = distance_matrix(graph)
    print_distance_matrix(dist_matrix)

    print("--------AD4--------")
    center_vertex = center_index(graph) + 1
    minmax_center_vertex = minmax_center_index(graph) + 1
    print("graph center vertex: " + str(center_vertex))
    print("graph minmax center vertex: " + str(minmax_center_vertex))
    draw_graph(graph)



if __name__ == "__main__":
    main()
