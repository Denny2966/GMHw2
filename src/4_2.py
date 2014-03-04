#!/usr/bin/env python

"""
Python source code - replace this with a description of the code and write the code below this text.
"""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import numpy as np
import potential as pt

from scipy.optimize import minimize

# note: I have change the sign of the object function, thus I am going to minize the new object function.

def tar_fun(x):
	return (1-x[0])**2 + 100*(x[1]-x[0]**2)**2

def tar_fun_der(x):
	der = np.zeros_like(x)
	der[0] = -2 + 2*x[0] - 400 * x[0] * x[1] + 400 * x[0]**3
	der[1] = 200*(x[1]-x[0]**2)
	return der

x0 = np.array([1.3, 0.7])

res = minimize(tar_fun, x0, method='BFGS', jac=tar_fun_der, options={'disp': True})

print 'location at maximum is:'
print res['x']
print 'the maximum value is:'
print tar_fun(res['x'])
