def mycallback_ns_rand_bitflip(pKP: ProblemContextKP, sol: SolutionKP) -> MoveBitFlip:
    k = random.randint(0, pKP.n - 1)
    mv = MoveBitFlip()
    mv.k = k
    return mv
