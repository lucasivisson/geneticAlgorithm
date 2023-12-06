import random
import time

num_vertices = 12  # Número de vértices no grafo.
graph = [
    [0, 255, 244, 286, 163, 119, 498, 264, 76, 585, 224, 297],
    [255, 0, 699, 757, 59, 451, 139, 146, 240, 369, 235, 44],
    [244, 699, 0, 197, 251, 350, 75, 136, 30, 112, 353, 17],
    [286, 757, 197, 0, 381, 76, 54, 69, 184, 34, 130, 569],
    [163, 59, 251, 381, 0, 311, 529, 166, 240, 263, 654, 184],
    [119, 451, 350, 76, 311, 0, 85, 50, 96, 42, 153, 107],
    [498, 139, 75, 54, 529, 85, 0, 145, 400, 404, 10, 182],
    [264, 146, 136, 69, 166, 50, 145, 0, 622, 53, 513, 402],
    [76, 240, 30, 184, 240, 96, 400, 622, 0, 132, 489, 338],
    [585, 369, 112, 34, 263, 42, 404, 53, 132, 0, 648, 575],
    [224, 235, 353, 130, 654, 153, 10, 513, 489, 648, 0, 547],
    [297, 44, 17, 569, 184, 107, 182, 402, 338, 575, 547, 0]
]  # Matriz de adjacência representando o grafo completo ponderado.

population_size = 100  # Tamanho da população na abordagem genética.
generations = 1000  # Número máximo de gerações para o algoritmo genético.
# Um limite adicional para o número máximo de gerações.


# Cria um cromossomo (solução) inicial de emparelhamento aleatório.
def random_chromosome(graph):
    num_vertices = len(graph)
    available_vertices = list(range(num_vertices))
    chromosome = [(0, 0)] * int(num_vertices/2)

    # Itera sobre cada vértice e, para cada vértice, escolhe aleatoriamente um vizinho não emparelhado e forma um par.
    for index in range(int(num_vertices/2)):
        if not available_vertices:
            break

        vertex = None
        vertex_chosen = False
        while vertex_chosen == False and vertex not in available_vertices:
            vertex = random.choice(available_vertices)
            if vertex in available_vertices:
                vertex_chosen = True

        available_vertices.remove(vertex)

        another_vertex = None
        another_vertex_chosen = False
        while another_vertex_chosen == False and another_vertex not in available_vertices:
            another_vertex = random.choice(available_vertices)
            if (another_vertex in available_vertices):
                another_vertex_chosen = True

        available_vertices.remove(another_vertex)

        chromosome[index] = (vertex, another_vertex)

    return chromosome


# Cria uma população inicial de cromossomos chamando a função
def create_population():
    return [random_chromosome(graph) for _ in range(population_size)]

# Calcula a aptidão (custo) de um cromossomo.


def fitness(chromosome):
    cost = 0

    # O custo é a soma dos pesos das arestas no emparelhamento.
    for edge in chromosome:
        vertex1, vertex2 = edge
        # Como o algoritmo busca um emparelhamento mínimo, o custo é negativo.
        cost += graph[vertex1][vertex2]

    return 1 / cost


# Realiza a operação de cruzamento (crossover) entre dois cromossomos.
def crossover(chromosome1, chromosome2):
    point = random.randint(1, len(chromosome1) - 1)
    new_chromosome1 = chromosome1[:point] + chromosome2[point:]
    new_chromosome2 = chromosome2[:point] + chromosome1[point:]

    new_chromosome1, new_chromosome2 = swap_repeated_vertices(
        new_chromosome1, new_chromosome2)

    return new_chromosome1, new_chromosome2


def swap_repeated_vertices(chromosome1, chromosome2):
    repeated_vertices_1 = find_repeated_vertices(chromosome1)
    repeated_vertices_2 = find_repeated_vertices(chromosome2)

    for v1, v2 in zip(repeated_vertices_1, repeated_vertices_2):
        swap_vertices(chromosome1, v1, chromosome2, v2)

    # Após a troca, verifique novamente e resolva possíveis duplicatas
    resolve_duplicate_vertices(chromosome1)
    resolve_duplicate_vertices(chromosome2)

    return chromosome1, chromosome2


def find_repeated_vertices(chromosome):
    visited_vertices = set()
    repeated_vertices = []

    for edge in chromosome:
        for vertex in edge:
            if vertex in visited_vertices:
                repeated_vertices.append(vertex)
            else:
                visited_vertices.add(vertex)

    return repeated_vertices


def swap_vertices(chromosome, vertex1, other_chromosome, vertex2):
    for i in range(len(chromosome)):
        if chromosome[i][0] == vertex1:
            chromosome[i] = (vertex2, chromosome[i][1])
        elif chromosome[i][1] == vertex1:
            chromosome[i] = (chromosome[i][0], vertex2)

    for i in range(len(other_chromosome)):
        if other_chromosome[i][0] == vertex2:
            other_chromosome[i] = (vertex1, other_chromosome[i][1])
        elif other_chromosome[i][1] == vertex2:
            other_chromosome[i] = (other_chromosome[i][0], vertex1)


def resolve_duplicate_vertices(chromosome):
    vertex_count = {}
    for edge in chromosome:
        for vertex in edge:
            if vertex in vertex_count:
                vertex_count[vertex] += 1
            else:
                vertex_count[vertex] = 1

    for i in range(len(chromosome)):
        for j in range(2):
            vertex = chromosome[i][j]
            if vertex_count[vertex] > 1:
                available_vertex = find_available_vertex(chromosome, vertex)
                chromosome[i] = (available_vertex, chromosome[i][1 - j])
                vertex_count[vertex] -= 1
                vertex_count[available_vertex] = vertex_count.get(
                    available_vertex, 0) + 1


def find_available_vertex(chromosome, exclude_vertex):
    for i in range(12):
        if i != exclude_vertex and all(i not in edge for edge in chromosome):
            return i


# Realiza a operação de mutação em um cromossomo.
# Escolhe aleatoriamente uma aresta no cromossomo e tenta trocar um de seus vértices por um vizinho não emparelhado.
def mutation(chromosome, graph, max_attempts=10):
    # Cria uma cópia do cromossomo.
    mutated_chromosome = chromosome.copy()

    # Escolhe aleatoriamente duas posições distintas no cromossomo.
    position1, position2 = random.sample(range(len(mutated_chromosome)), 2)

    # Obtém os vértices correspondentes às posições escolhidas.
    vertex1a, vertex1b = mutated_chromosome[position1]
    vertex2a, vertex2b = mutated_chromosome[position2]

    # Realiza a troca de vértices entre as arestas.
    mutated_chromosome[position1] = (vertex1a, vertex2b)
    mutated_chromosome[position2] = (vertex2a, vertex1b)

    return mutated_chromosome


# Seleciona dois pais da população com base na probabilidade proporcional à sua aptidão.
# Esse método implementa um método chamado "roleta viciada", onde a probabilidade de um cromossomo ser escolhido como pai é proporcional à sua aptidão relativa em relação à aptidão total da população.
# A abordagem de "roleta viciada" dá preferência a cromossomos mais aptos, ajudando a preservar boas características e a acelerar a convergência para soluções melhores.
def select_parents(population):
    # Calcula a soma total da aptidão (fitness) de todos os cromossomos na população.
    total_fitness = sum(fitness(chromosome) for chromosome in population)
    selection_probabilities = [
        fitness(chromosome) / total_fitness for chromosome in population]  # Calcula as probabilidades de seleção para cada cromossomo com base na sua aptidão relativa.
    selected_indices = random.choices(
        range(population_size), weights=selection_probabilities, k=2)  # Seleciona dois índices de cromossomos aleatoriamente com base nas probabilidades calculadas.
    return population[selected_indices[0]], population[selected_indices[1]]


if __name__ == "__main__":
    # Inicializa a população de cromossomos.
    population = create_population()
    # Inicializa a variável que armazenará o melhor cromossomo encontrado.
    final_best_chromosome = None
    # Inicializa a variável que armazenará a aptidão do melhor cromossomo.
    final_best_fitness = None

    start_time = time.time()
    for generation in range(generations):
        print("Geração %s | Aptidão: %s" %
              (generation, 1 / fitness(max(population, key=fitness))))

        new_population = []

        # Loop de Cruzamento e Mutação:
        for _ in range(population_size // 2):
            # Seleciona dois pais da população usando o método de "roleta viciada".
            parent1, parent2 = select_parents(population)
            # Realiza o cruzamento para gerar dois filhos a partir dos pais selecionados.
            child1, child2 = crossover(parent1, parent2)
            # Adiciona os descendentes mutados à nova população.
            new_population.extend(
                [mutation(child1, graph), mutation(child2, graph)])

        # Atualiza a população para a nova população gerada.
        population = new_population
        #  Encontra o cromossomo com a maior aptidão na população atual.
        best_chromosome = max(population, key=fitness)
        # Calcula a aptidão do melhor cromossomo.
        best_fitness = fitness(best_chromosome)
        if final_best_chromosome is None or 1/best_fitness < 1/final_best_fitness:
            final_best_chromosome = best_chromosome
            final_best_fitness = best_fitness
        print('Melhor aptidão encontrada', 1 / final_best_fitness)

    end_time = time.time()
    total_time = end_time - start_time
    print("\nEstatística:")
    if total_time >= 60:
        minutes = total_time // 60
        seconds = total_time % 60
        print(
            f"\nTempo total de execução: {minutes:.0f} minutos e {seconds:.2f} segundos")
    else:
        print(f"\nTempo total de execução: {total_time:.2f} segundos")

    print("Quantidade da população: ", population_size)
    print("Quantidade de gerações: ", generations)
    print("\nMelhor Emparelhamento Encontrado:")
    print("Grafo Emparelhamento referente ao menor custo: ", final_best_chromosome)
    print("Menor Custo do Emparelhamento Encontrado: ", 1 / final_best_fitness)
    print("\nÚltimo Emparelhamento Encontrado:")
    print("Último Grafo Emparelhamento: ", best_chromosome)
    print("Último Custo do Emparelhamento: ", 1 / best_fitness)
