
def frandom(pVRP: ProblemContextVRP) -> SolutionVRP:
    #print(f"frandom(n={pVRP.n})")
    rep = SolutionVRP()

    # mistura todos os clientes (cliente 0 é o 'deposito')
    v = [-1 for _ in range(pVRP.n)]  # informação do contexto
    for i in range(len(v)):
        v[i] = i + 1  # excluindo o deposito 0
    # shuffle (TODO: use randgen)
    import random
    random.shuffle(v)
    #print(v)
    #
    # utilizando a construcao randomica
    # Os clientes são adicionados um por um, a menos que a capacidade seja excedida e uma nova rota seja necessária.
    sumDemands = 9999999  # Acumular demandas na rota atual (começar MUITO GRANDE)
    #
    for i in range(len(v)):
        if sumDemands + pVRP.d[v[i]] > pVRP.Q:
            # começando uma nova rota
            rep.sol.append([0])  # "rota vazia" (deposito 0 está sempre presente)
            sumDemands = 0
        # adicionando um cliente na posicao v[i]
        rep.sol[-1].append(v[i])
        # adicionando as demandas
        sumDemands += pVRP.d[v[i]]
    # rota viável (nao é a melhor)
    return rep