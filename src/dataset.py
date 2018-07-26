#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import numpy as np
import random
import pymongo
import json
import csv
import time
from scipy.io import loadmat

#################
# Be attention! This dataset building code is one case usage!
# Every time you rerun this code, you should delete the exiting
# collection first!! Or it will insert duplicate documents!!
#################
def creatDB():
    datafolder = '../ut-zap50k-data/'

    # The database and collection code.
    client = pymongo.MongoClient()
    db = client.shoe
    meta = db.meta   # A collection of all meta data documents
    label_fg = db.label_fg  # A collection of label_fine-grained documents
    ration_fg = db.ration_fg # A collection of rationale_fine-grained documents
    path = db.path # A collection of image path documents
    meta_fg = db.meta_fg # A collection of meta data documents that are in fine-grained pairs

    #The following lines are used to delete collection if the collection is insuitable
    meta.drop()
    meta = db.meta
    label_fg.drop()
    label_fg = db.label_fg
    ration_fg.drop()
    ration_fg = db.ration_fg
    path.drop()
    path = db.path
    meta_fg.drop()
    meta_fg = db.meta_fg
    meta_fg.drop()
    meta_fg = db.meta_fg


    labels_path = datafolder + 'zappos-labels-fg.mat'
    label = loadmat(labels_path)['mturkHard']
    for i in range(4):
        for pair in label[:, i][0]:
            #Used to check the maximum index
            #if (int(pair[0]) < index_max) or  (int(pair[1]) < index_max):
            #    index_max = (int(pair[0]),int(pair[1]))
            label_json = {
                'index_1': int(pair[0]),
                'index_2': int(pair[1]),
                'attribute': int(pair[2]),
                'comparison': int(pair[3]),
                'confidence': pair[4],
                'agreement': pair[5]

            }
            label_fg.insert(label_json)

    print('label data has been store in client.shoe.label_fg  !!!!!!')


    index = 1
    image_path = datafolder + 'image-path.mat'
    image_all = loadmat(image_path)['imagepath']
    for image in image_all:
        image_json = {
            'index': index,
            'path': image[0][0]   #str(image[0][0]).replace('[u\'','').replace('\']','').replace('\"','')
        }
        path.insert(image_json)
        index += 1

    print('path data has been store in client.shoe.path  !!!!!!')




    meta_path = datafolder + 'meta-data.csv'
    with open(meta_path, 'rb') as f:
        spamreader = csv.reader(f, quotechar='|')
        index = 0
        for row in spamreader:
            if index == 0:
                index += 1
            else:
                meta_json = {
                    'index': index,
                    'cid': row[0],
                    'category': row[1],
                    'subcategory': row[2],
                    'heelheight': row[3],
                    'insole': row[4],
                    'closure': row[5],
                    'gender': row[6],
                    'material': row[7],
                    'toestyle': row[8]
                }
                # This will take a long time (5 mintues)... Because it needs to find if the index exists in label_fg or not every time
                if (label_fg.find({'index_1': index}).count() != 0) or (label_fg.find({'index_2': index}).count() != 0):
                    meta_fg.insert(meta_json)

                meta.insert(meta_json)
                index += 1
                #Used for debug
                #if index == 10:
                #    break
                #print(meta_json)
    print('Meta data has been store in client.shoe.meta  !!!!!!')
    print('Meta_fg data has been store in client.shoe.meta_fg  !!!!!!')




    ration_path = datafolder + 'ration.txt'
    ration_all = open(ration_path, "r").readlines()
    for ration in ration_all:
        ration = ration.split()
        comment = ''
        for i in range(5, len(ration) - 1):
            comment = comment + ration[i] + ' '
        comment = comment + ration[-1]
        ration_json = {
            'index_1': int(ration[0]),
            'index_2': int(ration[1]),
            'attribute': int(ration[2]),
            'comparison': int(ration[3]),
            'confidence': ration[4],
            'comment': comment
        }
        ration_fg.insert(ration_json)

    print('rationale data has been store in client.shoe.ration_fg  !!!!!!')

    return True



if __name__ == '__main__':
    creatDB()
