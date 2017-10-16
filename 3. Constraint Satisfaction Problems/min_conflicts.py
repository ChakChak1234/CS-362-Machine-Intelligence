import random, copy
random.seed(1)

class CSP_Solver(object):
    # CSP Solver using min conflicts algorithm
    # See assignment description for details regarding the return value of each method

    def get_num_of_conflicts(self, student, arrangement):
        conflicts = []
        file = open("conflicts.txt", "r")
        for i in file:
            if i.split("-")[0] == student:
                conflicts = i.split("-")[1].strip().split(",")

        error_count = 0
        for row in range(len(arrangement)):
            if student in arrangement[row]:
                coord = (row, arrangement[row].index(student))
                break

        for i in range(len(arrangement)):
            for j in range(len(arrangement)):
                if arrangement[i][j] in conflicts:
                    if i == coord[0]-1 or i == coord[0] or i == coord[0] + 1:
                        if j == coord[1]-1 or j == coord[1] or j == coord[1] + 1:
                            error_count += 1
        return error_count

    def get_total_conflicts(self, arrangement):
        error = 0
        for i in range(len(arrangement)):
            for j in range(len(arrangement)):
                error += self.get_num_of_conflicts(arrangement[i][j], arrangement)
        return error
    
    def find_a_random_student(self, arrangement):
        return arrangement[random.randint(0,3)][random.randint(0,3)]

    def get_best_arrangement(self, student, current_arrangement):
        current_conflict = self.get_total_conflicts(current_arrangement)  # conflict count
        coord = (0,0)
        for row in range(len(current_arrangement)):
            if student in current_arrangement[row]:
                coord = (row, current_arrangement[row].index(student))

        try_conflict = current_conflict
        return_arrangement = current_arrangement
        changed_seat = (5,5)

        for i in range(len(current_arrangement)):
            for j in range(len(current_arrangement)):
                try_arrangement = copy.deepcopy(current_arrangement)
                try_arrangement[i][j], try_arrangement[coord[0]][coord[1]] = try_arrangement[coord[0]][coord[1]], try_arrangement[i][j]
                last_conflict = self.get_total_conflicts(try_arrangement)
                if last_conflict > try_conflict:
                    continue
                else:
                    if last_conflict == try_conflict:
                        if i > changed_seat[0]:
                            continue
                        elif i == changed_seat[0]:
                            if j > changed_seat[0]:
                                continue
                    return_arrangement = copy.deepcopy(try_arrangement)
                    try_conflict = last_conflict
                    changed_seat = (i,j)
        return return_arrangement

    def solve_csp(self, arrangement):
        if self.get_total_conflicts(arrangement) > 0:
            return self.solve_csp(self.get_best_arrangement(self.find_a_random_student(arrangement),arrangement))
        else:
            return arrangement