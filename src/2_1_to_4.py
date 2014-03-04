#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import numpy as np
import potential as pt

# Only for test word 11

if __name__ == '__main__' :
	f_arr = [[-20.614, 19.861, -1.097, 9.697, -2.313, 1.233, -4.426, -0.069, -1.758, -0.514], 
			[-5.174, -3.729, 11.162, -5.95, 2.665, -3.841, -17.474, 5.556, 24.229, -7.444], 
			[6.861, -9.531, 7.494, -6.572, -4.751, 1.221, -8.027, 0.881, 9.138, 3.286], 
			[24.668, -9.555, -3.154, -3.499, -12.169, -2.781, -2.541, -0.551, 1.395, 8.187]]

	f_arr = np.array(f_arr)
	prefix = 'test'
	word_ind_list = [1]

	model_folder_path = '../model/'
	t_po_file_name = model_folder_path + 'transition-params.txt'
	t_arr = np.loadtxt(t_po_file_name)
	t_arr = np.array(t_arr)

#	clique potential
#	wj = phi_F_yj * phi_T_yjy(j+1) where j=0,1
#	wj = phi_F_yj * phi_F_y(j+1) * phi_T_yjy(j+1) where j=2
	
	w0 = f_arr[0] + np.transpose(t_arr)
	w1 = f_arr[1] + np.transpose(t_arr)

	w2 = f_arr[2] + np.transpose(t_arr)
	w2 = f_arr[3] + np.transpose(w2)

	w0 = np.array(w0)
	w1 = np.array(w1)
	w2 = np.array(w2)

	w_val = np.array([w0.transpose(), w1.transpose(), w2])	
	#w_val = np.array([w0, w1, w2])	
	print 'Problem 2.1\n'

# Report for 'e,t,r'
	to_rp = 'etr'
	to_rp_ind = map(lambda a: pt.c_dict[a], to_rp)
#	print to_rp_ind

	for val in w_val :
		#print val
		val = val[to_rp_ind, :]
		val = val[:, to_rp_ind]
		print val
	print '\nProblem 2.2\n'	

# For 2.2
# Calculate	theta
	theta_1_2 = map(pt.logsumexp, w_val[0].transpose()) # vec for Y2
	theta_2_3 = map(pt.logsumexp, w_val[1].transpose()+theta_1_2) # vec for Y3
	theta_3_2 = map(pt.logsumexp, w_val[2]) # vec for Y3
	theta_2_1 = map(pt.logsumexp, w_val[1] + theta_3_2) # vec for Y2

	theta = np.around([theta_1_2, theta_2_3, theta_3_2, theta_2_1],3)
	print theta
	print '\nProblem 2.3:\n'

# For 2.3
# Calculate	beta
	beta_1 = w_val[0] + theta_2_1

	beta_2 = w_val[1] + theta_3_2
	beta_2 = beta_2.transpose() + theta_1_2
	beta_2 = beta_2.transpose()

	beta_3 = w_val[2].transpose() + theta_2_3
	beta_3 = beta_3.transpose()

	beta = np.around([beta_1, beta_2, beta_3], 3)
#	print beta
# Report for 'et'
	to_rp = 'et'
	to_rp_ind = map(lambda a: pt.c_dict[a], to_rp)
#	print to_rp_ind

	for val in beta :
		#print val
		val = val[to_rp_ind, :]
		val = val[:, to_rp_ind]
		print val

# For 2.4
# Calculate	marginal pd over each position in the word
	print '\nProblem 2.4:\n'
	print 'Y1'
	beta_Y = map(lambda a: pt.logsumexp(a), beta_1)
	beta_Z = pt.logsumexp(beta_Y) # logZ
	P_Y_Z = np.exp(beta_1-beta_Z)
	P_Y1 = P_Y_Z.sum(1)
	print ['%.2e' %val for val in P_Y1]

	print 'Y2'
	beta_Y = map(lambda a: pt.logsumexp(a), beta_2)
	beta_Z = pt.logsumexp(beta_Y) # logZ
	P_Y_Z = np.exp(beta_2-beta_Z)
	P_Y2 = P_Y_Z.sum(1)
	print ['%.2e' %val for val in P_Y2]

	print 'Y3'
	beta_Y = map(lambda a: pt.logsumexp(a), beta_3)
	beta_Z = pt.logsumexp(beta_Y) # logZ
	P_Y_Z = np.exp(beta_3-beta_Z)
	P_Y3 = P_Y_Z.sum(1)
	print ['%.2e' %val for val in P_Y3]
	P_Y4 = P_Y_Z.sum(0)

	print 'Y4'
	print ['%.2e' %val for val in P_Y4]

	print 'Y1,Y2'
	beta_Y = map(lambda a: pt.logsumexp(a), beta_2)
	beta_Z = pt.logsumexp(beta_Y) # logZ
	P_Y_Z = np.exp(beta_2-beta_Z)

	to_rp = 'etr'
	to_rp_ind = map(lambda a: pt.c_dict[a], to_rp)
#	print to_rp_ind
	
	val = P_Y_Z
	val = val[to_rp_ind, :]
	val = val[:, to_rp_ind]
	print val
# Calculate	pairwise marginals

