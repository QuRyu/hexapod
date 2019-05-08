''' 
Lab 2: Dynamics 
CS442 Spring 2018 
Qingbo Liu
'''
import sys 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
from math import radians, sin, cos, sqrt


def jacobian_inverse(thetas, lengths):
    # compute the inverse of the Jacobian matrix given angles 

    theta1 = thetas[0]
    theta2 = thetas[1]

    l1 = lengths[0]
    l2 = lengths[1]

    return np.array([ [cos(theta1 + theta2)/(l1*sin(theta2)), sin(theta1 + theta2)/(l1*sin(theta2))], 
                      [-(l1*cos(theta1) + l2*cos(theta1 + theta2))/(l1*l2*sin(theta2)), -(l1*sin(theta1) + l2*sin(theta1 + theta2))/(l1*l2*sin(theta2))]
                   ])

def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

def main(argv):

    # convert the parameters 
    thetas = list(map(float, argv[1:3]))
    leg_angle = thetas[1]
    thetas = list(map(radians, thetas))
    leg_lengths = list(map(float, argv[3:5]))
    upper_segment = leg_lengths[0]
    lower_segment = leg_lengths[1]
    weight = float(argv[5])
    force_m = np.array([0, weight])

    # print the torques given the force from user
    # torques = jacobian_inverse(thetas, leg_lengths) @ force_m
    # print("torques: ", torques)
        

    # given the leg angle and lengths, find the initial position of legs 
    # the height of legs is assumed to be 15cm
    height = sqrt(upper_segment**2 + lower_segment**2 - 2*upper_segment*lower_segment*cos(radians(leg_angle)))
    lower_theta = abs(asin(upper_segment/height*sin(leg_angle)))
    dist = cos(radians(90) - lower_theta)*lower_segment # distance from segment joint to contact point 
    joint_height = sin(radians(90) - lower_theta)*lower_segment # height of the segment joint 
    
    # data stores all the points to be drawn 
    # in the order (contact point, segment joint, hip joint)
    data = np.array([ [5, 5-dist, 5],
                      [0, joint_height, height]
                   ])


    step_angle = 2 # number of degrees for rotation 
    angle = 90 
    

    
    


    # fig1 = plt.figure()

    # data = np.array([ [2, 4, 6, 8, 10, 12, 14],
                      # [1, 2, 3, 4, 5, 6, 7]
                   # ])
    # l, = plt.plot([], [], 'r-')
    # plt.xlim(0, 10)
    # plt.ylim(0, 10)
    # plt.xlabel('x')
    # line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
                                               # interval=50, blit=True)

    plt.show()

if __name__ == "__main__":
    main(sys.argv) 



