#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import itertools
import copy as cp

def candidate1(filename):
    f= open(filename,"r")
    c1 ={}
    l = 0
    for line in f.readlines():
        l+=1
        line = line.strip()
        line =line.replace('"','')
        lst = line.split(',')
        for item in lst:
            count = c1.get(item,0)
            c1[item] = count+1
    return c1,l

def freq(cand,n,support):
    l = []
    for item in cand:
        x = cand[item]/n
        if x >= support:
            l.append(item)
    return l

def findsubsets(s, n): 
    lst = []
    for i in itertools.combinations(s, n):
        lst.append(frozenset(i))
    return lst

def pruning(lk,ele):
    k = len(ele)-1
    subset = findsubsets(ele,k)
    for i in subset:
        if i not in lk:
            return False
    return True

def gen_cand(lk1):
    lk = cp.deepcopy(lk1)
    n = len(lk)
    lk2 = []
    k = len(lk[0])
    for i in range(n-1):
        lkt1 = list(lk[i])
        for j in range(i+1,n):
            lkt2 = list(lk[j])
            flag =True
            for l in range(k-1):
                if lkt1[l]!=lkt2[l]:
                    flag =False
            if flag:
                lst = cp.deepcopy(lkt1)
                lst.append(lkt2[k-1])
                lst = frozenset(lst)
                if pruning(lk,lst):
                    lk2.append(lst)
    return lk2

def get_candidate(filename,lk1):
    lk = cp.deepcopy(lk1)
    f = open(filename,"r")
    c ={}
    l = 0
    k = len(lk[0])
    for line in f.readlines():
        l+=1
        line = line.strip()
        line =line.replace('"','')
        lst = line.split(',')
        subset = findsubsets(lst,k)
        for i in lk:
            #i_t = tuple(i)
            if i in subset:
                count = c.get(i,0)
                c[i]=count+1
    return c

def Apriory(filename,support=0.35):
    freq_set = []
    cand1,n = candidate1(filename)
    l1 = freq(cand1,n,support)
    for i in l1:
        freq_set.append(frozenset({i}))
    c2 = findsubsets(l1,2)
    while len(c2)!=0:
        cand = get_candidate(filename,c2)
        l2 = freq(cand,n,support)
        if len(l2)==0:
            break
        for i in l2:
            freq_set.append(i)
        c2 = gen_cand(l2)
    return freq_set


# In[ ]:




