#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import numpy as np
from random import randint
import sys
import pymongo
import json
import os
import csv
import time
from scipy.io import loadmat
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import dataset
import warnings
#Ignore all warning. If there are any problems, should turn on the warnings.
warnings.filterwarnings("ignore")


#Get dataset and corresponding collection
client = pymongo.MongoClient() 
db = client.shoe
meta = db.meta
label_fg = db.label_fg
ration_fg = db.ration_fg
path = db.path
meta_fg = db.meta_fg

class ShoeDB:
    def __init__(self):
        self.flag = True
        self.count = 0
        self.attributes = ['open', 'pointy', 'sporty', 'comfort']
        self.comparison_labels = ['more', 'less']

    def buildDB(self):
        if meta_fg.find().count() == 0:
            print('Starting to create the shoe dataset in mongodb...')
            self.flag = dataset.creatDB()
            if self.flag:
                print('Successfully create the dataset...')

    def query(self, query_dict, collection = meta_fg, number = 0, print_console = False):
        query_result = collection.find(query_dict)
        self.count = query_result.count()
        if self.count != 0:
            #print('Sucessful query \'' + str(value) + '\' within key \'' + str(keys) + '\' in ' + str(collection) + '...')
            return_result = []
            if number == 1:
                i = randint(0, self.count - 1)
                return_result.append(query_result[i])
                return return_result
            elif number != 0:
                i = 1               
                for result in query_result:
                    if i <= min(number, self.count):
                        return_result.append(result)
                        i += 1
                        if print_console:
                            print(result)
                    else:
                        break
                print('Number of return result: ' + str(len(return_result)))
                return return_result
            else:
                print('Number of total result: ' + str(self.count))
                return query_result
        else:
            print("Cannot find \'" + str(query_dict) + "\' in " + str(collection) + '...')
            return False

    def findPair(self, index, number = 0, print_console = False):
        find_results = []
        for find_1 in label_fg.find({'index_1': index}):
            find_results.append(find_1)
        for find_2 in label_fg.find({'index_2': index}):
            find_results.append(find_2)
        self.count = len(find_results)
        if self.count != 0:
            #print('Successfully finding the pair of shoe: No. ' + str(index))
            return_result = []
            if number == 1:
                i = randint(0, self.count - 1)
                return_result.append(find_results[i])
                return return_result
            elif number != 0:
                i = 1
                for result in find_results:
                    if i <= min(number, self.count):
                        return_result.append(result)
                        i += 1
                        if print_console:
                            print(result)
                    else:
                        break
                return return_result
            else:
                return find_results
        else:
            print('Cannot find the pair of shoe: No.' + str(index))

    def showOnePairs(self, query_result, pair_result, pair_comparison, image_raw_folder = '../ut-zap50k-images-square/'):
        description_1 = ('Category: ' + query_result[0]['category'] + '\n'
        + 'Subcategory: ' + query_result[0]['subcategory'] + '\n'
        + 'Heelheight: ' + query_result[0]['heelheight'] + '\n'
        + 'Insole: ' + query_result[0]['insole'] + '\n'
        + 'Closure: ' + query_result[0]['closure'] + '\n'
        + 'Material: ' + query_result[0]['material'] + '\n'
        + 'Gender: ' + query_result[0]['gender'] + '\n'
        + 'ToeStyle: ' + query_result[0]['toestyle'])

        description_2 = ('Category: ' + pair_result[0]['category'] + '\n'
        + 'Subcategory: ' + pair_result[0]['subcategory'] + '\n'
        + 'Heelheight: ' + pair_result[0]['heelheight'] + '\n'
        + 'Insole: ' + pair_result[0]['insole'] + '\n'
        + 'Closure: ' + pair_result[0]['closure'] + '\n'
        + 'Material: ' + pair_result[0]['material'] + '\n'
        + 'Gender: ' + query_result[0]['gender'] + '\n'
        + 'ToeStyle: ' + pair_result[0]['toestyle'])

        if query_result[0]['index'] == pair_comparison[0]['index_1']:
            choice_1 = '1'
            choice_2 = '2'
        else:
            choice_1 = '2'
            choice_2 = '1'

        comparison = ('Choice ' + choice_1 + ' is ' + self.comparison_labels[pair_comparison[0]['comparison'] - 1] 
        + ' '  + self.attributes[pair_comparison[0]['attribute'] - 1] + ' than Choice ' + choice_2 + '\n'  
        + 'with average confidence: ' + str(pair_comparison[0]['confidence']))

        image_1_path = image_raw_folder + path.find({'index': query_result[0]['index']})[0]['path']
        image_2_path = image_raw_folder + path.find({'index': pair_result[0]['index']})[0]['path']
        img1 = mpimg.imread(image_1_path)
        img2 = mpimg.imread(image_2_path)

        plt.clf()

        plt.figure('Recommend to you!', figsize=(9,6))
        plt.suptitle(comparison)
        plt.subplot(1,2,1)
        plt.title('Choices 1')
        plt.imshow(img1)
        plt.axis('off')
        plt.text(-0.2, -0.3, description_1, size = 11, ha="left", transform=plt.subplot(1,2,1).transAxes)

        plt.subplot(1,2,2)
        plt.title('Choices 2')
        plt.imshow(img2)
        plt.axis('off')
        plt.text(0.0, -0.3, description_2, size = 11, ha="left", transform=plt.subplot(1,2,2).transAxes)

        plt.ion()
        plt.show(block=False)

    def queryShow(self, query_dict):
        query_result = self.query(query_dict, number = 1, print_console = False)
        if query_result == False:
            return 0
        pair_comparison = self.findPair(index = query_result[0]['index'], number = 1, print_console = False)
        if query_result[0]['index'] == pair_comparison[0]['index_1']:
            pair_index = pair_comparison[0]['index_2']
        else:
            pair_index = pair_comparison[0]['index_1']

        pair_result = self.query(query_dict = {'index': pair_index}, number = 1, print_console = False)
        shoedb.showOnePairs(query_result, pair_result, pair_comparison)



if __name__ == '__main__':
    shoedb = ShoeDB()
    shoedb.buildDB()

    pid = 0 # In order to run the while loop at the beginning, we should set pid = 0 here.
    query_count = 1 # For printing usage
    while True:
        query_keys = []
        query_values = []
        while True:
            print('If you do not need more keys or want to exit, press \'q\' to continue')
            query_key = raw_input('Enter the key: ')
            if query_key == 'q': # Press q to exits
                break
            query_value = raw_input('Enter the value: ')
            query_keys.append(query_key)
            query_values.append(query_value)
        if query_key == 'q' and len(query_keys) == 0:
            break

        if pid != 0:
            os.kill(pid, 9) # kill the child process which is showing the image
    
        query_dict = {}
        for i in range(0, len(query_keys)):
            query_dict[query_keys[i]] = query_values[i]

        print('{}-round query: key = {}, value = {}'.format(query_count, query_key, query_value))
        query_count += 1

        shoedb.queryShow(query_dict)   ### The query_dict format should be {'key1': 'value1', 'key2': 'value2', ...}

    #     try:
    #         pid = os.fork()
    #     except OSError:
    #         exit("Could not create a child process")
    #     if pid == 0: # Show the image
    #         shoedb.queryShow(query_dict)   ### The query_dict format should be {'key1': 'value1', 'key2': 'value2', ...}
    #         exit()

    # os.kill(pid, 9)

