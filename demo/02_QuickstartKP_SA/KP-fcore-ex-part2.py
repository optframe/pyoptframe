

class ExampleKP(object):
    def __init__(self):
        self.engine = Engine()
        self.n : int = 0          # number of items
        self.w : List[float] = [] # item weights
        self.p : List[float] = [] # item profits
        self.Q : float = 0.0      # knapsack capacity

    def load(self, filename : str):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            self.Q = int(lines[1])
            p_lines = lines[2].split()
            self.p = [int(i) for i in p_lines] 
            w_lines = lines[3].split()
            self.w = [int(i) for i in w_lines] 

    def __str__(self):
        return f"ExampleKP(n={self.n};Q={self.Q};w={self.w};p={self.p})"

