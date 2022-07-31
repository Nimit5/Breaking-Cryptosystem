#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pexpect
from pyfinite import ffield


# In[ ]:


password = "mshjhijrlufshtgqitfnmlhkkuhimgjh" 
sort_set=sorted(set(password))
st,en=sort_set[0],sort_set[-1]
list_of_words=[chr(i) for i in range(ord(st),ord(en)+1)]    


# In[ ]:


mapping={}
for i in range(len(list_of_words)):
    mapping['{0:04b}'.format(i)]=list_of_words[i]


# In[ ]:


with open("plaintexts.txt","w+") as f:
    for i in range(8):
        for j in range(128):
            binary_value = bin(j)[2:].zfill(8)
            plaintext = 'ff'*i + mapping[binary_value[:4]] + mapping[binary_value[4:]] + 'ff'*(8-i-1)
            f.write(plaintext + " ")
        f.write("\n")
        


# In[ ]:


child = pexpect.spawn('/usr/bin/ssh students@172.27.26.188')   
que=['students@172.27.26.188\'s password:','Enter your group name: ','Enter password: ','\r\n\r\n\r\nYou have solved 5 levels so far.\r\nLevel you want to start at: ','.*','.*','.*','.*','.*']
response=['cs641a',"flash","Gate_Toppers","5","go","wave","dive","go","read"]


# In[ ]:


for i in range(len(response)):
    child.expect(que[i])
    child.sendline(response[i])

child.expect('.*')

with open("plaintexts.txt", 'r') as file1,open("ciphertexts.txt",'w') as file2:
    for line in file1.readlines():
        li = line.split()
        for l in li:
            child.sendline(l)
            s = str(child.before)[48:64]
            file2.write(s)
            file2.write(" ")
            child.expect("Slowly, a new text starts*")
            child.sendline("c")
            child.expect('The text in the screen vanishes!')
        file2.write("\n")

    child.sendline("ffffffffffffffmu")
    s = str(child.before)[48:64]
    file2.write(s)
    file2.write(" ")
    child.close()


# In[ ]:


temp=[]
with open("ciphertexts.txt",'r') as file:
    for line in file.readlines():
        li = line.split()
        temp.extend(li)
    
with open("ciphertexts.txt",'w+') as file:
    for i in range(0,1024,128):
        temp1=temp[i:i+128]
        s=""
        for i in range(128):
            if i==127:
                s=s+temp1[i]
            else:
                s=s+temp1[i]+" "
        file.write(s)
        file.write("\n")


# In[ ]:


expo = [[-1]*128 for i in range(128)]


# In[ ]:


F = ffield.FField(7, gen=0x83, useLUT=-1)


# In[ ]:


def Expo_Calc(element, power):
    if(expo[element][power]!=-1):
        return expo[element][power]
    val=1 if (power==0) else element if(power==1)  else F.Multiply(element,F.Multiply(Expo_Calc(element,power//2),Expo_Calc(element,power//2))) if(power%2 == 1)  else F.Multiply(Expo_Calc(element,power//2),Expo_Calc(element,power//2)) 
    expo[element][power]=val
    return val


# In[ ]:


def Linear_Transformation(matrix, elements):
    val=[0]*8
    for row, ele in zip(matrix, elements):
        temp = [F.Multiply(e,ele) for i, e in enumerate(row)]
        val= [F.Add(ele1, ele2) for i, (ele1, ele2) in enumerate(zip(temp, val))]
    return val


# In[ ]:


def decode_block(cipher_text):
    len_cipher_text=len(cipher_text)
    if(len_cipher_text!=16):
        print("Length of ciphertext is not equal to 16 for cipher : %s" %cipher)
        exit(0)
    plaintext= ""
    for i in range(0,len_cipher_text,2):
        plaintext+=chr(16*(ord(cipher_text[i:i+2][0]) - ord('f')) + ord(cipher_text[i:i+2][1]) - ord('f'))
    return plaintext


# In[ ]:


E_Candidates = [[] for i in range(8)]
A_Candidates=[[[] for i in range(8)] for i in range(8)]

with open("plaintexts.txt", 'r') as plaintext_file, open("ciphertexts.txt", 'r') as ciphertext_file:
    for index, (plaintext, ciphertext) in enumerate(zip(plaintext_file.readlines(), ciphertext_file.readlines())):
        plaintext_string = [decode_block(msg)[index] for msg in plaintext.strip().split(" ")]
        ciphertext_string = [decode_block(msg)[index] for msg in ciphertext.strip().split(" ")]
      
        for i in range(1, 127):
            for j in range(1, 128):
                flag = True
                for inp, out in zip(plaintext_string, ciphertext_string):
                    temp4=Expo_Calc(ord(inp), i)
                    temp5=F.Multiply(temp4, j)
                    temp4=Expo_Calc(temp5, i)
                    temp5=F.Multiply(temp4, j)
                    if(ord(out) != Expo_Calc(temp5, i)):
                        flag = False
                        break
                if(flag):
                    E_Candidates[index].append(i)
                    A_Candidates[index][index].append(j)


# In[ ]:


with open("plaintexts.txt", 'r') as plaintext_file, open("ciphertexts.txt", 'r') as ciphertext_file:
    for ind, (plaintext, ciphertext) in enumerate(zip(plaintext_file.readlines(), ciphertext_file.readlines())):
        if ind > 6 :
            break

        plaintext_string = [decode_block(msg)[ind] for msg in plaintext.strip().split(" ")]
        ciphertext_string = [decode_block(msg)[ind+1] for msg in ciphertext.strip().split(" ")]

        for i in range(1, 128):
            for p1, e1 in zip(E_Candidates[ind+1], A_Candidates[ind+1][ind+1]):
                for p2, e2 in zip(E_Candidates[ind], A_Candidates[ind][ind]):
                    flag = True
                    for inp, outp in zip(plaintext_string, ciphertext_string):
                        temp4=Expo_Calc(ord(inp), p2)
                        temp5=F.Multiply(temp4, i)
                        temp4=Expo_Calc(temp5, p1)
                        temp6=F.Multiply(temp4, e1)
                        temp7=Expo_Calc(ord(inp), p2)
                        temp8=F.Multiply(temp7, e2)
                        temp9=Expo_Calc(temp8, p2)
                        temp10=F.Multiply(temp9, i)
                        temp11=F.Add(temp10 ,temp6)
                        if(ord(outp) != Expo_Calc(temp11, p1)):
                            flag = False
                            break
                    if flag:
                        E_Candidates[ind+1] = [p1]
                        A_Candidates[ind+1][ind+1] = [e1]
                        E_Candidates[ind] = [p2]
                        A_Candidates[ind][ind] = [e2]
                        A_Candidates[ind][ind+1] = [i]


# In[ ]:


def EAEAE (plaintext, lin_mat, exp_mat): 
    plaintext = [ord(c) for c in plaintext]
    output=[[0]*8 for i in range(8)]
    
    for index, ele in enumerate(plaintext):
        output[0][index] = Expo_Calc(ele, exp_mat[index])
        
    output[1] = Linear_Transformation(lin_mat, output[0])
    
    for index, ele in enumerate(output[1]):
        output[2][index] = Expo_Calc(ele, exp_mat[index])
    
    output[3] = Linear_Transformation(lin_mat, output[2])

    for index, ele in enumerate(output[3]):
        output[4][index] = Expo_Calc(ele, exp_mat[index])
        
    return output[4]
    
for indexex in range(0,6):
    
    offset = indexex + 2
    exponentiation_list = [e[0] for e in E_Candidates]
    linear_transformation_list = [[0 for i in range(8)] for j in range(8)]

    for i in range(8):
        for j in range(8):     
            linear_transformation_list[i][j] = A_Candidates[i][j][0] if(len(A_Candidates[i][j]) != 0) else 0
                
    with open("plaintexts.txt", 'r') as plaintext_file, open("ciphertexts.txt", 'r') as ciphertext_file:
        for index, (plaintext, ciphertext) in enumerate(zip(plaintext_file.readlines(), ciphertext_file.readlines())):
            if(index > (7-offset)):
                continue
          
            plaintext_string = [decode_block(msg) for msg in plaintext.strip().split(" ")]
            ciphertext_string = [decode_block(msg) for msg in ciphertext.strip().split(" ")]

            for i in range(1, 128):
                linear_transformation_list[index][index+offset] = i
                flag = True
                for inps, outs in zip(plaintext_string, ciphertext_string):
                    if EAEAE(inps, linear_transformation_list, exponentiation_list)[index+offset] != ord(outs[index+offset]):
                        flag = False
                        break
                if flag==True:
                    A_Candidates[index][index+offset] = [i]

linear_transformation_list = [[0 for i in range(8)] for j in range(8)]

for i in range(0,8):
    for j in range(0,8):
        linear_transformation_list[i][j]=0 if (len(A_Candidates[i][j]) == 0) else A_Candidates[i][j][0]


# In[ ]:


At = linear_transformation_list
E = exponentiation_list
A = [[At[j][i] for j in range(len(At))] for i in range(len(At[0]))]


# In[ ]:


block_size = 8
F = ffield.FField(7, gen=0x83, useLUT=-1)
A = np.array((A))

augmented_A = np.zeros((block_size, block_size*2), dtype = int)
inverse_A = np.zeros((block_size, block_size), dtype = int)
inverse_E = np.zeros((128, 128), dtype = int)
exponents = [[1] for i in range(0,128)]

base=0
while(base<128):
    exponent=1
    while(exponent<127):
        temp = exponents[base][exponent-1]
        result = F.Multiply(temp, base)
        exponents[base]+=[result]
        exponent+=1
    base+=1
    
base=0
while(base<128):
    exponent=1
    while(exponent<127):
        inverse_E[exponent][exponents[base][exponent]] = base
        exponent+=1
    base+=1

inverses = [1]
for i in range(1, 128):
    inverses+=[F.Inverse(i)]
    #assert F.Multiply(i, inverses[i]) == 1

for i in range(0,block_size):
    for j in range(0,block_size):
        augmented_A[i][j] = A[i][j]
    augmented_A[i][i+j+1] = 1

for j in range(0,block_size):
    
    assert np.any(augmented_A[j:,j] != 0) 
    pivot_row = np.where(augmented_A[j:,j] != 0)[0][0] + j
    
    augmented_A[[j, pivot_row]] = augmented_A[[pivot_row, j]]
    mul_fact = inverses[augmented_A[j][j]]
    
    for k in range(block_size*2):
        augmented_A[j][k] = F.Multiply(augmented_A[j][k], mul_fact)
    
    for i in range(0,block_size):
        if i!=j and augmented_A[i][j] != 0:
            mult_fact = augmented_A[i][j]
            for k in range(block_size*2):
                temp = F.Multiply(augmented_A[j][k], mult_fact)
                augmented_A[i][k] = F.Add(temp, augmented_A[i][k])

for i in range(block_size):
    for j in range(block_size):
        inverse_A[i][j] = augmented_A[i][block_size+j]


# In[ ]:


password = "mshjhijrlufshtgqitfnmlhkkuhimgjh" 
decrypted_password = ""
block_size = 16
no_block = int(len(password) / block_size) 

def E_Inverse_Calc(block, E):
    return [inverse_E[E[j]][block[j]] for j in range(8)]

def A_Inverse_Calc(block, A):
    inversed = []
    r_no=0
    while(r_no<8):
        elem_sum = 0
        c_no=0
        while(c_no<8):
            elem = F.Multiply(A[r_no][c_no], block[c_no])
            elem_sum = F.Add(elem, elem_sum)
            c_no+=1
        inversed+=[elem_sum]
        r_no+=1
    return inversed


i=0
while(i<2):
    elements = password[block_size*i:block_size*(i+1)]
    present_Block = []
    j=0
    while(j<8):
        present_Block+=[(ord(elements[2*j]) - ord('f'))*16 + (ord(elements[2*j+1]) - ord('f'))]
        j+=1
    
    temp1 = A_Inverse_Calc(E_Inverse_Calc(present_Block, E), inverse_A)
    EA = E_Inverse_Calc(temp1, E)
    
    temp2 = A_Inverse_Calc(EA, inverse_A)
    EAEAE = E_Inverse_Calc(temp2, E)
    
    print("Inverse EAEAE values for block",str(i)+": ",EAEAE)
    i+=1
    


# In[ ]:


s=set()
for c in "fghijklmnopqrstu":
      s.add(c)
s=sorted(s)
#print(s)
t=set()
for c in "fghijklm":
      t.add(c)
t=sorted(t)
c=0
dict={}
for x in t:
    for y in s:
        dict[c]=x+y
        c=c+1
password=""
s=[119, 114, 112, 113, 122, 113, 113, 121,101, 105, 48, 48, 48, 48, 48, 48]
for x in s:
    password+=dict[x]
    
print("Decrypted password :",password)

finalpassword=""
s=[119, 114, 112, 113, 122, 113, 113, 121,101, 105, 48, 48, 48, 48, 48, 48]
for x in s:
    finalpassword+=chr(x)
print("Final password for level up :",finalpassword[:10])

