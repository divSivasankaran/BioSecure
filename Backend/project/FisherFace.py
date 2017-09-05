# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 15:54:52 2017

@author: e0013178
"""

import os
import numpy as np
from PIL import Image
from numpy import linalg
#import matlab.engine
def ComputeNorm(x):
    # function r=ComputeNorm(x)
    # computes vector norms of x
    # x: d x m matrix, each column a vector
    # r: 1 x m matrix, each the corresponding norm (L2)

    [row, col] = x.shape
    r = np.zeros((1,col))

    for i in range(col):
        r[0,i] = linalg.norm(x[:,i])
    return r

def myLDA(A,Labels):
    # function [W,C,L]=myLDA(A,Labels)
    # computes LDA of matrix A
    # A: D by N data matrix. Each column is a vector
    # Labels: vector of class labels corresponding to each column in A
    # W: D by K LDA projection matrix
    # C: centers of each class (ie, the templates)
    # L: class labels


    classLabels = np.unique(Labels)
    classNum = len(classLabels)
    dim,datanum = A.shape
    totalMean = np.mean(A,1)
    partition = [np.where(Labels==label)[0] for label in classLabels]
    classMean = [(np.mean(A[:,idx],1),len(idx)) for idx in partition]

    #compute the within-class scatter matrix
    W = np.zeros((dim,dim))
    for idx in partition:
        W += np.cov(A[:,idx],rowvar=1)*len(idx)

    #compute the between-class scatter matrix
    B = np.zeros((dim,dim))
    for mu,class_size in classMean:
        offset = mu - totalMean
        B += np.outer(offset,offset)*class_size

    #solve the generalized eigenvalue problem for discriminant directions
    import scipy.linalg as linalg
    import operator
    ew, ev = linalg.eig(B,W+B)
    sorted_pairs = sorted(enumerate(ew), key=operator.itemgetter(1), reverse=True)
    selected_ind = [ind for ind,val in sorted_pairs[:classNum-1]]
    LDAW = ev[:,selected_ind]
    Centers = [np.dot(mu,LDAW) for mu,class_size in classMean]
    Centers = np.transpose(np.array(Centers))
    return LDAW,Centers, classLabels

def myPCA(A):
    # function [W,LL,m]=mypca(A)
    # computes PCA of matrix A
    # A: D by N data matrix. Each column is a random vector
    # W: D by K matrix whose columns are the principal components in decreasing order
    # LL: eigenvalues
    # m: mean of columns of A

    # Note: "lambda" is a Python reserved word


    # compute mean, and subtract mean from every column
    [r,c] = A.shape
    m = np.mean(A,1)
    A = A - np.transpose(np.tile(m, (c,1)))
    B = np.dot(np.transpose(A), A)
    [d,v] = linalg.eig(B)
    # v is in descending sorted order

    # compute eigenvectors of scatter matrix
    W = np.dot(A,v)
    Wnorm = ComputeNorm(W)

    W1 = np.tile(Wnorm, (r, 1))
    W2 = W / W1
    
    LL = d[0:-1]

    W = W2[:,0:-1]      #omit last column, which is the nullspace
    
    return W, LL, m


def read_faces(directory,lst):
    # function faces = read_faces(directory)
    # Browse the directory, read image files and store faces in a matrix
    # faces: face matrix in which each colummn is a colummn vector for 1 face image
    # idLabels: corresponding ids for face matrix

    A = []  # A will store list of image vectors
    Label = [] # Label will store list of identity label
    Context = []
    # browsing the directory
    for line in lst:
        f = ("/").join([line.split(",")[0],"face",line.split(",")[1]])
        infile = os.path.join(directory, f)
        im = Image.open(infile)
        im_arr = np.asarray(im)
        im_arr = im_arr.astype(np.float32)

        # turn an array into vector
        im_vec = np.reshape(im_arr, -1)
        A.append(im_vec)
        name = line.split(",")[0]
        c = line.split(",")[3]
        Label.append(int(name))
        Context.append(int(c))

    faces = np.array(A)
    faces = np.transpose(faces)
    idLabel = np.array(Label)
    context = np.array(Context)

    return faces,idLabel,context

def extractVoiceFeatures(voices,lst):
    return np.array([]),np.array([]),np.array([])