# Goal
An code example to search the shoe and plot two kind of shoes in the dataset [UT Zappos50K
](http://vision.cs.utexas.edu/projects/finegrained/utzap50k/). 

Up to now, I only use the shoes in zappos-labels-fg.mat, because it contains comparative information about the similar pairs and reasons (Mturk).

Input: a dict of the 'key: value', i.e. {key1: value1, key2: value2, ...}

* Query mode
![Input Example_1](https://github.com/PenguinZhou/Shoe_Searching_Comparison/raw/master/InteractiveMode.png)

* Recommendation based on your previous choice
![Recommend Example](https://github.com/PenguinZhou/Shoe_Searching_Comparison/raw/master/Learn_preference_example.png)

Output: An image showing two kind of shoes, one will match the conditions we speicify in the input (randomly from the mathcing result), and the other one is the pair of the matching one. The image will also show the attributes of the shoes and the comparison result. 

![Output Example](https://github.com/PenguinZhou/Shoe_Searching_Comparison/raw/master/Recommend_to_you!.png)

## The successful testing environment

### System

* Ubuntu 16.04
* Python 2.7.14
* Install all the packages as list in the .py file in the src folder

### MongoDB

We use MongoDB to store the data. So you need to install the MongoDB. And we use pymongo. 
Remember to start MongoDB service in a separate window.

	mongo

### Matlab2017b (Optional)

To store the dataset in the MongoDB, I need to process the **.mat**. Most of the **.mat** file in the dataset can be directly processed using **spicy.io** except the **rationale-fg.mat**. This file is a little like h5df. So I process it in Matlab and convert the information to **ration.txt** before processing in python. 

## Notes
If you are interesting in this coding example, give me a star ~_~
Thanks~