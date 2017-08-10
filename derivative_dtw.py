#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import numbers
import numpy as np
from collections import defaultdict
def dtw(x, y, dist=None):
    ''' return the distance between 2 time series without approximation
        Parameters
        ----------
        x : array_like
            input array 1
        y : array_like
            input array 2
        dist : function or int
            The method for calculating the distance between x[i] and y[j]. If
            dist is an int of value p > 0, then the p-norm will be used. If
            dist is a function then dist(x[i], y[j]) will be used. If dist is
            None then abs(x[i] - y[j]) will be used.
        Returns
        -------
        distance : float
            the approximate distance between the 2 time series
        path : list
            list of indexes for the inputs x and y
        Examples
        --------
        >>> import numpy as np
        >>> import fastdtw
        >>> x = np.array([1, 2, 3, 4, 5], dtype='float')
        >>> y = np.array([2, 3, 4], dtype='float')
        >>> fastdtw.dtw(x, y)
        (2.0, [(0, 0), (1, 0), (2, 1), (3, 2), (4, 2)])
    '''
    x, y, dist = __prep_inputs(x, y, dist)
    return __dtw(x, y, None, dist)


def __dtw(x, y, window, dist):
    len_x, len_y = len(x), len(y)
    if window is None:
        window = [(i, j) for i in range(1, len_x - 1) for j in range(1, len_y - 1)]
    window = [(i + 1, j + 1) for i, j in window]
    #print("window", len(window))
    D = defaultdict(lambda: (float('inf'),))
    D[1, 1] = (0, 0, 0)
    for i, j in window:
        '''if i == 0 or j == 0:
            continue
        elif i == len_x - 1 or j == len_y - 1:
            continue'''
        #print("First for loop vals", i - 1, j - 1)
        dt = dist(x, y, i - 1, j - 1)
        D[i, j] = min((D[i-1, j][0]+dt, i-1, j), (D[i, j-1][0]+dt, i, j-1),
                      (D[i-1, j-1][0]+dt, i-1, j-1), key=lambda a: a[0])
    path = []
    i, j = len_x - 1, len_y - 1
    while not (i == j == 1):
        '''if i == 0 or j == 0:
            break
        elif i == len_x - 1 or j == len_y - 1:
            continue'''
        #print("indices", (i, j))
        try:
            path.append((i-1, j-1))
            i, j = D[i, j][1], D[i, j][2]
        except IndexError:
            print("Getting IndexError here", D[i, j])
    path.reverse()
    return (D[len_x - 1, len_y - 1][0], path)