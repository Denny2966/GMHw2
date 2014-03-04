#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import numpy as np

c_dict = {
	'e': 0,
	't': 1,
	'a': 2,
	'i': 3,
	'n': 4,
	'o': 5,
	's': 6,
	'h': 7,
	'r': 8,
	'd': 9
	}

c_rev_str = 'etainoshrd'

def logsumexp(vec) :
	vec = np.array(vec)
	max_vec = max(vec)
	return max_vec + np.log(sum(np.exp(vec - max_vec)))

def cal_node_po(prefix = 'test', w_ind = '1', p_ind_list = ['1'], given_t_label = 'False') :
	folder_path = '../data/'
	file_name = folder_path + prefix + '_img' + w_ind + '.txt'
	arr = np.loadtxt(file_name)

	model_folder_path = '../model/'
	f_po_file_name = model_folder_path + 'feature-params.txt'
	f_arr = np.loadtxt(f_po_file_name)
	
	ret_arr = []
	if given_t_label == 'False' :
		for p_ind in p_ind_list :
	#		t_label = t_word_label[int(p_ind)-1]
	#		_cal_node_po_sub(arr[int(p_ind)-1]), t_label, f_arr[c_dict[t_label]])
			ret_arr.append(_cal_node_po_sub(arr[int(p_ind)-1], f_arr))
	else :
		t_label_file_name = folder_path + prefix + '_words.txt'
		t_label_file_object = open(t_label_file_name, 'rb')
		t_label_list = t_label_file_object.readlines() 
		t_word_label = t_label_list[int(w_ind)-1]
		for p_ind in p_ind_list :
			t_label = t_word_label[int(p_ind)-1]
	#		_cal_node_po_sub(arr[int(p_ind)-1]), t_label, f_arr[c_dict[t_label]])
			ret_arr.append(_cal_node_po_sub(arr[int(p_ind)-1], f_arr, t_label))
	return ret_arr

def _cal_node_po_sub(xijf, wcf, t_label = '') :
	if t_label == '' :
		return map(lambda a:round(a,3), list(np.dot(wcf, xijf)))
	else :
		return round(float(np.dot(wcf[c_dict[t_label]], xijf)), 3)

def cal_trans_po(prefix = 'test', w_ind = '1') :
	model_folder_path = '../model/'
	t_po_file_name = model_folder_path + 'transition-params.txt'
	t_arr = np.loadtxt(t_po_file_name)

	folder_path = '../data/'
	t_label_file_name = folder_path + prefix + '_words.txt'
	t_label_file_object = open(t_label_file_name, 'rb')
	t_label_list = t_label_file_object.readlines() 
	t_word_label = t_label_list[int(w_ind)-1]
	t_word_label = t_word_label[0:len(t_word_label)-1]
	
	ret_arr = []
	for j in range(len(t_word_label) - 1) :
		yi_j = t_word_label[j]
		yi_jplusone = t_word_label[j+1]
		ret_arr.append(t_arr[ c_dict[yi_j] ][ c_dict[yi_jplusone] ])
	return map(lambda a:round(a,3), ret_arr)

if __name__ == '__main__' :
	paras = ['test', '1', ['1']]; #default
	in_paras = sys.argv
	if len(in_paras) <= 3 :
		paras[0:len(in_paras)-1] = in_paras[1:len(in_paras)]
	elif len(in_paras) == 4 :
		paras[0:2] = in_paras[1:3]
		paras[2] = [in_paras[3]]
	else :
		paras[0:2] = in_paras[1:3]
		paras[2] = in_paras[3:len(in_paras)]
	prefix = paras[0]
	w_ind = paras[1]
	p_ind_list = paras[2]

	try :
		node_po = cal_node_po(prefix, w_ind, p_ind_list)
	except :
		info = sys.exc_info()
		print "Unexpected exception, cannot connect to the server:", info[0],",",info[1]
		sys.exit(1)
	else :
		print 'node potential for node ' + str(paras) + ' is:'
		print node_po
