# continuation of ExampleKP class...
    @staticmethod
    def maximize(pKP: 'ExampleKP', sol: SolutionKP) -> float:
        import numpy as np
        wsum = np.dot(sol.bag, pKP.w)
        if wsum > pKP.Q:
            return -1000.0*(wsum - pKP.Q)
        return np.dot(sol.bag, pKP.p)

# optional tests...
assert isinstance(SolutionKP, XSolution)     # composition tests 
assert isinstance(ExampleKP,  XProblem)      # composition tests 
assert isinstance(ExampleKP,  XConstructive) # composition tests    
assert isinstance(ExampleKP,  XMaximize)     # composition tests
