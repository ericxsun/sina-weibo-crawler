# coding: utf-8
import sys
import os

DEBUG = True

PAGE_PORT = 8800

if getattr(sys, 'frozen', False):
    PATH = os.path.dirname(sys.executable)
elif __file__:
    PATH = os.path.dirname(__file__)

STATIC_PATH = os.path.join(PATH, 'static')