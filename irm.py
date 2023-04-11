#!/usr/bin/env python
# coding: utf-8

# In[31]:


import numpy as np
import matplotlib.pyplot as plt


# In[32]:


def RLE_encode_binary(chaine):
    
    #convert string of bits into liste of bits 
    liste=[]
    liste[:0]=chaine
    
    #Add -1 at first and end 
    liste = np.concatenate([[-1], liste, [-1]])
    
    #determine the index of where there is change of value
    index = np.where(liste[1:] != liste[:-1])[0] + 1
        
    if chaine[0]=='1':
        return np.diff(index)
    
    else:
        return np.concatenate([[0],np.diff(index)])


# In[33]:


import mylib

def RLE_decode_binary(liste):
    
    #function return the symbol and his repetion
    couple=mylib.tupl(liste)
    
    #convert liste of symbol repetion into string sequence
    suit=''.join([couple[i][0]*str(couple[i][1]) for i in range(len(liste))])
    
    suit_liste=[]
    #convert string into liste of one variables
    suit_liste[:0]=suit
    
    return suit_liste


# In[34]:


def LZW_encode(seq):
    #craete ascci dictionary
    code=dict((chr(i),i) for i in range(256))
    
    #first caracteres in string
    previous=seq[0]
    
    #add new caracters into dictionary
    liste=[]
    for i in seq[1:]:
        if previous+i in code:
            previous+=i
        else:
            liste.append(code[previous])
            code[previous+i]=len(code)
            previous=i
    
    #append the last caracters
    liste.append(code[previous])
    
    return liste


# In[35]:


def LZW_decode(seq):
    #craete ascci dictionary
    code=dict((i,chr(i)) for i in range(256))
    
    liste=[]
    #first caracters
    previous=code[seq[0]]
    #append first caracters
    liste.append(previous)
    
    #add new caracters into dictionary and decode in the same time
    for i in seq[1:]:
        if i not in code:
            char=previous+previous[0]
        else:
            char=code[i]
        liste.append(char)
        code[len(code)]=previous+char[0]
        previous=char
    
    return ''.join(liste)


# In[36]:


from heapq import heappush, heappop, heapify
from collections import defaultdict

def Huffman_encode(dictionary) :
    
    #create default dictionary
    tree = [[fq, [sym, ""]] for sym, fq in dictionary.items()]
    
    #give dictionary the shpae of tree
    heapify(tree)
    
    while len(tree) > 1:
        #Pop and return the smallest item from the tree
        right = heappop(tree)  
        left = heappop(tree)

        for pair in right[1:]: 
            # add zero to all the right note
            pair[1] = '0' + pair[1]
        for pair in left[1:]: 
            # add one to all the left note
            pair[1] = '1' + pair[1]  
            
        #add new node in tree
        heappush(tree, [right[0] + left[0]] + right[1:] + left[1:]) 
        
    return right[1:] + left[1:]


# In[37]:


#with open('compressed_file.irm', 'wb') as f:
#    encoded_text.tofile(f)


# In[38]:


#padding = 8 - (len(encoded_text) % 8)


# In[39]:


from bitarray import bitarray

def Huffman_decode(data,huffman_dict):
    
    #decode data using huffman dictinary
    decoded_text = data.decode(huffman_dict) 

    return [int(i) for i in decoded_text]


# In[40]:


#function of bit plane slice
def bit_plane(liste):
    
    #initialize the 8 listes
    l0=[];l1=[];l2=[];l3=[]
    l4=[];l5=[];l6=[];l7=[]
    
    #convert numbers into binary
    bitplan=[bin(i)[2:].zfill(8) for i in liste]
    
    #append the i bite into the i liste
    for i in bitplan:
        l0.append(i[0])
        l1.append(i[1])
        l2.append(i[2])
        l3.append(i[3])
        l4.append(i[4])
        l5.append(i[5])
        l6.append(i[6])
        l7.append(i[7])
        
    return l0+l1+l2+l3+l4+l5+l6+l7


# In[41]:


def bit_plane_decode(suit,scan,nl,nc):
    
    #split array into 8 sub-arrays
    new_arrays =(np.array_split(suit, 8))
    
    #concatenate i varibale from each array to give one (8bits) string 
    liste=[''.join([j[i] for j in new_arrays]) for i in range(len(suit)//8)]
    
    #convert binary into int
    newliste=[int(i,2) for i in liste]
    
    #split array into 3 sub-arrays
    newliste_arrays =(np.array_split(newliste, 3))
    
    #function reshape 3 array into one
    image=mylib.type_scan_reverse(newliste_arrays,scan,nl,nc) 
    
    return image


# In[42]:


import pickle

#write data in image
def write(path,head,data,dictionary):
    file = open(path, "wb")
    pickle.dump(head,file)
    pickle.dump(data,file)
    pickle.dump(dictionary,file)
    file.close()


# In[43]:


import pickle

#read data from image 
def extract(path):
    file = open(path,'rb')
    head = pickle.load(file)
    data = pickle.load(file)
    dictionary = pickle.load(file)
    file.close()
    return head,data,dictionary


# In[44]:


from bitarray import bitarray

def header(extention,row,column,sys_color,data,scan):
    
    #initialize variables
    color=bitarray()
    ext=bitarray()
    scan_type=bitarray()
    
    #encode systeme_color with 32 bits
    color.frombytes(sys_color.encode('utf-8'))
    if len(sys_color)<4:
        #complete 32 bits by 0
        color=color+bitarray('0'*(4-len(sys_color))*8)
    
    #encode format with 32 bits
    ext.frombytes(extention.encode('utf-8'))
    #complete 32 bits by 0
    ext=ext+bitarray('0'*8)
    
    #encode width and height with 16 bits
    width=bitarray(bin(column)[2:].zfill(16))
    height=bitarray(bin(row)[2:].zfill(16))
    
    #encode data_size with 32 bits
    data_size=bitarray(bin(len(data))[2:].zfill(32))
    
    #encode scan_type with 48 bits
    scan_type.frombytes(scan.encode('utf-8'))
    if len(scan)<6:
        #complete 48 bits by 0
        scan_type=scan_type+bitarray('0'*(6-len(scan))*8)
    
    #reserve empty 64 bits if need it after
    non=bitarray('0'*8*8)
    
    return ext+width+height+color+data_size+scan_type+non


# In[45]:


from bitarray.util import ba2int
from bitarray import bitarray

def extract_head(bits):
    
    #get 32 bits for format
    ext=bits[:32].tobytes().decode('utf-8').translate({ord(chr(0)): None})
    
    #get 32 bits for width and height
    width=ba2int(bits[32:48])
    height=ba2int(bits[48:64])
    
    #get 32 bits for systeme_color
    color=bits[64:96].tobytes().decode('utf-8').translate({ord(chr(0)): None})
    
    #get 32 bits for data_size
    data_size=ba2int(bits[96:128])
    
    #get 48 bits for scane_type
    scan=bits[128:176].tobytes().decode('utf-8').translate({ord(chr(0)): None})
    
    #get 64 bits for non_utilisable
    non=ba2int(bits[176:])
    
    return [ext,width,height,color,data_size,scan,non]


# In[ ]:




