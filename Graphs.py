class Grafo:
    def __init__(self, filename):
        self.vertices = 0
        self.matrizAdj = []
        self.file_name = filename

    def preenche_matrizAdj(self):
        # print(self.file_name)

        # Abrindo o arquivo para ler os dados
        with open(self.file_name) as file_object:
            # Le a primeira linha do arquivo que contem a quantidade de vertices
            tipoArquivo = file_object.readline().strip()
            self.vertices = int(file_object.readline())

            if (tipoArquivo == 'Arestas'):
                matrizAux = [[0 for i in range(self.vertices)]
                             for j in range(self.vertices)]
                for row in file_object:
                    valores = [int(x) for x in row.split()]
                    x, y = valores[:2]
                    matrizAux[x-1][y-1] = 1
                    matrizAux[y-1][x-1] = 1
                for i in range(self.vertices):
                    self.matrizAdj.append(matrizAux[i])

            elif (tipoArquivo == 'Matriz'):
                for row in file_object:

                    valores = [int(x) for x in row.split()]
                    self.matrizAdj.append(valores)

            elif (tipoArquivo == 'MatrizTS'):
                matrizAux = [[0 for i in range(self.vertices)]
                             for j in range(self.vertices)]
                j = 1
                for row in file_object:
                    valores = [int(x) for x in row.split()]
                    for i in range(j, self.vertices):
                        matrizAux[i][j-1] = valores[i-j]
                        matrizAux[j-1][i] = valores[i-j]

                    j += 1

                for row in matrizAux:
                    self.matrizAdj.append(row)
        # print(self.matrizAdj)

    def createFile(self):

        with open(self.file_name + "_matrizAdj.txt", 'w') as file_object:

            for row in self.matrizAdj:
                file_object.write(str(row))

    def getMatrizAdj(self):
        return self.matrizAdj

    def mostra_listaAdj2(self):
        return self.listaAdjPesos

    def run(self):
        self.preenche_matrizAdj()
       # self.createFile()
        return self.matrizAdj, self.vertices
