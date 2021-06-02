from RRT import NodeRRT, rrt_mpf, plotRRT
from RRT import sample_random_point


def sample_MPF_point(nodesAstar, mapX_max, mapX_min, mapY_max, mapY_min):
    return sample_random_point(mapX_max, mapX_min, mapY_max, mapY_min)


def main():
    NUMBER_OF_SAMPLES = 7000
    STEP = 0.1
    LAMBDA = 0.9
    nodesRRT = [NodeRRT(x=0.01, y=0.02)]
    x_goal, y_goal = 9, 9
    list_x_obstacle = []
    list_y_obstacle = []

    nodes, sampled_points, status = rrt_mpf(nodes=nodesRRT,
                                            number_of_samples=NUMBER_OF_SAMPLES,
                                            LAMBDA=LAMBDA,
                                            step=STEP,
                                            x_goal=x_goal,
                                            y_goal=y_goal,
                                            x_obst_list=list_x_obstacle,
                                            y_obst_list=list_y_obstacle,
                                            mapX_max=10, mapX_min=0,
                                            mapY_max=10, mapY_min=0,
                                            sample_func=sample_MPF_point,
                                            nodesAstar=[])
    # rrt_mpf()

    print(f'Finish with << {status} >> \nThere were {len(sampled_points)} sampled points')
    plotRRT(nodesRRT, sampled_points, status)


if __name__ == '__main__':
    main()
