'''
Here's a template to get you started on CS442 lab 1: forward kinematics.
While you'll have to fill in the kinematic math yourselves, I've provided
a function that will draw the arm for you. 

Feel free to write your own solution from scratch! If you choose to 
start from scratch, please make sure the links and Zi axes are easy to 
see, and that the Z axes are labeled in a color-coded legend.

Lab 1: Forward Kinematics
CS442 Spring 2019
Caitrin Eaton
'''

import sys									# for command line arguments
from math import sin, cos, radians  					# for trig functions (cos and sin)
import numpy as np							# for matrix math
import matplotlib.pyplot as plt				# for visualization
from mpl_toolkits.mplot3d import Axes3D 	# for 3D plotting

ALPHA = 0
A = 1
D = 2
THETA = 3


def visualizeArm( t0, z0=[], ax=None ):
    '''Draw a stick figure of the the arm in its current configuration.
    
    t0 is a numpy ndarray of shape (N, 4, 4), where N is the number of 
    degrees of freedom. t0[i][:][:] is the transformation
    matrix describing the position and orientation of frame i in frame 0.
    
    Similarly, z0 is a numpy ndarray of shape (N, 4, 4), where N is the 
    number of degrees of freedom. z0[i][:][:] is the transformation
    matrix describing the position and orientation of the end of the Zi
    axis in frame 0.
    
    All angles must be in radians and all distances must be in cm.'''
    
    # If no existing axis was given as a parameter, then create a new figure
    if ax == None:
    	# Create a new figure and configure the axes for 3D plotting
    	fig = plt.figure()
    	ax = fig.add_subplot(111, aspect='equal', projection='3d')
    	
    	# Label the figure and axes (including units)
    	ax.set_title("WAM forward kinematics")
    	ax.set_xlabel("X0 (cm)")
    	ax.set_ylabel("Y0 (cm)")
    	ax.set_zlabel("Z0 (cm)")
    	
    	# Fix axis limits so that they're the same size regardless of
    	# the configuration of the arm 
    	ax.set_xlim( [-100, 100] )
    	ax.set_ylim( [-100, 100] )
    	ax.set_zlim( [0, 100] )
    
    # Draw the links of the arm
    for i in range( 1, t0.shape[0] ):
        ax.plot( [t0[i-1][0][3], t0[i][0][3]], [t0[i-1][1][3], t0[i][1][3]], [t0[i-1][2][3], t0[i][2][3]], 'o-', color='#B0B0B0', linewidth=5)
    
    if z0 is not None:
    	# Draw the Z axis for each joint, if they were provided
    	for i in range( t0.shape[0] ):
    		ax.plot( [t0[i][0][3], z0[i][0][3]], [t0[i][1][3], z0[i][1][3]], [t0[i][2][3], z0[i][2][3]], 'o-', markersize=6, linewidth=1, label="z{0}".format(i+1))
    
    ax.legend(loc='center left')
    
    return (fig, ax)

def compute_trans_matrix(n): 
    ''' accepts the DH parameters of frame n 
        returns the transposition matrix for frame n in frame n-1 
    '''

    alpha_prev_n = n[ALPHA]
    a_prev_n = n[A]
    d_n = n[D] 
    theta_n = n[THETA]

    m = np.matrix([[cos(theta_n), -sin(theta_n), 0, a_prev_n], 
                   [sin(theta_n)*cos(alpha_prev_n), cos(theta_n)*cos(alpha_prev_n), -sin(alpha_prev_n), -d_n*sin(alpha_prev_n)],
                   [sin(theta_n)*sin(alpha_prev_n), cos(theta_n)*sin(alpha_prev_n), cos(alpha_prev_n), d_n*cos(alpha_prev_n)],
                   [0, 0, 0, 1] ])

    return m

def compose_trans_matrix(i, j, tmatrices): 
    ''' multiply two matrices i and j from the argument tmatrices, 
        with the requirement that i < j
    ''' 

    if i >= j: 
        raise ValueError("frame i (" + i + ") must be smaller than frame j (" + j + ")") 

    return np.dot(tmatrices[i], tmatrices[j])
    
	
def main( argv ):

    # The WAM arm's modified DH parameters (leaving thetas as zeros)
    parameters = np.array([ [0, 0, 0, 0],
                            [radians(-90), 0, 0, 0],
                            [radians(90), 0, 0, 0],
                            [0, 0, 55, 0],
                            [radians(-90), 4.5, 0, 0],
                            [radians(90), -4.5, 30, 0]
                          ])

    DOF = parameters.shape[0]
	
    # Copy joint angles that were provided as command line arguments
    # into the table of DH parameters.
    
    # check command line arguments 
    thetas = argv[1:]

    if len(thetas) != 3: 
        raise ValueError("need three command line arguments") 

    for i in range(3): 
        thetas[i] = radians(float(thetas[i]))

    parameters[0, 3] = thetas[0]
    parameters[1, 3] = thetas[1] 
    parameters[4, 3] = thetas[2]

    print(parameters, "\n")

    # Compute the forward kinematics of the arm, finding the orientation
    # and position of each joint's frame in the base frame (X0, Y0, Z0).

    tmatrices = np.ndarray((DOF, 4, 4), dtype=float)
    for i in range(DOF): 
        tmatrices[i] = compute_trans_matrix(parameters[i]) 

    for i in range(1, DOF):
        tmatrices[i] = compose_trans_matrix(i-1, i, tmatrices)

    		
    # Print the joint coordinates (in the base frame) to the Terminal

    for i in range(tmatrices.shape[0]): 
        m = tmatrices[i]
        x = m[0, 3]
        y = m[1, 3] 
        z = m[2, 3] 
        print("Joint {}, x: {:.2f}, y: {:.2f}, z: {:.2f}".format(i, x, y, z))

    # Draw the arm in its current configuration

    z = np.matrix([ [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 15],
                    [0, 0, 0, 1] ])
    z0 = np.array([np.matmul(x, z) for x in tmatrices])

    (fig, ax) = visualizeArm( tmatrices, z0 )
    plt.show()


	
if __name__=="__main__":
    main( sys.argv )
		
