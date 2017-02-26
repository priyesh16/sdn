import os
import ctypes
import numpy as np

metric = [[]]
NamingConvention={}
past_fib = {}


def init_Matrix():
    global NamingConvention
    NamingConvention=dict({'san francisco':0,'los angeles':1, 'dallas':2,'chicago':3,'houston':4,'miami':5,'tampa':6,'new york':7})
    w,h=8,8
    m=4  #currently all the link metrics in northstar are seen as 4
    global metric
    metric = [[0 for i in xrange(w)] for i in xrange(h)]
    metric[0][1]=metric[0][2]=metric[0][3]=4
    metric[1][0]=metric[1][2]=metric[1][4]=4
    metric[2][0]=metric[2][2]=metric[2][3]=metric[2][4]=metric[2][5]=4
    metric[3][0]=metric[3][2]=metric[3][5]=metric[3][7]=4
    metric[4][1]=metric[4][2]=metric[4][5]=metric[4][6]=4
    metric[5][2]=metric[5][3]=metric[5][4]=metric[5][6]=metric[5][7]=4
    metric[6][3]=metric[6][4]=metric[6][5]=metric[6][7]=4
    metric[7][3]=metric[7][5]=metric[7][6]=4
    print(metric)

def fibonacci(n):
    if n in past_fib:
        return past_fib[n]

    if n == 0 or n == 1:
        past_fib[n] = 1
        return 1

    total = fibonacci(n-1) + fibonacci(n-2)
    past_fib[n] = total
    return total

def allPairsShortestPath(g):
    #Return distance structure as computed
    dist = {}
    pred = {}
    for u in g:
        print("Trying to print u::")
        print(u)
        dist[u] = {}
        pred[u] = {}
        for v in g:
            dist[u][v] = sys.maxint
            pred[u][v] = None

        dist[u][u] = 0
        pred[u][u] = None

        for v in g[u]:
            dist[u][v] = g[u][v]
            pred[u][v] = u

    for mid in g:
        for u in g:
            for v in g:
                newlen = dist[u][mid] + dist[mid][v]
                if newlen < dist[u][v]:
                    dist[u][v] = newlen
                    pred[u][v] = pred[mid][v]

    return (dist,pred)


def constructShortestPath(s, t, pred):
    path = [t]
    while t != s:
        t = pred[s][t]
        if t is None:
            return None
        path.insert(0, t)
    print(path)
    return path


def ChangeMetric():
    return

def returnLSPS():
    return

if(__name__ == "__main__"):
    init_Matrix()
    dist, pred = allPairsShortestPath(metric)
    constructShortestPath(0, 7, pred)
