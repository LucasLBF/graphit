from functions import *

executando = True
while (executando == True):
    
    decisao = menuInicial();

    if decisao == 1:
        inserirGrafo()
    elif decisao == 2:
        inserirGrafoEmLote()
    elif decisao == 3:
        imprimirGrafo()
    elif decisao == 4:
        imprimirOrdemAndTamanho()
    elif decisao == 5:
        listaVerticesAdjacentes()
    elif decisao == 6:
        obterGrauVertice()
    elif decisao == 7:
        adjacenciaEntreVertices()
    elif decisao == 8:
        obterCaminhoMaisCurto()
    else:
        executando = False