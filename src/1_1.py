#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import potential as pt

prefix = 'test'
word_ind_list = [1]

folder_path = '../data/'
t_label_file_name = folder_path + prefix + '_words.txt'
t_label_file_object = open(t_label_file_name, 'rb')
t_label_list = t_label_file_object.readlines() 
t_l_len_list = map(lambda a:len(a)-1, t_label_list)
#print t_l_len_list

for word_ind in word_ind_list :
	p_ind_list = range(t_l_len_list[word_ind-1])
	p_ind_list = map(lambda a: str(a+1), p_ind_list)
	node_po = pt.cal_node_po(prefix, str(word_ind), p_ind_list)
	print node_po

