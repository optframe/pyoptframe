

class ProblemContextVRP(object):
    def __init__(self):
        print('Init VRP')
        # may store current optframe engine for local usage
        self.engine = None
        # number of clients
        self.n = -1
        # number of clients + depot
        #self.N = 0 # n+1
        # delivery packet size for each client
        self.d = []
        # homogeneous capacity among vehicles
        # self.Q = 0
        # x coordinates
        self.vx : List[int] = []
        # y coordinates
        self.vy : List[int] = []
        # distance matrix
        self.dist = []

    def load(self, filename : str):
        # example files
        '''Example: 
            4
            0 10 10
            1 20 40
            2 30 30
            3 40 20
            4 50 50
            10
            4 4 3 3
        '''
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            self.N = self.n+1
            for i in range(self.N):
               id_x_y = lines[i+1].split()
               # ignore id_x_y[0]
               self.vx.append(int(id_x_y[1]))
               self.vy.append(int(id_x_y[2]))
            #
            self.dist = [[0 for _ in range(self.N)] for _ in range(self.N)]
            for i in range(self.N):
               for j in range(self.N):
                  self.dist[i][j] = round(self.euclidean(self.vx[i], self.vy[i], self.vx[j], self.vy[j]))
            #
            self.Q = int(lines[self.N+1])
            self.d = [int(i) for i in lines[self.N+2].split()]


    def euclidean(self, x1: int, y1: int, x2: int, y2: int) -> float:
        import math
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def __str__(self):
        return f"ProblemContextVRP(n={self.n};N={self.N};Q={self.Q};d={self.d};vx={self.vx};vy={self.vy};dist={self.dist})"

####### testing #######
# exec(open('VRP-fcore-part2.py').read())
# p = ProblemContextVRP()
# p.load('instance.txt')
# print(p)
# output: ProblemContextVRP(n=4;N=5;Q=10;d=[4, 4, 3, 3];vx=[10, 20, 30, 40, 50];vy=[10, 40, 30, 20, 50];
#         dist=[[0, 32, 28, 32, 57], [32, 0, 14, 28, 32], [28, 14, 0, 14, 28], [32, 28, 14, 0, 32], [57, 32, 28, 32, 0]])
#######################