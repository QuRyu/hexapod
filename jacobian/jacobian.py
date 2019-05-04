import sys
from sympy import * 
from mpmath import radians

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

    print("alpha {}, a {}, d {}, theta {}".format(alpha, a, d, theta))
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

# def jacobian(coordinates, theta1, theta2, theta3): 
    # x = coordinates[0]
    # y = coordinates[1] 
    # z = coordinates[2]

    # return Matrix([ [diff(x, theta1), diff(x, theta2), diff(x, theta3)],
                    # [diff(y, theta1), diff(y, theta2), diff(y, theta3)],
                    # [diff(z, theta1), diff(z, theta2), diff(y, theta3)]
                 # ])
  
def main( _argv ): 

    # three angle variables  
    theta1, theta2, theta5 = symbols("theta1 theta2 theta5") 

    # DH_parameters = Matrix([ [0, 0, 0, theta_1],
                             # [radians(-90), 0, 0, theta_2],
                             # [radians(90), 0, 0, 0],
                             # [0, 0, 55, 0],
                             # [radians(-90), 4.5, 0, theta_5],
                             # [radians(90), -4.5, 30, 0]
                          # ])
                    

    # final_matrx = eye(4) 

    # for i in range(DH_parameters.shape[0]):
        # final_matrx = final_matrx * simplify_zero(generate_trans_matrix(DH_parameters.row(i)))


    # print("trans matrix of frame 6 with respect to base frame:\n", final_matrx, "\n")

    # final_matrx_simplified = simplify(final_matrx)

    # print("matrix_simplified:\n", final_matrx_simplified, "\n\n")

    # theta1 = radians(10) 
    # theta2 = radians(20) 
    # theta5 = radians(45) 
    # final_matrx_simplified = final_matrx_simplified.subs({theta_1:theta_1_radians, theta_2:theta_2_radians, theta_5:theta_5_radians})

    # print("final matrix:\n", N(final_matrx_simplified))

    # jacobian_m = jacobian(final_matrx_simplified, theta_1, theta_2, theta_5)

    # print("Jacobian matrix:\n", jacobian_m)

    # jacobian_m = jacobian_m.subs({theta_1:theta_1_radians, theta_2:theta_2_radians, theta_5:theta_5_radians})

    # print(jacobian_m)

    jacobian = Matrix([ [-55*sin(theta2)*sin(theta1) - 30*sin(theta2+theta5)*sin(theta1) - 4.5*sin(theta1)*cos(theta2) + 4.5*sin(theta1)*cos(theta2+theta5), 
                                55*cos(theta1)*cos(theta2) + 30*cos(theta2+theta5)*cos(theta1) - 4.5*cos(theta1)*sin(theta2) + 4.5*cos(theta1)*sin(theta2+theta5), 
                                30*cos(theta2+theta5) + 4.5*cos(theta1)*sin(theta2+theta5)], # first row 
                        [55*cos(theta1)*sin(theta2) + 30*cos(theta1)*sin(theta2+theta5) + 4.5*cos(theta1)*cos(theta2) - 4.5*cos(theta1)*cos(theta2+theta5),
                                55*sin(theta1)*cos(theta2) + 30*sin(theta1)*cos(theta2+theta5) - 4.5*sin(theta1)*sin(theta2) + 4.5*sin(theta1)*sin(theta2+theta5),
                                30*sin(theta1)*cos(theta2+theta5) + 4.5*sin(theta1)*sin(theta2+theta5)],
                        [0, -4.5*cos(theta2) + 4.5*cos(theta2+theta5) - 55*sin(theta2) - 30*sin(theta2+theta5), 
                                4.5*cos(theta2+theta5) - 30*sin(theta2+theta5)]
                    ])


    # jacobian.subs({theta1:theta_1_radians, theta2:theta_2_radians, theta5:theta_5_radians})

    # print("determinant ", jacobian.det())
    # print(N(jacobian))

    jacobian_inverse = jacobian ** -1
    
    print(jacobian_inverse)

    # forces = Matrix([ [5.7], [0], [0] ]) 

    # torques = jacobian_inverse * forces 

    # print("jacobian inverse:\n", jacobian_inverse, "\n")
    # print("torques:\n", torques)



if __name__ == "__main__":
    main(sys.argv) 


