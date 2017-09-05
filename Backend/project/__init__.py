# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 15:48:21 2017

@author: divya
"""

from flask import Flask

app = Flask(__name__)

from . import views

views.initVGG()