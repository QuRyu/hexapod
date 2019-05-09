''' 
Lab 2: Dynamics 
CS442 Spring 2018 
Qingbo Liu
'''
import sys 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
from math import radians, sin, cos, sqrt, asin, pi, degrees

step_angle = 0.1 

def jacobian_inverse(thetas, lengths):
    # compute the inverse of the Jacobian matrix given angles 

    theta1 = thetas[0]
    theta2 = thetas[1]

    l1 = lengths[0]
    l2 = lengths[1]

    return np.array([ [cos(theta1 + theta2)/(l1*sin(theta2)), sin(theta1 + theta2)/(l1*sin(theta2))], 
                      [-(l1*cos(theta1) + l2*cos(theta1 + theta2))/(l1*l2*sin(theta2)), -(l1*sin(theta1) + l2*sin(theta1 + theta2))/(l1*l2*sin(theta2))]
                   ])

def update_line(num, data, line, height, upper_theta, upper_segment):
    angle = step_angle*num

    if angle != 0:
        hip_height = cos(radians(angle)) * height # height of the hip joint 
        hip_dist = sin(radians(angle))*height # distance from the hip joint to contact point 

        beta = radians(angle)+upper_theta # hard to explain here, see graph 
        
        print(degrees(upper_theta), degrees(beta))
        joint_height = cos(beta)*upper_segment # height relative to hip joint 
        joint_dist = sin(beta)*upper_segment # distance relative to hip joint 
        
        data = np.array([ [5, 5+hip_dist-joint_dist, 5+hip_dist],
                          [0, hip_height-joint_height, hip_height]
                       ])

    line.set_data(data)
    return line,

def main(argv):

    # convert the parameters 
    thetas = list(map(radians, map(float, argv[1:3])))
    leg_angle = thetas[1]
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
    height = sqrt(upper_segment**2 + lower_segment**2 - 2*upper_segment*lower_segment*cos(leg_angle))
    lower_theta = abs(asin(upper_segment*sin(leg_angle)/height))
    upper_theta = pi - lower_theta - leg_angle
    dist = cos(radians(90) - lower_theta)*lower_segment # distance from segment joint to contact point 
    joint_height = sin(radians(90) - lower_theta)*lower_segment # height of the segment joint 
    
    # data stores all the points to be drawn 
    # in the order (contact point, segment joint, hip joint)
    data = np.array([ [5, 5-dist, 5],
                      [0, joint_height, height]
                   ])


    fig1 = plt.figure()

    # data = np.array([ [2, 4, 6, 8, 10, 12, 14],
                      # [1, 2, 3, 4, 5, 6, 7]
                   # ])
    l, = plt.plot([], [], 'r-')
    plt.xlim(4.8, 5.2)
    plt.ylim(0, 0.1)
    plt.xlabel('x')
    line_ani = animation.FuncAnimation(fig1, update_line, fargs=(data, l, height, upper_theta, upper_segment),
                                               interval=50, blit=True)

    plt.show()

if __name__ == "__main__":
    main(sys.argv) 



