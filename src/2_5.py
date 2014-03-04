#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import numpy as np
import potential as pt

# Only for test word 11

if __name__ == '__main__' :
	prefix = 'test'

	model_folder_path = '../model/'
	t_po_file_name = model_folder_path + 'transition-params.txt'
	t_arr = np.loadtxt(t_po_file_name)
	t_arr = np.array(t_arr)

	folder_path = '../data/'
	t_label_file_name = folder_path + prefix + '_words.txt'
	t_label_file_object = open(t_label_file_name, 'rb')
	t_label_list = t_label_file_object.readlines() 
	t_l_len_list = map(lambda a:len(a)-1, t_label_list)

	t_label_list = map(lambda a:a[0:len(a)-1], t_label_list)
	all_char_list = reduce(lambda a,b: a+b, t_label_list)

	all_char_ind = map(lambda a:pt.c_dict[a], all_char_list)
	all_char_len = len(all_char_ind)

	P_Y_all = []

	num = 200
	word_ind_list = range(1, num + 1)#[1,2,3]

	print 'Problem 2.5:\n'


	for word_ind in word_ind_list :
		t_l_len = t_l_len_list[word_ind-1]
		p_ind_list = range(t_l_len)
		p_ind_list = map(lambda a: str(a+1), p_ind_list)
		f_arr = pt.cal_node_po(prefix, str(word_ind), p_ind_list)
		f_arr = np.array(f_arr)

		w_val = []

		# I observe all words in test_word.txt have as least 3 characters
		for i in range(t_l_len-2) :
			w_val.append(np.transpose(f_arr[i] + np.transpose(t_arr)))

		w_tmp = f_arr[t_l_len-2] + np.transpose(t_arr)
		w_val.append(f_arr[t_l_len-1] + np.transpose(w_tmp))
		w_val = np.array(w_val)

		theta = []
		theta.append(map(pt.logsumexp, w_val[0].transpose())) # vec for Y2
		for i in range(t_l_len-2) :
			if i == 0 :
				continue
			else :
				theta.append(map(pt.logsumexp, w_val[i].transpose()+theta[i-1]))
		
		theta_rev = []
		theta_rev.append(map(pt.logsumexp, w_val[t_l_len-2])) # vec for Y2
		for i in range(t_l_len-2) :
			if i == 0 :
				continue
			else :
				theta_rev.append(map(pt.logsumexp, w_val[t_l_len-2-i]+theta[i-1]))
		
		theta = np.array(theta)
		theta_rev = np.array(theta_rev)

		t_rev_len = len(theta_rev)
		t_len = len(theta)

		beta = []
		beta.append(w_val[0]+theta_rev[t_rev_len-1])
		
		for i in range(len(w_val)-1) :
			if i == 0 :
				continue
			else :
				beta_tmp = w_val[i] + theta_rev[t_rev_len-1-i]
				beta_tmp = beta_tmp.transpose() + theta[i-1]
				beta.append(beta_tmp.transpose())

		beta.append(w_val[len(w_val)-1]+theta[t_len-1])
		
		beta = np.array(beta)

		P_Y = []
		for i in range(t_l_len-2) :
			beta_Y = map(lambda a: pt.logsumexp(a), beta[i])
			beta_Z = pt.logsumexp(beta_Y) # logZ
			P_Y_Z = np.exp(beta[i]-beta_Z)
			P_Y.append(P_Y_Z.sum(1))
		
		beta_Y = map(lambda a: pt.logsumexp(a), beta[t_l_len-2])
		beta_Z = pt.logsumexp(beta_Y) # logZ
		P_Y_Z = np.exp(beta[t_l_len-2]-beta_Z)
		P_Y.append(P_Y_Z.sum(1))
		P_Y.append(P_Y_Z.sum(0))

		P_Y = np.array(P_Y)
		P_Y_all.extend(map(np.argmax, P_Y))

		if word_ind <= 5 :
			tmp = map(np.argmax, P_Y)
			print map(lambda a: pt.c_rev_str[a], list(tmp))

	diff_vec = np.array(P_Y_all) - np.array(all_char_ind)
	print ''
	print 'Character level accuracy is:'
	print float((diff_vec == 0).sum()) / all_char_len
