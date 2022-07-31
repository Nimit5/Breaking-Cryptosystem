#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tqdm import tqdm


# In[2]:


from itertools import combinations_with_replacement


# In[3]:


asci=[i for i in range(ord('f'),ord('v'))]


# In[4]:


print("Asci Values :",asci)


# In[5]:


combinations=combinations_with_replacement(asci,21)


# In[6]:


l="21 7 68 86 4 50 123 5 29 110 35 23 98 36 55 4 22 109 57 52 113 52 50 58 87 13 8 35 117 96 77 24"
l=l.split(' ')


# In[7]:


arr=[int(i) for i in l]


# In[8]:


print("Given Hashed Values :",arr)


# In[9]:


def func(x,i):
    return pow(x,i,127)


# In[10]:


possible_solutions=[x for x in tqdm(combinations) if (sum(x)%127==arr[1]) and (sum(map(func,x,[2]*21))%127==arr[2]) and (sum(map(func,x,[3]*21))%127==arr[3]) and (sum(map(func,x,[4]*21))%127==arr[4]) and (sum(map(func,x,[5]*21))%127==arr[5]) and (sum(map(func,x,[6]*21))%127==arr[6]) and (sum(map(func,x,[7]*21))%127==arr[7]) and (sum(map(func,x,[8]*21))%127==arr[8]) and (sum(map(func,x,[9]*21))%127==arr[9]) and (sum(map(func,x,[10]*21))%127==arr[10]) and (sum(map(func,x,[11]*21))%127==arr[11]) and (sum(map(func,x,[12]*21))%127==arr[12]) and (sum(map(func,x,[13]*21))%127==arr[13]) and (sum(map(func,x,[14]*21))%127==arr[14]) and (sum(map(func,x,[15]*21))%127==arr[15])]


# In[11]:


print("Possible Passwords :")
for i in range(len(possible_solutions)):
    s=""
    for j in possible_solutions[i]:
        s=s+chr(j)
    print(i+1,":",s,sep="")

