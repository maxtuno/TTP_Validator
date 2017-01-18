"""
Author: Oscar Riveros
https://klout.com/maxtuno
"""


class TTPInstance:
    def __init__(self, file_name):
        self._tsp = False
        self._knapsack = False
        self._xy = {}
        self._wp = {}
        with open(file_name, 'r') as TTPInstance:
            for line in TTPInstance.readlines():
                line = line.replace('\n', '').replace('\t', ' ')
                if 'PROBLEM NAME:' in line:
                    self._problem_name = line.replace('PROBLEM NAME:', '').strip(' ')
                if 'KNAPSACK DATA TYPE:' in line:
                    self._knapsack_data_type = line.replace('KNAPSACK DATA TYPE:', '').strip(' ')
                if 'DIMENSION:' in line:
                    self._dimension = eval(line.replace('DIMENSION:', '').strip(' '))
                if 'NUMBER OF ITEMS:' in line:
                    self._number_of_items = eval(line.replace('NUMBER OF ITEMS:', '').strip(' '))
                if 'CAPACITY OF KNAPSACK:' in line:
                    self._capacity_of_knapsack = eval(line.replace('CAPACITY OF KNAPSACK:', '').strip(' '))
                if 'MIN SPEED:' in line:
                    self._min_speed = eval(line.replace('MIN SPEED:', '').strip(' '))
                if 'MAX SPEED:' in line:
                    self._max_speed = eval(line.replace('MAX SPEED:', '').strip(' '))
                if 'RENTING RATIO:' in line:
                    self._renting_ratio = eval(line.replace('RENTING RATIO:', '').strip(' '))
                if 'EDGE_WEIGHT_TYPE:' in line:
                    self._edge_weight_type = line.replace('EDGE_WEIGHT_TYPE:', '').strip(' ')
                if 'NODE_COORD_SECTION (INDEX, X, Y):' in line:
                    self._tsp = True
                    self._knapsack = False
                if 'ITEMS SECTION (INDEX, PROFIT, WEIGHT, ASSIGNED NODE NUMBER):' in line:
                    self._tsp = False
                    self._knapsack = True
                if self._tsp and 'NODE_COORD_SECTION (INDEX, X, Y):' not in line:
                    i, x, y = eval(line.replace(' ', ','))
                    self._xy[i] = complex(x, y)
                if self._knapsack and 'ITEMS SECTION (INDEX, PROFIT, WEIGHT, ASSIGNED NODE NUMBER):' not in line:
                    j, p, w, i = eval(line.replace(' ', ','))
                    self._wp[i] = self._wp.get(i, [])
                    self._wp[i] += [(j, (p, w))]

    @property
    def problem_name(self):
        return self._problem_name

    @property
    def knapsack_data_type(self):
        return self._knapsack_data_type

    @property
    def dimension(self):
        return self._dimension

    @property
    def number_of_items(self):
        return self._number_of_items

    @property
    def capacity_of_knapsack(self):
        return self._capacity_of_knapsack

    @property
    def min_speed(self):
        return self._min_speed

    @property
    def max_speed(self):
        return self._max_speed

    @property
    def renting_ratio(self):
        return self._renting_ratio

    @property
    def edge_weight_type(self):
        return self._edge_weight_type

    @property
    def xy(self):
        return self._xy

    @property
    def wp(self):
        return self._wp

    def ds(self, a, b):
        return abs(self._xy[a] - self._xy[b])

    def eval_solution(self, seq, sub):
        profit, weight = 0, 0
        speed_coefficient = (self._max_speed - self._min_speed) / self._capacity_of_knapsack
        for i in range(len(seq)):
            for j, (p, w) in self._wp.get(seq[i], []):  # get all items for city seq[i] on instance
                if j in sub:  # is item on solution
                    profit += p
                    weight += w
            profit -= self.ds(seq[i], seq[(i + 1) % self._dimension]) * self._renting_ratio / (self._max_speed - speed_coefficient * weight)
        return profit, weight


if __name__ == '__main__':
    import sys

    file_name = sys.argv[1]
    solution_file = sys.argv[2]

    TTPInstance = TTPInstance(file_name)
    print(TTPInstance.problem_name)
    print(TTPInstance.knapsack_data_type)
    print(TTPInstance.dimension)
    print(TTPInstance.number_of_items)
    print(TTPInstance.capacity_of_knapsack)
    print(TTPInstance.min_speed)
    print(TTPInstance.max_speed)
    print(TTPInstance.renting_ratio)
    print(TTPInstance.edge_weight_type)
    print(TTPInstance.xy)
    print(TTPInstance.wp)

    solution = open(solution_file, 'r')
    seq, sub = map(eval, solution.readlines())
    print(TTPInstance.eval_solution(seq, sub))
