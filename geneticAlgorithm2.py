import random

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
generations = 10000  # Número máximo de gerações para o algoritmo genético.
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
    # Um ponto de corte aleatório é escolhido, e partes dos pais são trocadas para formar dois novos cromossomos.
    point = random.randint(1, len(chromosome1) - 1)
    new_chromosome1 = chromosome1[:point] + chromosome2[point:]
    new_chromosome2 = chromosome2[:point] + chromosome1[point:]

    return new_chromosome1, new_chromosome2


# Realiza a operação de mutação em um cromossomo.
# Escolhe aleatoriamente uma aresta no cromossomo e tenta trocar um de seus vértices por um vizinho não emparelhado.
def mutation(chromosome, graph, max_attempts=10):
    print('chromosoe', chromosome)
    # cria uma copia do chromosome
    mutated_chromosome = chromosome.copy()
    # escolhe uma aresta aleatoria dele e busca seus vertices
    mutated_edge_index = random.randint(0, len(mutated_chromosome) - 1)
    vertex1, vertex2 = mutated_chromosome[mutated_edge_index]

    # Cria uma lista de vizinhos não emparelhados do vertex1.
    # Filtra os vizinhos com base no peso da aresta no grafo e se a aresta já está presente no cromossomo
    non_paired_neighbors = [neighbor for neighbor in range(len(
        graph)) if graph[vertex1][neighbor] > 0 and (neighbor, vertex1) not in mutated_chromosome]

    # Verifica se existem vizinhos não emparelhados.
    if non_paired_neighbors:
        # Escolhe aleatoriamente um vizinho não emparelhado da lista de vizinhos não emparelhados.
        vertex_to_unpair = random.choice(non_paired_neighbors)
        # Atualiza a aresta escolhida no cromossomo para conectar vertex1 ao novo vizinho escolhido aleatoriamente.
        mutated_chromosome[mutated_edge_index] = (vertex1, vertex_to_unpair)
    else:
        # Se não houver vizinhos não emparelhados, mantém a aresta existente, preservando o emparelhamento.
        mutated_chromosome[mutated_edge_index] = (vertex1, vertex2)

    # Inicializa o contador de tentativas para garantir que o loop de mutação não seja executado indefinidamente.
    attempts = 0
    # Inicia um loop que tenta realizar a mutação com um número máximo de tentativas (max_attempts).
    while attempts < max_attempts:
        # Escolhe aleatoriamente outro índice de aresta no cromossomo.
        other_edge_index = random.randint(0, len(mutated_chromosome) - 1)
        # Garante que o índice escolhido aleatoriamente não seja o mesmo da aresta original.
        if other_edge_index != mutated_edge_index:
            other_vertex1, other_vertex2 = mutated_chromosome[other_edge_index]

            # Verifica se a troca proposta não gera arestas duplicadas no cromossomo e se a troca é possível no grafo original.
            if (other_vertex2, vertex_to_unpair) not in mutated_chromosome and (vertex1, other_vertex2) not in mutated_chromosome and graph[other_vertex2][vertex_to_unpair] > 0:
                # Realiza a troca nos vértices da aresta original.
                mutated_chromosome[mutated_edge_index] = (
                    vertex1, other_vertex2)
                mutated_chromosome[other_edge_index] = (
                    vertex_to_unpair, other_vertex1)
                return mutated_chromosome

        attempts += 1

    return chromosome


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

    for generation in range(generations):
        print("Geração %s | Aptidão: %s" %
              (generation, 1 / fitness(population[0])))

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
        print('final', 1 / best_fitness, 1 / final_best_fitness)

    print("\nMelhor Emparelhamento Encontrado:")
    print("Emparelhamento: ", final_best_chromosome)
    print("Custo do Emparelhamento (inverso): ", 1 / final_best_fitness)
    print("Custo do Emparelhamento (inverso): ", 1 / best_fitness)