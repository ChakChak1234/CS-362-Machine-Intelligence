import copy

class CSP_Solver(object):
    # CSP Solver using backtracking search
    # See assignment description for details regarding the return value of each method

    conflicts = {}
    file = open("conflicts.txt", "r")
    for i in file:
        conflicts.setdefault(i.split("-")[0],i.split("-")[1].strip().split(","))

    def get_domain(self):
        domain = {}
        students = self.get_students()
        for i in range(4):
            for j in range(4):
                domain.setdefault((i, j), students)
        return domain

    def get_students(self):
        output = []
        file = open("conflicts.txt", "r")
        for i in file:
            output.append(i.split("-")[0])
        output.sort()
        return output

    def get_num_of_conflicts(self, student, arrangement):
            error_count = 0
            for row in range(len(arrangement)):
                if student in arrangement[row]:
                    coord = (row, arrangement[row].index(student))
                    break

            for i in range(len(arrangement)):
                for j in range(len(arrangement)):
                    if arrangement[i][j] == "":
                        return error_count
                    if arrangement[i][j] in self.conflicts[student]:
                        if i == coord[0]-1 or i == coord[0] or i == coord[0] + 1:
                            if j == coord[1]-1 or j == coord[1] or j == coord[1] + 1:
                                error_count += 1
            return error_count

    def total_num_of_conflicts(self, arrangement):
        error = 0
        for i in range(len(arrangement)):
            for j in range(len(arrangement)):
                if arrangement[i][j] == "":
                    return error
                error += self.get_num_of_conflicts(arrangement[i][j], arrangement)
        return error

    def is_done(self, arrangement):  # 0 = not a full list, -1 = conflicted list, 1 = done
        empty = 0
        for i in range(len(arrangement)):
            for j in range(len(arrangement)):
                if arrangement[i][j] == "":
                    return 0

        if self.total_num_of_conflicts(arrangement) > 0:
            return -1
        return 1

    def backtracking_search(self, arrangement):
        print "it will show the result in 30 seconds in my computer. After 8601 iterations, sorry :("
        tm = time.time()

        students = self.get_students()
        initial_node = arrangement
        stack = [initial_node]
        visited = []
        final = []
        while stack:
            node = stack.pop()
            if self.is_done(node) == 1:
                final = node
                break
            added = []
            for i, j in self.arrangement_index():
                if node[i][j] == "":
                    for student in students[::-1]:
                        if student not in added:
                            new_arrangement = copy.deepcopy(node)
                            new_arrangement[i][j] = student
                            if self.total_num_of_conflicts(new_arrangement) == 0:
                                if new_arrangement not in visited:
                                    stack.append(new_arrangement)
                            visited.append(new_arrangement)
                    break
                else:
                    added.append(node[i][j])

        print time.time() - tm
        return final

    def forward_checking(self, assignment,domain_dict):
        output = {}
        dm = domain_dict.items()
        dm.sort()
        index, student = assignment

        for key, value in dm:
            if index == key:
                output.setdefault(index, [student])
            elif (key[0] == index[0]-1 or key[0] == index[0] or key[0] == index[0] + 1) and (key[1] == index[1]-1 or key[1] == index[1] or key[1] == index[1] + 1):
                new_value = []
                for i in value:
                    if i not in self.conflicts[student] and i != student:
                        new_value.append(i)
                output.setdefault(key, new_value)
            else:
                new_value = []
                for i in value:
                    if i != student:
                        new_value.append(i)
                output.setdefault(key, new_value)

        return output

    def domain_to_arrangement(self, domain):
        arrangement = [["","","",""], ["","","",""], ["","","",""], ["","","",""]]
        for coord, students in domain.items():
            if len(students) == 1:
                arrangement[coord[0]][coord[1]] = students[0]
        return arrangement

    def backtracking_with_forward_checking(self):
        stack = [self.get_domain()]
        final = {}
        while stack:
            node = stack.pop()
            arrangement = self.domain_to_arrangement(node)
            if self.is_done(arrangement) == 1:
                final = node
                break
            for i, j in self.arrangement_index():
                if arrangement[i][j] == "":
                    for student in node[(i,j)][::-1]:
                        stack.append(self.forward_checking(((i,j),student),node))
                    break
        return self.domain_to_arrangement(final)

    def backtracking_with_ac3(self):
        stack = [self.get_domain()]
        final = {}

        while stack:
            node = stack.pop()
            arrangement = self.domain_to_arrangement(node)
            if self.is_done(arrangement) == 1:
                final = node
                break
            for i,j in self.arrangement_index():
                if arrangement[i][j] == "":
                    for student in node[(i, j)][::-1]:
                        ac3 = self.forward_checking(((i, j), student), node)
                        removed = self.remove_inconsistent(ac3, student)
                        if removed:
                            stack.append(removed)
                    break
        return self.domain_to_arrangement(final)

    def arrangement_index(self):
        index = []
        for i in range(4):
            for j in range(4):
                index.append((i,j))
        return index

    def remove_inconsistent(self, domain, student):
        leng = len(domain)
        count = 0
        assigned = [student]

        keys = domain.keys()
        keys.sort()

        while count < leng:
            key = keys[count]
            print key
            if len(domain[key]) == 0:
                return []
            new = domain[key][0]
            if len(domain[key]) == 1 and new not in assigned:
                domain = self.forward_checking(((key[0], key[1]), domain[key][0]), domain)
                assigned.append(new)
                count = 0
            count += 1
        return domain