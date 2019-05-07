''' 
Lab 2: Dynamics 
CS442 Spring 2018 
Qingbo Liu
'''
import sys 
import numpy as np 
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

def main(argv):

    # convert the parameters 
    thetas = list(map(radians, map(float, argv[1:3])))
    leg_lengths = list(map(float, argv[3:5]))
    weight = float(argv[5])
    force_m = np.array([0, weight])

    # print the torques given the force from user
    torques = jacobian_inverse(thetas, leg_lengths) @ force_m
    print("torques: ", torques)
        

if __name__ == "__main__":
    main(sys.argv) 



