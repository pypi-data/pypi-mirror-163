import os, sys, json
from epcam_api import BASE

#打开料号
def open_job(path, job):
    try:
       return  BASE.open_job(path, job)     
    except Exception as e:
        print(e)

def open_eps(job, path):
    try:
        return BASE.open_eps(job, path)
    except Exception as e:
        print(e)
