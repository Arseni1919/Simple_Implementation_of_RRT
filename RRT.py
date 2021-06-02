import random
import math
import matplotlib.pyplot as plt


class NodeRRT:
    def __init__(self, x, y, parentXY=None, parentNode=None):
        self.x = x
        self.y = y
        self.parentXY = parentXY
        self.parentNode = parentNode


def dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def sample_random_point(mapX_max, mapX_min, mapY_max, mapY_min):
    return random.uniform(mapX_min, mapX_max), random.uniform(mapY_min, mapY_max)


def Nearest(x_rand, y_rand, nodes):
    node_nearest = nodes[0]
    x_nearest, y_nearest = node_nearest.x, node_nearest.y
    dist_nearest = dist((x_rand, y_rand), (x_nearest, y_nearest))
    for node in nodes:
        node_distance = dist((x_rand, y_rand), (node.x, node.y))
        if dist_nearest > node_distance:
            dist_nearest = node_distance
            node_nearest = node
            x_nearest, y_nearest = node_nearest.x, node_nearest.y
    return x_nearest, y_nearest, node_nearest


def Steer(x_nearest, y_nearest, x_rand, y_rand, step):
    distance = dist((x_rand, y_rand), (x_nearest, y_nearest))
    x_nearest += step * (x_rand - x_nearest) / distance
    y_nearest += step * (y_rand - y_nearest) / distance
    return x_nearest, y_nearest


def ObstacleFree(x_nearest, y_nearest, x_new, y_new, x_obst, y_obst):
    for x_o, y_o in zip(x_obst, y_obst):
        if dist((x_o, y_o), (x_new, y_new)) < 0.2:
            return False
    return True


def rewire():
    pass


def plotRRT(nodes, sampled_points, status):
    if status == 'success':

        # for x, y in sampled_points:
        #     plt.scatter(x, y, marker='.', color='blue', alpha=0.5, edgecolors=None)

        for node in nodes:
            if node.parentXY:
                plt.plot([node.x, node.parentXY[0]], [node.y, node.parentXY[1]], linewidth=2, color='green')

        path_node = nodes[-1]
        while path_node.parentNode:
            # node.parentXY
            parent = path_node.parentNode
            plt.plot([path_node.x, parent.x], [path_node.y, parent.y], linewidth=3, color='red')
            path_node = parent
        plt.show()





def rrt_mpf(nodes,
            number_of_samples,
            LAMBDA,
            step,
            x_goal, y_goal,
            x_obst_list, y_obst_list,
            mapX_max, mapX_min,
            mapY_max, mapY_min,
            sample_func,
            nodesAstar):
    sampled_points = []
    for i in range(number_of_samples):
        if random.random() < LAMBDA:
            x_rand, y_rand = sample_func(nodesAstar, mapX_max, mapX_min, mapY_max, mapY_min)
        else:
            x_rand, y_rand = sample_random_point(mapX_max, mapX_min, mapY_max, mapY_min)

        sampled_points.append((x_rand, y_rand))

        x_nearest, y_nearest, node_nearest = Nearest(x_rand, y_rand, nodes)
        x_new, y_new = Steer(x_nearest, y_nearest, x_rand, y_rand, step)

        if ObstacleFree(x_nearest, y_nearest, x_new, y_new, x_obst_list, y_obst_list):
            node_new = NodeRRT(x_new, y_new, parentXY=(x_nearest, y_nearest), parentNode=node_nearest)
            nodes.append(node_new)
            if dist((x_new, y_new), (x_goal, y_goal)) < step:
                nodes.append(NodeRRT(x_goal, y_goal, parentXY=(node_new.x, node_new.y), parentNode=node_new))
                return nodes, sampled_points, 'success'
            rewire()

        # plot(nodes)
    return nodes, sampled_points, 'failure'




# def rrt_simple(nodes, number_of_samples, step, x_goal, y_goal):
#     for i in range(number_of_samples):
#         x_rand, y_rand = sample_random_point()
#         sampled_points.append((x_rand, y_rand))
#         x_nearest, y_nearest = Nearest(x_rand, y_rand, nodes)
#         x_new, y_new = Steer(x_nearest, y_nearest, x_rand, y_rand, step)
#         if ObstacleFree(x_nearest, y_nearest, x_new, y_new):
#             nodes.append(NodeRRT(x_new, y_new, parent=(x_nearest, y_nearest)))
#             if dist((x_new, y_new), (x_goal, y_goal)) < step:
#                 nodes.append(NodeRRT(x_goal, y_goal, parent=(x_new, y_new)))
#                 return nodes
#             rewire()
#
#         # plot(nodes)
#     return None
