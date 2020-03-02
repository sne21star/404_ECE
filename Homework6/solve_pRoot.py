# Author: Tanmay Prakash
#         tprakash at purdue dot edu
# Solve x^p = y for x
# for integer values of x, y, p
# Provides greater precision than x = pow(y,1.0/p)
# Example:
# >>> x = solve_pRoot(3,64)
# >>> x
# 4L

import numpy as np
import sys

def solve_pRoot(p,y):
    p = int(p);
    y = int(y);
    # Initial guess for xk
    try:
        xk = int(pow(y,1.0/p));
    except:
        # Necessary for larger value of y
        # Approximate y as 2^a * y0
        y0 = y;
        a = 0;
        while (y0 > sys.float_info.max):
            y0 = y0 >> 1;
            a += 1;
        # log xk = log2 y / p
        # log xk = (a + log2 y0) / p
        xk = int(pow(2.0, ( a + np.log2(float(y0)) )/ p ));

    # Solve for x using Newton's Method
    err_k = int(pow(xk,p))-y;
    while (abs(err_k) > 1):
        gk = p*int(pow(xk,p-1));
        err_k = int(pow(xk,p))-y;
        xk = int(-err_k/gk) + xk;
    return xk