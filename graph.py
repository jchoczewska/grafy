import numpy as np
import random

# number of first vertex used in displaying and reading data
vertex_offset = 1

# this class represents graph as adjacency list
# __init__ takes array of neighbours of 'index' vertex with 
# vertices numbers starting with 0 and array[vertex] being list of 
# neighbours (arrays in 'array' have various length)
class AdjacencyList:

    def __init__(self, array):
        self.vertices_count = len(array)
        self.neighbours_lists = array

    def __str__(self):
        result = "Lista sąsiedztwa\n"
        for vertex in range(self.vertices_count):
            # vertex nr
            result += str(vertex + vertex_offset) + ": "
            # listed neighbours
            result += ", ".join(str(neighbour + vertex_offset) 
                    for neighbour in self.neighbours_lists[vertex])
            result += "\n"

        return result


# first dimension is row, second is column
def matrix_to_string(matrix, rows_desc, columns_desc, offset = 0):

    max_len_row_desc = max(map(len, rows_desc))
    max_len_col_desc = max(max(map(len, columns_desc)), 2)
    def make_row_desc(string):
        return string.ljust(max_len_row_desc)
    def make_col_desc(string):
        return string.ljust(max_len_col_desc)
    def make_node_desc(number):
        return make_col_desc(str(number + offset))
    def make_separator():
        result = make_row_desc("")
        for col_iter in range(columns_nr):
            result += "+"
            result += "-" * max_len_col_desc

        result += "+\n"
        return result

    rows_nr = len(matrix)
    columns_nr = len(matrix[0])

    result = make_row_desc("") + " " + " ".join(make_col_desc(column)
            for column in columns_desc) + "\n"
    result += make_separator()

    for row_iter in range(rows_nr):
        result += make_row_desc(rows_desc[row_iter])
        for col_iter in range(columns_nr):
            result += "|"
            result += make_node_desc(matrix[row_iter][col_iter])

        result += "|\n"
        result += make_separator()


    return result




# matrix member of AdjacencyMatrix is 2 dim matrix with fixed number
# of columns. Each value is either 0 or 1 and tells if two
# vertices are adjacent or not
# matrix[vertex1][vertex2] == matrix[vertex2][vertex1] == 1 =>
# vertex1 and vertex2 are neighbours
class AdjacencyMatrix:

    def __init__(self, array):
        self.vertices_count = len(array)
        self.matrix = array

    def __str__(self):
        global vertex_offset

        columns_and_rows_description = list(map(str, \
                range(vertex_offset, self.vertices_count + vertex_offset)))

        result = "Macierz sąsiedztwa\n"
        result += matrix_to_string(self.matrix, \
                columns_and_rows_description, \
                columns_and_rows_description)

        return result

def adjacency_list_to_adjacency_matrix(adjacency_list):
    vertices_count = adjacency_list.vertices_count
    result_matrix = np.zeros((vertices_count, vertices_count), dtype = int)
    for vertex in range(vertices_count):
        for neighbour in adjacency_list.neighbours_lists[vertex]:
            result_matrix[vertex][neighbour] = 1

    return AdjacencyMatrix(result_matrix)

def adjacency_matrix_to_adjacency_list(adjacency_matrix):
    vertices_count = adjacency_matrix.vertices_count
    matrix = adjacency_matrix.matrix
    result_list = []
    for vertex_index in range(vertices_count):
        vertex_neighbours = []
        for neighbour_nr in range(vertices_count):
            if bool(matrix[vertex_index][neighbour_nr]):
                vertex_neighbours.append(neighbour_nr)
        result_list.append(vertex_neighbours)

    return AdjacencyList(result_list)


# rows of matrix are vertices, and columns are edges
# if matrix[vertex][edge] == 1 => vertex and edge are incident
class IncidenceMatrix:

    def __init__(self, array):
        self.vertices_count = len(array)
        self.matrix = array
        self.edges_count = len(array[0])

    def __str__(self):
        global vertex_offset

        rows_description = []
        for row_nr in range(self.vertices_count):
            rows_description.append(str(row_nr + vertex_offset))

        edges_description = []
        for edge_nr in range(self.edges_count):
            edges_description.append("L" + str(edge_nr + vertex_offset))

        result = "Macierz incydencji\n"
        result += matrix_to_string(self.matrix, \
                rows_description, edges_description)
        return result

def adjacency_matrix_to_incidence_matrix(adjacency_matrix):
    vertices_count = adjacency_matrix.vertices_count
    edges_count = 0
    for vertex_index in range(vertices_count):
        for other_vertex_index in range(vertex_index, vertices_count):
            if bool(adjacency_matrix.matrix[vertex_index][other_vertex_index]):
                edges_count += 1

    result_matrix = np.zeros((vertices_count, edges_count), dtype = int)

    edge_index = 0
    for vertex_index in range(vertices_count):
        for other_vertex_index in range(vertex_index, vertices_count):
            if bool(adjacency_matrix.matrix[vertex_index][other_vertex_index]):
                result_matrix[vertex_index][edge_index] = 1
                result_matrix[other_vertex_index][edge_index] = 1
                edge_index += 1

    return IncidenceMatrix(result_matrix)

def incidence_matrix_to_adjacency_matrix(incidence_matrix):
    vertices_count = incidence_matrix.vertices_count
    edges_count = incidence_matrix.edges_count

    result_matrix = np.zeros((vertices_count, vertices_count), dtype = int)

    for edge_index in range(edges_count):
        vertices = []
        for vertex_index in range(vertices_count):
            if bool(incidence_matrix.matrix[vertex_index][edge_index]):
                vertices.append(vertex_index)

        result_matrix[vertices[0]][vertices[1]] = 1
        result_matrix[vertices[1]][vertices[0]] = 1

    return AdjacencyMatrix(result_matrix)

def adjacency_list_to_incidence_matrix(adjacency_list):
    adjacency_matrix = adjacency_list_to_adjacency_matrix(adjacency_list)
    return adjacency_matrix_to_incidence_matrix(adjacency_matrix)

def incidence_matrix_to_adjacency_list(incidency_matrix):
    adjacency_matrix = incidence_matrix_to_adjacency_matrix(incidency_matrix)
    return adjacency_matrix_to_adjacency_list(adjacency_matrix)

# class type should be an argument
def random_graph_edges_count(vertices_count, edges_count):
    all_pairs = []
    for idx1 in range(vertices_count):
        for idx2 in range(idx1):
            all_pairs.append((idx1, idx2))

    random_pairs = random.sample(all_pairs, edges_count)
    # IncidenceMatrix
    matrix = np.zeros((vertices_count, edges_count), dtype = int)
    for edge_nr in range(edges_count):
        matrix[random_pairs[edge_nr][0]][edge_nr] = 1
        matrix[random_pairs[edge_nr][1]][edge_nr] = 1

    return IncidenceMatrix(matrix)

# class type should be an argument
def random_graph_edge_probability(vertices_count, edge_probability):
    all_pairs = []
    for idx1 in range(vertices_count):
        for idx2 in range(idx1):
            all_pairs.append((idx1, idx2))

    matrix = np.zeros((vertices_count, vertices_count), dtype = int)
    for pair in all_pairs:
        if random.random() < edge_probability:
            matrix[pair[0]][pair[1]] = 1
            matrix[pair[1]][pair[0]] = 1

    return AdjacencyMatrix(matrix)


