#coding:UTF-8


import scipy.io as scio

#dataFile = 'zappos-labels-fg.mat'

#dataFile = 'image-path.mat'
dataFile = 'zappos-fg-rationale.mat'
data = scio.loadmat(dataFile)
print(data.keys())
#print(data['mturkHard'][0][0].shape)
#print(data['imagepath'].shape)