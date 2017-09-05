# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 12:22:22 2017

@author: divya
"""

# set up Python environment: numpy for numerical routines, and matplotlib for plotting
import numpy as np
from scipy.spatial import distance
from sklearn import preprocessing 
import FisherFace as ff

# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
import sys
#### TODO: UPDATE CAFFE ROOT PATH #######
#### TODO: COPY VGG_FACE_CAFFE to caffe_root/models ######### 
caffe_root = '/home/divya/caffe-rc5/'  #set caffe_root_path
sys.path.insert(0, caffe_root + 'python')

import caffe
# If you get "No module named _caffe", either you have not built pycaffe or you have the wrong path.

class FaceVerifier(object):
    def init(self,use_VGGFace = True, use_PCA = False):
        #self.loadVGGFace()
        self.batch_size = 5
        self.loadVGGFace(cpu_only = True)
        self.use_pca=use_PCA
        self.threshold = 0.4
    def loadVGGFace(self,cpu_only = True):
        if cpu_only:
            caffe.set_mode_cpu() #Using onyl cpu
        else:
            caffe.set_device(0)  # if we have multiple GPUs, pick the first one
            caffe.set_mode_gpu()

        self.model_def = caffe_root + 'models/vgg_face_caffe/VGG_FACE_deploy.prototxt'
        self.model_weights = caffe_root + 'models/vgg_face_caffe/VGG_FACE.caffemodel'

        self.net = caffe.Net(self.model_def,      # defines the structure of the model
                self.model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)
            
        mean = np.array([129.1863,104.7624,93.5940])
        print("mean:",mean)

        # create transformer for the input called 'data'
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        
        self.transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
        self.transformer.set_mean('data', mean)            # subtract the dataset-mean value in each channel
        self.transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
        self.transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR
        # set the size of the input (we can skip this if we're happy
        #  with the default; we can also change it later, e.g., for different batch sizes)
        self.net.blobs['data'].reshape(self.batch_size,        # batch size
                          3,         # 3-channel (BGR) images
                          224, 224)  # image size is 227x227

    def get_caffe_feature(self,image_path):
        image = caffe.io.load_image(image_path)
        transformed_image = self.transformer.preprocess('data',image)
        self.net.blobs['data'].data[0] = transformed_image
        self.net.forward()
        return np.array(preprocessing.normalize(self.net.blobs['fc6'].data,norm='l2')[0])

    
    def get_caffe_features(self,facesT):
        length = len(facesT)        
        t = int(length/self.batch_size)
        full_features = []
        print("number of batches ",self.batch_size," ",t)
        for j in range(0,t+1): 
            if j == t:
                faces = facesT[j*self.batch_size:]
            else:
                faces = facesT[j*self.batch_size:(j+1)*self.batch_size]
            new_length = min(self.batch_size,len(faces))
            print("new_length", new_length)
            for i in range(0,new_length):
                image = caffe.io.load_image(faces[i])
                transformed_image = self.transformer.preprocess('data',image)
                self.net.blobs['data'].data[i] = transformed_image
            print("forwarding net ",self.net.blobs['data'].data.shape)
            self.net.forward()
            features = np.array(preprocessing.normalize(self.net.blobs['fc6'].data,norm='l2'))
            if j == t:
                features = features[:new_length]
            if j == 0:
                full_features = features
            else:                
                full_features = np.concatenate((full_features,features),axis=0)
            print("feature size: ", full_features.shape)
        return full_features
    
    def get_distance(self,image_path1,image_path2):
        return  distance.cosine(self.get_caffe_feature(image_path1),self.get_caffe_feature(image_path2))

    def verify(self,feat1,feat2):
        if feat1==None or feat2==None:
            return False
            
        if self.get_distance(feat1,feat2) <= self.threshold:
            return True
        else:
            return False
    
    def verifyClaim(self,Id = -1, feature = ''):
        if feature == '' or Id == -1:
            return False,1
        if self.use_pca  == True and self.pca_w != None:
            feature = np.dot(np.transpose(self.pca_w),feature-self.pca_m)
        dist = distance.cosine(self.template[Id],feature)
        return dist <= self.threshold, dist
    
    def train(self,faces,ids):
        features = self.get_caffe_features(faces)      
        ids = np.array(ids)
        if self.use_pca == True:
            print("starting pca with features", features.shape)
            self.pca_w,self.pca_m,self.template = self.generateTemplate_PCA(np.transpose(features),ids)
            print("pca: done")
        else:
            self.template = self.generateTemplate(features,ids)
            self.pca_w = None
            self.pca_m = None
       
        #return features
    def test(self,faces,ids,outfile = None):
        print("testing started" )        
        if outfile == None:
            outfile = open("result.csv","w")
        features = self.get_caffe_features(faces)
        features = np.transpose(features)
        for i in range(0,len(faces)):
            res,dist = self.verifyClaim(Id = ids[i],feature = features[:,i])
            outfile.write(",".join(str(x) for x in [faces[i],ids[i],res,dist,"\n"]))
        print("test done")
    
    def reduceDimension(self,faces_train,id_train,r):
        W, LL, m = ff.myPCA(faces_train)
        W_e = W[:,:r]
        y = np.empty([id_train.shape[0],r])
        print(W_e.shape,y.shape,m.shape)
        #calculate PCA feature for each training image
        for i in range(0,id_train.shape[0]):
           f = faces_train[:,i] - m
           y_e = np.dot(np.transpose(W_e),f)
           y[i] = y_e   

        return W_e,y,m   
    
    def generateTemplate_PCA(self,faces_train,id_train):
        K = 30
        W_e,X,m = self.reduceDimension(faces_train,id_train,K)
        y = dict()
        for i in range(0,X.shape[0]):
            if id_train[i] not in y.keys():
                y[id_train[i]] = []
            y[id_train[i]].append(X[i])
        #create template for each person in the training set
        z = dict()
        
        for key in y.keys():
            print("key",key)
            t = np.mean(np.array(y[key]),0)
            z[key] = t
        return W_e,m,z
        
    def generateTemplate(self,faces,ids):
        #m = np.mean(faces,1)
        y = dict()
        for i in range(0,faces.shape[0]):
            if ids[i] not in y.keys():
                y[ids[i]] = []
            y[ids[i]].append(faces[i])
        #create template for each person in the training set
        z = dict()
        
        for key in y.keys():
            print("key",key)
            t = np.mean(np.array(y[key]),0)
            z[key] = t
        return z