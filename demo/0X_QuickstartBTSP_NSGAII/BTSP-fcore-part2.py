
import math

class ProblemContextBTSP(object):
    def __init__(self):
        print('Init BTSP')
        # may store current optframe engine for local usage
        self.engine = None
        # number of cities
        self.n = 0
        # x coordinates for obj 0
        self.vx0 = []
        # y coordinates for obj 0
        self.vy0 = []
        # distance matrix for obj 0
        self.dist0 = []
        # x coordinates for obj 1
        self.vx1 = []
        # y coordinates for obj 1
        self.vy1 = []
        # distance matrix for obj 1
        self.dist1 = []
        
   # Example: "3\n1 10 10\n2 20 20\n3 30 30\n"

    def load(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.n = int(lines[0])
            for i in range(self.n):
               id_x_y = lines[i+1].split()
               # ignore id_x_y[0]
               self.vx0.append(int(id_x_y[1]))
               self.vy0.append(int(id_x_y[2]))
            for i in range(self.n):
               id_x_y = lines[self.n+i+1].split()
               # ignore id_x_y[0]
               self.vx1.append(int(id_x_y[1]))
               self.vy1.append(int(id_x_y[2]))
            #
            self.dist0 = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist0[i][j] = round(self.euclidean(self.vx0[i], self.vy0[i], self.vx0[j], self.vy0[j]))
            #
            self.dist1 = [[0 for col in range(self.n)] for row in range(self.n)]
            for i in range(self.n):
               for j in range(self.n):
                  self.dist1[i][j] = round(self.euclidean(self.vx1[i], self.vy1[i], self.vx1[j], self.vy1[j]))

    def euclidean(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def __str__(self):
        return f"ProblemContextBTSP(n={self.n};vx0={self.vx0};vy0={self.vy0};dist0={self.dist0};vx1={self.vx1};vy1={self.vy1};dist1={self.dist1})"
