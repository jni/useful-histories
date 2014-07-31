datadir = '/Users/nuneziglesiasj/Data/myo/'
import os
import scandir

def all_images(path):
    for p, _, files in scandir.walk(path):
        for f in files:
            if f.endswith('.tif'):
                yield os.path.join(p, f)

image_fns = list(all_images(datadir))
import subprocess as sp
sp.Popen(["mongod", "--dbpath", "/Users/nuneziglesiasj/mongodb"])
from husc.screens import myofusion as myo
filenames = [l.rstrip() for l in open('db/filenames.txt', 'r').readlines()]
myo.populate_db('db/all_annots2.csv', filenames)
from pymongo import MongoClient
collection = MongoClient()["myofusion"]["wells"]
for image_fn in [image_fns[450]]:
    key = myo.filename2coord(image_fn)
    mongo_id = myo.key2mongo(key)
    doc = collection.update({'_id': mongo_id},
                            {'$set': {u'local_filename': image_fn}})

