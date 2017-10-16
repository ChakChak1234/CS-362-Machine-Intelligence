import math
def compute_v_values(grid_config):
    v_values = []
    for i in range(8):
        for j in range(8):
            value = 0
            if grid_config[i][j] == 2:
                value = -10
            elif grid_config[i][j] == 1:
                value = -5
            elif grid_config[i][j] == 3:
                value = 30
            v_values.append(((7-i,j), value))

    q_values = {}
    for i in v_values:
        q_values.setdefault(i[0],{"N":i[1], "S":i[1], "E":i[1],"W":i[1]})

    return find_v_values(v_values, q_values, grid_config)

def find_v_values(v_val, q_val, grid):
    curretn_sum = calc_convergence(v_val)
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x][y] > 0:
                continue
            index = x * len(grid) + y
            south = 0
            north = 0
            east = 0
            west = 0

            if x > 0:
                north = v_val[index - len(grid)][1]
            if x < len(grid) - 1:
                south = v_val[index + len(grid)][1]
            if y > 0:
                west = v_val[index - 1][1]
            if y < len(grid) - 1:
                east = v_val[index + 1][1]

            q_val[(x, y)]["N"] = 0.7 * north + 0.15 * west + 0.15 * east - 1
            q_val[(x, y)]["S"] = 0.7 * south + 0.15 * west + 0.15 * east - 1
            q_val[(x, y)]["E"] = 0.7 * east + 0.15 * north + 0.15 * south - 1
            q_val[(x, y)]["W"] = 0.7 * west + 0.15 * north + 0.15 * south - 1

            v_val[index] = (v_val[index][0], max(q_val[(x, y)]["N"], q_val[(x, y)]["S"], q_val[(x, y)]["W"], q_val[(x, y)]["E"]))

    if math.fabs(curretn_sum - calc_convergence(v_val)) < 0.0001:
        return v_val
    else:
        return find_v_values(v_val, q_val, grid)

def calc_convergence(v_values):
    sum = 0
    for i in v_values:
        sum += i[1]
    return sum


def get_optimal_policy(grid_config):
    v_val = compute_v_values(grid_config)
    policy = []
    for i in range(8):
        for j in range(8):
            value = -1
            if grid_config[i][j] == 2 or grid_config[i][j] == 1 or grid_config[i][j] == 3:
                value = 4
            else:
                index = i * len(grid_config) + j
                south = -30
                north = -30
                east = -30
                west = -30

                if i > 0:
                    north = v_val[index - len(grid_config)][1]
                if i < len(grid_config) - 1:
                    south = v_val[index + len(grid_config)][1]
                if j > 0:
                    west = v_val[index - 1][1]
                if j < len(grid_config) - 1:
                    east = v_val[index + 1][1]

                if max(north, south, east, west) == north:
                    value = 0
                elif max(north, south, east, west) == south:
                    value = 2
                elif max(north, south, east, west) == east:
                    value = 1
                elif max(north, south, east, west) == west:
                    value = 3
            policy.append(((7-i,j), value))
    return policy