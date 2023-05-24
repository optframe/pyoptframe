
# full evaluation: count distances (cannot update ADS, since its const)
def fevaluateVRP(pVRP: ProblemContextVRP, s: SolutionVRP):
    # Soma das Distancias
    f = 0.0
    # valor alto para capacidade extra
    W_ExtraCap = 99999.0
    f_extra = 0.0
    for r in range(len(s.sol)):
        # somatorio das demandas na rota
        sumDemands = 0
        for i in range(len(s.sol[r]) - 1):
            f += pVRP.dist[s.sol[r][i]][s.sol[r][i+1]]
            sumDemands += pVRP.d[s.sol[r][i]]
        f += pVRP.dist[s.sol[r][-1]][0]  # retornando ao deposito
        sumDemands += pVRP.d[s.sol[r][-1]]
        if sumDemands > pVRP.Q:
            f_extra += (sumDemands - pVRP.Q)
    return f + W_ExtraCap * f_extra
