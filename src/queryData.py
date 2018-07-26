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

time_stamp = time.time()
save_dir = './recommendations/{}'.format(time_stamp)
os.mkdir(save_dir)

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

    def showOnePairs(self, query_result, pair_result, pair_comparison, image_raw_folder = '../ut-zap50k-images-square/', query_count = 1):
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


        # Update, always show the query result as the choice 1
        if query_result[0]['index'] == pair_comparison[0]['index_1']:
            image_1_path = image_raw_folder + path.find({'index': query_result[0]['index']})[0]['path']
            image_2_path = image_raw_folder + path.find({'index': pair_result[0]['index']})[0]['path']
        else:
            image_2_path = image_raw_folder + path.find({'index': query_result[0]['index']})[0]['path']
            image_1_path = image_raw_folder + path.find({'index': pair_result[0]['index']})[0]['path']

        comparison = ('Choice {} is '.format(2 * query_count - 1) + self.comparison_labels[pair_comparison[0]['comparison'] - 1] 
        + ' '  + self.attributes[pair_comparison[0]['attribute'] - 1] + ' than Choice {}\n'.format(2 * query_count)  
        + 'with average confidence: ' + str(pair_comparison[0]['confidence']))


        img1 = mpimg.imread(image_1_path)
        img2 = mpimg.imread(image_2_path)


        plt.ion()
        fig_1 = plt.figure('Recommend to you!', figsize=(9,6))
        plt.clf()
        plt.suptitle(comparison)
        plt.subplot(1,2,1)
        plt.title('Choices {}'.format(2 * query_count - 1))
        plt.imshow(img1)
        plt.axis('off')
        plt.text(-0.2, -0.3, description_1, size = 11, ha="left", transform=plt.subplot(1,2,1).transAxes)

        plt.subplot(1,2,2)
        plt.title('Choices {}'.format(2 * query_count))
        plt.imshow(img2)
        plt.axis('off')
        plt.text(0.0, -0.3, description_2, size = 11, ha="left", transform=plt.subplot(1,2,2).transAxes)

        plt.savefig('./recommendations/{}/{}-recommendation.png'.format(time_stamp, query_count))

        # fig2 = plt.figure('All recommendations', figsize = (8,20))
        # plt.clf()

        # rec_images_path = [f for f in os.listdir(save_dir) if os.path.isfile(os.path.join(save_dir, f))]
        # for i in range(0, query_count):
        #     plt.subplot(6, 3, i + 1)
        #     img = mpimg.imread(save_dir + '/' + rec_images_path[i])
        #     plt.imshow(img)
        #     plt.axis('off')


        plt.show(block=False)






    def queryShow(self, query_dict, query_count = 1):
        query_result = self.query(query_dict, number = 1, print_console = False)
        if query_result == False:
            return 'no result', 'no result', 'no result'
        pair_comparison = self.findPair(index = query_result[0]['index'], number = 1, print_console = False)
        if query_result[0]['index'] == pair_comparison[0]['index_1']:
            pair_index = pair_comparison[0]['index_2']
        else:
            pair_index = pair_comparison[0]['index_1']

        pair_result = self.query(query_dict = {'index': pair_index}, number = 1, print_console = False)


        shoedb.showOnePairs(query_result, pair_result, pair_comparison, query_count = query_count)
        return query_result, pair_result, pair_comparison



if __name__ == '__main__':
    shoedb = ShoeDB()
    shoedb.buildDB()

    query_count = 1 # For printing usage

    

# 
# Block 1: demo
#
    # preferences = {} # To store user's preference in each round
    # while True:
    #     query_keys = []
    #     query_values = []
    #     while True:
    #         print('If you do not need more keys or want to exit, press \'q\' to continue')
    #         query_key = raw_input('Enter the key: ')
    #         if query_key == 'q': # Press q to exits
    #             break
    #         value_input = raw_input('Enter the value: ')
    #         # Update. We can query the documents with the same substring as query_value.
    #         query_value = {'$regex': value_input}

    #         query_keys.append(query_key)
    #         query_values.append(query_value)

    #     if query_key == 'q' and len(query_keys) == 0:
    #         break

    #     # if pid != 0:
    #     #     os.kill(pid, 9) # kill the child process which is showing the image
    
    #     query_dict = {}
    #     for i in range(0, len(query_keys)):
    #         query_dict.update({query_keys[i]: query_values[i]})
    #         #query_dict[query_keys[i]] = query_values[i]

    #     print('{}-round query: {}'.format(query_count, str(query_dict)))
    #     query_count += 1
    #     shoedb.queryShow(query_dict)   ### The query_dict format should be {'key1': 'value1', 'key2': 'value2', ...}


# 
# End of block 1
# 

#
# Block 2: proactive recommendation, in the task that the user needs to buy a shoes for a male friend
#
    preferences = {'gender': {'$in': ['Men', 'Boys']}, 
                   'category': {'$regex': '.*'}, 
                   'subcategory': {'$regex': '.*'}, 
                   'heelheight': {'$regex': '.*'}, 
                   'insole': {'$regex': '.*'}, 
                   'closure': {'$regex': '.*'}, 
                   'material': {'$regex': '.*'}, 
                   'toestyle': {'$regex': '.*'}
                   } # To store user's preference in each round
    attributes = ['category', 'subcategory', 'heelheight', 'insole', 'closure', 'material', 'toestyle']
    recommendation_list = []
    print('Hi! Let me help you! Let me give you some recommendations!')
    while True:
        print('How about these two kinds of shoes?')
        

        choiceNo_1 = 2 * query_count - 1
        choiceNo_2 = 2 * query_count
        print('{}-round recommendation based on preferences: {}'.format(query_count, str(preferences)))
        query_result, pair_result, pair_comparison = shoedb.queryShow(preferences, query_count)
        if query_result == 'no result' or query_count > 5:
            final_choice = raw_input('Please choose from the previous recommendations by number. Press 0 if you want more recommendations. Please type the number: ')
            if query_result != 'no result':
                recommendation_list.append(query_result[0])
                recommendation_list.append(pair_result[0])

            if final_choice == '0':
                update_attribute = attributes[randint(0, len(attributes) - 1)]
                preferences.update({update_attribute: {'$regex': '.*'}})
                continue
            else: 
                print('You choose shoe No.{}'.format(final_choice))
                print(recommendation_list[int(final_choice) - 1])
                print('I am glad that you choose this one! Enjoy!')
                break
        recommendation_list.append(query_result[0])
        recommendation_list.append(pair_result[0])
        
        choice = raw_input('Which one do you prefer? {} or {}? Please type a number: '.format(choiceNo_1, choiceNo_2))
        while True:
            if choice == str(choiceNo_1):
                update_attribute = attributes[randint(0, len(attributes) - 1)]
                new_preference = {update_attribute: {'$regex': query_result[0][update_attribute]}}
                break
            elif choice == str(choiceNo_2):
                update_attribute = attributes[randint(0, len(attributes) - 1)]
                new_preference = {update_attribute: {'$regex': pair_result[0][update_attribute]}}
                break
            else:
                choice = raw_input('Please press {} or press {}: '.format(choiceNo_1, choiceNo_2))

        preferences.update(new_preference)
        query_count += 1
        print('\n\nNew preference: {}\n\n'.format(new_preference))













    #     try:
    #         pid = os.fork()
    #     except OSError:
    #         exit("Could not create a child process")
    #     if pid == 0: # Show the image
    #         shoedb.queryShow(query_dict)   ### The query_dict format should be {'key1': 'value1', 'key2': 'value2', ...}
    #         exit()

    # os.kill(pid, 9)

