# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:48:21 2017

@author: divya
"""

from flask import jsonify
from flask import request, render_template
from flask import abort, make_response
from PIL import Image
from scipy.spatial import distance
import numpy as np
import io
import os

from .import app
from . import FaceVerifier
base = "/biosecure/api/v1"

FV = None
########################
#### helper methods ####
########################

def import_data(request):
    img = None
    try:
        if 'image' in request.files:
            img = request.files['image']
            print("Image Received")

    except KeyError as e:
        raise ValidationError('Invalid image: Operation failed')
    return img

def initVGG():
    global FV
    FV = FaceVerifier.FaceVerifier()
    FV.init()
    FV.loadVGGFace()

def getVGGFeature(image):
    global FV
    feature = None
    if FV != None:
        feature = FV.get_caffe_feature(image)
    return  feature

def saveEnrolledFeature(feature):
    np.array(feature)
    np.savetxt(os.path.join('project', 'data',"enrolled_feature.csv"),feature)
    return None

def loadEnrolledFeature():
    return np.loadtxt(os.path.join('project', 'data',"enrolled_feature.csv"))

def compare(feature1,feature2):
    score = -1
    score = distance.cosine(feature1,feature2)
    return score

########################
####  api methods   ####
########################


@app.route(base + '/')
def index():
    return jsonify(render_template('index.html')),200

@app.route(base + '/enroll', methods=['POST'])
def enroll():
    print("args ", request.args)
    print("files ", request.files)
    print("data ",request.data)
    print("val ", request.values)
    print("json ", request.form)
    img  = import_data(request)
    if img == None:
        abort(415)
    try:
        img.save(os.path.join('project', 'data', 'enrolled_image.jpg'))
        fp = os.path.join(os.getcwd(), 'project', 'data', 'enrolled_image.jpg')
        print(fp)
        feature = getVGGFeature(fp)
        saveEnrolledFeature(feature)
    except KeyError as e:
        abort(503)
    return jsonify({'status': 'Success'}),200

@app.route(base + '/verify', methods=['POST'])
def verify():
    if not os.path.isfile("project/data/enrolled_feature.csv"):
        abort(412)
    img  = import_data(request)
    if img == None:
        abort(415)
    img.save(os.path.join('project', 'data', 'verify_image.jpg'))
    test_feature = getVGGFeature(os.path.join(os.getcwd(), 'project', 'data', 'verify_image.jpg'))
    enrolled_feature = loadEnrolledFeature()
    score = compare(test_feature,enrolled_feature)
    print("SCORE ", score)
    return jsonify({'status': 'Success', 'score': str(score)}),200

####### ERROR HANDLERS #######

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(415)
def invalid_image(error):
    return make_response(jsonify({'error': 'Invalid Image'}), 415)
    
@app.errorhandler(503)
def enroll_fail(error):
    return make_response(jsonify({'error': 'Failed to enroll. Try again'}), 503)
    
@app.errorhandler(412)
def no_enrollments(error):
    return make_response(jsonify({'error': 'No enrollments. Enroll first.'}), 412)

    
    