import sys
from sympy import * 
from mpmath import radians
import numpy as np							# for matrix math

ALPHA = 0
A = 1 
D = 2 
THETA = 3 

e = 0.0000001 

def generate_trans_matrix(dh_params): 
    alpha = dh_params[ALPHA]
    a = dh_params[A]
    d = dh_params[D]
    theta = dh_params[THETA]

    # print("alpha {}, a {}, d {}, theta {}".format(alpha, a, d, theta))
    return Matrix([ [cos(theta), -sin(theta), 0, a],
                    [sin(theta)*cos(alpha), cos(theta)*cos(alpha), -sin(alpha), -d*sin(alpha)],
                    [sin(theta)*sin(alpha), cos(theta)*sin(alpha), cos(alpha), d*cos(alpha)],
                    [0, 0, 0, 1] 
                 ])

def simplify_zero(m):
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if isinstance(m[i,j], Float): 
                v = abs(m[i,j])
                if (v < e):
                    m[i, j] = 0 
    return m 

def jacobian(coordinates, theta1, theta2): 
    x = coordinates[0]
    y = coordinates[1] 
    # z = coordinates[2]

    # print("x {}, y {}, z {}".format(x, y, z))

    return Matrix([ [diff(x, theta1), diff(x, theta2)],
                    [diff(y, theta1), diff(y, theta2)],
                 ])
  
def main( argv ): 

    # three angle variables  
    theta1, theta2, theta3 = symbols("theta1 theta2 theta3") 
    l1, l2 = symbols("l1 l2") 

    DH_parameters = Matrix([ [0, 0, 0, theta1],
                             [0, l1, 0, theta2],
                             [0, l2, 0, 0]
                          ])
                    

    final_matrix = eye(4) 

    for i in range(DH_parameters.shape[0]):
        final_matrix = final_matrix * (generate_trans_matrix(DH_parameters.row(i)))

    final_matrix = simplify(final_matrix)

    print("transformation matrix\n", final_matrix, "\n")

    jacobian_m = jacobian(final_matrix.col(3), theta1, theta2)

    print("jacobian matrix\n", jacobian_m, "\n")

    jacobian_inverse = jacobian_m ** -1 
    jacobian_inverse = simplify(jacobian_inverse)
    
    print("inverse jacobian matrix\n", jacobian_inverse)

    #Compose Matrix of Forces
    Fx, Fy = symbols("Fx Fy")
    forces = np.array([ [Fx], [Fy] ])
    
    #Calculate the torque values
    torques = jacobian_inverse@forces
    print("Torques")
    print(torques)
        
    #Calculate the actual force values at the end effector
    forces2 = jacobian_m@torques
    print("Recalculated Forces")
    print(forces2)

    # jacobian_m = jacobian(final_matrx_simplified, theta_1, theta_2, theta_5)

    # print("Jacobian matrix:\n", jacobian_m)

    # jacobian_m = jacobian_m.subs({theta_1:theta_1_radians, theta_2:theta_2_radians, theta_5:theta_5_radians})

    # print(jacobian_m)

    # jacobian.subs({theta1:theta_1_radians, theta2:theta_2_radians, theta5:theta_5_radians})

    # print("determinant ", jacobian.det())
    # print(N(jacobian))

    # jacobian_inverse = jacobian ** -1
    
    # print(jacobian_inverse)

    # forces = Matrix([ [5.7], [0], [0] ]) 

    # torques = jacobian_inverse * forces 

    # print("jacobian inverse:\n", jacobian_inverse, "\n")
    # print("torques:\n", torques)



if __name__ == "__main__":
    main(sys.argv) 


