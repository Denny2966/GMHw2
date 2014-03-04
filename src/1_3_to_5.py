#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import numpy as np
import potential as pt

if __name__ == '__main__' :

	prefix = 'test'
	word_ind_list = [1,2,3]

	model_folder_path = '../model/'
	t_po_file_name = model_folder_path + 'transition-params.txt'
	t_arr = np.loadtxt(t_po_file_name)

	folder_path = '../data/'
	t_label_file_name = folder_path + prefix + '_words.txt'
	t_label_file_object = open(t_label_file_name, 'rb')
	t_label_list = t_label_file_object.readlines() 
	t_l_len_list = map(lambda a:len(a)-1, t_label_list)
	#print t_l_len_list

	for word_ind in word_ind_list :
# For 1.3		
		t_l_len = t_l_len_list[word_ind-1]
		p_ind_list = range(t_l_len)
		p_ind_list = map(lambda a: str(a+1), p_ind_list)
		node_po = pt.cal_node_po(prefix, str(word_ind), p_ind_list)
		
		case_num = pow(10, t_l_len)
		partition_val = []
		margi_partition_val = []
		for i in range(t_l_len) :
			margi_partition_val.append([[],[],[],[],[],[],[],[],[],[]])

		for i in range(case_num) :
			label_arr = []
			tmp_val = i
			for j in range(t_l_len) :
				label_arr.append(tmp_val % 10)
				tmp_val /= 10

			t_po_sum = 0
			p_po_sum = 0
			for j in range(t_l_len - 1) :

				t_po_sum += t_arr[ label_arr[j] ][ label_arr[j+1] ]
				p_po_sum += node_po[ j ][ label_arr[j] ]
			
			p_po_sum += node_po[t_l_len - 1][ label_arr[t_l_len-1] ]

			partition_val.append(t_po_sum + p_po_sum)

			tmp_val = i
			for j in range(t_l_len) :
				margi_partition_val[j][label_arr[j]].append(t_po_sum+p_po_sum)
				tmp_val /= 10

		partition_val = np.array(partition_val)
		
		log_partition = pt.logsumexp(partition_val)
		print log_partition

# For 1.4
		max_val, max_ind = partition_val.max(), partition_val.argmax()
		pro_max = np.exp(max_val - log_partition)
		
		tmp_val = max_ind
		r_label_arr = []
		for j in range(t_l_len) :
			r_label_arr.append(tmp_val % 10)
			tmp_val /= 10
		
		print pro_max
		print map(lambda a: pt.c_rev_str[a], r_label_arr)
			
# For 1.5
		margi_par_sum = []	
		for j in range(t_l_len) :
			margi_par_sum.append([])
			margi_par_sum[j] = map(lambda a: round(pt.logsumexp(a),3),margi_partition_val[j])
			margi_par_sum[j] = map(lambda a: np.exp(a-log_partition), margi_par_sum[j])
			print ['%.2e' %val for val in  margi_par_sum[j]]

#		print margi_par_sum
